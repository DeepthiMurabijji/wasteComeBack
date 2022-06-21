from attr import field
from rest_framework import serializers
from .models import *

class Collectorserializer(serializers.ModelSerializer):
    class Meta:
        model = Collector
        fields = '__all__'