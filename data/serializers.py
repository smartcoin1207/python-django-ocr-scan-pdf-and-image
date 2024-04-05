from rest_framework import serializers
from core.models import History, Result, User

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
        read_only_fields = ('id',)

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ('id',)

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']

class SimpleHistorySerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    class Meta:
        model = History
        fields = ['name', 'ledger_type', 'num_pages', 'user', 'created_at']

class ResultDetailsSerializer(serializers.ModelSerializer):
    history = SimpleHistorySerializer(read_only=True)
    class Meta:
        model = Result
        fields = ['id', 'index', 'data', 'history']