from __future__ import unicode_literals

from django.db import models


class MyModel(models.Model):
  myField = models.CharField(max_length=128)
