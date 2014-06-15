# from django.conf.urls.defaults import patterns, include, url
# from django.conf import settings
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from django.contrib import admin
# admin.autodiscover()

# urlpatterns = patterns('',
#     url(r'^admin/', include(admin.site.urls)),
#     url(r'^$', 'globals.views.home', name="globals-home"),
#     url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#     url(r'^logout/$', 'globals.views.globals_logout', name="globals-logout"),

#     (r'^api/', include('api.urls')),
# )

# urlpatterns += staticfiles_urlpatterns()

from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import os


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'globals.views.index', name='globals-home'),
    # url(r'^lovely/', include('lovely.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': os.path.join(settings.SITE_ROOT, 'media')}),

)

urlpatterns += staticfiles_urlpatterns()
