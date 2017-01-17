from django.conf.urls import url
from test_app.views import MyModelList

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
  url(r'^my-models$', MyModelList.as_view(), name='my-model-list'),
]
