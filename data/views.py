from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django_q.tasks import async_task
from core.models import  User, Company, Result, History
from .functions import process_data_with_document_ai, generate_json_data
from .tasks import process_document
from .serializers import HistorySerializer, ResultSerializer
# from .serializers import (
#   ClientSerializer,
#   )
import logging, tempfile, shutil, uuid, os
from django.conf import settings

logging.basicConfig(level=logging.DEBUG)

@api_view(['POST'])
def read_from_image(request):
    if 'file' not in request.FILES:
        return Response({"error": "File not provided."}, status=status.HTTP_400_BAD_BAD_REQUEST)
    file = request.FILES['file']
    if 'type' not in request.data:
        return Response({'error': 'No type provided'}, status=status.HTTP_400_BAD_REQUEST)
    ledger_type = request.data['type']

    result = process_data_with_document_ai(file)

    json_data = generate_json_data(ledger_type, result)

    return Response({'data': json_data }, status=status.HTTP_200_OK)

@api_view(['POST'])
def process_ocr(request):
    if 'file' not in request.FILES:
        return Response({"error": "File not provided."}, status=status.HTTP_400_BAD_BAD_REQUEST)
    files = request.FILES.getlist('file')
    user_id = request.query_params.get('user')
    company_id = request.query_params.get('company')
    ledger_type = request.query_params.get('ledger')

    try:
        user = User.objects.get(pk=user_id)
        company = Company.objects.get(pk=company_id)
    except (User.DoesNotExist, Company.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {
        'name': files[0].name if files[0].name else '',
        'ledger_type': ledger_type,
        'num_pages': len(files),
        'user': user.pk,
        'company': company.pk
    }

    serializer = HistorySerializer(data=data)
    if serializer.is_valid():
        history = serializer.save()
        history_id = history.id

        # historyの保存後、すぐにhistory id をフロントに返す。同時に非同期でOCRタスクを開始
        for idx, file in enumerate(files):
            mime_type = file.content_type
            # temp_file_suffix = f"_{idx}_{uuid.uuid4()}"
            # with tempfile.NamedTemporaryFile(suffix=temp_file_suffix, delete=False) as temp_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                shutil.copyfileobj(file, temp_file)
                temp_file_path = temp_file.name
            async_task(process_document, idx, history_id, mime_type, ledger_type, temp_file_path)
        return Response({'history_id': history_id}, status=status.HTTP_201_CREATED)
    else:
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
def manage_result(request, id):
    if request.method == 'GET':
        result = Result.objects.get(id=id)
        serializer = ResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        data = request.data.get('data')
        result = Result.objects.get(id=id)
        result.data = data
        result.save()
        serializer = ResultSerializer(result)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_results_by_history(request, history_id):
    results = Result.objects.filter(history_id=history_id).all().order_by('index')
    serializer = ResultSerializer(results, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_results_with_history(request, history_id):
    results = Result.objects.filter(history_id=history_id).all().order_by('index')
    history = History.objects.get(id=history_id)
    result_serializer = ResultSerializer(results, many=True)
    history_serializer = HistorySerializer(history)
    return Response({'results': result_serializer.data, 'history': history_serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_history(request, company_id):
    history = History.objects.filter(company_id=company_id).all().order_by('created_at')
    serializer = HistorySerializer(history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)