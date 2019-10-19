#from django.conf.urls import url,include
#from insta.views.item import Itemlist,ItemDetail




#urlpatterns = [
    #url('auth/', include('auth.urls')),

    #url('item/', Itemlist.as_view(),name='Itemlist'),
    #url('item/<int:pk>/', ItemDetail.as_view(),name='ItemDetail'),

#]
from django.conf.urls import url
from insta.auth import views 

urlpatterns = [
    url('me/', views.UserView.as_view(),name='user'),
    url('me/profile/', views.ProfileView.as_view(),name='profile'),
    url('me/login/', views.Loginview.as_view(),name='login'),
    url('me/logout/', views.LogoutView.as_view(),name='logout'),
    url('me/register/', views.RegisterView.as_view(),name='register'),
]