# ML Model Deployment Guide: BQML to TensorFlow Serving

This guide outlines the process of exporting a machine learning model from BigQuery ML (BQML) and deploying it locally using TensorFlow Serving.

## Prerequisites

- [Google Cloud SDK (gcloud)](https://cloud.google.com/sdk/docs/install)
- [Docker](https://www.docker.com/products/docker-desktop/) installed and running
- Access to a Google Cloud Project with the `tip_hyperparam_model` created in BigQuery (see [`queries/ml_model_queries.sql`](queries/ml_model_queries.sql))

## Step 1: Authenticate with Google Cloud

Ensure you are logged into your Google Cloud account to access the resources.

```bash
gcloud auth login
```

## Step 2: Export Model from BigQuery to GCS

Export the BQML model to a Google Cloud Storage (GCS) bucket.

```bash
# Replace <PROJECT_ID> if different
bq --project_id taxi-rides-ny extract \
  -m nyc_taxi_tripdata.tip_hyperparam_model \
  gs://nyc-taxi-tripdata/models/tip_hyperparam_model
```

## Step 3: Download Model Locally

Download the exported model files to your local machine for serving.

```bash
mkdir /tmp/model
gsutil cp -r gs://nyc-taxi-tripdata/models/tip_hyperparam_model /tmp/model
```

## Step 4: Prepare the Serving Directory Structure

TensorFlow Serving requires a specific directory structure with versioning.

```bash
mkdir -p serving_dir/tip_hyperparam_model/1
cp -r /tmp/model/tip_hyperparam_model/* serving_dir/tip_hyperparam_model/1
```

## Step 5: Deploy Model with TensorFlow Serving (Docker)

Run the TensorFlow Serving container, mounting your local model directory.

```bash
# Pull the latest TF Serving image
docker pull tensorflow/serving

# Run the container (Single line recommended to avoid escaping issues)
docker run -p 8501:8501 \
  --mount type=bind,source="$(pwd -W)"/serving_dir/tip_hyperparam_model,target=/models/tip_hyperparam_model \
  -e MODEL_NAME=tip_hyperparam_model \
  -t tensorflow/serving &
```

## Step 6: Test the Deployment

Send a POST request to the local serving endpoint to get a prediction. The features must match the schema defined during model creation.

```bash
curl -d '{
  "instances": [
    {
      "passenger_count": 1,
      "trip_distance": 12.2,
      "PULocationID": "193",
      "DOLocationID": "264",
      "payment_type": "2",
      "fare_amount": 20.4,
      "tolls_amount": 0.0
    }
  ]
}' -X POST http://localhost:8501/v1/models/tip_hyperparam_model:predict
```

To verify the model status, visit: [http://localhost:8501/v1/models/tip_hyperparam_model](http://localhost:8501/v1/models/tip_hyperparam_model)

## Cleanup

### Stop the container

```bash
# List all running containers
docker ps

# Stop the container
docker stop <container_id>

# Remove the container
docker rm <container_id>
```

### Remove the model from local machine

```bash
# Remove the serving directory
rm -rf serving_dir

# Remove the model from local machine
rm -rf /tmp/model
```
