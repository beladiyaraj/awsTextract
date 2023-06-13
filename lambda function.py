import boto3
import csv
import urllib
import os
import time

def start_job(client, s3_bucket_name, object_name):
    response = None
    response = client.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3_bucket_name,
                'Name': object_name
            }})

    return response["JobId"]


def is_job_complete(client, job_id):
    response = client.get_document_text_detection(JobId=job_id)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while(status == "IN_PROGRESS"):
        time.sleep(7)
        response = client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status


def get_job_results(client, job_id):
    pages = []
    response = client.get_document_text_detection(JobId=job_id)
    pages.append(response)
    print("Getting Pages from Textract Started")
    next_token = None
    if 'NextToken' in response:
        next_token = response['NextToken']

    while next_token:
        response = client.get_document_text_detection(JobId=job_id, NextToken=next_token)
        pages.append(response)
        next_token = None
        if 'NextToken' in response:
            next_token = response['NextToken']
    print("All Result pages received")
    return pages


def lambda_handler(event, context):
    # Document
    s3_bucket_name = "taxtract-input-pdfs"
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    file_name = object_key.rsplit('/', 1)[-1]
    region = os.environ['AWS_REGION']
    client = boto3.client('textract', region_name=region)

    job_id = start_job(client, s3_bucket_name, object_key)
    print("Started job with id: {}".format(job_id))

    if is_job_complete(client, job_id):
        response = get_job_results(client, job_id)

        # Write detected text into CSV
        csv_filename = file_name.replace('.pdf', '.csv')
        s3 = boto3.resource('s3')
        s3_obj = s3.Object('textract-output-csvs', csv_filename)
        with open('/tmp/{}'.format(csv_filename), 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Page Number', 'Type', 'Text', 'Confidence Score % (Line)'])
            for result_page in response:
                for item in result_page["Blocks"]:
                    if item["BlockType"] == "LINE":
                        writer.writerow([item['Page'], item['BlockType'], item['Text'], item['Confidence']])

        # Upload CSV to S3
        s3_obj.upload_file('/tmp/{}'.format(csv_filename))
        print(f"Text extracted successfully and saved to:- {s3_obj.bucket_name}/{s3_obj.key}")

    return {
        'statusCode': 200,
        'body': 'Text extracted and saved to CSV successfully'
    }