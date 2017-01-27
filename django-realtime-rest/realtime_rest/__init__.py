from threading import Condition
from django.conf.urls import url
from django.db.models.signals import post_save
from rest_framework import routers


class RTView():
  def __init__(self, prefix, viewSetClass):
    self.viewSetClass = viewSetClass
    self.router = routers.DefaultRouter()
    self.router.register(prefix, viewSetClass)
    self.cv = Condition()
    # Positioned to True is post_save signal handler is called
    self.updatedInstances = []
    # Hook the post save signal
    post_save.connect(self.post_save_handler, sender=self.viewSetClass.queryset.model)
    # Create the urls map based on the rest_
    rtRouteRegex = '^' + prefix + '-rt' + '/$'
    self.urls = self.router.urls + [url(rtRouteRegex, self.view, name=prefix)]

  @classmethod
  def as_view(cls, prefix, viewSetClass):
    view = cls(prefix, viewSetClass)
    return view.urls

  def view(self, request, *args, **kwargs):
    # wait for a change
    self.cv.acquire()
    self.cv.wait()
    self.cv.release()
    return self.urls[0].callback(request, *args, **kwargs)

  def post_save_handler(self, sender, instance, **kwargs):
    self.cv.acquire()
    # self.updatedInstances.append(instance)
    self.cv.notifyAll()
    self.cv.release()
