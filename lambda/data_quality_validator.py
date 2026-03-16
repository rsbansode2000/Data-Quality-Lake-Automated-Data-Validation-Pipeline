import boto3
import pandas as pd
import io
import json
from datetime import datetime

s3 = boto3.client('s3')

sns = boto3.client('sns')
glue = boto3.client('glue')

LOG_BUCKET = "BUCKET_NAME"
GLUE_JOB = "sales_etl_job"


def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    file_path = f"s3://{bucket}/{key}"

    obj = s3.get_object(Bucket=bucket, Key=key)

    df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    errors = []
    null_count = df['amount'].isnull().sum()
    if null_count > 0:
        errors.append("Null values in amount as count > 0")

    if df['order_id'].duplicated().sum() > 0:
        errors.append("Duplicate order_id")

    status = "PASSED" if len(errors) == 0 else "FAILED"
    if errors:
        sns.publish(
            TopicArn='SNS_ARN',
            Message=str(errors),
            Subject='Data Quality Alert'
        )
    else :
        glue.start_job_run(JobName=GLUE_JOB)

    log = {
        "file": key,
        "timestamp": datetime.utcnow().isoformat(),
        "total_records": len(df),
        "null_count": int(null_count),
        "status": status
    }

    log_key = f"data-quality-lake/audit_logs/validation_results/dq_logs/{datetime.utcnow().strftime('%Y/%m/%d')}/{context.aws_request_id}.json"

    s3.put_object(
        Bucket=LOG_BUCKET,
        Key=log_key,
        Body=json.dumps(log),
        ContentType='application/json'
    )


    return log
