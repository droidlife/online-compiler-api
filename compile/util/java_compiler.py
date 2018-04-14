import docker
import os
from config import DOCKER_IMAGE, MEMORY_LIMIT, AUTO_REMOVE, FILE_OPEN_MODE, LOCAL_DIR, CONTAINER_DIR

def java_runner(client, file_name, container_name, command_string, return_dict):
    try:
        local_directory = LOCAL_DIR + '/' + str(file_name)
        
        if not os.path.exists(local_directory):
            raise Exception('File not found : ' + str(local_directory))

        with open(local_directory, 'r') as content_file:
            content = content_file.read()
        
        try:
            void_main_splitter = content.split("public static void main")
            class_splitter = void_main_splitter[0].split("class")
            psvm_class_name = class_splitter[len(class_splitter)-1].split('{')[0].strip()

            print psvm_class_name
        except:
            return_dict['result'] = "public static void main not found!"
            return
        
        psvm_java_file_name = str(psvm_class_name) + '.java'
        container_directory = CONTAINER_DIR + '/' + psvm_java_file_name

        container = client.containers.run(DOCKER_IMAGE,
                                       mem_limit=MEMORY_LIMIT,
                                       name=container_name,
                                       detach=True,
                                       tty=True,
                                       volumes={local_directory: {
                                                'bind': container_directory,
                                                'mode': FILE_OPEN_MODE}
                                                })
        
        java_output_dir = LOCAL_DIR + '/' + container_name + 'temp'

        java_compile_command = 'docker exec -it {0} javac {1}'.format(container.short_id, 
                                                                'javac ' + str(psvm_java_file_name))
        system_compile_command = '{0} > {1}'.format(java_compile_command, java_output_dir)
        os.system(system_compile_command)

        with open(java_output_dir, 'r') as content_file:
            compile_output = content_file.read()

        if compile_output:
            return_dict['result'] = str(compile_output)
            return
        
        java_run_command = 'docker exec -it {0} javac {1}'.format(container.short_id, 
                                                                'java ' + str(psvm_class_name))
        system_run_command = '{0} > {1}'.format(java_run_command, java_output_dir)
        os.system(system_run_command)

        run_output = open(java_output_dir, 'r').read()
        return_dict['result'] = str(run_output)
    except docker.errors.ContainerError as e:
        return_dict['result'] = e.message
    except Exception as e:
        print e.message
        return_dict['result'] = e.message