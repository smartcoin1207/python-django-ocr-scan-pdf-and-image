from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from core.models import  Client, AccountItem, Keyword
from .functions import process_document, generate_json_data
from .utils import get_card_billing_prompt, get_bankbook_prompt
# from .serializers import (
#   ClientSerializer,
#   )
import logging

logging.basicConfig(level=logging.DEBUG)

@api_view(['POST'])
def read_from_image(request):
    if 'file' not in request.FILES:
        return Response({"error": "File not provided."}, status=status.HTTP_400_BAD_BAD_REQUEST)
    file = request.FILES['file']
    filename = file.name
    if 'type' not in request.data:
        return Response({'error': 'No type provided'}, status=status.HTTP_400_BAD_REQUEST)
    data_type = request.data['type']
    
    result = process_document(file)
    # GEMINI API を使い データをJSONに成形
    if data_type == "クレジット明細":
        prompt = get_card_billing_prompt(result.text)
    elif data_type == "通帳":
        prompt = get_bankbook_prompt(result.text)
    json_data = generate_json_data(prompt)
    return Response({'data': json_data }, status=status.HTTP_200_OK)