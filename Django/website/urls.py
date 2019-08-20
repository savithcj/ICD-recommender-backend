"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from users.views import CustomTokenView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/token/', CustomTokenView.as_view(), name="token"),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),  # Added for OAuth2
    # path('accounts/login/', auth_views.LoginView.as_view(), name="login"),
    #path('accounts/', include('accounts.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('', include('recommendations.urls')),
    path('', include('web.urls')),
    path('api/', include('api.urls')),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]
urlpatterns += staticfiles_urlpatterns()
