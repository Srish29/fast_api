from google.cloud import storage
import datetime
import os
from google.oauth2 import service_account
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

type1 = os.getenv("TYPE")
project_id = os.getenv("PROJECT_ID")
private_key_id = os.getenv("PRIVATE_KEY_ID")
private_key = os.getenv("PRIVATE_KEY").replace("\\n", '\n')

client_email = os.getenv("CLIENT_EMAIL")
client_id = os.getenv("CLIENT_ID")
auth_uri = os.getenv("AUTH_URI")
token_uri = os.getenv("TOKEN_URI")
auth_provider_x509_cert_url = os.getenv("AUTH_PROVIDER_X509_CERT_URL")
client_x509_cert_url = os.getenv("CLIENT_X509_CERT_URL")



info = {
    "type": type1,
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": auth_uri,
    "token_uri": token_uri,
    "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url
}
# print(info)


credentials = service_account.Credentials.from_service_account_info(info)

def move_blob(bucket_name, blob_name, destination_bucket_name, destination_blob_name):
    """Moves a blob from one bucket to another with a new name."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The ID of your GCS object
    # blob_name = "your-object-name"
    # The ID of the bucket to move the object to
    # destination_bucket_name = "destination-bucket-name"
    # The ID of your new GCS object (optional)
    # destination_blob_name = "destination-object-name"

    msg = ""
    try:
        storage_client = storage.Client()

        source_bucket = storage_client.bucket(bucket_name)
        source_blob = source_bucket.blob(blob_name)
        destination_bucket = storage_client.bucket(destination_bucket_name)

        blob_copy = source_bucket.copy_blob(
            source_blob, destination_bucket, destination_blob_name
        )
        source_bucket.delete_blob(blob_name)
        msg = "success"
        print(
            "Blob {} in bucket {} moved to blob {} in bucket {}.".format(
                source_blob.name,
                source_bucket.name,
                blob_copy.name,
                destination_bucket.name,
            )
        )
    except:
        msg = "failed"
    return msg


def generate_download_signed_url_v4(bucket_name, blob_name):
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        # This URL is valid for 15 minutes
        expiration=datetime.timedelta(minutes=15),
        # Allow GET requests using this URL.
        method="GET",
        credentials=credentials
    )
    return url




