Title: Building A 'Hello World' Docker Image For A Python Service
Date: 2017-04-16 10:20
Category: Articles

_Note: this walkthrough assumes you have Python 3 and docker installed on your machine._

Python 3.4 added support for asynchronous I/O code, known as [asyncio](https://docs.python.org/3/library/asyncio.html). 
Asyncio allows writing performant code that would have previously been bottlenecked by IO performance, and has spawned 
a number of great libraries based on it. One of these libraries is [aiohttp](http://aiohttp.readthedocs.io/en/stable/),
an asynchronous HTTP client/server which can support much larger number of parallel requests when compared to other 
client-side libraries (e.g. urllib or requests), or server-side libraries (e.g. flask). 

After a cursory search, I could not find a Docker image with a basic 'hello world' implementation of an aiohttp server,
so decided to build one, and document the process. 
<!-- PELICAN_END_SUMMARY -->

Creating the service in Python
------------------------------

For a basic hello-world style service only two files are needed:
- server.py with the routing and handler code
- requirements.txt to list the external dependencies. For this project, it'll only be the `aiohttp` package

To start, create a directory to contain the project files, e.g. docker-aiohttp-hello-world. 

In the directory, create the 'requirements.txt' file and add the aiohttp dependency to it:

    aiohttp==2.0.7


I'm pinning the version to 2.0.7 to ensure the image still works if future releases of aiohttp break backwards 
compatibility.

Then create 'server.py' file, and add the example code, slightly modified from aiohttp's docs:

    from aiohttp import web

    async def handle(request):      
        name = request.match_info.get('name', "World!")
        text = "Hello, " + name
        print('received request, replying with "{}".'.format(text))
        return web.Response(text=text)

    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_get('/{name}', handle)

    web.run_app(app, port=5858)

Install the dependencies listed in requirements.txt by running `pip install -r requirements.txt`. You can now run the 
service, and will see it's running on port 5858 after it starts:

```
Connected to pydev debugger (build 163.10154.50)
======== Running on http://0.0.0.0:5858 ========
(Press CTRL+C to quit)
```

Hitting the service at http://localhost:5858 will display the hello world message:
```
Hello, World!
```

While adding another segment to the url will use it as the `name` variable. http://localhost:5858/everybody will return:
```
Hello, everybody
```

This means the service is working as expected. We can stop it, and focus on creating a Docker image for it.  



Creating the Docker image
-------------------------

To run this service in Docker, we need to specify that:

* The base image to use is the python:3 image
* The server.py and requirements.txt files need to be included in the new image
* PIP needs to install the dependencies listed in requirements.txt
* The service itself needs to be run

To achieve this, first create a file called 'Dockerfile' in the same directory as the other files. 

Add the line instructing Docker to use the python:3 base image:
```
FROM python:3
```

This will pull a base image that already has Python 3 installed, so there is no need to set it up separately.

Next, add the line indicating the two files that need to be added to the new image:
```
COPY server.py /
COPY requirements.txt /
```

Then, add the line that will install the Python application's dependencies from requirements.txt:
```
RUN pip install -r requirements.txt
```

The RUN command is executed when the image is built, as opposed to the CMD command, which is executed when the docker image is actually run 
(i.e. a running container is actually created).

Lastly, add the line that instructs Docker to start our Python service when the image is run:
```
CMD [ "python", "-u", "server.py" ]
```

The '-u' parameter will instruct the Python interpreter to not buffer the output to console. Without this, the 
Python output does not seem to be forwarded to the docker host. 

To contrast the last two commands, `RUN` and `CMD`:
- `RUN` will be executed during the creation of the docker image. Thus, any changes to the file system (e.g. 
downloading dependencies from PIP) will be included in the image
- `CMD` will be executed when the docker image is run. The 'pip install' command could be performed at this step
as well, but it would slow down the start time of each instance. 

After this, your Dockerfile should look like this:
```
FROM python:3
COPY server.py /
COPY requirements.txt /
RUN pip install -r requirements.txt
CMD [ "python", "-u", "server.py" ]
```

To build the docker image, open your command prompt/shell at the directory you created the sources, and run:
```
docker build -t docker-aiohttp-hello-world .
```
This will build the image and give it a 'docker-aiohttp-hello-world' name tag. After running this, you should 
see docker successfully create the image, finishing with a message similar to `Successfully built 776b870cbe1d`.

You can now run the new docker image by executing:
```
docker run -p 5858:5858 docker-aiohttp-hello-world
```  

This will run the image in a new container, and map the service's 5858 port to the host's 5858 port. You should see the 
output of the service forwarded to your console:

```
C:\dev\git\docker-aiohttp-hello-world>docker run -p 5858:5858 docker-aiohttp-hello-world
======== Running on http://0.0.0.0:5858 ========
(Press CTRL+C to quit)
```

Hitting http://localhost:5858 should again return 'Hello, World!', but this time you are hitting the service running in 
a Docker container. You should see this reflected in the STDOUT:
```
======== Running on http://0.0.0.0:5858 ========
(Press CTRL+C to quit)
received request, replying with "Hello, World!".
received request, replying with "Hello, World!".
```

To publish the Docker image to Docker Hub, follow the steps [here](https://docs.docker.com/engine/getstarted/step_six/). 
I've published the image to a docker repo, and it can be run by executing:
```
docker run -p 5858:5858 rendijssmukulis/docker-aiohttp-hello-world
```
This means the service can be run from any machine that has docker installed and has access to the docker repository, 
e.g. in Amazon's EC2 Container Service.

_The entire source can be found on [github](https://github.com/RendijsSmukulis/docker-aiohttp-hello-world)_