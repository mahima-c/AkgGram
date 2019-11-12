
from django.conf.urls import url
from . import views
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.urls import include
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls
from .views import PostViewSet
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from .views import SearchList
router = DefaultRouter()
router.register(r'post',views.PostViewSet)
#http://127.0.0.1:8000/insta/api/post/

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/signup/$', views.SignUp.as_view()),
    #url( r'^/api/post/$',PostViewSet.as_view(),name='post'),

    url(r'^api/activate/(?P<user_id>[0-9]+)/$', views.Activate.as_view(), name='activate'),
    url(r'^api/resendotp/(?P<user_id>[0-9]+)/$',views.ResendOtp.as_view(), name='resend-otp'),
    #url(r'^api/login/$',views.Login.as_view()),
    #url(r'^api/logout/$',views.Logout.as_view()),
    url('login/',obtain_jwt_token),
    url('me/', views.ManageUserView.as_view(),
         name='me'),
     url(r'^Search/(?P<username>[\w.@+-]+)/$', SearchList.as_view()),

     #for string using regex otherwise page not found 
     #http://127.0.0.1:8000/insta/profile/mahima-l/
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.UserProfileView.as_view(),
         name='userprofile'),
         
     url('<slug:username>/follow/', views.FollowUserView.as_view(),
          name='follow-user'),


    url('comment/<post_id>/',
         views.AddCommentView.as_view(),
         name='addcomment'),
         
    url('comment/<int:comment_id>/',
         views.ManageCommentView.as_view(),
         name='managecomment'),
    url('like/<post_id>/',
         views.LikeView.as_view(),
         name='like'),
    
#     path('<slug:username>/get-followers/', views.GetFollowersView.as_view(),
#          name='get-followers'),
#     path('<slug:username>/get-following/', views.GetFollowingView.as_view(),
#          name='get-following'),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
