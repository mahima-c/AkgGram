from django.conf.urls import url
from insta.auth import views 

urlpatterns = [
    url('me/', views.UserView.as_view(),name='user'),
    url('me/profile/', views.ProfileView.as_view(),name='profile'),
    url('me/login/', views.LoginView.as_view(),name='login'),
    url('me/logout/', views.LogoutView.as_view(),name='logout'),
    url('me/register/', views.RegisterView.as_view(),name='register'),
]