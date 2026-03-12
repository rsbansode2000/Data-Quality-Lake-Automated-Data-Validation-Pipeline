**Data Quality Lake – Automated Data Validation Pipeline**

Tech Stack: Amazon S3, AWS Lambda, AWS Glue, Amazon Athena, Python, Pandas

**Project Description**

Designed and implemented a serverless Data Quality Lake framework that validates incoming datasets before triggering downstream ETL processing. The system automatically performs quality checks on data stored in S3 and logs validation results for monitoring and auditing.

**Key Responsibilities**

Built a serverless data quality validation pipeline using AWS Lambda to automatically trigger checks when new files are uploaded to Amazon S3.

Implemented multiple data validation rules including null checks, duplicate detection, schema validation, and record count verification using Python and Pandas.

Designed logic to conditionally trigger ETL jobs in AWS Glue only when data quality checks pass, preventing bad data from entering downstream pipelines.

Implemented structured JSON logging stored in Amazon S3 for auditability and monitoring of data quality results.

Created external tables in Amazon Athena to query and analyze data quality logs for operational insights.

Designed partitioned S3 log storage (year/month/day) to optimize query performance and reduce Athena query costs.

Enabled monitoring of data quality trends, failure rates, and ingestion statistics through SQL queries on validation logs.

**Key Features**

Automated data validation before ETL execution

Serverless and event-driven architecture

Structured logging and audit trail

Queryable logs for monitoring and reporting

Impact

Improved data reliability and pipeline stability by preventing invalid datasets from entering the ETL process.

Reduced manual data validation efforts and enabled automated monitoring of data quality metrics.
