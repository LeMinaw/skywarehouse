#-*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',                                views.home,    name='home'),
    url(r'^list/?$',                          views.main,    name='main'),
    url(r'^list/(?P<id>[0-9]+)/?$',           views.main,    name='main'),
    url(r'^ship/(?P<slug>[-a-zA-Z0-9_]+)/?$', views.ship,    name='ship'),
    url(r'^file/(?P<id>[0-9]+)/?$',           views.file,    name='file'),
    url(r'^user/(?P<username>[-a-zA-Z0-9_@.+]+)/?$',         views.user,      name='user'),
    url(r'^user/(?P<username>[-a-zA-Z0-9_@.+]+)/edit/?$',    views.useredit,  name='useredit'),

    url(r'^about/?$',                         views.about,   name='about'),
    url(r'^contact/?$',                       views.contact, name='contact'),
]
