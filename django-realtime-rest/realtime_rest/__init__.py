
from functools import partial
from threading import Condition, Lock
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
    self.updated_instances = []
    self.updated_instances_mutex = Lock()
    # Hook the post save signal
    post_save.connect(partial(self.post_save_handler, self=self),
                      sender=self.viewSetClass.queryset.model)
    # Create the urls map based on the rest_
    primaryRoute = self.router.urls[0]
    rtRouteRegex = primaryRoute._regex[:-2] + '-rt' + primaryRoute._regex[-2:]
    rtRouteView = partial(self.view, self=self)
    self.urls = self.router.urls + [url(rtRouteRegex, rtRouteView, name=prefix)]

  @classmethod
  def as_view(cls, prefix, viewSetClass):
    view = cls(prefix, viewSetClass)
    return view.urls

  def view(self, request):
    # wait for a change
    self.cv.acquire()
    while not len(self.updated_instances) > 0:
      self.cv.wait()
    self.cv.release()
    self.updated_instances_mutex.acquire()
    self.updated_instances = []

  def post_save_handler(self, sender, instance, **kwargs):
    print('post_save_handler')
    self.updated_instances_mutex.acquire()
    self.updated_instances.push(instance)
    self.cv.notifyAll()


# curl -siL -w'\n' -X UPDATE -d '{ "myField": "test" }' localhost:8000/api/my-models/0/ -H "Content-Type: application/json"
