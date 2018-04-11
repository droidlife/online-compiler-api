import docker
import os
import multiprocessing
from config import DOCKER_IMAGE, MEMORY_LIMIT, AUTO_REMOVE, FILE_OPEN_MODE, BASE_DIR, CONTAINER_TIMEOUT


def __run_code(client, directory_where_file_is_located, file_name, container_name, return_dict):
    try:
        python_run_command = 'python ' + str(file_name)
        local_directory = str(directory_where_file_is_located) + '/' + str(file_name)
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
        return_dict['result'] = result
    except docker.errors.ContainerError as e:
        try:
            pretty_message = str(e.message).split('Traceback (most recent call last):')[1]
            return_dict['result'] = pretty_message
        except:
            return_dict['result'] = e.message
    except Exception as e:
        return_dict['result'] = e.message


def run_code(file_name, container_name):
    client = docker.from_env()
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    process = multiprocessing.Process(target=__run_code, 
                                    args=(client, BASE_DIR, file_name, container_name, return_dict))
    process.start()
    process.join(CONTAINER_TIMEOUT)
    if process.is_alive():
        process.terminate()
        process.join()
        running_containers = client.containers.list(filters={'name': container_name})
        if running_containers:
            running_containers[0].remove(force=True)

        return_dict['result'] = 'Time limit Exceeded'

    return return_dict
