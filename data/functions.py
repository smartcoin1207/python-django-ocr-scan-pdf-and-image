from google.cloud import documentai_v1 as documentai
import google.generativeai as genai
from openai import OpenAI
from .utils import get_card_billing_prompt, get_bankbook_prompt
import os, json, base64, tempfile, logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# load_dotenv()

def process_data_with_document_ai(data_file_path, mime_type):
    """
    Document AI APIを使用してドキュメントを処理
    """
    # GOOGLE_APPLICATION_CREDENTIALS 環境変数を設定
    ENV = os.getenv('DJANGO_ENV', 'dev')
    if ENV == 'dev':
        credentials_path = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    elif ENV == 'prod':
        encoded_credentials = os.getenv('GOOGLE_CREDENTIALS_BASE64')
        decoded_credentials = base64.b64decode(encoded_credentials)
        credentials_json = json.loads(decoded_credentials.decode('utf-8'))
        # print(credentials_json)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            # Write credentials to the temporary file
            json.dump(credentials_json, temp_file)
            temp_file_path = temp_file.name

        # Set the environment variable
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file_path

    #OCRの環境変数を設定
    project_id = os.environ.get("DOCUMENT_AI_PROJECT_ID")
    location = os.environ.get("DOCUMENT_AI_LOCATION")
    processor_id = os.environ.get("DOCUMENT_AI_PROCESSOR_ID")

    #ファイルのコンテントを読み出す
    with open(data_file_path, 'rb') as file:
        content = file.read()

    # クライアントのインスタンス化
    documentai_client = documentai.DocumentProcessorServiceClient()

    # プロセッサーの完全なリソース名を構築
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # バイトデータをDocument AI RawDocumentオブジェクトにロード
    raw_document = documentai.RawDocument(content=content, mime_type=mime_type)

    # プロセスリクエストを構成
    request = documentai.ProcessRequest(name=resource_name, raw_document=raw_document)

    # Document AIクライアントを使用して処理
    result = documentai_client.process_document(request=request)

    if ENV == 'prod':
        os.remove(temp_file_path)

    os.remove(data_file_path)

    return result.document.text


def generate_json_data(ledger_type, result):
    logger.info(f"読み取り結果: {result}")
    if ledger_type == "クレジットカード":
        prompt = get_card_billing_prompt(result)
    elif ledger_type == "通帳":
        prompt = get_bankbook_prompt(result)

    """GEMINI"""
    # genai.configure(api_key=os.environ["GOOGLE_AI_STUDIO_API_KEY"])
    # model = genai.GenerativeModel('gemini-pro')
    # response = model.generate_content(prompt)
    # cleaned_data = response.text.strip('` \n').replace('json\n', '').strip()

    """GPT-4"""
    client = OpenAI(
        api_key=os.environ.get("OPENAI_KEY"),
    )
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt,}]
    )
    response = completion.choices[0].message.content
    cleaned_data = response.strip('` \n').replace('json\n', '').strip()

    logger.info(f"JSON: {cleaned_data}")
    try:
        data = json.loads(cleaned_data)
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return {}