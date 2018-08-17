from django.conf.urls import url
from . import views

app_name = 'warehouse'
urlpatterns = [
    url(r'^$',                                               views.home,      name='home'),
    url(r'^list/?$',                                         views.main,      name='main'),
    url(r'^list/(?P<id>[0-9]+)/?$',                          views.main,      name='main'),
    url(r'^list/(?P<slug>[-a-zA-Z0-9_]+)/?$',                views.main,      name='main'),
    url(r'^list/(?P<slug>[-a-zA-Z0-9_]+)/(?P<id>[0-9]+)/?$', views.main,      name='main'),
    url(r'^blueprint/new/?$',                                views.edit,      name='edit'),
    url(r'^blueprint/(?P<slug>[-a-zA-Z0-9_]+)/edit/?$',      views.edit,      name='edit'),
    url(r'^blueprint/(?P<slug>[-a-zA-Z0-9_]+)/?$',           views.blueprint, name='blueprint'),
    url(r'^blueprint/(?P<slug>[-a-zA-Z0-9_]+)/files/?$',     views.files,     name='files'),
    url(r'^user/(?P<username>[-a-zA-Z0-9_@.+]+)/?$',         views.user,      name='user'),
    url(r'^user/(?P<username>[-a-zA-Z0-9_@.+]+)/edit/?$',    views.useredit,  name='useredit'),

    url(r'^about/?$',                                        views.about,     name='about'),
]
