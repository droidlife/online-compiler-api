from django.conf.urls import url
from compile.views import CompileCodeView
urlpatterns = [
    url(r'^compile/code$', CompileCodeView.as_view())
]