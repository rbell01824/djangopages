#!/usr/bin/env python

"""

11/18/13 - Initial creation

"""

from __future__ import unicode_literals
import logging
log = logging.getLogger(__name__)

__author__ = 'rbell01824'
__date__ = '11/18/13'
__copyright__ = "Copyright 2013, Richard Bell"
__credits__ = ["rbell01824"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "rbell01824"
__email__ = "rbell01824@gmail.com"
__status__ = "dev"

from django.db import models


class CIA(models.Model):
    """
    cia world fact book
    """
    country_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=50)
    total_area = models.FloatField()
    land_area = models.FloatField()
    water_area = models.FloatField()
    coastline = models.FloatField()
    total_border = models.FloatField()
    population = models.FloatField()
    p_young = models.FloatField()
    p_adult = models.FloatField()
    p_old = models.FloatField()
    p_growth = models.FloatField()
    labor_force = models.FloatField()
    phone_mobiles = models.FloatField()
    phone_mainlines = models.FloatField()
    internet_users = models.FloatField()
    isps = models.FloatField()
    birth_rate = models.FloatField()
    death_rate = models.FloatField()

    class Meta:
        verbose_name = 'CIA World Factbook'
        verbose_name_plural = 'CIA World Factbook'

    def __unicode__(self):
        return u'{}'.format(self.name)


class Countries(models.Model):
    """
    world countries
    """
    id = models.IntegerField(primary_key=True)
    a2 = models.CharField(max_length=2)
    a3 = models.CharField(max_length=2)
    num = models.IntegerField()
    country_name = models.CharField(max_length=50)
    country_size = models.IntegerField()
    population = models.IntegerField()
    life_expectancy = models.FloatField()
    infant_mortality = models.FloatField()

    class Meta:
        verbose_name = 'Countries'
        verbose_name_plural = 'Countries'

    def __unicode__(self):
        return u'{}'.format(self.country_name)

########################################################################################################################
#
# Matrix experimental data
#
########################################################################################################################

MAX_SYSLOG_MESSAGE_LENGTH = 100
MAX_SYSLOG_MESSAGE_TYPE = 20
MAX_SYSLOG_ERROR_MESSAGE = 100
MAX_HOSTNAME = 50
MAX_COMPANY_NAME = 50


class VCompany(models.Model):
    """
    Holds definition of a company and company related data.
    """
    company_name = models.CharField(max_length=MAX_COMPANY_NAME,  # the name of the company
                                    blank=False,
                                    help_text='Enter company name',
                                    unique=True,
                                    verbose_name='Company name')

    #noinspection PyClassicStyleClass
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        return unicode(self.company_name)


class VNode(models.Model):
    """
    Holds definition of a single node for use within the core matrix applications.
    """
    company = models.ForeignKey(VCompany,  # company who has this node
                                #help_text="Select company for this node",
                                # limit_choices_to={'company_name__in': ['TestCo', 'TestCo_1']},
                                verbose_name="Company")
    host_name = models.CharField(max_length=MAX_HOSTNAME,  # host name
                                 blank=True,
                                 default='',
                                 #help_text='Host name',
                                 unique=False,
                                 verbose_name='Host name')
    node_ip = models.GenericIPAddressField(blank=True,  # node ip address
                                           null=True,
                                           # default='0.0.0.0',
                                           #help_text='IP address for this node',
                                           verbose_name='Node IP address')
    # node_type = models.ManyToManyField(VNodeType,
    #                                    blank=True,
    #                                    null=True,
    #                                    #help_text='Select node type',
    #                                    verbose_name='Node types')
    is_active = models.BooleanField(default=True,
                                    help_text='True if this node is actively in use',
                                    verbose_name='Is Active')
    has_syslog_records = models.BooleanField(default=True,
                                             help_text='True if this node has any syslog records',
                                             verbose_name='Has syslog records')

    #noinspection PyClassicStyleClass
    class Meta:
        verbose_name = 'Node'
        verbose_name_plural = 'Nodes'
        permissions = (('change_restricted_vnode', 'Restricted edits'),)

    def __unicode__(self):
        return unicode(u"{}-{}:{}".format(self.company.company_name, self.host_name, self.node_ip))


class VSyslog(models.Model):
    """
    Syslog data
    """
    node = models.ForeignKey(VNode,                                             # got from IP, otherwise None
                             db_index=True,
                             null=True,
                             verbose_name='Node',
                             help_text='The node for this syslog entry')
    time = models.DateTimeField(db_index=True,
                                null=True,                                      # got from datetime
                                verbose_name='Record date time',
                                help_text='The date time for this syslog entry')
    # when the message is cli 30051 trace
    message_text = models.CharField(max_length=MAX_SYSLOG_MESSAGE_LENGTH,       # cli 30051
                                    verbose_name='Message text',
                                    help_text='The syslog message left of type, ex. sessctrl 8855')
    message_type = models.CharField(max_length=MAX_SYSLOG_MESSAGE_TYPE,         # trace
                                    verbose_name='Message type',
                                    help_text='The syslog message type, ex. info')
    message_error = models.CharField(max_length=MAX_SYSLOG_ERROR_MESSAGE,       # in this case none
                                     verbose_name='Syslog error message',
                                     help_text='The syslog error message, if any, extracted from line')
    line = models.TextField(verbose_name='Raw line',
                            help_text='The raw syslog line')

    class Meta:
        verbose_name = 'Syslog'
        verbose_name_plural = 'Syslog'

    def __unicode__(self):
        return u'{}:{}:{}:{}:{}'.format(self.node, self.time,
                                        self.message_text, self.message_type, self.message_error)

########################################################################################################################
#
# Helper for Matrix query and graph experiments
#
########################################################################################################################

from django.db.models import Q


def syslog_query(company=None, node=None, start_time=None, end_time=None):
    """
    Method to build a syslog query set of records in the specified company(s) and node(s).
    :param company: A company
    :param node: A node
    :param start_time: start time for syslog records
    :param end_time: end time for syslog records
    """

    # Company.objects.all()                 qs of Company objects
    # Node.objects.all()                    qs of Node objects
    # Syslog.objects.all()                  qs for syslog objects
    #
    # valuesqs of host_names for TestCo_1
    # Node.objects.filter(company__company_name='TestCo_1').values('host_name').distinct()
    #
    # valuesqs of node pks for all nodes with syslog records
    # Syslog.objects.all().order_by('node').values('node').distinct()
    #
    # values qs of pk(s) for nodes for TestCo1
    # Node.objects.filter(company__company_name='TestCo_1').values('pk').distinct()
    #
    # qs of syslog objects for TestCo_1
    # Syslog.objects.filter(node__company__company_name='TestCo_1')
    #
    # qs of syslog objects for TestCo_1 host_name A0040CnBEPC1
    # Syslog.objects.filter(node__company__company_name='TestCo_1', node__host_name='A0040CnBEPC1')
    #

    # make sure company and node are objects
    if isinstance(company, basestring):
        company = VCompany.objects.get(company_name=company)
    if company and isinstance(node, basestring):
        node = VNode.objects.get(company=company, host_name=node)

    if node:                    # if we have a node, use it to subset the syslog records
        qs = VSyslog.objects.filter(node=node)
    elif company:               # if we have a company, use it to subset the syslog records
        qs = VSyslog.objects.filter(node__company=company)
    else:                       # work with all companies, all nodes
        qs = VSyslog.objects.all()
    if start_time:
        qs = qs.filter(time__gte=start_time)
    if end_time:
        qs = qs.filter(time__lte=end_time)
    return qs
