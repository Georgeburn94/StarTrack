from django.urls import path, include
from .views import home_page_view
from django.contrib import admin

urlpatterns = [
    path('', home_page_view, name='home'),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]