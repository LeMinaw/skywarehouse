from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin
from warehouse.models   import *
from warehouse.webhooks import webhook


admin.site.site_title = "Skywa.re admin"
admin.site.site_header = "Skywa.re administration"
admin.site.index_title = "Skywanderers blueprint archive admin panel"


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
            'fields': (
                ('is_active', 'is_staff', 'is_superuser'),
                'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Chronologie', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        })
    )


class BlueprintAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug', 'categ', 'author', 'pin')
    list_filter = ('slug', 'categ', 'author', 'pin')
    date_hierarchy = 'added'
    actions = ['send_webhook']
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'categ', 'author')
        }),
        ('Meta', {
            'fields': ('desc', 'image', 'pin')
        }),
    )
    inlines = [FileVersionInline, ReviewInline, CommentInline]

    def send_webhook(self, request, queryset):
        for bp in queryset:
            webhook.send_new_blueprint(bp)
        self.message_user(request, f"{len(queryset)} webhooks sent!")
    send_webhook.short_description = "Send the 'new blueprint added' webhook"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author')
    date_hierarchy = 'added'
    fieldsets = (
        (None, {
            'fields': ('author', 'blueprint')
        }),
        ('Notes', {
            'fields': (('aesthetic_grade', 'technic_grade'),)
        }),
    )


class FileVersionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'number', 'dwnlds')
    date_hierarchy = 'added'
    fieldsets = (
        (None, {
            'fields': ('file', 'blueprint', 'number', 'dwnlds')
        }),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'index', 'slug')
    fieldsets = (
        (None, {
            'fields': ('name', 'index', 'slug')
        }),
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author')
    date_hierarchy = 'added'
    fieldsets = (
        (None, {
            'fields': ('blueprint', 'author', 'content')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Blueprint, BlueprintAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FileVersion, FileVersionAdmin)
admin.site.register(Category, CategoryAdmin)
