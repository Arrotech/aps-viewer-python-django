from dotenv import load_dotenv
import os
from autodesk_forge_sdk import OSSClient, OAuthTokenProvider
from autodesk_forge_sdk.md import urnify
from autodesk_forge_sdk.dm import DataRetention

load_dotenv()

client = OSSClient(OAuthTokenProvider(
    os.getenv("FORGE_CLIENT_ID"), os.getenv("FORGE_CLIENT_SECRET")))


# def create_bucket(bucket_name, data_retention_policy, region):
#     bucket = client.create_bucket(
#         bucket_key=bucket_name,
#         data_retention_policy=data_retention_policy,
#         region=region)
#     return bucket


# def get_bucket(bucket_key):
#     bucket = client.get_bucket_details(bucket_key=bucket_key)
#     return bucket


# def list_objects(bucket_key):
#     objects = client.get_objects(bucket_key=bucket_key)
#     return objects

def ensure_bucket_exists(bucket_key):
    try:
        client.get_bucket_details(bucket_key=bucket_key)
    except Exception as e:
        client.create_bucket(
            bucket_key=bucket_key,
            data_retention_policy=DataRetention.TRANSIENT,
            region='US')


def upload_object(bucket_key, filename, buff):
    ensure_bucket_exists(bucket_key=bucket_key)
    uploaded_model = client.upload_object(bucket_key, filename, buff)
    return uploaded_model


def list_objects(bucket_key):
    ensure_bucket_exists(bucket_key=bucket_key)
    objects = client.get_objects(bucket_key=bucket_key)
    objs = objects["items"]
    data = []
    for i in range(len(objs)):
        urn_dict = {"name": objs[i]["objectKey"],
                    "urn": urnify(objs[i]["objectId"])}
        data.append(urn_dict)
    return data

