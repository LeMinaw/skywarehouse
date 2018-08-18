from django.conf             import settings
from django.conf.urls        import include, url
from django.conf.urls.static import static
from django.contrib          import admin
# from warehouse.views      import create_error_view

urlpatterns = [
    url(r'^admin/',   admin.site.urls),
    url(r'^account/', include("django.contrib.auth.urls")),
    url(r'^account/', include("registration.urls")),
    url(r'^',         include("warehouse.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler400 = create_error_view(code=400)
# handler403 = create_error_view(code=403)
# handler404 = create_error_view(code=404)
# handler500 = create_error_view(code=500)
