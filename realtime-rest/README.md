# Small long-polling client

This tool, provided with the django-realtime-rest, can be used to easily link a model (a simple javascript object) to data fed by the server through the use of a long-polling call.

### Usage

To use it, just create an RTView object and then call monitor:
```
const rtView = RTView('/api/my-models-rt/', function (data) {
  // Do something with the data, which is a Javascript object
});
```

If you work with angular, RTView can take a third parameter which will be the function used to perform the HTTP GET call:
```
const rtView = RTView('/api/my-models-rt/', function (data) {
  $scope.evalAsynch(function () {
    // Do something with the data, which is a Javascript object
  });
}, $http.get);
```
