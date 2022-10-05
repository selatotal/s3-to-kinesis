# s3-to-kinesis

Get all content in an AWS S3 Bucket and send their data to a Kinesis Stream

To configure:

```shell
pip3 install -r requirements.txt
```

To execute:

```shell
python3 s3-to-kinesis.py <bucket_name> <stream_name>
```

Be sure that you have AWS Credentials OK in your execution environment.