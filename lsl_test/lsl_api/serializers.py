from rest_framework import serializers
from .models import LSLScript,Result

class LSLScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = LSLScript
        fields = ['script', 'email', 'share', 'type']
