import boto3
import botocore.exceptions
from botocore.client import Config
import zipfile
from io import BytesIO
import awsConfig


def handle_upload_img(f):  # f = 파일명
    data = open(f, 'rb')
    # '로컬의 해당파일경로'+ 파일명 + 확장자
    s3 = boto3.resource(
        's3',
        aws_access_key_id=awsConfig.ACCESS_KEY_ID,
        aws_secret_access_key=awsConfig.ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    s3.Bucket(awsConfig.BUCKET_NAME).put_object(
        Key=f, Body=data)


def read_zip(f):
    try:
        s3_resource = boto3.resource(
            's3',
            aws_access_key_id=awsConfig.ACCESS_KEY_ID,
            aws_secret_access_key=awsConfig.ACCESS_SECRET_KEY,
            config=Config(signature_version='s3v4')
        )
        zip_obj = s3_resource.Object(bucket_name=awsConfig.BUCKET_NAME, key=f)
        buffer = BytesIO(zip_obj.get()["Body"].read())
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print("Cant search file")

    z = zipfile.ZipFile(buffer)
    for filename in z.namelist():
        file_info = z.getinfo(filename)
        s3_resource.meta.client.upload_fileobj(
            z.open(filename),
            Bucket=awsConfig.BUCKET_NAME,
            Key=f'{filename}'
        )


# if __name__ == '__main__':
    # handle_upload_img("dog-and-cat")
    # read_zip("dog-and-cat")
