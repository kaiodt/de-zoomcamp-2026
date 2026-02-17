/* @bruin
name: staging.trips
type: duckdb.sql
depends:
  - ingestion.trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp

columns:
  - name: vendor_id
    type: integer
    description: Vendor ID
    checks:
      - name: not_null

  - name: ratecode_id
    type: integer
    description: Ratecode ID

  - name: pu_location_id
    type: integer
    description: Pickup location ID
    checks:
      - name: not_null

  - name: do_location_id
    type: integer
    description: Dropoff location ID
    checks:
      - name: not_null

  - name: pickup_datetime
    type: timestamp
    description: Pickup datetime

  - name: dropoff_datetime
    type: timestamp
    description: Dropoff datetime

  - name: passenger_count
    type: integer
    description: Passenger count

  - name: trip_distance
    type: float
    description: Trip distance

  - name: store_and_fwd_flag
    type: string
    description: Store and forward flag

  - name: payment_type
    type: integer
    description: Payment type

  - name: fare_amount
    type: float
    description: Fare amount

  - name: extra
    type: float
    description: Extra

  - name: mta_tax
    type: float
    description: MTA tax

  - name: tip_amount
    type: float
    description: Tip amount

  - name: tolls_amount
    type: float
    description: Tolls amount

  - name: improvement_surcharge
    type: float
    description: Improvement surcharge

  - name: total_amount
    type: float
    description: Total amount

  - name: congestion_surcharge
    type: float
    description: Congestion surcharge

  - name: trip_type
    type: integer
    description: Trip type

  - name: ehail_fee
    type: float
    description: EHail fee

  - name: extracted_at
    type: timestamp
    description: Extracted at
    checks:
      - name: not_null

  - name: taxi_type
    type: string
    description: Taxi type
    checks:
      - name: not_null

  - name: payment_type_name
    type: string
    description: Payment type name

custom_checks:
  - name: row_count_positive
    description: Ensures the table is not empty
    query: |
      SELECT COUNT(*) > 0
      FROM staging.trips
    value: 1
@bruin */

SELECT
  -- Renaming and Casting
  vendor_id::int AS vendor_id,
  ratecode_id::int AS ratecode_id,
  pu_location_id::int AS pu_location_id,
  do_location_id::int AS do_location_id,
  
  -- Timestamp casting (already normalized in ingestion)
  pickup_datetime::timestamp AS pickup_datetime,
  dropoff_datetime::timestamp AS dropoff_datetime,
  
  -- Other columns
  passenger_count::int AS passenger_count,
  trip_distance::float AS trip_distance,
  store_and_fwd_flag,
  payment_type::int AS payment_type,
  
  -- Financials
  fare_amount::float AS fare_amount,
  extra::float AS extra,
  mta_tax::float AS mta_tax,
  tip_amount::float AS tip_amount,
  tolls_amount::float AS tolls_amount,
  improvement_surcharge::float AS improvement_surcharge,
  total_amount::float AS total_amount,
  congestion_surcharge::float AS congestion_surcharge,
  
  -- Yellow/Green compatibility columns
  trip_type::int AS trip_type,
  ehail_fee::float AS ehail_fee,
  
  -- Metadata
  extracted_at::timestamp AS extracted_at,
  taxi_type,
  
  -- Enriched columns
  pl.payment_type_name

FROM
  ingestion.trips t
  LEFT JOIN ingestion.payment_lookup pl
    ON t.payment_type = pl.payment_type_id

WHERE
  pickup_datetime >= '{{ start_date }}'
  AND pickup_datetime < '{{ end_date }}'

-- Deduplication: keep most recently extracted record for a unique trip header
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY 
    pickup_datetime, 
    dropoff_datetime, 
    pu_location_id, 
    do_location_id, 
    fare_amount, 
    taxi_type
  ORDER BY
    extracted_at DESC
) = 1
