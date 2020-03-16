from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import UserRegistrationView

urlpatterns = [
    path('',views.index,name='index'),
    path('extern',views.extern,name='extern'),
    path('device',views.device,name='device'),
    path('io',views.io,name='io'),
    path('deviceIO',views.deviceIO,name='deviceIO'),
    url(r'^signup', UserRegistrationView.as_view()),
    
 #   path('device/<int:id>',views.device,name='device'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)