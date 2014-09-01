from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from ranking.models import Stock

# Create your views here.
@api_view(['GET'])
def get_stock_symbols(request):

    if request.method == 'GET':
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)


# Stock serializer
class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = ('exchange', 'symbol', 'name')
