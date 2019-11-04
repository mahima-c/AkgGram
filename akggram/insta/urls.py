from django.conf.urls import url
from . import views
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.urls import include
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls
from .views import PostViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'post',views.PostViewSet)
#http://127.0.0.1:8000/insta/api/post/

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/signup/$', views.SignUp.as_view()),
    #url( r'^/api/post/$',PostViewSet.as_view(),name='post'),

    url(r'^api/activate/(?P<user_id>[0-9]+)/$', views.Activate.as_view(), name='activate'),
    url(r'^api/resendotp/(?P<user_id>[0-9]+)/$',views.ResendOtp.as_view(), name='resend-otp'),
    url(r'^api/login/$',views.Login.as_view()),
    url(r'^api/logout/$',views.Logout.as_view()),
    
    url('comment/<uuid:post_id>/',
         views.AddCommentView.as_view(),
         name='add-comment'),
         #http://127.0.0.1:8000/insta/comment/4/
    url('comment/<int:comment_id>/',
         views.ManageCommentView.as_view(),
         name='manage-comment'),
    url('like/<uuid:post_id>/',
         views.LikeView.as_view(),
         name='like'),
    url('<uuid:post_id>/get-likers/',
         views.GetLikersView.as_view(),
         name='get-likers'),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
