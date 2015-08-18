from django.conf import settings
from django.core.management.base import NoArgsCommand, CommandError
from optparse import make_option
import sys
import json
from sitesmanagement.models import VirtualMachine, Site


group = "mwsclients"


class Command(NoArgsCommand):
    args = "{ --list | --host <hostname> }"
    help = "Generates a dynamic inventory for ansible from the MWS database."
    output_transaction = True
    option_list = NoArgsCommand.option_list + (
        make_option("--list", action='store_true',
                    help="emit a list of configured MWS clients"),
        make_option("--host", action='store',
                    help="emit the configuration of a single MWS client"),
        )

    def handle_noargs(self, list=None, host=None, outfile=None, **options):
        if (not list and not host) or (list and host):
            raise CommandError("Exactly one of --list and --host must be specified.")
        outfile = outfile or sys.stdout
        if list:
            vms = VirtualMachine.objects.filter(
                service__status__in=('ansible', 'ansible_queued', 'ready'))
            result = {'_meta': {'hostvars': {}}}
            result[group] = [self.hostid(vm) for vm in vms]
            for site in Site.objects.all():
                if not site.is_canceled():
                    result[self.sitegroup(site)] = [
                        self.hostid(vm) for vm in vms.filter(service__site=site)]
            for vm in vms:
                result['_meta']['hostvars'][self.hostid(vm)] = (
                    self.hostvars(vm))
            json.dump(result, outfile)
            outfile.write("\n")
        else:
            vm = VirtualMachine.objects.get(
                network_configuration__name=host)
            json.dump(self.hostvars(vm), outfile)
            outfile.write("\n")

    def sitegroup(self, site):
        return "mwssite-%d" % (site.id,)

    def servicegroup(self, service):
        return "mwsservice-%d" % (service.id,)

    def hostid(self, vm):
        return vm.network_configuration.name

    def hostvars(self, vm):
        v = {}
        v['ansible_ssh_host'] = (vm.network_configuration.name or
                                 vm.network_configuration.IPv4 or
                                 vm.network_configuration.IPv6)
        v['mws_name'] = vm.site.name
        v['mws_webmaster_email'] = vm.site.email

        def user_vars(user):
            uv = {}
            uv['username'] = user.username
            if hasattr(user, "mws_user") and user.mws_user.uid is not None:
                uv['uid'] = user.mws_user.uid
                if user.mws_user.ssh_public_key:
                    uv['ssh_key'] = user.mws_user.ssh_public_key
            return uv
        v['mws_users'] = [user_vars(u) for u in
                          vm.site.list_of_all_type_of_active_users()]

        def vhost_vars(vh):
            vhv = {}
            vhv['id'] = vh.id
            vhv['name'] = vh.name
            vhv['domains'] = [dom.name for dom in
                              vh.domain_names.filter(status='accepted')]
            if vh.main_domain:
                vhv['main_domain'] = vh.main_domain.name
            if vh.certificate:
                vhv['certificate'] = vh.certificate
            if vh.tls_key_hash:
                vhv['tls_key_hash'] = vh.tls_key_hash
            vhv['tls_enabled'] = vh.tls_enabled
            vhv['generate_csr'] = 'tls_key_hash' in vhv and vh.tls_key_hash == "requested"
            return vhv
        v['mws_vhosts'] = [vhost_vars(vh) for vh in vm.service.vhosts.all()]
        v['mws_is_primary'] = vm.primary
        if vm.network_configuration.IPv4:
            v['mws_ipv4'] = vm.network_configuration.IPv4
            v['mws_ipv4_netmask'] = vm.network_configuration.IPv4_netmask
            v['mws_ipv4_gateway'] = vm.network_configuration.IPv4_gateway
        if vm.network_configuration.IPv6:
            v['mws_ipv6'] = vm.network_configuration.IPv6
        v['mws_tls_enabled'] = any(['certificate' in vhv
                                    for vhv in v['mws_vhosts']])
        v['mws_os_type'] = vm.os_type
        v['mws_os_version'] = vm.os_version

        v['mws_with_pacemaker'] = False

        # Corosync needs a 32-bit node ID.  ID 0 is reserved, and
        # according to corosync.conf(5), "Some openais clients require
        # a signed 32 bit nodeid that is greater than zero".  For
        # safety, we thus insist on something between 1 and 0x7fffffff
        # inclusive.  For a reasonably-sized MWS, just using the
        # primary key of the VirtualMachine should be fine.
        v['mws_cluster_nodeid'] = vm.id
        assert(1 <= v['mws_cluster_nodeid'] <= 0x7fffffff)

        # mws_site_group refers to the Ansible host group representing
        # this host's site.
        v['mws_site_group'] = self.sitegroup(vm.site)
        # mws_site_id is a convenient string identifying the site for use
        # in filenames etc.
        v['mws_site_id'] = v['mws_site_group']

        # mws_service_group refers to the Ansible host group representing
        # this host's service.
        if vm.service.type == "production":
            # Only output mws_service_* if the VM is in the prod service, do not use/show test service addresses
            v['mws_service_group'] = self.servicegroup(vm.service)
            v['mws_service_fqdn'] = vm.service.network_configuration.name
            v['mws_service_ipv4'] = vm.service.network_configuration.IPv4
            v['mws_service_ipv4_netmask'] = vm.service.network_configuration.IPv4_netmask
            v['mws_service_ipv4_gateway'] = vm.service.network_configuration.IPv4_gateway
            v['mws_service_ipv6'] = vm.service.network_configuration.IPv6

        return v
