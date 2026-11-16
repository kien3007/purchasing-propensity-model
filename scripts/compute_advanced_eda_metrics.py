import pandas as pd
import numpy as np
import os

data_dir = r'sample_data\dunnhumby_The-Complete-Journey\dunnhumby_The-Complete-Journey CSV'

print("=== 1. Pareto 80/20 & Customer Lifetime Value (CLV) ===")
trans_cols = ['household_key', 'SALES_VALUE', 'RETAIL_DISC', 'COUPON_DISC', 'PRODUCT_ID', 'BASKET_ID', 'DAY']
df_trans = pd.read_csv(os.path.join(data_dir, 'transaction_data.csv'), usecols=trans_cols)

hh_spend = df_trans.groupby('household_key')['SALES_VALUE'].sum().sort_values(ascending=False)
total_revenue = hh_spend.sum()
top_20_pct_count = int(len(hh_spend) * 0.20)
top_20_pct_revenue = hh_spend.iloc[:top_20_pct_count].sum()
top_10_pct_count = int(len(hh_spend) * 0.10)
top_10_pct_revenue = hh_spend.iloc[:top_10_pct_count].sum()

print(f"Total Revenue across 2,500 households: ${total_revenue:,.2f}")
print(f"Top 10% households ({top_10_pct_count} households) contribute: ${top_10_pct_revenue:,.2f} ({top_10_pct_revenue/total_revenue*100:.2f}%)")
print(f"Top 20% households ({top_20_pct_count} households) contribute: ${top_20_pct_revenue:,.2f} ({top_20_pct_revenue/total_revenue*100:.2f}%)")
print(f"Bottom 50% households contribute: {hh_spend.iloc[int(len(hh_spend)*0.50):].sum()/total_revenue*100:.2f}%")

print("\n=== 2. Discount & Markdown Sensitivity ===")
total_gross = (df_trans['SALES_VALUE'] - df_trans['RETAIL_DISC'] - df_trans['COUPON_DISC']).sum()
# Note: In dunnhumby, RETAIL_DISC and COUPON_DISC are negative values representing discounts
total_retail_disc = df_trans['RETAIL_DISC'].abs().sum()
total_coupon_disc = df_trans['COUPON_DISC'].abs().sum()
total_sales = df_trans['SALES_VALUE'].sum()
print(f"Total Sales Value: ${total_sales:,.2f}")
print(f"Total Retail Markdown (Store discounts): ${total_retail_disc:,.2f} ({total_retail_disc/(total_sales+total_retail_disc)*100:.2f}% of gross)")
print(f"Total Manufacturer Coupon Discounts: ${total_coupon_disc:,.2f} ({total_coupon_disc/(total_sales+total_coupon_disc)*100:.2f}% of gross)")

print("\n=== 3. Private Label (Store Brand) vs National Brand Penetration ===")
df_prod = pd.read_csv(os.path.join(data_dir, 'product.csv'), usecols=['PRODUCT_ID', 'DEPARTMENT', 'BRAND', 'COMMODITY_DESC'])
# Merge sample transactions to check sales share
df_sample_trans = df_trans.sample(500000, random_state=42).merge(df_prod[['PRODUCT_ID', 'BRAND', 'DEPARTMENT']], on='PRODUCT_ID', how='left')
brand_sales = df_sample_trans.groupby('BRAND')['SALES_VALUE'].agg(['sum', 'count'])
brand_sales['spend_share'] = brand_sales['sum'] / brand_sales['sum'].sum() * 100
brand_sales['item_share'] = brand_sales['count'] / brand_sales['count'].sum() * 100
print(brand_sales)

print("\n=== 4. Top Departments by Spend & Basket Penetration ===")
dept_sales = df_sample_trans.groupby('DEPARTMENT')['SALES_VALUE'].sum().sort_values(ascending=False).head(8)
dept_sales_pct = dept_sales / df_sample_trans['SALES_VALUE'].sum() * 100
for dept, pct in dept_sales_pct.items():
    print(f"  - {dept}: {pct:.2f}%")

print("\n=== 5. Inactive / Churn Households Analysis ===")
last_day_per_hh = df_trans.groupby('household_key')['DAY'].max()
print("Distribution of Last Active Day across households:")
print(f"  - Last seen before Day 500: {(last_day_per_hh < 500).sum()} households ({(last_day_per_hh < 500).mean()*100:.2f}%)")
print(f"  - Last seen before Day 600: {(last_day_per_hh < 600).sum()} households ({(last_day_per_hh < 600).mean()*100:.2f}%)")
print(f"  - Active until Day 650+: {(last_day_per_hh >= 650).sum()} households ({(last_day_per_hh >= 650).mean()*100:.2f}%)")

