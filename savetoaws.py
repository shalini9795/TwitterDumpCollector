import json

import boto.s3
import boto3


def get_s3_resource(profile):
    pass


def upload_file_to_s3(file_to_upload, bucketname, key_, content_type="text/csv", make_public=True, profile=None):
    with open('DriveStore\\aws.json') as f:
        data = json.load(f)

    AWS_ACCESS_KEY_ID = data["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = data["AWS_SECRET_ACCESS_KEY"]
    '''

    :param file_to_upload:
    :param bucketname:
    :param key_:
    :param content_type: string
    :param make_public: bool
    :param profile:
    :return: downaloadable S3 file link
    '''
    try:
        s3 = boto3.resource('s3',aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        print("Uploading " + file_to_upload)
        extra_args = {}
        if (make_public == True):
            extra_args['ACL'] = "public-read"
        if content_type != None:
            extra_args['ContentType'] = content_type

        s3.meta.client.upload_file(file_to_upload, bucketname, key_, ExtraArgs=extra_args)
        downloadable_file_path = "/".join(["https://s3.amazonaws.com", bucketname, key_])
        return downloadable_file_path
    except Exception as e:
        print(e)
        raise AssertionError("Unable to upload the file")
