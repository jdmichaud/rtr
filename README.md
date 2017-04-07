# rtr

Real Time Rest for django

## What does it do?

From a `ModelViewSet` provided by [django-restframework](http://www.django-rest-framework.org/), this package allows you to easily moditor the change of model from an REST frontend. Just add the RTView to your url and your done:
```
url(r'^', include(RTView.as_view(r'my-models', MyModelViewSet))),
```

You can then perform long polling by GETting `my-models-rt/`.

## What are those folders?

This repo is composed of:

1. a [django package](django-realtime-rest/README.md) to enable realtime update through long-polling,
2. **WIP** an [npm module](realtime-rest/README.md) to easily use the realtime REST api provided by the latter and
3. a [test application](django-realtime-rest-test/README.md) to demonstrate the use of the package.

## How do I install it?

To install the django package, just:
```
pip instal -e git+https://github.com/jdmichaud/rtr.git#egg=django-realtime-rest&subdirectory=django-realtime-rest
```

## Need more help?

See the frontend module [README](realtime-rest/README.md) or the tests [README](django-realtime-rest-test/README.md).
