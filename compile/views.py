from rest_framework.views import APIView
from rest_framework import status
import os
import hashlib
from rest_framework.response import Response
from util.runner import run_code

class CompileCodeView(APIView):

    def post(self, request):
        code = request.data['code']
        language = 'python'
        version = 2
        output = run_code(code, language, version)
        result = output['result'] if 'result' in output else ''

        return Response(result, status=status.HTTP_200_OK)

