import pandas as pd
import numpy as np
import os

data_dir = r'c:\Users\kienn\projectphase3\sample_data\dunnhumby_The-Complete-Journey\dunnhumby_The-Complete-Journey CSV'

trans_cols = ['household_key', 'BASKET_ID', 'DAY', 'SALES_VALUE']
df_trans = pd.read_csv(os.path.join(data_dir, 'transaction_data.csv'), usecols=trans_cols)
baskets = df_trans.groupby(['household_key', 'BASKET_ID', 'DAY'])['SALES_VALUE'].sum().reset_index()
baskets = baskets[baskets['SALES_VALUE'] > 0].sort_values(['household_key', 'DAY'])

camp_table = pd.read_csv(os.path.join(data_dir, 'campaign_table.csv'))
camp_desc = pd.read_csv(os.path.join(data_dir, 'campaign_desc.csv'))
camp_merged = pd.merge(camp_table, camp_desc, on='CAMPAIGN')

n_camp = len(camp_desc)
n_hh = camp_table['household_key'].nunique()
print(f"Campaign count: {n_camp}, Households targeted: {n_hh}")

# Merge baskets with campaigns
b_c = pd.merge(baskets, camp_merged, on='household_key', how='left')
b_c['is_active_camp'] = (b_c['DAY'] >= b_c['START_DAY']) & (b_c['DAY'] <= b_c['END_DAY'])
active_baskets = set(b_c[b_c['is_active_camp'] == True]['BASKET_ID'])

baskets['in_campaign'] = baskets['BASKET_ID'].isin(active_baskets)
baskets['prev_day'] = baskets.groupby('household_key')['DAY'].shift(1)
baskets['interval'] = baskets['DAY'] - baskets['prev_day']

print("\n--- Campaign Impact on Inter-trip Interval ---")
print("Inter-trip mean IN campaign:", round(baskets[baskets['in_campaign']]['interval'].mean(), 2))
print("Inter-trip mean OUT of campaign:", round(baskets[~baskets['in_campaign']]['interval'].mean(), 2))
print("Inter-trip median IN campaign:", baskets[baskets['in_campaign']]['interval'].median())
print("Inter-trip median OUT of campaign:", baskets[~baskets['in_campaign']]['interval'].median())

# Demographics spend
df_demo = pd.read_csv(os.path.join(data_dir, 'hh_demographic.csv'))
hh_spend = baskets.groupby('household_key')['SALES_VALUE'].agg(['sum', 'count', 'mean']).reset_index()
hh_spend.columns = ['household_key', 'total_spend', 'trip_count', 'aov']
demo_spend = pd.merge(hh_spend, df_demo, on='household_key')

print("\n--- Demographics vs AOV ($ per basket) ---")
print("AOV by Household Size (classification_4):")
print(demo_spend.groupby('classification_4')['aov'].mean().round(2))

print("\nAOV by Kid Category:")
print(demo_spend.groupby('KID_CATEGORY_DESC')['aov'].mean().round(2))

