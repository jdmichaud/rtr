from django.conf.urls import url, include
from rest_framework import routers
from test_app.views import MyModelViewSet
from realtime_rest.views import RTView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'my-models', MyModelViewSet)

urlpatterns = [
  # url(r'^', include(router.urls)),
  url(r'^', include(RTView.as_view(r'my-models', MyModelViewSet))),
]
