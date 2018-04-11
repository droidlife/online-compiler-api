import docker
import os
import signal
from config import DOCKER_IMAGE, MEMORY_LIMIT, AUTO_REMOVE, FILE_OPEN_MODE

class InfiniteLoopException(Exception):
    pass

def handler(signum, frame):
    raise InfiniteLoopException("Infinte loop detected.")

def __run_code(client, directory_where_file_is_located, file_name, container_name):
    try:
        python_run_command = 'python ' + str(file_name)
        local_directory = str(
            directory_where_file_is_located) + '/' + str(file_name)
        container_directory = '/data/' + str(file_name)

        if not os.path.exists(local_directory):
            raise Exception('File not found : ' + str(local_directory))

        result = client.containers.run(DOCKER_IMAGE, python_run_command,
                                       remove=AUTO_REMOVE, mem_limit=MEMORY_LIMIT,
                                       name=container_name,
                                       volumes={local_directory: {
                                                'bind': container_directory,
                                                'mode': FILE_OPEN_MODE}
                                                })
        return result
    except docker.errors.ContainerError as e:
        return e
    except InfiniteLoopException as e:
        print e
        a = client.containers.list(filters={'name': container_name})
        if a:
            print 'stopping the container'
            a[0].stop()
            print 'removing the container'
            a[0].remove()

        return 'The code took more time than required. Hence the process was killed.'
    except Exception as e:
        print e
        return False

def run_code():
    client = docker.from_env()
    container_name = 'run'
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(5)
    output =  __run_code(client, '/home/ankur/Documents/Projects/Docker/compiler/temp', 'one.py', container_name)
    signal.alarm(0)
    return output