function poll(getFn, url, model) {
  return getFn(url).then((response) => {
    if (typeof model === 'function') {
      model(JSON.parse(response.data));
    } else {
      model = JSON.parse(response.data);
    }
  });
}

function RTViewModule() {
  /**
   * An embedded get function based on XMLHttpRequest, provided by modern
   * browsers.
   * @param  {string}     url
   * @return {[Promise]}  Promise resolved on server response.
   */
  this.browserGet = function browserGet(_url) {
    return new Promise((resolve, reject) => {
      const xmlHttp = new XMLHttpRequest();
      xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
          resolve({ status: xmlHttp.status, data: xmlHttp.responseText });
        } else {
          reject(xmlHttp);
        }
      };
      xmlHttp.open('GET', _url, true); // true for asynchronous
      xmlHttp.send(null);
    });
  };

  /**
   * An embedded get function based on node's http module, provided by the
   * node standard library.
   * @param  {string}     url
   * @return {[Promise]}  Promise resolved on server response.
   */
  this.nodeGet = function nodeGet(_url) {
    return new Promise((resolve, reject) => {
      var http = require('http');
      const urlModule = require('url');
      if (!_url.startsWith('http')) _url = `http://${_url}`;
      _url = urlModule.parse(_url);
      const req = http.request({
        hostname: _url.hostname,
        port: _url.port,
        path: _url.path,
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      }, (res) => {
        if (res.statusCode !== 200) {
          reject({ status: res.statusCode, response: `Request Failed.\nStatus Code: ${res.statusCode}` });
        } else if (!/^application\/json/.test(res.headers['content-type'])) {
          reject({
            status: res.statusCode,
            response: `Invalid content-type.\nExpected application/json but received ${res.headers['content-type']}`,
          });
        }
        let data = '';
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () => {
          resolve({ data: data });
        });
      });
      req.on('error', (e) => {
        reject({ status: e.statusCode, response: e.message });
      });
      req.end();
    });
  };

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
  this.RTView = function RTView(url, model, httpGet) {
    const service = {};
    let running = false;
    const getFn = (httpGet || service.browserGet);


    service.monitor = function monitor() {
      running = true;

      function next(condition) {
        if (condition) {
          // setTimeout make this a non recursive called to avoid stack overflow.
          poll(getFn, url, model)
            .then(() => setTimeout(next(running), 0))
            .catch(() => {}); // Silently ignore
        }
      }
      next(running);
    };

    service.interrupt = function () { running = false; };

    return service;
  };

  return this;
}

module.exports = RTViewModule();
