import boto3

ROLE_ARN = "arn:aws:iam::081416278585:role/S3-STS-Role"
BUCKET = "sts-boto3-poc-043"

# Step 1: Assume Role
sts = boto3.client('sts')

response = sts.assume_role(
    RoleArn=ROLE_ARN,
    RoleSessionName="mysession"
)

creds = response['Credentials']

# Step 2: Create S3 client using temporary credentials
s3 = boto3.client(
    's3',
    aws_access_key_id=creds['AccessKeyId'],
    aws_secret_access_key=creds['SecretAccessKey'],
    aws_session_token=creds['SessionToken']
)

# Step 3: Upload file
with open("test.txt", "w") as f:
    f.write("Hello STS")

s3.upload_file("test.txt", BUCKET, "test.txt")
print("Uploaded")

# Step 4: List files
response = s3.list_objects_v2(Bucket=BUCKET)

if 'Contents' in response:
    for obj in response['Contents']:
        print(obj['Key'])

# Step 5: Download file
s3.download_file(BUCKET, "test.txt", "downloaded.txt")
print("Downloaded")

# Step 6: Delete file
s3.delete_object(Bucket=BUCKET, Key="test.txt")
print("Deleted")
