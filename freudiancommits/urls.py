from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', TemplateView.as_view(template_name='index.html')),

    # Examples:
    # url(r'^$', 'freudiancommits.views.home', name='home'),
    # url(r'^freudiancommits/', include('freudiancommits.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
