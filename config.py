# ----------------------  BASE PARAMETERS ---------------------- #
DOCKER_IMAGE = 'ankur/compiler'
LOCAL_DIR = '/home/ankur/Documents/Projects/Docker/compiler/temp'

# ----------------------  ADDITIONAL PARAMETERS ---------------------- #
MEMORY_LIMIT = '8000k'  # the memory limit for the each docker container
AUTO_REMOVE = True # remove the docker container when it has completed the execution
FILE_OPEN_MODE = 'ro' #read only : use rw for read write
CONTAINER_DIR = '/data' # the container directory where code execution take place
CONTAINER_TIMEOUT = 8 # number of seconds the container is allowed to run
