from django.conf.urls import url
from insta.views.item import Itemlist,ItemDetail




urlpatterns = [
    url('item/', Itemlist.as_view(),name='Itemlist'),
    url('item/<int:pk>/', ItemDetail.as_view(),name='ItemDetail'),

]
