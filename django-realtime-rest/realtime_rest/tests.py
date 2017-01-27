import threading
from functools import wraps

from django.test import TestCase

from django.test.client import Client as DjangoClient
from django.test.client import RequestFactory as DjangoRequestFactory

from django.db import models
from django.db.models import signals
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from views import RTView


class TestModel(models.Model):
  myField = models.CharField(max_length=128)


class TestModelSerializer(serializers.ModelSerializer):
  class Meta:
    model = TestModel
    fields = (
      'myField',
    )


class TestModelViewSet(ModelViewSet):
  queryset = TestModel.objects.all()
  serializer_class = TestModelSerializer


def setTimeout(fn, delay=0.):
  """
  Decorator delaying the execution of a function for a while.
  Warning: delay is in seconds
  """
  timer = threading.Timer(delay, fn)
  timer.start()
  return timer


class RTViewTestCase(TestCase):
  prefix = 'test-model'

  def test_urls(self):
    urls = RTView.as_view(RTViewTestCase.prefix, TestModelViewSet)
    self.assertEquals(4, len(urls))
    self.assertEquals('^test-model-rt/$', urls[-1].regex)

  def test_long_poll(self):
    # How to test long polling easily?
    pass
