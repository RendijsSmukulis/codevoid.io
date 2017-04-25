Title: Hosting a Python web service in Gunicorn and Docker
Date: 2017-04-16 10:20
Category: Articles

So you've written an aiohttp (or Flask, or Tornado..) app in Python, and want to run it as a production service. 
The easiest approach would be to simply run it in production the same way you do while developing, simply 
by calling `python server.py`. While this is a simple approach, and works well while developing, aiohttp is
not a actually a webserver - it's a framework that is intended to be hosted in a production-ready webserver. 
One such webserver is [Gunicorn](http://gunicorn.org/), often used to host Python web services. The main argument for using Gunicorn
is raw performance: Gunicorn will run enough aiohttp processes to use all available CPU cores, while aiohttp's
development webserver would only run it in a single process. Other benefits of hosting aiohttp
inside Gunicorn are improved security and its configurability. There is a good post on this topic found on 
[serverfault](https://serverfault.com/questions/331256/why-do-i-need-nginx-and-something-like-gunicorn)
by the Gunicorn's developer. 

This walkthrough will start off with the code from the simple aiohttp project built in the [previous
post](//codevoid.io/building-a-hello-world-docker-image-for-a-python-service.html). You can clone it 
from [github](https://github.com/RendijsSmukulis/docker-aiohttp-hello-world) or modify the code samples to
match your own project. 
<!-- PELICAN_END_SUMMARY -->

Running Gunicorn natively
-------------------------

First, install Gunicorn:
```
pip install gunicorn
```

As it currecntly stands, `server.py` will attempt to run the aiohttp's internal webserver whenever the 
code is run as a main program, or if it is included as a module:
    :::python
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/{name}', handle)

    web.run_app(app, port=5858)


Gunicorn will include this file as a module, and we don't want the development server to be started - but 
it would be handy to still be able to run it from the python interpreter while developing. To achieve this,
add this check before the line that starts the server:

    :::python
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/{name}', handle)

    if __name__ == '__main__':
        web.run_app(app, port=5858)

Next step is to create the configuration file for Gunicorn. Create a `gunicorn.conf` file in the same folder
as `server.py`, and populate it with:
    :::python
    import multiprocessing

    # listen to port 5858 on all available network interfaces
    bind = "0.0.0.0:5858"

    # Run the aiohttp app in multiple processes
    workers = multiprocessing.cpu_count() * 2 + 1

    # Use the correct worker class for aiohttp - this will change is using a different framework
    worker_class = 'aiohttp.worker.GunicornWebWorker'

Gunicorn can now be run by calling:
```
gunicorn -c gunicorn.conf server:app
```

`-c gunicorn.conf` will instruct Gunicorn to use the appropriate config file, while `server:app` defines
the entry point into the aiohttp app. 

_Note: At the time of writing, Gunicorn does not run on Windows systems. To run it natively you will have to
use a Linux or Mac machine, or run it in Docker under Windows. The issue is tracked 
[here](https://github.com/benoitc/gunicorn/issues/524)._  

Once Gunicorn has started, it will report its state to the console:
```
2017-04-24 22:23:03 +0000] [1] [INFO] Starting gunicorn 19.7.1
2017-04-24 22:23:03 +0000] [1] [INFO] Listening at: http://0.0.0.0:5858 (1)
2017-04-24 22:23:03 +0000] [1] [INFO] Using worker: aiohttp.worker.GunicornWebWorker
2017-04-24 22:23:03 +0000] [8] [INFO] Booting worker with pid: 8
2017-04-24 22:23:03 +0000] [9] [INFO] Booting worker with pid: 9
2017-04-24 22:23:03 +0000] [10] [INFO] Booting worker with pid: 10
2017-04-24 22:23:03 +0000] [11] [INFO] Booting worker with pid: 11
2017-04-24 22:23:03 +0000] [13] [INFO] Booting worker with pid: 13
```

After seeing this, you can now hit the service with your browser at http://127.0.0.1:5858. 


Running Gunicorn in Docker
--------------------------

To run Gunicorn in Docker, we'll have to modify our existing `Dockerfile` to:
* include the gunicorn.conf file in the Docker image
* install Gunicorn
* run the service using Gunicorn rather than the Python interpreter

To copy the configuration file, add a `COPY` instruction after the `COPY` instructions already in the file:
```
COPY gunicorn.conf /
```

Next, add a command that will install the `gunicorn` dependency in the image:
```
RUN pip install gunicorn
```
Alternatively, we could have added `gunicorn` to the `requirements.txt` file, and thus have it installed
when `pip install -r requirements.txt` is run. However, the project does not require Gunicorn to run with the 
aiohttp's development server, so can be excluded from `requirements.txt`. 

Next, replace the existing `CMD` command with a call to start the Gunicorn server:
```
CMD [ "gunicorn", "-c", "gunicorn.conf", "server:app" ]
```

After this, your `Dockerfile` should look like this:
```
FROM python:3
COPY server.py /
COPY gunicorn.conf /
COPY requirements.txt /
COPY opentsdb_tagcounter_reporter.py /
COPY tagged_counter.py /
RUN pip install -r requirements.txt
CMD [ "gunicorn", "-c", "gunicorn.conf", "server:app" ]
```

You can now build and run the Docker image:
```
docker build -t docker-aiohttp-gunicorn .
docker run -p 5858:5858 docker-aiohttp-gunicorn
```

You can now verify the image has been built successfully and server is running as expected
by navigating to http://127.0.0.1:5858 .

This Docker image can now be easily shared (e.g. by uploading it to [Docker Hub](https://hub.docker.com/)) 
and run on various platforms, such as [Amazon's EC2 Container Services](https://aws.amazon.com/ecs/getting-started/).  

_The entire source can be found on [github](https://github.com/RendijsSmukulis/docker-aiohttp-gunicorn)_
