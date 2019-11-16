
from django.conf.urls import url
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.urls import include
from rest_framework.documentation import include_docs_urls
from .views import PostViewSet,UpdateUserView
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from . import views
from .views import SearchViewset


app_name = 'insta'

router = DefaultRouter()
router.register(r'post',views.PostViewSet)
# router.register(r'search/(?P<username>)',SearchViewset,basename='')

#http://127.0.0.1:8000/insta/api/post/

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/signup/$', views.SignUp.as_view()),
    #url( r'^/api/post/$',PostViewSet.as_view(),name='post'),
#    url(r'^api/post/$', views.PostViewSet()),

    url(r'^api/activate/(?P<user_id>[0-9]+)/$', views.Activate.as_view(), name='activate'),
    url(r'^api/resendotp/(?P<user_id>[0-9]+)/$',views.ResendOtp.as_view(), name='resend-otp'),
    #url(r'^api/login/$',views.Login.as_view()),
    #url(r'^api/logout/$',views.Logout.as_view()),
    url('login/',obtain_jwt_token),
    url('me/', views.UpdateUserView.as_view(),
         name='me'),
    url(r'^Search/(?P<username>[\w.@+-]+)/$', SearchViewset.as_view()),

     #for string using regex otherwise page not found 
     #http://127.0.0.1:8000/insta/profile/mahima-l/
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.UserProfileView.as_view(),
         name='userprofile'),
         
    url(r'^follow/(?P<username>[\w.@+-]+)/$', views.FollowUserView.as_view(),
          name='follow-user'),


    url(r'^comment/(?P<post_id>[0-9]+)/$',views.AddCommentView.as_view(),name='addcomment'),
         
    url(r'^comment/manage/(?P<comment_id>[0-9]+)/$',views.ManageCommentView.as_view(),name='managecomment'),
     #r'^/(?P<user_id>[0-9]+)/$'
    url(r'^like/(?P<post_id>[0-9]+)/$',views.LikeView.as_view(),name='like'),
    

    url(r'^followers/(?P<username>[\w.@+-]+)/$',views.FollowersView.as_view(),name='getfollowers'),
    url(r'^following/(?P<username>[\w.@+-]+)/$',views.FollowingView.as_view(),name='getfollowing'),

    ]
