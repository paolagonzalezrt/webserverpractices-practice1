import io
import json
import os

import boto3
import pandas as pd
from botocore.exceptions import (
    ClientError,
    NoCredentialsError,
    PartialCredentialsError,
)
from pandas.errors import EmptyDataError, ParserError


REGION_NAME = os.environ.get("AWS_REGION")
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")


def load_and_profile_s3(file_key, is_json=False):
    """Load an S3 object into memory and print a basic data profile."""

    print(f"\n{'=' * 60}")
    print("Processing S3 object")
    print("=" * 60)

    try:
        if not REGION_NAME or not BUCKET_NAME:
            print("Error: AWS_REGION or S3_BUCKET_NAME is not configured.")
            return None

        s3_client = boto3.client("s3", region_name=REGION_NAME)

        response = s3_client.get_object(
            Bucket=BUCKET_NAME,
            Key=file_key
        )

        body = response["Body"].read()

        if not body:
            print("Error: The S3 object is empty.")
            return None

        if is_json:
            data = json.loads(body.decode("utf-8"))
            df = pd.json_normalize(data)
        else:
            df = pd.read_csv(io.BytesIO(body))

        print(
            f"\nDataset dimensions: "
            f"{df.shape[0]} rows x {df.shape[1]} columns"
        )

        print("\nColumn data types:")
        print(df.dtypes.to_string())

        print("\nMissing values per column:")
        print(df.isnull().sum().to_string())

        print("\nDescriptive statistics:")
        numeric_columns = df.select_dtypes(include="number")

        if numeric_columns.empty:
            print("No numeric columns available.")
        else:
            print(numeric_columns.describe().T.to_string())

        date_columns = [
            column for column in df.columns
            if column in ("transaction_date", "timestamp")
        ]

        for column in date_columns:
            df[column] = pd.to_datetime(
                df[column], errors="coerce"
            )

        if date_columns:
            print("\nDate columns converted to datetime:")
            print(df[date_columns].dtypes.to_string())

        print("\nFirst five rows:")
        print(df.head().to_string(index=False))

        return df

    except (NoCredentialsError, PartialCredentialsError):
        print("AWS credentials are missing or incomplete.")

    except ClientError as error:
        error_code = error.response.get("Error", {}).get(
            "Code", "Unknown"
        )
        print(f"AWS request failed. Error code: {error_code}")

    except (json.JSONDecodeError, UnicodeDecodeError):
        print("The JSON file could not be decoded.")

    except (ParserError, EmptyDataError):
        print("The CSV file could not be parsed.")

    except Exception as error:
        print(f"Unexpected error: {type(error).__name__}")

    return None


if __name__ == "__main__":
    transactions_df = load_and_profile_s3(
        "raw/transacciones.csv"
    )

    logs_df = load_and_profile_s3(
        "raw/logs_m2m.json",
        is_json=True
    )
