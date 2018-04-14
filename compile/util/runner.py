import docker
import os
import hashlib
import multiprocessing
from compile.service import get_command, get_extension, get_target_method
from config import LOCAL_DIR, CONTAINER_TIMEOUT


def run_code(code, language, version):
    # getting the docker client
    client = docker.from_env()
    manager = multiprocessing.Manager()

    # the dict that will be send to the separate python process for collecting the result
    return_dict = manager.dict()

    # getting the command to be run
    result, command_string = get_command(language, version)

    if not result:
        return_dict['result'] = command_string
        return return_dict

    # saving the code in a temp file 
    container_name = str(hashlib.sha1(os.urandom(128)).hexdigest())[:10]
    file_name = container_name + str(get_extension(language))
    file_path = LOCAL_DIR + '/' + file_name
    file = open(file_path, 'w')
    file.write(code)
    file.close()

    # getting which compiler method will handle this request
    target_method = get_target_method(language)

    # starting the docker container in separate process
    process = multiprocessing.Process(target=target_method,
                                      args=(client, file_name, container_name, command_string, return_dict))
    process.start()

    # setting the timeout for the process
    process.join(CONTAINER_TIMEOUT)

    # if the process/container is still alive kill the process
    if process.is_alive():
        process.terminate()
        process.join()
        return_dict['result'] = 'Time limit Exceeded'

    # check if the container is still running. if yes, kill the container
    running_containers = client.containers.list(filters={'name': container_name}, all=True)
    if running_containers:
        running_containers[0].remove(force=True)

    # remove the temp file
    os.remove(file_path)
    return return_dict
