"""ghini URL Configuration

"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView, LogoutView

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)
root_view = RedirectView.as_view(url='/browse/', permanent=True)

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    # include
    path('taxonomy/', include('taxonomy.urls')),
    path('collection/', include('collection.urls')),
    path('garden/', include('garden.urls')),
    path('browse/', include('browse.urls')),
    path('select2/', include('django_select2.urls')),
    # root redirect views
    path("favicon.ico", favicon_view, name='favicon'),
    path('', root_view, name='home'),
]
