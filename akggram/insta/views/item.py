'''from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from insta.models import Item
from insta.serializers import  ItemSerializer,ItemDetailSerilizer
from rest_framework import generics,mixins,status
from rest_framework.response import Response
from django.conf import settings


# Create your views here.
class ItemList(generics.ListCreateAPIView):
    """
    List:create,list
    """
    queryset = Item.objects.all()
    serializer_class =ItemSerializer

    def list(self,request):
        self.serializer_class=ItemSerializer
        return super(ItemList,self).list(request)

class IremDetail(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer = ItemDetailSerilizer(queryset,many=False)  

    def retrieve(self,request,pk):
        queryset = self.get.object()
        serializer = ItemDetailSerilizer(queryset,many=False)
        return Response(serializer.data)
'''