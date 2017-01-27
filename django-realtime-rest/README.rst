===
Realtime Rest
===
This package leverage the ModelViewSet class provided by the package
django-restframework in order to offer long-polling solutions on REST resources.

Quick Start
===
1. Add 'realtime_rest' to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'realtime_rest',
    ]
2. In your url.py, add a RTView class using the `include` function
 url(r'^', include(RTView.as_view(r'my-models', MyModelViewSet))),

3. Call the GET method on .../my-models-rt/

The call will return with the equivalent of the call to .../my-models/ if any
MyModel object is modified, delete or created in the database.
