import streamlit as st
import pandas as pd
import boto3
from io import StringIO
from PIL import Image

def read_csv_from_s3(bucket_name, file_key):
    """Read a CSV file from S3 into a Pandas DataFrame."""
    
    session = boto3.Session(
        aws_access_key_id = 'AKIAUWDEBVLESY4ZTDNC',
        aws_secret_access_key ='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',
        region_name='eu-west-3'
        )
    
    # Initialize an S3 client with boto3
    s3_client = session.client('s3')
    
    # Get the object from the bucket
    csv_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    csv_string = csv_obj['Body'].read().decode('utf-8')
    
    # Use Pandas to read the CSV data
    df = pd.read_csv(StringIO(csv_string))
    
    return df


def get_file(bucket_name):
    ###This function gets the most  recent file
    
    session = boto3.Session(
    aws_access_key_id = 'AKIAUWDEBVLESY4ZTDNC',
    aws_secret_access_key ='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',
    region_name='eu-west-3'
    )

    # Initialize the S3 client
    s3 = session.client('s3')
    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    # Sort objects by last modified timestamp
    objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'], reverse=True)
    # Get the key (file name) of the most recent object
    most_recent_file = objects[0]['Key']

    return most_recent_file

# Example usage in your Streamlit app
bucket_name = "surf-spot-conditions"
file_key = get_file(bucket_name)

# Read the CSV file
df = read_csv_from_s3(bucket_name, file_key)

# Display the DataFrame in your app
image = Image.open("logo.png")
st.image(image, use_column_width=True)
left_column, center_column, right_column = st.columns([1,10,1])
with center_column:
    st.dataframe(df)
