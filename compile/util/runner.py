import docker
import os
import hashlib
import multiprocessing
from compile.service import get_command, get_extension, get_target_method
from config import LOCAL_DIR, CONTAINER_TIMEOUT

def run_code(code, language, version):
    client = docker.from_env()
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    result, command_string = get_command(language, version)
    
    if not result:
        return_dict['result'] = command_string 
        return return_dict

    container_name = str(hashlib.sha1(os.urandom(128)).hexdigest())[:10]
    file_name = container_name + str(get_extension(language))
    file_path = LOCAL_DIR + '/' + file_name
    file = open(file_path, 'w')
    file.write(code)
    file.close()

    
    target_method = get_target_method(language)
    process = multiprocessing.Process(target=target_method, 
                                    args=(client, file_name, container_name, command_string, return_dict))
    process.start()
    process.join(CONTAINER_TIMEOUT)
    if process.is_alive():
        process.terminate()
        process.join()
        running_containers = client.containers.list(filters={'name': container_name})
        if running_containers:
            running_containers[0].remove(force=True)

        return_dict['result'] = 'Time limit Exceeded'

    os.remove(file_path)
    return return_dict

