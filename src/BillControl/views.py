from datetime import date
import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.views import APIView

from .serializers import *
from .models import *

# Create your views here.

def cors_allow_origin(origin):
    def decorator(cls):
        _dispatch = cls.dispatch

        def wrapper(method):
            def action(self, request, *args, **kwargs):
                response = method(self, request, *args, **kwargs)
                response.headers['Access-Control-Allow-Origin'] = origin
                return response
            return action

        cls.dispatch = wrapper(_dispatch)
        return cls

    return decorator


class ListCreateBillTypes(ListCreateAPIView):
    serializer_class = BillTypeSerializer
    queryset = BillType.objects.all()

class ListBills(ListAPIView):
    serializer_class = BillSerializer
    queryset = Bill.objects.all()


class CreateBills(APIView):
    #serializer_class = BillSerializer
    #queryset = Bill.objects.all()

    def post(self, request):
        serializer = BillCreateSerializer(data = request.data)
        if serializer.is_valid():
            type = BillType.objects.get(id = serializer.data['type'])
            try:
                bill = Bill.objects.create(
                    type = type,
                    due_date = date(
                        year = serializer.data['year'],
                        month = serializer.data['month'],
                        day = type.payment_day,
                    )
                )
                bill_serializer = BillSerializer(bill)
                return Response(bill_serializer.data)
            except Exception as e:
                return Response(data = {'error': f'{e}'}, status=500)
        else:
            return Response(data={'error': f'{serializer.errors}'}, status=500)


class CreateMonthBills(APIView):
    def post(self, request):
        serializer = MonthBillsCreateSerializer(data = request.data)
        if serializer.is_valid():
            created_bills = []
            errors = []
            types = BillType.objects.all()
            for type in types:
                try:
                    bill = Bill.objects.create(
                        type = type,
                        due_date = date(
                            year = serializer.data['year'],
                            month = serializer.data['month'],
                            day = type.payment_day,
                        )
                    )
                    created_bills.append(bill)
                    #return Response(bill_serializer.data)
                except Exception as e:
                    errors.append(f'{e}')
                    #return Response(data = {'error': f'{e}'}, status=500)
            bill_serializer = BillSerializer(created_bills, many = True)
            response_data = {'data': []}
            print(bill_serializer.data)
            response_data['data'].extend(bill_serializer.data)
            response_data['errors'] = errors
            #return Response(bill_serializer.data)
            return Response(response_data)

        else:
            return Response(data={'error': f'{serializer.errors}'}, status=500)


class RetrieveUpdateDestroyBills(RetrieveUpdateDestroyAPIView):
    serializer_class = BillDetailSerializer
    queryset = Bill.objects.all()

    def put(self, request, *args, **kwargs):
        #serializer = self.serializer_class(data = request.data)
        print(json.dumps(request.data, indent = 2))
        return super().put(request, *args, **kwargs)