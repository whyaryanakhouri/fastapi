import boto3
s3 = boto3.resource("s3")

# # Print out bucket names
# for bucket in s3.buckets.all():
#     print(bucket.name)
s3= boto3.client("s3")
s3.upload_file(
    Filename="/Users/aryanakhouri/Desktop/python/main.py",
    Bucket="test1234567891234567",
    Key="aryan-op-hai",
)