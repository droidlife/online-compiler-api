# Docker Compiler
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
> Online compiler API using docker

# Overview
This uses docker to compile untrusted code from the client and DRF is used to provide the high level api. 
<br>
Just a simple POST call with form data is enough to compile the code and get the output.

![Alt Text](https://res.cloudinary.com/ankurj/image/upload/v1523729772/ezgif.com-video-to-gif_ay6su2.gif)

# Language Supported
1. Python 2 <br>
2. Python 3 <br>
3. Java 8

# Requirements
* Python (2.x, 3.x)
* Django (1.8+)
* Django REST (3.x)
* Docker

# Installation

1. Install <a href="https://docs.docker.com/install/" target='_blank'>docker</a>.

2. Install python dependencies by running<br>
   `pip install -r requirements.txt`
 
3. Go to the root of the code directory where the Dockerfile is located and build the docker image by running <br>
  `docker build -t <image_name> .`
  
4. Open config.py and set the base parameters:

   * <b>DOCKER_IMAGE</b> :  The name of the docker image created
   * <b>LOCAL_DIR</b> : The path of the local directory needed to save the code.

# Execution

1. Run the django development server by running the command<br>
   `python manage.py runserver`

2. Make a <b>POST</b> api call to `http://localhost:8000/compile/code` with following parameters as <b>form-data</b>:
   * <b>code: </b> print "hello world"
   * <b>language: </b> 'python'
   * <b>version: </b> 2
