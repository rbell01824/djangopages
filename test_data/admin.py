#!/usr/bin/env python
# coding=utf-8

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


from django.contrib import admin
from .models import CIA, Countries, VCompany, VNode, VSyslog


# noinspection PyDocstring
class CIAAdmin(admin.ModelAdmin):
    model = CIA
    search_fields = ('name', 'country_code')
    # list_filter = ('is_active', 'users', 'created_by', 'created_on', 'status')
    # ordering = ('name')
    list_display = ('name', 'country_code',
                    'total_area', 'land_area', 'coastline',
                    'population', 'birth_rate', 'p_growth',
                    'phone_mobiles', 'internet_users')
    fields = (('name', 'country_code'),
              ('total_area', 'land_area', 'water_area'),
              ('coastline', 'total_border'),
              ('labor_force', 'p_young', 'p_adult', 'p_old', 'p_growth'),
              ('phone_mobiles', 'phone_mainlines'),
              ('internet_users', 'isps'),
              ('birth_rate', 'death_rate'))
    readonly_fields = ('name', 'country_code', 'total_area', 'land_area', 'water_area',
                       'coastline', 'total_border', 'labor_force', 'p_young', 'p_adult', 'p_old', 'p_growth',
                       'phone_mobiles', 'phone_mainlines', 'internet_users', 'isps',
                       'birth_rate', 'death_rate')
    # filter_horizontal = ('users',)
    list_editable = ('phone_mobiles', 'internet_users',)
    save_on_top = True
    pass
admin.site.register(CIA, CIAAdmin)


# noinspection PyDocstring
class CountriesAdmin(admin.ModelAdmin):
    model = Countries
    search_fields = ('country_name', 'a2', 'a3')
    # list_filter = ('is_active', 'users', 'created_by', 'created_on', 'status')
    # ordering = ('name')
    list_display = ('country_name', 'a2', 'a3', 'id', 'num',
                    'country_size', 'population', 'life_expectancy', 'infant_mortality')
    fields = ('country_name',
              ('a2', 'a3',),
              ('id', 'num',),
              ('country_size',),
              'population', 'life_expectancy', 'infant_mortality')
    list_editable = ('population', )
    readonly_fields = ('country_name', 'a2', 'a3', 'id', 'num', 'country_size',
                       'population', 'life_expectancy', 'infant_mortality')
    # list_filter = ('country_size', 'population', 'life_expectancy', 'infant_mortality')
    # filter_horizontal = ('users',)
    save_on_top = True
    pass
admin.site.register(Countries, CountriesAdmin)


# noinspection PyDocstring
class CompanyAdmin(admin.ModelAdmin):
    model = VCompany
    pass
admin.site.register(VCompany, CompanyAdmin)


# noinspection PyDocstring
class NodeAdmin(admin.ModelAdmin):
    model = VNode
    search_fields = ('company__company_name', 'host_name', 'node_ip',)
    list_filter = ('company__company_name', 'host_name', 'node_ip', 'has_syslog_records',)
    list_display = ('company', 'host_name', 'node_ip', 'has_syslog_records',)
    fields = ('company', 'host_name', 'node_ip', 'has_syslog_records',)
    save_on_top = True
    pass
admin.site.register(VNode, NodeAdmin)


# noinspection PyDocstring
class SyslogAdmin(admin.ModelAdmin):
    model = VSyslog
    search_fields = ('node__company__company_name',
                     'node__host_name',
                     'node__node_ip',
                     'time',
                     'message_text', 'message_type', 'message_error',)
    list_filter = ('node', 'time', 'message_type', 'message_error', 'node__company')
    list_display = ('node', 'time', 'message_text', 'message_type', 'message_error')
    fields = ('node', 'time', 'message_text', 'message_type', 'message_error')
    readonly_fields = ('node', 'time', 'message_text', 'message_type', 'message_error')
    save_on_top = True
    pass
admin.site.register(VSyslog, SyslogAdmin)
