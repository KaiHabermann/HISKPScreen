"""HISKPScreen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from HISKPScreen import views as internal_view
from django.conf.urls.static import static
from HISKPScreen import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',internal_view.main),
    path('div_rotation',internal_view.rotation),
    path('PoD',internal_view.particle_of_the_day),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


