
from django.conf.urls import url
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.urls import include
from rest_framework.documentation import include_docs_urls
from .views import Postviewset,Updateuserview
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from . import views
from .views import Searchviewset,Notification,Storyviewset,Userfeed


app_name = 'insta'

router = DefaultRouter()
router.register(r'post',views.Postviewset)
# router.register(r'story',views.StoryViewSet)

# router.register(r'story',views.StoryViewSet)

# router.register(r'search/(?P<username>)',SearchViewset,basename='')

#http://127.0.0.1:8000/insta/api/post/

urlpatterns = [
     path('chat/', views.index, name='index'),
     path('<str:room_name>/', views.room, name='room'),


     url('api/feed/',views.Userfeed.as_view(),name='feed'),
     url(r'^api/getlikers/(?P<post_id>[0-9]+)/$',views.Getlikers.as_view(),name='getlikers'),
     url(r'^api/getsavepost/$',views.Getsavepost.as_view(),name='getsavepost'),

    url(r'^api/', include(router.urls)),
    url(r'^api/signup/$', views.SignUp.as_view()),
    #url( r'^/api/post/$',PostViewSet.as_view(),name='post'),
#    url(r'^api/post/$', views.PostViewSet()),
     # url(r'^Notification/$',views.Notification.as_view(),'notifications'),
    url(r'^api/activate/(?P<user_id>[0-9]+)/$', views.Activate.as_view(), name='activate'),
    url(r'^api/resendotp/(?P<user_id>[0-9]+)/$',views.ResendOtp.as_view(), name='resend-otp'),
    #url(r'^api/login/$',views.Login.as_view()),
    #url(r'^api/logout/$',views.Logout.as_view()),
    url('api/login/',obtain_jwt_token),
    url('api/me/', views.Updateuserview.as_view(),name='me'),

    url(r'^Search/(?P<username>[\w.@+-]+)/$', Searchviewset.as_view()),
    url(r'^api/story/', Storyviewset.as_view()),

     #for string using regex otherwise page not found 
     #http://127.0.0.1:8000/insta/profile/mahima-l/
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.Userprofileview.as_view(),
         name='userprofile'),
         
    url(r'^follow/(?P<username>[\w.@+-]+)/$', views.Followuserview.as_view(),
          name='follow-user'),


    url(r'^comment/(?P<post_id>[0-9]+)/$',views.Addcommentview.as_view(),name='addcomment'),
         
    url(r'^comment/manage/(?P<comment_id>[0-9]+)/$',views.Managecommentview.as_view(),name='managecomment'),
     #r'^/(?P<user_id>[0-9]+)/$'
    url(r'^api/like/(?P<post_id>[0-9]+)/$',views.Likeview.as_view(),name='like'),
    url(r'^api/savepost/(?P<post_id>[0-9]+)/$',views.Postsaveview.as_view(),name='savepost'),

    url(r'^follow/(?P<username>[\w.@+-]+)/$', views.Followuserview.as_view(),name='followuser'),
    
    url(r'^api/followers/(?P<username>[\w.@+-]+)/$',views.Getfollowersview.as_view(),name='getfollowers'),
    url(r'^api/following/(?P<username>[\w.@+-]+)/$',views.Getfollowingview.as_view(),name='getfollowing'),

    ]
