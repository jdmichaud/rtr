function embeddedHttpGet(url)
{
  return new Promise(function (resolve, reject) {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
      if (xmlHttp.readyState == 4 && xmlHttp.status == 200) {
        resolve({ status: xmlHttp.status, data: xmlHttp.responseText });
      } else {
        reject(xmlHttp);
      }
    }
    xmlHttp.open("GET", url, true); // true for asynchronous
    xmlHttp.send(null);
  });
}

function poll(getFn, url, model) {
  get(url).then((response) => {
    if (typeof model === "function") {
      model(JSON.parse(response.data));
    } else {
      model = JSON.parse(response.data);
    }
  });
}


/**
 * Create an object to interact with the -rt url of django-realtime-rest
 * @param {string}             url     the url of the -rt API (usually
 *                                     '/modelname-rt')
 * @param {function or object} model   model is either an object that will be
 *                                     updated with data sent by the server or
 *                                     a function called with the data sent by
 *                                     the server
 * @param {function}           httpGet (optional) A function that takes a url
 *                                     and returns a promise which resolves with
 *                                     the data sent by the server. Could be
 *                                     useful when working with a framework that
 *                                     uses its own http facility (e.g $http)
 */
function RTView(url, model, httpGet) {
  const service = {};
  let running = false;
  let getFn = (httpGet || embeddedHttpGet);

  service.monitor = function monitor() {
    running = true;

    function _while(condition) {
      if (condition) {
        // setTimeout make this a non recursive called to avoid stack overflow.
        poll(getFn, url, model).then(() => setTimeout(while(running), 0));
      }
    }
    _while(running);
  }

  service.interrupt = function () { running = false; };

  return service;
}

module.exports = RTView;
