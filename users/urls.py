from django.urls import path,include
from . import views

urlpatterns = [


    path('',views.home,name='home'),
    path('search',views.search,name='search'),
    path('explore',views.explore,name='explore'),
    path('notification',views.notification,name='notification'),
    path('createpost',views.createpost,name='createpost'),
    path('profile',views.profile,name='profile'),
    path('settings',views.settings,name='settings'),
    path('saved',views.saved,name='saved'),

]