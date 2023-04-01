from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('search',views.search_users,name='search-user'),
    path('explore',views.explore,name='explore'),
    path('notification',views.notification,name='notification'),
    path('profile',views.profile,name='profile'),
    path('update-profile',views.update_profile,name='update-profile'),
    path('create-post',views.post,name='create-post'),
    path('other-user/<int:pk>',views.other_user_profile,name='other-user'),
    path('post-detail/<int:pk>',views.post_detail,name='post-detail'),
    path('post-delete/<int:pk>',views.delete_post,name='post-delete'),
    path('post-update/<int:pk>',views.PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/comment',views.comments,name='post-comment'),
    path('add/follow/<int:pk>',views.add_follow,name='add-follow'),
    path('saved/<int:pk>',views.saved,name='saved-post'),
    path('unsaved/<int:pk>',views.unsave,name='unsaved-post'),
    path('saved/posts/',views.savedposts,name='user-saved-post'),
    


]