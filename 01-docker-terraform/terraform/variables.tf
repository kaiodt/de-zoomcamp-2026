variable "credentials" {
  default     = "./keys/my-creds.json"
  description = "Path to Google Cloud credentials file"
}

variable "project_id" {
  default     = "de-zoomcamp-485317"
  description = "My Project ID"
}

variable "region" {
  default     = "us-central1"
  description = "Region of the resources"
}

variable "location" {
  default     = "US"
  description = "Location of the resources"
}

variable "bq_dataset_name" {
  default     = "demo_dataset"
  description = "My BigQuery Dataset"
}

variable "gcs_bucket_name" {
  default     = "de-zoomcamp-485317-demo-bucket"
  description = "My GCS Bucket"
}

variable "gcs_storage_class" {
  default     = "STANDARD"
  description = "GCS Storage Class"
}

