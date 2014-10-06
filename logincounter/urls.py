from django.conf.urls import patterns, include, url
from django.contrib import admin
from users import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^users/login$', views.login, name='login'),
    url(r'^users/add$', views.add, name='add'),
    url(r'^TESTAPI/resetFixture$', views.resetFixture, name='resetFixture'),
    url(r'^TESTAPI/unitTests', views.unitTests, name='unitTests'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    })
)

