from dotenv import load_dotenv
import os
import requests
from autodesk_forge_sdk import AuthenticationClient, Scope

load_dotenv()

client = AuthenticationClient()
internal_auth_client = client.authenticate(
    os.getenv("FORGE_CLIENT_ID"), os.getenv("FORGE_CLIENT_SECRET"), [Scope.BUCKET_READ, Scope.BUCKET_CREATE, Scope.DATA_READ, Scope.DATA_WRITE, Scope.DATA_CREATE])
public_auth_client = client.authenticate(
    os.getenv("FORGE_CLIENT_ID"), os.getenv("FORGE_CLIENT_SECRET"), [Scope.VIEWABLES_READ])
