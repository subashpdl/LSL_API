from django.urls import path
from .views import LSLScriptCreateView

app_name = 'lsl_api'

urlpatterns = [
    path('create/', LSLScriptCreateView.as_view(), name='create'),
]