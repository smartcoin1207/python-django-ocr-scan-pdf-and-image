from rest_framework import serializers
from core.models import Client, AccountItem, Keyword

class ClientSerializer(serializers.ModelSerializer):
    id = serializers.SlugField(required=False)
    class Meta:
        model = Client
        fields = '__all__'

class ClientUpdateSerializer(serializers.ModelSerializer):
    id = serializers.SlugField(required=False)
    class Meta:
        model = Client
        exclude = ['company']

class AccountItemSerializer(serializers.ModelSerializer):
    id = serializers.SlugField(required=False)
    class Meta:
        model = AccountItem
        fields = '__all__'

class AccountItemUpdateSerializer(serializers.ModelSerializer):
    id = serializers.SlugField(required=False)
    class Meta:
        model = AccountItem
        exclude = ['company']

class KeywordSerializer(serializers.ModelSerializer):
    id = serializers.SlugField(required=False)
    class Meta:
        model = Keyword
        fields = '__all__'

class KeywordUpdateSerializer(serializers.ModelSerializer):
    id = serializers.SlugField(required=False)
    class Meta:
        model = Keyword
        exclude = ['company']