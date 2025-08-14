from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from .models import *


class BillTypeSerializer(ModelSerializer):
    class Meta:
        model = BillType
        fields = [
            'id',
            'name',
            'payment_day',
            'owner',
        ]


class BillCreateSerializer(Serializer):
    type = serializers.PrimaryKeyRelatedField(queryset=BillType.objects.all())
    month = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = serializers.IntegerField()


class MonthBillsCreateSerializer(Serializer):
    month = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = serializers.IntegerField()


class BillSerializer(ModelSerializer):
    class Meta:
        model = Bill
        fields = [
            'id',
            'name',
            'type',
            'due_date',
            'paid_date',
        ]

class BillDetailSerializer(ModelSerializer):
    class Meta:
        model = Bill
        fields = [
            'name',
            'due_date',
            'paid_date',
        ]
