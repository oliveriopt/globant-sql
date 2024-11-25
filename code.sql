CREATE DATABASE IF NOT EXISTS globantcode;

#############################################################

CREATE EXTERNAL TABLE IF NOT EXISTS globantcode.employees (
    id INT,
    name STRING,
    datetime STRING,
    department_id INT,
    job_id INT
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'serialization.format' = ','
)
LOCATION 's3://globant-s3-oliver/employees/'
TBLPROPERTIES ('has_encrypted_data'='false');

#############################################################

CREATE EXTERNAL TABLE IF NOT EXISTS globantcode.departments (
    id INT,
    department STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'serialization.format' = ','
)
LOCATION 's3://globant-s3-oliver/departments/'
TBLPROPERTIES ('has_encrypted_data'='false');

#############################################################

CREATE EXTERNAL TABLE IF NOT EXISTS globantcode.jobs (
    id INT,
    job STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'serialization.format' = ','
)
LOCATION 's3://globant-s3-oliver/jobs/'
TBLPROPERTIES ('has_encrypted_data'='false');

#############################################################

SELECT * FROM globantcode.employees;

#############################################################

SELECT 
    d.department AS department,
    j.job AS job,
    SUM(CASE WHEN QUARTER(from_iso8601_timestamp(he.datetime)) = 1 THEN 1 ELSE 0 END) AS Q1,
    SUM(CASE WHEN QUARTER(from_iso8601_timestamp(he.datetime)) = 2 THEN 1 ELSE 0 END) AS Q2,
    SUM(CASE WHEN QUARTER(from_iso8601_timestamp(he.datetime)) = 3 THEN 1 ELSE 0 END) AS Q3,
    SUM(CASE WHEN QUARTER(from_iso8601_timestamp(he.datetime)) = 4 THEN 1 ELSE 0 END) AS Q4
FROM globantcode.employees AS he
JOIN globantcode.departments AS d
    ON he.department_id = d.id
JOIN globantcode.jobs AS j
    ON he.job_id = j.id
WHERE YEAR(from_iso8601_timestamp(he.datetime)) = 2021
  AND he.datetime IS NOT NULL
  AND he.datetime != ''
  AND TRY(from_iso8601_timestamp(he.datetime)) IS NOT NULL -- Ensure valid datetime format
GROUP BY d.department, j.job
ORDER BY d.department ASC, j.job ASC;

#############################################################


WITH department_hired_counts AS (
    SELECT 
        d.id AS department_id,
        d.department,
        COUNT(he.id) AS hired
    FROM globantcode.employees AS he
    JOIN globantcode.departments AS d
        ON he.department_id = d.id
    WHERE YEAR(from_iso8601_timestamp(he.datetime)) = 2021
      AND he.datetime IS NOT NULL
      AND he.datetime != ''
      AND TRY(from_iso8601_timestamp(he.datetime)) IS NOT NULL 
    GROUP BY d.id, d.department
),
mean_hired AS (
    SELECT AVG(hired) AS mean_hired
    FROM department_hired_counts
)
SELECT 
    dh.department_id AS id,
    dh.department,
    dh.hired
FROM department_hired_counts AS dh
JOIN mean_hired AS mh
    ON dh.hired > mh.mean_hired
ORDER BY dh.hired DESC;

#############################################################


DROP TABLE globantcode.employees;
DROP DATABASE employee;
DROP DATABASE globantcode;

#############################################################

WITH department_hired_counts AS (SELECT d.id AS department_id, d.department, COUNT(he.id) AS hired FROM globantcode.employees AS he JOIN globantcode.departments AS d ON he.department_id = d.id WHERE YEAR(from_iso8601_timestamp(he.datetime)) = 2021 AND he.datetime IS NOT NULL AND he.datetime != '' AND TRY(from_iso8601_timestamp(he.datetime)) IS NOT NULL GROUP BY d.id, d.department), mean_hired AS ( SELECT AVG(hired) AS mean_hired FROM department_hired_counts) SELECT dh.department_id AS id, dh.department, dh.hired FROM department_hired_counts AS dh JOIN mean_hired AS mh ON dh.hired > mh.mean_hired ORDER BY dh.hired DESC;