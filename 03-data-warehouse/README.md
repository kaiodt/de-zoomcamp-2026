# Module 3: Data Warehouse

## Overview

This module focuses on **Data Warehousing** concepts using **Google BigQuery**. It covers the architecture of BigQuery, data loading strategies, cost optimization through partitioning and clustering, and how to build machine learning models directly within the warehouse using **BigQuery ML**.

## Prerequisites

- [Google Cloud SDK (gcloud)](https://cloud.cloud.google.com/sdk/docs/install)
- [Docker](https://www.docker.com/products/docker-desktop/) installed and running (for local model deployment)
- A Google Cloud Platform (GCP) Account and Project with billing enabled.

## Key Concepts

### BigQuery Architecture

- **Separation of Storage and Compute**: BigQuery stores data in the Capacitor format and uses Dremel as its compute engine.

- **External vs Managed Tables**:

  - **External Tables**: Reference data stored in GCS (e.g., Parquet files) without moving it into BigQuery.
  - **Managed Tables**: Data is fully ingested into BigQuery storage for maximum performance.

### Data Ingestion

- Methods to load data from Google Cloud Storage into BigQuery tables.
- Refer to the [`gcs_ingestion`](./gcs_ingestion) directory for scripts and flows related to data loading.

### Performance and Cost Optimization

- **Partitioning**: Dividing a table into segments based on a column (e.g., Date) to reduce the amount of data scanned per query.
- **Clustering**: Sorting data within partitions based on specific columns (e.g., VendorID) to improve filter and aggregation performance.

### BigQuery ML (BQML)

- Building and evaluating Machine Learning models using standard SQL.
- Common models: Linear Regression, Logistic Regression, and Hyperparameter Tuning.
- See the [`queries`](./queries) directory for SQL examples of model creation and evaluation.

## Model Deployment

Once a model is trained in BQML, it can be exported and deployed for local serving.

- [**ML Model Deployment Guide**](./ml_model_deployment.md): Detailed steps to export BQML models to GCS, download them, and run them using TensorFlow Serving in Docker.

## Repository Structure

- [`gcs_ingestion/`](./gcs_ingestion): Scripts and configuration for loading taxi data into GCS/BigQuery.
- [`queries/`](./queries): SQL scripts for data exploration (`exploration_queries.sql`) and model training (`ml_model_queries.sql`).
- [`homework/`](./homework): Solutions and documentation for the Module 03 homework assignments.

---

For specific setup instructions and homework solutions, refer to the documentation in the respective subdirectories.
