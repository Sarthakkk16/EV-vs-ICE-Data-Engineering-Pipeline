# Databricks notebook source
# MAGIC %sql
# MAGIC create or replace table gold_ev_adoption as 
# MAGIC
# MAGIC select 
# MAGIC     Year,
# MAGIC     Make,
# MAGIC     count(*) as total_vehicles,
# MAGIC     sum(
# MAGIC         case
# MAGIC             when Vehicle_Category = 'EV' then 1 
# MAGIC             else 0
# MAGIC         end
# MAGIC     ) as ev_count,
# MAGIC
# MAGIC     round(
# MAGIC         100.0*
# MAGIC         sum(
# MAGIC             case
# MAGIC                 when Vehicle_Category = 'EV' then 1 
# MAGIC                 else 0
# MAGIC             end
# MAGIC         )/count(*),
# MAGIC         2
# MAGIC         ) as ev_adoption_silver
# MAGIC from ev_vs_ice_vehicle.silver.vehicle_specs
# MAGIC group by Year, Make;
# MAGIC
# MAGIC select * from gold_ev_adoption;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ev_vs_ice_vehicle.silver.vehicle_specs;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- “Which category produces highest emissions?”
# MAGIC create or replace table gold_emission_analytics as 
# MAGIC
# MAGIC select 
# MAGIC     Year,
# MAGIC     Vehicle_Category,
# MAGIC     round(avg(CO2_Emissions_g_per_mile),2) as avg_Co2_emission,
# MAGIC     min(CO2_Emissions_g_per_mile) as min_emission,
# MAGIC     max(CO2_Emissions_g_per_mile) as max_emission
# MAGIC from ev_vs_ice_vehicle.silver.vehicle_specs
# MAGIC group by Year, Vehicle_Category;
# MAGIC
# MAGIC select * from gold_emission_analytics;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- Automatic vs Manual Growth
# MAGIC CREATE OR REPLACE TABLE gold_transmission_trends AS
# MAGIC
# MAGIC SELECT
# MAGIC     Year,
# MAGIC     Transmission_Type,
# MAGIC
# MAGIC     COUNT(*) AS vehicle_count,
# MAGIC
# MAGIC     ROUND(
# MAGIC         100.0 * COUNT(*) /
# MAGIC         SUM(COUNT(*)) OVER(PARTITION BY Year),
# MAGIC         2
# MAGIC     ) AS percentage_share
# MAGIC
# MAGIC FROM ev_vs_ice_vehicle.silver.vehicle_specs
# MAGIC
# MAGIC GROUP BY Year,Transmission_Type;
# MAGIC
# MAGIC select * from gold_transmission_trends;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from ev_vs_ice_vehicle.silver.vehicle_specs;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Manufacturer Share
# MAGIC CREATE OR REPLACE TABLE gold_market_share AS
# MAGIC
# MAGIC SELECT
# MAGIC     Year,
# MAGIC     Make,
# MAGIC     Vehicle_Category,
# MAGIC
# MAGIC     COUNT(*) AS vehicle_count,
# MAGIC
# MAGIC     ROUND(
# MAGIC         100.0 * COUNT(*) /
# MAGIC         SUM(COUNT(*)) OVER(PARTITION BY Year),
# MAGIC         2
# MAGIC     ) AS market_share_percentage
# MAGIC
# MAGIC FROM ev_vs_ice_vehicle.silver.vehicle_specs
# MAGIC
# MAGIC GROUP BY Year,Make,Vehicle_Category;
# MAGIC
# MAGIC select * from gold_market_share;

# COMMAND ----------

