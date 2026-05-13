# EV vs ICE Vehicle Data Engineering Pipeline

![](![Uploading Gemini_Generated_Image_optnttoptnttoptn.png…]()
)
## Overview
This project demonstrates a real-world Data Engineering pipeline built using Databricks, PySpark, and Delta Lake on an EV vs ICE Vehicle dataset (2015–2026).

The project focuses on solving practical data quality issues, implementing Medallion Architecture, and generating business-level analytics for vehicle trends, sustainability reporting, and EV adoption insights.

---

## Dataset Details

- Dataset: EV_vs_ICE_Vehicle_Specs_2015_2026.csv
- Total Records: 15,301
- Total Columns: 14
- Year Range: 2015–2026

---

## Project Objectives

- Build scalable ETL pipelines using PySpark
- Implement Bronze, Silver, and Gold architecture
- Handle real-world data quality problems
- Optimize analytics using Delta Lake
- Generate business KPIs and reporting datasets

---

## Major Data Engineering Problems Solved

### 1. Missing Fuel Type Values
- Null handling using PySpark
- Business-safe replacement strategies

### 2. Invalid EV Range for ICE Vehicles
- Validation rule implementation
- Data correction pipelines

### 3. Inconsistent Vehicle Categories
- Standardization logic for analytics consistency

### 4. Transmission Naming Standardization
- Reduced high-cardinality categorical values

### 5. EV Engine Data Issues
- Nullable engine metrics for EV vehicles

### 6. Missing Primary Key
- Surrogate key generation using Spark

### 7. High Cardinality Optimization
- Delta optimization and Z-Ordering

### 8. Schema Drift Handling
- Auto schema evolution in Delta Lake

### 9. Data Validation Constraints
- Delta table constraints implementation

### 10. Partitioning Strategy
- Year-based partition optimization

---

## Architecture

CSV Ingestion
↓
Bronze Layer (Raw Delta Tables)
↓
Silver Layer (Cleaned & Validated Data)
↓
Gold Layer (Business KPIs & Analytics)
↓
Power BI Dashboard

---

## Technologies Used

- PySpark
- Databricks
- Delta Lake
- SQL
- Auto Loader
- Structured Streaming
- Power BI
- Unity Catalog

---

## Business KPIs

- EV Adoption Percentage
- CO2 Emission Analytics
- Fuel Efficiency Benchmarking
- Vehicle Segment Analysis
- Transmission Trend Analysis
- Engine Trend Insights

---

## Sample Optimization

```sql
OPTIMIZE vehicle_specs
ZORDER BY (Make, Model)
