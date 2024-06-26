import streamlit as st
import pandas as pd
import boto3
from io import StringIO
from PIL import Image
import os
from PIL import Image
import streamlit as st

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
#file_key = "2024-03-25.csv"

# Read the CSV file
df = read_csv_from_s3(bucket_name, file_key)

# Display content on the app
image_path = os.path.join(os.path.dirname(__file__), 'images', 'logo.png')
image = Image.open(image_path)
st.image(image, use_column_width=True)

st.markdown("""<br>""", unsafe_allow_html=True)

regions = df['region'].unique().tolist()
stars = sorted(df['stars'].unique().tolist())

# Sidebar selectors for 'region' and 'stars'
selected_region = st.sidebar.selectbox('Select Region', ['All'] + regions)
selected_stars = st.sidebar.selectbox('Select Stars', ['All'] + stars)

# Filtering the DataFrame based on selections
if selected_region != 'All':
    df = df[df['region'] == selected_region]
if selected_stars != 'All':
    df = df[df['stars'] == selected_stars]

if df.empty:
    # Display a message and the URL to the users
    st.markdown("Looks like there are no (good) waves in France today... Why not sit back and read [the latest duck dive article](https://theduckdive.substack.com/)?")
    st.write(f"Last update : {file_key}"[:-3])
else:
    # Display the filtered DataFrame
    st.write("Here are the best surf spots in the next 3 days.")
    st.write(f"Last update : {file_key}"[:-3])
    st.write(df)

left_column, center_column, right_column = st.columns([1,6,1])
with center_column:
    st.dataframe(df)
