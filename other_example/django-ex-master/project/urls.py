from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import index, health
#form 기준이 이전폴더(manage.py가 있는)임 -> setting때문에 변한걸로 추측
urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index),
    url(r'^health$', health),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
