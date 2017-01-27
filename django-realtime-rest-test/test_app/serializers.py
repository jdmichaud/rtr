from rest_framework import serializers
from test_app.models import MyModel

class MyModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = MyModel
    fields = (
      'myField',
    )

