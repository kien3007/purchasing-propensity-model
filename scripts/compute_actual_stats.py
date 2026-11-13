import pandas as pd
import numpy as np
import glob, os

data_dir = r'c:\Users\kienn\projectphase3\sample_data\dunnhumby_The-Complete-Journey\dunnhumby_The-Complete-Journey CSV'

print("--- 1. Loading core transaction & basket data ---")
trans_cols = ['household_key', 'BASKET_ID', 'DAY', 'PRODUCT_ID', 'QUANTITY', 'SALES_VALUE', 'STORE_ID', 'RETAIL_DISC', 'COUPON_DISC', 'TRANS_TIME']
df_trans = pd.read_csv(os.path.join(data_dir, 'transaction_data.csv'), usecols=trans_cols)

print(f"Total transactions: {len(df_trans):,}")
print(f"Total distinct households: {df_trans['household_key'].nunique():,}")
print(f"Total distinct baskets: {df_trans['BASKET_ID'].nunique():,}")
print(f"Day range: {df_trans['DAY'].min()} to {df_trans['DAY'].max()}")

# 1. Basket-level aggregation
baskets = df_trans.groupby(['household_key', 'BASKET_ID', 'DAY', 'STORE_ID']).agg(
    basket_spend=('SALES_VALUE', 'sum'),
    basket_items=('QUANTITY', 'sum'),
    total_coupon_disc=('COUPON_DISC', 'sum'),
    trans_time=('TRANS_TIME', 'first')
).reset_index()

# Filter out zero/negative spend baskets
valid_baskets = baskets[baskets['basket_spend'] > 0].sort_values(['household_key', 'DAY'])
print(f"Valid baskets (> 0 spend): {len(valid_baskets):,}")
print(f"Average basket spend (AOV): ${valid_baskets['basket_spend'].mean():.2f}")
print(f"Median basket spend: ${valid_baskets['basket_spend'].median():.2f}")

# 2. Inter-trip calculation
valid_baskets['prev_day'] = valid_baskets.groupby('household_key')['DAY'].shift(1)
valid_baskets['inter_trip_days'] = valid_baskets['DAY'] - valid_baskets['prev_day']

inter_trips = valid_baskets['inter_trip_days'].dropna()
print(f"\n--- 2. Inter-trip Days Distribution ---")
print(f"Mean inter-trip days: {inter_trips.mean():.2f}")
print(f"Median inter-trip days: {inter_trips.median():.2f}")
print(f"P10: {inter_trips.quantile(0.10):.1f}, P25: {inter_trips.quantile(0.25):.1f}, P50: {inter_trips.quantile(0.50):.1f}, P75: {inter_trips.quantile(0.75):.1f}, P90: {inter_trips.quantile(0.90):.1f}")
print(f"% trips at <= 7 days: {(inter_trips <= 7).mean()*100:.1f}%")
print(f"% trips at <= 14 days: {(inter_trips <= 14).mean()*100:.1f}%")
print(f"% trips at <= 30 days: {(inter_trips <= 30).mean()*100:.1f}%")

# Mode of inter-trip days
vc = inter_trips[inter_trips > 0].value_counts().head(10)
print(f"Top 5 most frequent inter-trip days:\n{vc.head(5)}")

# 3. Fresh food / Perishables analysis
df_prod = pd.read_csv(os.path.join(data_dir, 'product.csv'), usecols=['PRODUCT_ID', 'DEPARTMENT', 'BRAND'])
perishable_depts = ['PRODUCE', 'GROCERY', 'MEAT', 'MEAT-PCKGD', 'DELI', 'PASTRY', 'DAIRY']
print(f"\nDepartments in product table: {df_prod['DEPARTMENT'].value_counts().head(8).to_dict()}")

