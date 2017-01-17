from rest_framework.generics import ListCreateAPIView
from test_app.models import MyModel
from serializers import MyModelSerializer


class MyModelList(ListCreateAPIView):
  queryset = MyModel.objects.all()
  serializer_class = MyModelSerializer
