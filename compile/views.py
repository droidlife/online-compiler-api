from rest_framework.views import APIView
from rest_framework import status
import os
from docker_util import run_code

class CompileCodeView(APIView):

    def get(self, request):
        code = "while True:\n\tprint 1"
        file_path = 'temp/one.py'
        file = open(file_path, 'w')
        file.write(code)
        file.close()
        print run_code()
        os.remove(file_path)