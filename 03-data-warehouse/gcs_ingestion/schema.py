"""
Data schemas for the NYC Taxi GCS Ingestion tool.
"""

# Yellow Taxi Schema
YELLOW_SCHEMA = {
    "VendorID": "Int64",
    "tpep_pickup_datetime": "datetime64[ns]",
    "tpep_dropoff_datetime": "datetime64[ns]",
    "passenger_count": "Float64",
    "trip_distance": "Float64",
    "RatecodeID": "Float64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "Float64",
    "extra": "Float64",
    "mta_tax": "Float64",
    "tip_amount": "Float64",
    "tolls_amount": "Float64",
    "improvement_surcharge": "Float64",
    "total_amount": "Float64",
    "congestion_surcharge": "Float64",
    "airport_fee": "Float64",
}

# Green Taxi Schema
GREEN_SCHEMA = {
    "VendorID": "Int64",
    "lpep_pickup_datetime": "datetime64[ns]",
    "lpep_dropoff_datetime": "datetime64[ns]",
    "store_and_fwd_flag": "string",
    "RatecodeID": "Float64",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "passenger_count": "Float64",
    "trip_distance": "Float64",
    "fare_amount": "Float64",
    "extra": "Float64",
    "mta_tax": "Float64",
    "tip_amount": "Float64",
    "tolls_amount": "Float64",
    "ehail_fee": "Float64",
    "improvement_surcharge": "Float64",
    "total_amount": "Float64",
    "payment_type": "Int64",
    "trip_type": "Int64",
    "congestion_surcharge": "Float64",
}

TAXI_SCHEMAS = {
    "yellow": YELLOW_SCHEMA,
    "green": GREEN_SCHEMA,
}
