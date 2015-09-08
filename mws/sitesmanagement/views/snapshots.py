"""Views(Controllers) for managing Snapshots"""
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView
from ucamlookup import user_in_groups
from apimws.ansible import ansible_create_custom_snapshot, delete_snapshot
from sitesmanagement.forms import SnapshotForm
from sitesmanagement.models import Service, Snapshot
from sitesmanagement.views.sites import LoginRequiredMixin


class ServicePriviledgeCheck(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        service = get_object_or_404(Service, pk=self.kwargs['service_id'])
        site = service.site
        self.site = site
        self.service = service

        # If the user is not in the user auth list of the site and neither belongs to a group in the group auth list or
        # the site is suspended or canceled return None
        try:
            if (site not in request.user.sites.all() and not user_in_groups(request.user, site.groups.all())) \
                    or site.is_admin_suspended() or site.is_canceled() or site.is_disabled():
                return HttpResponseForbidden()
        except Exception:
            return HttpResponseForbidden()

        if not service or not service.active or service.is_busy:
            return redirect(site)

        return super(ServicePriviledgeCheck, self).dispatch(request, *args, **kwargs)


class SnapshotPriviledgeCheck(ServicePriviledgeCheck):
    def dispatch(self, request, *args, **kwargs):
        snapshot = get_object_or_404(Snapshot, pk=self.kwargs['snapshot_id'])
        self.snapshot = snapshot
        self.kwargs['service_id'] = snapshot.service.id
        return super(SnapshotPriviledgeCheck, self).dispatch(request, *args, **kwargs)


class SnapshotCreate(ServicePriviledgeCheck, CreateView):
    model = Snapshot
    form_class = SnapshotForm

    def get(self, request, *args, **kwargs):
        return redirect(reverse('sitesmanagement.views.backups', kwargs={'service_id': self.service.id}))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.service = self.service
        self.object.save()
        ansible_create_custom_snapshot.delay(self.service, self.object)
        return redirect(reverse('sitesmanagement.views.backups', kwargs={'service_id': self.service.id}))

    def form_invalid(self, form):
        response = redirect('sitesmanagement.views.backups', service_id=self.service.id)
        key, value = form.errors.popitem()
        response['Location'] += '?error_message=%s' % value.data[0].messages[0]
        return response

    def get_success_url(self):
        return reverse('sitesmanagement.views.backups', kwargs={'service_id': self.service.id})


class SnapshotDelete(SnapshotPriviledgeCheck, DeleteView):
    model = Snapshot
    pk_url_kwarg = 'snapshot_id'

    def get(self, request, *args, **kwargs):
        return redirect(reverse('sitesmanagement.views.backups', kwargs={'service_id': self.service.id}))

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.pending_delete = True
        self.object.save()
        delete_snapshot.delay(self.object.id)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('sitesmanagement.views.backups', kwargs={'service_id': self.service.id})