from rest_framework.views import APIView
from rest_framework import status
import os
import hashlib
from rest_framework.response import Response
from docker_util import run_code

class CompileCodeView(APIView):

    def post(self, request):
        code = request.data['code']
        file_name = str(hashlib.sha1(os.urandom(128)).hexdigest())[:10] + '.py'
        file_path = 'temp/' + file_name
        file = open(file_path, 'w')
        file.write(code)
        file.close()

        output = run_code(file_name, file_name)
        os.remove(file_path)

        result = output['result'] if 'result' in output else ''

        return Response(result, status=status.HTTP_200_OK)

