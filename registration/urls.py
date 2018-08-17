from django.urls import path, re_path, include
from . import views

app_name = 'registration'
urlpatterns = [
    re_path(r'^register/?',                                                       views.register,      name='register'     ),
    re_path(r'^register-done/?$',                                                 views.register_done, name='register_done'),
    re_path(r'^activate/(?P<uidb64>[\w\-]+)/(?P<token>[\w]{1,13}-[\w]{1,20})/?$', views.activate,      name='activate'     )
]
