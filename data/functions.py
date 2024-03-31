from google.cloud import documentai_v1 as documentai
import google.generativeai as genai
import os, json, base64


def process_document(file):
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
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_json

    #OCRの環境変数を設定
    project_id = 'wingaiocr'
    location = 'us'
    processor_id = '4f6a660f137b320c'

    #ファイルのコンテントを読み出す
    content = file.read()
    mime_type = file.content_type

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

    return result.document


def generate_json_data(prompt):
    genai.configure(api_key=os.environ["GOOGLE_AI_STUDIO_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    # Print the raw response
    print("Raw response:", response.text)

    # Clean the response
    cleaned_data = response.text.strip('` \n').replace('json\n', '').strip()

    # Print the cleaned data
    print("Cleaned data:", cleaned_data)

    # Attempt to load the JSON
    try:
        data = json.loads(cleaned_data)
        return data
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        # Return or handle the error appropriately
        return None