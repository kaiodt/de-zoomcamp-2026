# Homework 03

## Setup

1. **GCP Credentials**:

    Obtain your GCP Service Account JSON key and save it as `service-account.json` in this directory.

2. **Upload Yellow Taxi Data to GCS**:

    Change the `BUCKET_NAME` variable in `load_yellow_taxi_data.py` to your bucket name.

    Run the script:

    ```bash
    uv run --with google-cloud-storage --with google-api-core load_yellow_taxi_data.py
    ```

3. **Create an external table in BigQuery**:

    ```sql
    CREATE EXTERNAL TABLE `nyc_taxi_tripdata.yellow_tripdata_2024_external`
    OPTIONS (
      format = 'PARQUET',
      uris = ['gs://nyc-taxi-tripdata/yellow_tripdata_2024-*.parquet']
    );
    ```

4. **Create a regular table in BigQuery**:

    ```sql
    CREATE TABLE `nyc_taxi_tripdata.yellow_tripdata_2024`
    AS
    SELECT *
    FROM `nyc_taxi_tripdata.yellow_tripdata_2024_external`;
    ```


## Question 01 - Counting Records

What is the count of records for the yellow taxi data for the year 2024?

### Solution

```sql
SELECT COUNT(1)
FROM `nyc_taxi_tripdata.yellow_tripdata_2024`;
```

**The result is: `20,332,093`**


## Question 02 - Data Read Estimation

Write a query to count the distinct number of `PULocationIDs` for the entire dataset on both the tables.

What is the estimated amount of data that will be read when this query is executed on the **External Table** and the **Table**?

### Solution

- **External Table**

    ```sql
    SELECT COUNT(DISTINCT PULocationID)
    FROM `nyc_taxi_tripdata.yellow_tripdata_2024_external`;
    ```

- **Regular Table**

    ```sql
    SELECT COUNT(DISTINCT PULocationID)
    FROM `nyc_taxi_tripdata.yellow_tripdata_2024`;
    ```

**The result is: `0 MB` for the External Table and `155.12 MB` for the Materialized Table**


## Question 03 - Understanding Columnar Storage

Write a query to retrieve the `PULocationID` from the **table** (not the external table) in BigQuery.

Now write a query to retrieve the `PULocationID` and `DOLocationID` on the same table.

Why are the estimated number of Bytes different?

### Solution

- **Query 1**

    ```sql
    SELECT PULocationID
    FROM `nyc_taxi_tripdata.yellow_tripdata_2024`;
    ```

    **Estimated Data Read**: `155.12 MB`

- **Query 2**

    ```sql
    SELECT PULocationID, DOLocationID
    FROM `nyc_taxi_tripdata.yellow_tripdata_2024`;
    ```

    **Estimated Data Read**: `310.24 MB`

**The estimated number of bytes read is different because:**

- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (`PULocationID`, `DOLocationID`) requires reading more data than querying one column (`PULocationID`), leading to a higher estimated number of bytes processed.


## Question 04 - Counting Zero Fare Trips

How many records have a `fare_amount` of `0`?

### Solution

```sql
SELECT COUNT(1)
FROM `nyc_taxi_tripdata.yellow_tripdata_2024`
WHERE fare_amount = 0;
```

**The result is: `8,333`**


## Question 05 - Partitioning and Clustering

What is the best strategy to make an optimized table in Big Query if your query will always filter based on `tpep_dropoff_datetime` and order the results by `VendorID` (Create a new table with this strategy)?

### Solution

**Partition by `tpep_dropoff_datetime` and Cluster on `VendorID`**

```sql
CREATE TABLE `nyc_taxi_tripdata.yellow_tripdata_2024_optimized`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
SELECT *
FROM `nyc_taxi_tripdata.yellow_tripdata_2024`;
```

## Question 06 - Partition benefits

Write a query to retrieve the distinct `VendorID`s between `tpep_dropoff_datetime` `2024-03-01` and `2024-03-15` (inclusive).

Use the materialized table you created earlier in your `FROM` clause and note the estimated bytes.

Now change the table in the `FROM` clause to the partitioned table you created for **Question 5** and note the estimated bytes processed.

What are these values?

### Solution

- **Non-partitioned table**

    ```sql
    SELECT DISTINCT VendorID
    FROM `nyc_taxi_tripdata.yellow_tripdata_2024`
    WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
    ```

    **Estimated Data Read**: `310.24 MB`

- **Partitioned table**

    ```sql
    SELECT DISTINCT VendorID
    FROM `nyc_taxi_tripdata.yellow_tripdata_2024_optimized`
    WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
    ```

    **Estimated Data Read**: `26.84 MB`

**The result is: `310.24 MB for non-partitioned table and 26.84 MB for the partitioned table`**


## Question 07 - External Table Storage

Where is the data stored in the **External Table** you created?

### Solution

**GCP Bucket**


## Question 08 - Clustering Best Practices

It is best practice in Big Query to always cluster your data:

### Solution

**False**


## Question 09 - Understanding Table Scans

Write a `SELECT COUNT(*)` query from the materialized table you created.

How many bytes does it estimate will be read? Why?

### Solution

```sql
SELECT COUNT(*)
FROM `nyc_taxi_tripdata.yellow_tripdata_2024`;
```

**Estimated Data Read**: `0 MB`

**The estimated number of bytes read is different because:**

BigQuery maintains metadata for managed tables (like row count). A simple `COUNT(*)` query without a `WHERE` clause or `JOIN`s can be resolved entirely from this metadata without scanning any columns in the table, resulting in zero bytes processed.

