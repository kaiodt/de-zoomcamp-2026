-- Select the features for training the model
SELECT
  passenger_count,
  trip_distance,
  PULocationID,
  DOLocationID,
  payment_type,
  fare_amount,
  tolls_amount,
  tip_amount
FROM
  `nyc_taxi_tripdata.yellow_tripdata_partitioned`
WHERE
  fare_amount != 0;


-- Create an ML table with appropriate types
CREATE OR REPLACE TABLE `nyc_taxi_tripdata.yellow_tripdata_ml` (
  `passenger_count` INTEGER,
  `trip_distance` FLOAT64,
  `PULocationID` STRING,
  `DOLocationID` STRING,
  `payment_type` STRING,
  `fare_amount` FLOAT64,
  `tolls_amount` FLOAT64,
  `tip_amount` FLOAT64
) AS (
SELECT
  CAST(passenger_count AS INTEGER) AS passenger_count,
  trip_distance,
  CAST(PULocationID AS STRING) AS PULocationID,
  CAST(DOLocationID AS STRING) AS DOLocationID,
  CAST(payment_type AS STRING) AS payment_type,
  fare_amount,
  tolls_amount,
  tip_amount
FROM
  `nyc_taxi_tripdata.yellow_tripdata_partitioned`
WHERE
  fare_amount != 0
);


-- Create model with default settings
CREATE OR REPLACE MODEL `nyc_taxi_tripdata.tip_model`
OPTIONS (
  model_type='linear_reg',
  input_label_cols=['tip_amount'],
  data_split_method='auto_split'
) AS
SELECT *
FROM `nyc_taxi_tripdata.yellow_tripdata_ml`
WHERE tip_amount IS NOT NULL;


-- Check features
SELECT * 
FROM ML.FEATURE_INFO(MODEL `nyc_taxi_tripdata.tip_model`);


-- Evaluate the model
SELECT *
FROM ML.EVALUATE(
  MODEL `nyc_taxi_tripdata.tip_model`,
  (
    SELECT *
    FROM `nyc_taxi_tripdata.yellow_tripdata_ml`
    WHERE tip_amount IS NOT NULL
  )
);


-- Make predictions
SELECT *
FROM ML.PREDICT(
  MODEL `nyc_taxi_tripdata.tip_model`,
  (
    SELECT *
    FROM `nyc_taxi_tripdata.yellow_tripdata_ml`
    WHERE tip_amount IS NOT NULL
  )
);


-- Explain the model
SELECT *
FROM ML.EXPLAIN_PREDICT(
  MODEL `nyc_taxi_tripdata.tip_model`,
  (
    SELECT *
    FROM `nyc_taxi_tripdata.yellow_tripdata_ml`
    WHERE tip_amount IS NOT NULL
  ),
  STRUCT(3 as top_k_features)
);


-- Hyperparameter tuning
CREATE OR REPLACE MODEL `nyc_taxi_tripdata.tip_hyperparam_model`
OPTIONS
(
  model_type='linear_reg',
  input_label_cols=['tip_amount'],
  data_split_method='AUTO_SPLIT',
  num_trials=5,
  max_parallel_trials=2,
  l1_reg=hparam_range(0, 20),
  l2_reg=hparam_candidates([0, 0.1, 1, 10])
) AS
SELECT *
FROM `nyc_taxi_tripdata.yellow_tripdata_ml`
WHERE tip_amount IS NOT NULL;


-- Check the best model
SELECT *
FROM
  ML.TRIAL_INFO(MODEL `nyc_taxi_tripdata.tip_hyperparam_model`);

