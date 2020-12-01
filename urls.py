from django.urls import path

from . views import ChauffeurListView , InvidChauffeurView , HomeView
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [

   path('home',views.test,name='home'),
   path('drivers', ChauffeurListView.as_view()),
   path('drivers<int:pk>',InvidChauffeurView.as_view(),name='driver'),
   path('sms',views.envoi_sms , name='sendsms'),
   path('radio', views.radio_label , name='radio'),
    path('hello', HomeView.as_view(),name='hello')

]





if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


