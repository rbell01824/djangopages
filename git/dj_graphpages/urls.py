from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login

from .views import index
from graphpages.views import GraphPageListView

urlpatterns = patterns('',
    url(r'^test_data/', include('test_data.urls')),
    url(r'^display_graph_pages$', GraphPageListView.as_view(), name=GraphPageListView),
    url(r'^graphpages/', include('graphpages.urls')),
    url(r'^demo/', include('chartkick_demo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login_required(index), name='index'),
    url(r'^login/$', login, {'template_name': 'admin/login.html'})
)

urlpatterns += staticfiles_urlpatterns()
