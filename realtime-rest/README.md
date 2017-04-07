# Small long-polling client

This tool, provided with the django-realtime-rest, can be used to easily link a
model (a simple javascript object) to data fed by the server through the use of
a long-polling call.

### Usage

To try it in node.js, just create an RTView object and then call monitor:
```
var realtime_rest = require('realtime_rest');
const rtView = realtime_rest.RTView('localhost:8000/api/my-models-rt/', function (data) {
  console.log(data);
}, realtime_rest.nodeGet);
rtView.monitor();
```

If you work with angular, RTView can take a third parameter which will be the
function used to perform the HTTP GET call:
```
const rtView = RTView('/api/my-models-rt/', function (data) {
  $scope.evalAsynch(function () {
    // Do something with the data, which is a Javascript object
  });
}, $http.get);
rtView.monitor();
```

### Get function

/!\ Note that by default, `realtime_rest` will use the `XMLHttpRequest` browser
function to perform the get request. If you use the tool on node, use the node
compatible function `nodeGet`. You can also provide you own implementation of
get which shall follow the following specifications:

1. It shall take a url as string
2. It shall return a ES6 promise which resolve an object containing a data field
which points to a JSON object:
```
{
  data: '[{"myField": "foo"}]',
}
```
3. It shall reject in case of error with an object like:
```
{
  status: <status code>,
  message: <error message>,
}
```

angular's `$http.get` satisfies those requirements.
