from rest_framework.viewsets import ModelViewSet
from test_app.models import MyModel
from serializers import MyModelSerializer


class MyModelViewSet(ModelViewSet):
  queryset = MyModel.objects.all()
  serializer_class = MyModelSerializer
