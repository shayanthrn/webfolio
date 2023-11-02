from django.contrib import admin
from controller.admin import Login_site
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user/',Login_site.urls),
    path('admin/', admin.site.urls),
    path('',include("controller.urls"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)