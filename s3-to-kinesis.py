import boto3
import sys


def send_to_kinesis(kinesis_stream_name, records):
    kinesis = boto3.client('kinesis')
    kinesis.put_records(StreamName=kinesis_stream_name, Records=records)
    print(len(records), " records published")


def get_s3_content_list(bucket_name, kinesis_stream_name):
    s3 = boto3.client('s3')
    s3_resource = boto3.resource('s3')
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket_name, PaginationConfig={'PageSize': 100})

    for page in page_iterator:
        records = []
        s3_objects = []
        for item in page['Contents']:
            s3_object = s3_resource.Object(bucket_name, item['Key'])
            content = s3_object.get()['Body'].read().decode('utf-8')
            record_kinesis = {'Data': content, 'PartitionKey': item['Key']}
            records.append(record_kinesis)
            s3_objects.append(s3_object)
        send_to_kinesis(kinesis_stream_name, records)
        for s3_object in s3_objects:
            s3_object.delete()


if __name__ == '__main__':
    bucket_name = sys.argv[1]
    kinesis_stream_name = sys.argv[2]
    get_s3_content_list(bucket_name, kinesis_stream_name)


