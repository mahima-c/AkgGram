from django.conf.urls import url
from . import views
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.urls import include
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls

router = DefaultRouter()

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/signup/$', views.SignUp.as_view()),
    url(r'^api/activate/(?P<user_id>[0-9]+)/$', views.Activate.as_view(), name='activate'),
    url(r'^api/resendotp/(?P<user_id>[0-9]+)/$',views.ResendOtp.as_view(), name='resend-otp'),
    url(r'^api/login/$',views.Login.as_view()),
    url(r'^api/logout/$',views.Logout.as_view()),
    url(r'^docs/', include_docs_urls(title='My API title'))
    ]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
