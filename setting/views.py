
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import  Client, AccountItem, Keyword
from .serializers import (
  ClientSerializer,
  ClientUpdateSerializer,
  AccountItemSerializer,
  AccountItemUpdateSerializer,
  KeywordSerializer,
  KeywordUpdateSerializer
  )


@api_view(['GET', 'POST'])
def create_or_get_clients(request, id):
    if request.method == 'GET':
        clients = Client.objects.filter(company_id=id).all().order_by('created_at')
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        data['company'] = id
        print(data)
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def manage_client(request, id):
    try:
        client = Client.objects.get(id=id)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = ClientUpdateSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            client.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def create_or_get_acount_items(request, id):
    if request.method == 'GET':
        account_items = AccountItem.objects.filter(company_id=id).all().order_by('created_at')
        serializer = AccountItemSerializer(account_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        data['company'] = id
        serializer = AccountItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def manage_account_item(request, id):
    try:
        account_item = AccountItem.objects.get(id=id)
    except AccountItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountItemSerializer(account_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = AccountItemUpdateSerializer(account_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            account_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def create_or_get_keywords(request, id):
    if request.method == 'GET':
        account_items = Keyword.objects.filter(company_id=id).all().order_by('created_at')
        serializer = KeywordSerializer(account_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        data['company'] = id
        serializer = KeywordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE'])
def manage_keyword(request, id):
    try:
        keyword = Keyword.objects.get(id=id)
    except Keyword.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = KeywordSerializer(keyword)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = KeywordUpdateSerializer(keyword, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            keyword.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