perish_ids = set(df_prod[df_prod['DEPARTMENT'].isin(['PRODUCE', 'MEAT', 'MEAT-PCKGD', 'DELI', 'PASTRY', 'DAIRY'])]['PRODUCT_ID'])
df_trans['is_perishable'] = df_trans['PRODUCT_ID'].isin(perish_ids)
basket_perish = df_trans.groupby('BASKET_ID')['is_perishable'].any()
print(f"% Baskets containing perishables (Meat, Produce, Dairy, Deli, Pastry): {basket_perish.mean()*100:.2f}%")

# 4. Coupon Halo Effect
# Baskets with coupon discount vs without
valid_baskets['has_coupon'] = valid_baskets['total_coupon_disc'] < 0
spend_with_coupon = valid_baskets[valid_baskets['has_coupon']]['basket_spend'].mean()
spend_without_coupon = valid_baskets[~valid_baskets['has_coupon']]['basket_spend'].mean()
print(f"\n--- 4. Coupon Halo Effect ---")
print(f"Number of baskets with coupon discount: {valid_baskets['has_coupon'].sum():,} ({valid_baskets['has_coupon'].mean()*100:.2f}%)")
print(f"Mean spend WITH coupon: ${spend_with_coupon:.2f}")
print(f"Mean spend WITHOUT coupon: ${spend_without_coupon:.2f}")
print(f"Ratio (Coupon spend / No-coupon spend): {spend_with_coupon / spend_without_coupon:.2f}x")

# 5. Store Hopping
store_counts = valid_baskets.groupby('household_key')['STORE_ID'].nunique()
print(f"\n--- 5. Store Hopping ---")
print(f"Households using only 1 store: {(store_counts == 1).mean()*100:.2f}%")
print(f"Households using 2-3 stores: {(store_counts.isin([2, 3])).mean()*100:.2f}%")
print(f"Households using 4+ stores: {(store_counts >= 4).mean()*100:.2f}%")

# Primary store spend share
hh_store_spend = valid_baskets.groupby(['household_key', 'STORE_ID'])['basket_spend'].sum().reset_index()
hh_total_spend = valid_baskets.groupby('household_key')['basket_spend'].sum().reset_index()
hh_primary_spend = hh_store_spend.groupby('household_key')['basket_spend'].max().reset_index()
hh_loyalty = pd.merge(hh_primary_spend, hh_total_spend, on='household_key', suffixes=('_primary', '_total'))
hh_loyalty['loyalty_share'] = hh_loyalty['basket_spend_primary'] / hh_loyalty['basket_spend_total']
print(f"Mean primary store spend share: {hh_loyalty['loyalty_share'].mean()*100:.2f}%")
print(f"% households with primary store share >= 80%: {(hh_loyalty['loyalty_share'] >= 0.80).mean()*100:.2f}%")

# 6. Demographics vs Inter-trip
df_demo = pd.read_csv(os.path.join(data_dir, 'hh_demographic.csv'))
hh_mean_interval = valid_baskets.groupby('household_key')['inter_trip_days'].median().reset_index()
hh_demo_merged = pd.merge(hh_mean_interval, df_demo, on='household_key')
print(f"\n--- 6. Demographics vs Inter-trip (Actual medians) ---")
print("By Household Size (classification_4):")
print(hh_demo_merged.groupby('classification_4')['inter_trip_days'].median())
print("\nBy Kids Category:")
print(hh_demo_merged.groupby('KID_CATEGORY_DESC')['inter_trip_days'].median())

# 7. Actual Positive Label Rate P(Y=1) for delta_t = 7, 14, 30
cutoffs = [300, 400, 500]
print(f"\n--- 7. Actual Label Rates P(Y=1) across cutoffs {cutoffs} ---")
all_hh = set(range(1, 2501))
for dt in [7, 14, 30]:
    rates = []
    for t0 in cutoffs:
        active_hh = set(valid_baskets[(valid_baskets['DAY'] > t0) & (valid_baskets['DAY'] <= t0 + dt)]['household_key'])
        rates.append(len(active_hh) / len(all_hh))
    print(f"delta_t = {dt:2d} days: mean P(Y=1) = {np.mean(rates)*100:.2f}% (min: {min(rates)*100:.2f}%, max: {max(rates)*100:.2f}%)")

