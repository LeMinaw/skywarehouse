from django.urls import path
from . import views

app_name = 'warehouse'
urlpatterns = [
    path('',                                     views.home,      name='home'),
    path('list',                                 views.main,      name='main'),
    path('list/<int:id>',                        views.main,      name='main'),
    path('list/<str:slug>',                      views.main,      name='main'),
    path('list/<str:slug>/<int:id>',             views.main,      name='main'),
    path('blueprint/new',                        views.bp_edit,   name='blueprint_add'),
    path('blueprint/<str:slug>/edit',            views.bp_edit,   name='blueprint_edit'),
    path('blueprint/<str:slug>',                 views.blueprint, name='blueprint'),
    path('blueprint/<str:slug>/files',           views.files,     name='files'),
    path('blueprint/<str:slug>/fav',             views.fav_edit,  name='fav_edit'),
    path('user/<str:username>',                  views.user,      name='user'),
    path('user/<str:username>/edit',             views.user_edit, name='user_edit'),
    path('about',                                views.about,     name='about'),
]
