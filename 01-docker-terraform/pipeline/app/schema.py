"""
Data schemas and constants for the NYC Taxi data ingestion pipeline.
"""

# Taxi data column data types (except datetime types)
TAXI_DATA_DTYPES = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "Float64",
    "RatecodeID": "Int64",
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
}

# Taxi data columns with date types to parse
TAXI_DATA_PARSE_DATES = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
]

# Taxi zone data column data types
TAXI_ZONE_DTYPES = {
    "LocationID": "Int64",
    "Borough": "string",
    "Zone": "string",
    "service_zone": "string",
}
