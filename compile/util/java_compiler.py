import os
from config import DOCKER_IMAGE, LOCAL_DIR, CONTAINER_DIR
import traceback


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
            psvm_class_name = class_splitter[len(class_splitter) - 1].split('{')[0].strip()
        except:
            return_dict['result'] = "public static void main not found!"
            return

        psvm_java_file_name = str(psvm_class_name) + '.java'
        container_directory = CONTAINER_DIR + '/' + psvm_java_file_name

        java_output_dir = LOCAL_DIR + '/' + container_name + 'temp'
        _file = open(java_output_dir, "w+")
        _file.close()

        container_run_command = 'docker run -d -it -v {0}:{1} --name {2} {3}'.format(local_directory,
                                                                                     container_directory,
                                                                                     container_name, DOCKER_IMAGE)
        os.system(container_run_command)

        container_id = client.containers.list(filters={'name': container_name})[0].short_id

        java_compile_command = 'docker exec -it {0} javac {1}'.format(container_id, str(psvm_java_file_name))
        system_compile_command = '{0} > {1}'.format(java_compile_command, java_output_dir)
        os.system(system_compile_command)

        with open(java_output_dir, 'r') as content_file:
            compile_output = content_file.read()

        if compile_output:
            os.remove(java_output_dir)
            return_dict['result'] = str(compile_output)
            return

        java_run_command = 'docker exec -it {0} java {1}'.format(container_id, str(psvm_class_name))
        system_run_command = '{0} > {1}'.format(java_run_command, java_output_dir)
        os.system(system_run_command)

        run_output = open(java_output_dir, 'r').read()

        os.remove(java_output_dir)
        return_dict['result'] = str(run_output)
    except Exception as e:
        print traceback.print_exc()
        return_dict['result'] = e.message
