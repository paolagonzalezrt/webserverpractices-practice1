# Practice 1: Multi-Source Ingestion and Data Profiling on AWS S3 with Python

## Description

This project connects to Amazon S3 using Boto3 to load and profile CSV and JSON files with pandas.
The script processes files directly in memory without saving downloaded copies to disk.

## Features

- CSV and JSON ingestion from Amazon S3.
- In-memory file processing.
- Dataset dimensions and data types profiling.
- Missing value identification.
- Descriptive statistics generation.

## Requirements

- Python 3.8+
- AWS Academy Account / AWS CLI configured

## Installation

1. Clone this repository and navigate to the project directory.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

### 1. AWS Credentials
Ensure your **AWS Academy credentials** are active. You can configure them using the AWS CLI (`aws configure`) or by exporting them in your terminal:

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_SESSION_TOKEN="your-session-token" 
```

### 2. Environment Variables
Set the target AWS Region and S3 bucket name:

```bash
export AWS_REGION="<your-aws-region>"
export S3_BUCKET_NAME="<your-s3-bucket-name>"
```

## Execution

Run the main profiling script from the root directory:

```bash
python scripts/profile_s3.py
```