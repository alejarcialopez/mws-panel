from django.contrib.auth.models import User, Group
from django.db import models
from django import forms
from .utils import get_institutions


class Site(models.Model):
    # Name of the site
    name = models.CharField(max_length=100, unique=True)
    # Description of the site
    description = models.CharField(max_length=250, blank=True)
    # The institution (retrieved using lookup)
    institution_id = models.CharField(max_length=100)
    # Start date of the site
    start_date = models.DateField()
    # End date of the site (when user decides to delete the site)
    end_date = models.DateField(null=True, blank=True)
    # is the site deleted?
    deleted = models.BooleanField(default=False)
    # webmaster email
    email = models.EmailField(null=True, blank=True)
    # main domain name for this mws site
    main_domain = models.ForeignKey('DomainName', related_name='+', null=True, blank=True)

    # Authorised users per site
    users = models.ManyToManyField(User, related_name='sites')
    # Authorised user groups per site
    groups = models.ManyToManyField(Group, related_name='sites', null=True, blank=True)

    def __str__(self):
        return self.name

    def is_admin_suspended(self):
        for susp in self.suspensions.all():
            if susp.active:
                return True
        return False

    def vm(self, primary):
        if self.virtual_machines.filter(primary=primary).count() is 0:
            return None
        else:
            return self.virtual_machines.get(primary=primary)

    def primary_vm(self):
        return self.vm(primary=True)

    def secondary_vm(self):
        return self.vm(primary=False)

    def calculate_billing(self, financial_year_start, financial_year_end):
        start_date = end_date = None
        if self.end_date is None:
            end_date = financial_year_end  # The site has not yet been deactivated
        elif financial_year_start <= self.end_date <= financial_year_end:
            end_date = self.end_date  # The site was deactivated this financial year

        if financial_year_start <= self.start_date <= financial_year_end:
            start_date = self.start_date  # The site started this financial year
        if self.start_date < financial_year_start:
            start_date = financial_year_start  # The site started before this financial year

        if start_date is None or end_date is None:
            return None  # The site was deactivated before this financial year or started after this financial year
        else:
            if hasattr(self, 'billing'):
                return [self.billing.group, self.billing.purchase_order_number, start_date, end_date]
            else:
                return ['Site ID: %d' % self.id, 'Pending', start_date, end_date]


class EmailConfirmation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
    )

    email = models.EmailField(null=True, blank=True)
    token = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    site = models.ForeignKey(Site, related_name='+') # do not to create a backwards relation


class Suspension(models.Model):
    reason = models.CharField(max_length=250)
    # is the suspension active?
    active = models.BooleanField(default=True)
    # start date of the suspension
    start_date = models.DateField()
    # end date of the suspension
    end_date = models.DateField(null=True, blank=True)

    site = models.ForeignKey(Site, related_name="suspensions")


class Billing(models.Model):
    purchase_order_number = models.CharField(max_length=100)
    purchase_order = models.FileField(upload_to='billing')
    group = models.CharField(max_length=250)
    site = models.OneToOneField(Site, related_name='billing')


class DomainName(models.Model):
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('denied', 'Denied'),
    )

    name = models.CharField(max_length=250, unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    site = models.ForeignKey(Site, related_name='domain_names')

    def __unicode__(self):
        return self.name


class NetworkConfig(models.Model):
    """ The network configuration for a VM (IPv4, IPv6, and domain name associated
    """
    IPv4 = models.GenericIPAddressField(protocol='IPv4')
    IPv6 = models.GenericIPAddressField(protocol='IPv6')
    mws_domain = models.CharField(max_length=250, unique=True)

    @classmethod
    def num_pre_allocated(cls):
        return cls.objects.filter(virtual_machine=None).count()

    def __unicode__(self):
        return self.IPv4 + " - " + self.mws_domain


class VirtualMachine(models.Model):
    """ A virtual machine is associated to a site and has a network configuration. Its attributes include
        a name and a boolean to indicate if it's the primary or secondary VM of a Site.
    """
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('denied', 'Denied'),
        ('ready', 'Ready'),
    )

    name = models.CharField(max_length=250, blank=True, null=True)
    primary = models.BooleanField(default=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    network_configuration = models.OneToOneField(NetworkConfig, related_name='virtual_machine')
    site = models.ForeignKey(Site, related_name='virtual_machines')

    def __unicode__(self):
        if self.name is None:
            return "<Under request>"
        else:
            return self.name


# FORMS

class SiteForm(forms.ModelForm):
    institution_id = forms.ChoiceField(label='The University institution responsible for this site')
    description = forms.CharField(label='Description for the web server (e.g. Web server for St Botolph\'s College '
                                        'main website)',
                                  widget=forms.Textarea(attrs={'maxlength': 250}),
                                  max_length=250,
                                  required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SiteForm, self).__init__(*args, **kwargs)
        self.fields['institution_id'].choices = get_institutions(user)

    class Meta:
        model = Site
        fields = ('name', 'description', 'institution_id', 'email')
        labels = {
            'name': 'A short name for this web server (e.g. St Botolph\'s main site)',
            'email': 'The webmaster email (please use a role email when possible)'
        }


class DomainNameFormNewSite(forms.ModelForm):
    name = forms.CharField(max_length=250, required=False, label="Main domain name")

    class Meta:
        model = DomainName
        fields = ('name', )


class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ('purchase_order_number', 'group', 'purchase_order')