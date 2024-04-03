import logging
from .serializers import ResultSerializer
from .functions import (
    process_data_with_document_ai,
    generate_json_data,
)

logger = logging.getLogger(__name__)

def process_document(idx, history_id, mime_type, ledger_type, file_path):
    logger.info(f"STARTED: PROCESS No.{idx}")
    try:
        result = process_data_with_document_ai(file_path, mime_type)
        logger.info(f"Sanned info {result}")
        json_data = generate_json_data(ledger_type, result)

        data = {
            "index": idx,
            "data": json_data,
            "history": history_id
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