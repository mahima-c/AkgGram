from django.conf.urls import url,include
from insta.auth import urls as auth_urls
#from insta.views.item import Itemlist,ItemDetail




urlpatterns = [
    url('auth/', include('auth_urls')),

    #url('item/', Itemlist.as_view(),name='Itemlist'),
    #url('item/<int:pk>/', ItemDetail.as_view(),name='ItemDetail'),

]
