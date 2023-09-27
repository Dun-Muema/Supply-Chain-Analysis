import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Loading data into a Panda dataframe

df_supply = pd.read_csv('C:/Users/DuncanMu/Desktop/Supply_Chain_Project/Data_Set/supply_chain_data.csv')
df_supply.head()
df_supply.info()
df_supply.describe()

# COST ANALYSIS
# Total cost for each product type
Production_Costs_per_product_type= df_supply.groupby('Product type')['Costs'].sum().reset_index().round(2)
Production_Costs_per_product_type

# comapring manufacturing cost and selling costs
Manufacturing_costs_vs_Selling_price = df_supply.groupby('Product type').agg({'Manufacturing costs': 'mean', 'Price': 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.35
index = range(len(Manufacturing_costs_vs_Selling_price))
bar1 = ax.bar(index, Manufacturing_costs_vs_Selling_price['Manufacturing costs'], bar_width, label='Average Manufacturing Costs')
bar2 = ax.bar([i + bar_width for i in index], Manufacturing_costs_vs_Selling_price['Price'], bar_width, label='Average Selling Prices')

ax.set_xlabel('Product Type')
ax.set_ylabel('Amount')
ax.set_title('Comparison of Average Manufacturing Costs and Average Selling Prices by Product Type')
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(Manufacturing_costs_vs_Selling_price['Product type'])
ax.legend()

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

#overall profitability per product
total_revenue = df_supply.groupby('Product type')['Revenue generated'].sum().reset_index().round(2)
total_costs = df_supply.groupby('Product type')['Costs'].sum().reset_index().round(2)

profitability = total_revenue.merge(total_costs, on='Product type', suffixes=('_revenue', '_costs'))
profitability['Profitability'] = profitability['Revenue generated'] - profitability['Costs']
profitability

#SUPPLY CHAIN ANALYSIS
# Average Lead time for each product
Avg_lead_time = df_supply.groupby('Product type')['Lead times'].mean().reset_index().round(2)
Avg_lead_time

#correlation Between lead time, stock levels and availability
Corr_columns = ['Lead time', 'Availability', 'Stock levels']
corr_matrix = df_supply.groupby('Product type')[Corr_columns].mean().corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1,fmt='.1g', linewidths=1,linecolor= 'Black')
plt.title('Correlation Matrix Heatmap')
plt.show()

#Logistics Analysis
#most commonly used transportation mode
Transportation_mode = df_supply['Transportation modes'].value_counts()
Transportation_mode

# Effects of transportation mode on the lead times and costs
transportation_mode_stats = df_supply.groupby('Transportation modes').agg({'Lead times': 'mean','Costs': 'mean'}).reset_index()
transportation_mode_stats

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.bar(transportation_mode_stats['Transportation modes'], transportation_mode_stats['Lead times'])
plt.xlabel('Transportation Mode')
plt.ylabel('Average Lead Time')
plt.title('Impact of Transportation Mode on Lead Times')

plt.subplot(1, 2, 2)
plt.bar(transportation_mode_stats['Transportation modes'], transportation_mode_stats['Costs'])
plt.xlabel('Transportation Mode')
plt.ylabel('Average Cost')
plt.title('Impact of Transportation Mode on Costs')

plt.tight_layout()
plt.show()

# most commonly used routes
Route =  df_supply['Routes'].value_counts()
Route

route_stats = df_supply.groupby('Routes').agg({'Lead times': 'mean','Costs': 'mean'}).reset_index()
most_common_routes = df_supply['Routes'].mode()

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.bar(route_stats['Routes'], route_stats['Lead times'])
plt.xlabel('Route')
plt.ylabel('Average Lead Time')
plt.title('Impact of Route on Lead Times')

plt.subplot(1, 2, 2)
plt.bar(route_stats['Routes'], route_stats['Costs'])
plt.xlabel('Route')
plt.ylabel('Average Cost')
plt.title('Impact of Route on Costs')

plt.tight_layout()
plt.show()

#Quality Analysis 
#Average defect rates  for product type
df_quality=df_supply.groupby('Product type')['Defect rates'].mean().round(3)
df_quality

#correlation between defects rates, inspection results and Manufacturing costs
corr_defects = df_supply.groupby('Inspection results').agg({'Manufacturing costs' : 'mean', 'Defect rates': 'mean'}).reset_index()

pig, ax = plt.subplots(figsize=(10, 6))

bar_width = 0.35
index = range(len(corr_defects))
bar1 = ax.bar(index, corr_defects['Manufacturing costs'], bar_width, label='Average Manufacturing Costs')
bar2 = ax.bar([i + bar_width for i in index], corr_defects['Defect rates'], bar_width, label='Average Defect rates')

ax.set_xlabel('inspection')
ax.set_ylabel('Amount')
ax.set_title('Comparison of Average Manufacturing Costs and Average Selling Prices by Product Type')
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(corr_defects['Inspection results'])
ax.legend()

plt.show()

#product Analysis
#correlation between stock levels and Order quantities
corr_stock_vs_quantities = df_supply['Stock levels'].corr(df_supply['Number of products sold'])
corr_stock_vs_quantities

# Are production quantities affect the market quantites

corr_production_Volumes_vs_Demand= df_supply['Number of products sold'].corr(df_supply['Production volumes'])
corr_production_Volumes_vs_Demand

#Demographic Analysis

Demo_Anl = df_supply.groupby('Product type')['Customer demographics'].value_counts()
Demo_Anl

#Location Analysis to optimize our advertising
loc_analysis = df_supply.groupby('Product type')['Location'].value_counts()
loc_analysis