from django.urls          import path, re_path, include
from . import views

app_name = 'registration'
urlpatterns = [
    re_path(r'^activate/(?P<uidb64>[\w\-]+)/(?P<token>[\w]{1,13}-[\w]{1,20})/?$', views.activate, name='activate'),
    path(    'register',                                                          views.register, name='register'),
]
