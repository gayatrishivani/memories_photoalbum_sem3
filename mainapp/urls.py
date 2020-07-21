from django.urls import path, re_path
from .views import *



urlpatterns = [
    path('', index,name='home'),
    path('single/<int:pk>/<str:title>', single, name='single'),
    path('search/', search, name='search'),
    path('add_album/', add_album, name='add_album'),
    path('add_sub_album/<int:album_id>',add_sub_album, name='add_sub_album'),
    path('edit_profile/',edit_profile, name='edit_profile'),
    path('<str:username>',others_profile, name='others_profile'),
    path('following/<int:id>',follow_request, name='following'),
    path('ui_profile/',ui_profile, name='ui_profile'),
    path('follow_request/<int:id>/',follow_request, name='follow_request'),
    path('follow_del_or_rej/<int:id>/',follow_del_or_rej, name='follow_del_or_rej'),


]