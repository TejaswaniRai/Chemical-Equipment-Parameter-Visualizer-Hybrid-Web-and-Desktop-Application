from rest_framework import serializers
from .models import Dataset, Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    equipment_items = EquipmentSerializer(many=True, read_only=True)
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'uploaded_at', 'uploaded_by_username', 'total_count', 
                  'avg_flowrate', 'avg_pressure', 'avg_temperature', 'equipment_types', 
                  'equipment_items']


class DatasetSummarySerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'uploaded_at', 'uploaded_by_username', 'total_count', 
                  'avg_flowrate', 'avg_pressure', 'avg_temperature', 'equipment_types']
