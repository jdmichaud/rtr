from __future__ import unicode_literals

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class MyModel(models.Model):
  myField = models.CharField(max_length=128)
