from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import UserRegistrationView
from .views import UserLoginView
from .views import UserProfileView
from .views import DeviceView
from .views import IOView
from .views import DeviceIOView

urlpatterns = [
    path('',views.index,name='index'),
    path('extern',views.extern,name='extern'),
    path('device',views.device,name='device'),
    path('io',views.io,name='io'),
    path('deviceIO',views.deviceIO,name='deviceIO'),
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^signin', UserLoginView.as_view()),
    url(r'^profile', UserProfileView.as_view()),
    url(r'^deviceview', DeviceView.as_view()),
    url(r'^ioview', IOView.as_view()),
    url(r'^deviceioview', DeviceIOView.as_view())
 #   path('profile/<int:id>',views.device,name='device'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)