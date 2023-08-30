from rest_framework import serializers
from api_fetcher.models import StockCompany, StockData


class StockCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = StockCompany
        fields = '__all__'


class InitialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = '__all__'
