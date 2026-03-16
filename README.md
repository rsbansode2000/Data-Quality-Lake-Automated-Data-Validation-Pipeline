# Data Quality Lake – Automated Data Validation Pipeline

## Overview

This project implements a **serverless Data Quality validation framework** that validates incoming datasets before running ETL pipelines. The system ensures only high-quality data is processed and stored in downstream data layers.

The pipeline automatically checks data quality rules such as **null values, schema validation, and record counts**, and then triggers an ETL job only when the data passes validation.

---

# Architecture

```
                +----------------------+
                |  Raw Data Uploaded   |
                |        (S3)          |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |  Lambda Function     |
                |  Data Quality Check  |
                |----------------------|
                | • Null validation    |
                | • Schema validation  |
                | • Record count check |
                +----------+-----------+
                           |
                +----------+-----------+
                |                      |
                v                      v
        +---------------+     +------------------+
        |  Write Log    |     | Trigger Glue Job |
        |   (S3 Logs)   |     |      (ETL)       |
        +---------------+     +--------+---------+
                                        |
                                        v
                               +------------------+
                               |  Glue ETL Job    |
                               | Data Processing  |
                               +--------+---------+
                                        |
                                        v
                               +------------------+
                               | Lambda Logging   |
                               | Write JSON Logs  |
                               +------------------+
                                        |
                                        v
                               +------------------+
                               |   Logs Stored    |
                               |       in S3      |
                               +------------------+
```

---

# Key Features

* Automated **data quality validation before ETL**
* Serverless architecture
* Event-driven pipeline
* Structured JSON logging
* Queryable logs for monitoring

---

# Data Quality Checks Implemented

| Check Type              | Description                                        |
| ----------------------- | -------------------------------------------------- |
| Null Check              | Ensures critical columns contain no null values    |
| Schema Validation       | Verifies dataset structure matches expected schema |
| Record Count Validation | Ensures dataset meets minimum row count            |
| Duplicate Detection     | Identifies duplicate records                       |

---

# Project Structure

```
data-quality-lake/
│
├── lambda/
│   ├── data_quality_validator.py
│   └── log_writer.py
│
├── glue/ │ └── etl_job_script.py
|
├── sample-data/
│   └── sales_data.csv
│
├── architecture/
│   └── architecture_diagram.png
│
└── README.md
```

---

# Example JSON Log

```
{
  "file": "raw/sales_data.csv",
  "timestamp": "2026-03-12T10:40:12",
  "total_records": 12000,
  "null_count": 0,
  "status": "PASSED"
}
```

---

# Setup Instructions

### 1. Create S3 Buckets

* Raw Data Bucket
* Logs Bucket

### 2. Deploy Lambda Function

Upload the **data quality validation Lambda code** and configure it to trigger when new files are uploaded to S3.

### 3. Configure Glue Job

Create a Glue ETL job that processes validated datasets.

### 4. Add IAM Permissions

Grant the Lambda role permissions to:

* Read objects from S3
* Write logs to S3
* Trigger Glue jobs

### 5. Upload Data

Upload sample data into the raw data bucket to trigger the pipeline.

---

# Query Logs with Athena

Logs stored in S3 can be queried using SQL for monitoring pipeline health.

Example query:

```
SELECT status, COUNT(*)
FROM dq_logs
GROUP BY status;
```

---

# Tech Stack

* Python
* AWS Lambda
* Amazon S3
* AWS Glue
* Amazon Athena
* Pandas

---

# Use Cases

* Data Lake validation layer
* ETL pipeline monitoring
* Data governance frameworks
* Automated data ingestion validation

---

# Future Improvements

* Add  **AWS Step Functions for orchestration**
* Convert logs to **Parquet format**
* Add **data quality dashboards**
* Implement **email alerts for failed checks**
