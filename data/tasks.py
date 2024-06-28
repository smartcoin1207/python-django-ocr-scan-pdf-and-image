import logging
from .serializers import ResultSerializer
import os, logging
import time
from django.conf import settings
from .functions import (
    process_data_with_document_ai,
    generate_json_data,
)

logger = logging.getLogger(__name__)

def process_document(idx, history_id, mime_type, ledger_type, file_path, filename):
    logger.info(f"STARTED: PROCESS No.{idx}")
    try:
        uploads_dir = os.path.join(settings.BASE_DIR, 'media')
        os.makedirs(uploads_dir, exist_ok=True)

        # Construct the file path for saving the file
        timestamp = str(int(time.time()))
        file_extension = ".jpg"
        saved_file_name = f"{timestamp}-{idx}-{file_extension}"
        saved_file_path = os.path.join(uploads_dir, saved_file_name)

        # Copy the file to the uploads directory
        with open(saved_file_path, 'wb') as f:
            with open(file_path, 'rb') as source_file:
                f.write(source_file.read())
                
        result = process_data_with_document_ai(file_path, mime_type)
        logger.info(f"Sanned info {result}")
        json_data = generate_json_data(ledger_type, result)

        filepath_filename = os.path.basename(saved_file_path)
        data = {
            "index": idx,
            "data": json_data,
            "history": history_id,
            "file_name": filename,
            "filePath" : filepath_filename
        }

        serializer = ResultSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            logger.error(f"ResultSerializer is invalid for index {idx} with errors: {serializer.errors}")
            temp_data = {
                "index": idx,
                "data": {},
                "history": history_id
            }
            serializer = ResultSerializer(data=temp_data)
            if serializer.is_valid():
                serializer.save()
            else:
                logger.error(f"Fallback ResultSerializer is also invalid for index {idx} with errors: {serializer.errors}")
    except Exception as e:
        logger.exception(f"Error processing document at index {idx}: {e}")