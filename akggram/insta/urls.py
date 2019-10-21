from django.conf.urls import url,include
from insta.auth import urls as auth_urls


urlpatterns = [
    url(r'^auth/',include(auth_urls)),
]


