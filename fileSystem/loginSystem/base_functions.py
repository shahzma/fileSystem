import msal

CLIENT_ID = '77580eec-927d-44a1-83c6-2b98c8b94e90'
TENANT_ID = '00a9ff8c-9830-4847-ae51-4579ec092cb4'
AUTHORITY_URL = 'https://login.microsoftonline.com/{}'.format(TENANT_ID)
RESOURCE_URL = 'https://graph.microsoft.com/'
API_VERSION = 'v1.0'
USERNAME = 'shahzma@redseerconsulting.com' #Office365 user's account username
PASSWORD = 'Ironman@3ms'
SCOPES = ['Sites.ReadWrite.All', 'Files.ReadWrite.All']


def get_token():
    app2 = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY_URL)
    token2 = app2.acquire_token_by_username_password(USERNAME, PASSWORD, SCOPES)
    return(token2)
