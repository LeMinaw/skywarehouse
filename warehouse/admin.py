from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from warehouse.models import *


class FileVersionInline(admin.TabularInline):
    model = FileVersion
    extra = 0


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


class UserAdmin(AbstractUserAdmin):
    list_display = ('__str__', 'email', 'is_active', 'is_staff', 'is_superuser')
    date_hierarchy = 'date_joined'
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Profil personnel', {
            'fields': ('email', 'avatar', 'bio')
        }),
        ('Permissions', {
            'fields': (('is_active', 'is_staff', 'is_superuser'), 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Chronologie', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        })
    )


class ShipAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug', 'author', 'pin')
    list_filter = ('slug', 'author', 'pin')
    date_hierarchy = 'added'
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'author')
        }),
        ('Meta', {
            'fields': ('desc', 'image', 'pin')
        }),
    )
    inlines = [FileVersionInline, ReviewInline, CommentInline]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author')
    date_hierarchy = 'added'
    fieldsets = (
        (None, {
            'fields': ('author', 'ship')
        }),
        ('Notes', {
            'fields': (('grade_interior', 'grade_exterior', 'grade_space'), ('grade_mechanics', 'grade_weapons', 'grade_maneuv')),
        }),
    )


class FileVersionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'number', 'dwnlds')
    date_hierarchy = 'added'
    fieldsets = (
        (None, {
            'fields': ('file', 'ship', 'number', 'dwnlds')
        }),
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author')
    date_hierarchy = 'added'
    fieldsets = (
        (None, {
            'fields': ('ship', 'author', 'content')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Ship, ShipAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FileVersion, FileVersionAdmin)
