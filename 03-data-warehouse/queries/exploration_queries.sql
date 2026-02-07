-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `nyc_taxi_tripdata.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = [
    'gs://nyc-taxi-tripdata/yellow/yellow_tripdata_2019-*.parquet',
    'gs://nyc-taxi-tripdata/yellow/yellow_tripdata_2020-*.parquet'
  ]
);


-- Check yellow trip data
SELECT *
FROM `nyc_taxi_tripdata.external_yellow_tripdata`
LIMIT 10;


-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE `nyc_taxi_tripdata.yellow_tripdata_non_partitioned` AS
SELECT *
FROM `nyc_taxi_tripdata.external_yellow_tripdata`;


-- Create a partitioned table from external table
CREATE OR REPLACE TABLE `nyc_taxi_tripdata.yellow_tripdata_partitioned`
PARTITION BY DATE(tpep_pickup_datetime)
AS
SELECT *
FROM `nyc_taxi_tripdata.external_yellow_tripdata`;


-- Impact of partition

-- Scanning 1.63GB of data
SELECT
  DISTINCT(VendorID)
FROM
  `nyc_taxi_tripdata.yellow_tripdata_non_partitioned`
WHERE
  DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';


-- Scanning ~106 MB of data
SELECT
  DISTINCT(VendorID)
FROM
  `nyc_taxi_tripdata.yellow_tripdata_partitioned`
WHERE
  DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';


-- Let's look into the partitions
SELECT
  table_name,
  partition_id,
  total_rows
FROM
  `nyc_taxi_tripdata.INFORMATION_SCHEMA.PARTITIONS`
WHERE
  table_name = 'yellow_tripdata_partitioned'
ORDER BY
  total_rows DESC;


-- Creating a partition and cluster table
CREATE OR REPLACE TABLE `nyc_taxi_tripdata.yellow_tripdata_partitioned_clustered`
PARTITION BY
  DATE(tpep_pickup_datetime)
CLUSTER BY
  VendorID
AS
SELECT *
FROM `nyc_taxi_tripdata.external_yellow_tripdata`;


-- Impact of partition and cluster

-- Query scans ~1.1 GB
SELECT
  COUNT(*) as trips
FROM
  `nyc_taxi_tripdata.yellow_tripdata_partitioned`
WHERE
  DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID = 1;


-- Scanning ~879 MB of data
SELECT
  COUNT(*) as trips
FROM
  `nyc_taxi_tripdata.yellow_tripdata_partitioned_clustered`
WHERE
  DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2020-12-31'
  AND VendorID = 1;

