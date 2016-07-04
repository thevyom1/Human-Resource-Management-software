"""coriolis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings               #used when we will be uploading resumes
from django.conf.urls.static import static     #used while resume uploading

urlpatterns = [
    url(r'^admin/', admin.site.urls),
     #127.0.0.1:8000/box/
    url(r'^box/',include('box.urls')),

    url(r'^box/', include('allauth.urls') , name='social'),

]

if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,documents_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns +=static(settings.MEDIA1_URL,document_root=settings.MEDIA1_ROOT)
    urlpatterns += static(settings.MEDIA2_URL, document_root=settings.MEDIA2_ROOT)