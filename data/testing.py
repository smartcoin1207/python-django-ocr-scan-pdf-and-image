import os

credentials_path = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], 'r') as file:
    credentials_contents = file.read()
    print(credentials_contents)