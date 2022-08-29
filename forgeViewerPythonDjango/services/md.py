from dotenv import load_dotenv
import os
from autodesk_forge_sdk import ModelDerivativeClient, OAuthTokenProvider

load_dotenv()

client = ModelDerivativeClient(OAuthTokenProvider(
    os.getenv("FORGE_CLIENT_ID"), os.getenv("FORGE_CLIENT_SECRET")))


def translate_object(urn, output_formats):
    job = client.submit_job(urn, output_formats)
    return job


def get_manifest(urn):
    manifest = client.get_manifest(urn)
    return manifest
