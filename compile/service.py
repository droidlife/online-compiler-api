from compile.util.python_compiler import python_runner
from compile.util.java_compiler import java_runner

commands = {
    'python': {
        2: 'python',
        3: 'python3'
    },
    'java': {
        8: 'javac'
    }
}


extensions = {
    'python': '.py',
    'java': '.java'
}

def get_command(language, version):
    if language not in commands:
        return False, 'Invalid language.'

    if version not in commands[language]:
        return False, 'Invalid version.'

    return True, commands[language][version]


def get_extension(language):
    return extensions[language]

def get_target_method(language):
    if language == 'python':
        return python_runner

    elif language == 'java':
        return java_runner