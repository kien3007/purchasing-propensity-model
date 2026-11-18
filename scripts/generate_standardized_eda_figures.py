"""
Standardized EDA Figure Generator
Implements the Gold Standard Template for Propensity Modeling:
- P(Y=1) by cohort on y-axis
- Cohort sample size n on each bar
- Base rate reference line (68.3%)
- Metric deltas expressed in percentage points (điểm phần trăm)
- Strict time boundaries and unified dataset statistics
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import duckdb

# Setup paths
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.data.loader import DataLoader

FIG_DIR = project_root / 'docs' / 'reports' / 'figures'
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Plotting style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['figure.titlesize'] = 14
plt.rcParams['figure.dpi'] = 150

print("🚀 Loading Dunnhumby dataset...")
data = DataLoader.load_all()
df_trans = data['transactions']
df_prod = data['products']
df_demo = data['demographics']
df_camp = data['campaigns']
df_camp_desc = data['campaign_desc']
df_redempt = data['redemptions']
baskets = DataLoader.build_trip_level_baskets(df_trans, df_prod)

con = duckdb.connect()
con.register('df_trans', df_trans)
con.register('df_prod', df_prod)
con.register('df_demo', df_demo)
con.register('baskets', baskets)
con.register('df_camp', df_camp)
con.register('df_camp_desc', df_camp_desc)
con.register('df_redempt', df_redempt)

cutoffs = [250, 350, 450, 550, 650]
BASE_RATE = 68.34

def plot_gold_standard_bar(df_agg, col_cohort, col_p, col_n, title, xlabel, fig_name,
                           delta_idx=(0, -1), delta_label="Chênh lệch", bar_color='#2b5c8f',
                           ylim=(0, 115), is_horizontal=False):
    """Draws a standardized P(Y=1) bar chart with n, base rate, and percentage point delta."""
    fig, ax = plt.subplots(figsize=(9.5, 5.2), constrained_layout=True)
    x = np.arange(len(df_agg))
    width = 0.52

    bars = ax.bar(x, df_agg[col_p], width, color=bar_color, edgecolor='#1b3c5f', linewidth=1.2, zorder=3)
    ax.axhline(BASE_RATE, color='#d95f02', linestyle='--', linewidth=1.8,
               label=f'Tỷ lệ cơ sở toàn mẫu ({BASE_RATE:.1f}%)', zorder=4)

    for i, bar in enumerate(bars):
        h = bar.get_height()
        n_val = int(round(df_agg.loc[i, col_n]))
        ax.annotate(f'{h:.1f}%\n(n = {n_val:,})',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#1b3c5f')

    # Delta annotation
    i_start, i_end = delta_idx
    p_start = df_agg.loc[i_start, col_p]
    p_end = df_agg.loc[i_end, col_p]
    delta_pts = p_end - p_start
    sign = '+' if delta_pts >= 0 else ''
    
    # Annotate delta box
    mid_x = (i_start + i_end) / 2.0
    ax.annotate(f'{delta_label}: {sign}{delta_pts:.1f} điểm phần trăm',
                xy=(i_end, p_end), xytext=(mid_x, min(max(p_end + 12, 45), 102)),
                arrowprops=dict(arrowstyle="->", color="#b2182b", lw=1.8, connectionstyle="arc3,rad=-0.15"),
                fontsize=10.5, fontweight='bold', color='#b2182b',
                bbox=dict(boxstyle="round,pad=0.35", facecolor="#fee8c8", edgecolor="#b2182b", lw=1.2))

    ax.set_ylabel('Xác suất mua hàng trong 14 ngày: P(Y=1) (%)', fontsize=11, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=11, fontweight='bold', labelpad=8)
    ax.set_xticks(x)
    ax.set_xticklabels([str(t).replace(' (', '\n(') for t in df_agg[col_cohort]], fontsize=10.5, fontweight='bold')
    ax.set_ylim(ylim)
    ax.set_title(title, fontsize=12.5, fontweight='bold', pad=12)
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9, fontsize=10.5)

    plt.savefig(FIG_DIR / fig_name, dpi=150)
    plt.close()
    print(f"✅ Generated {fig_name}")


# ==============================================================================
# 1. HORIZON CURVE (CĂN CỨ CHỌN DELTA T = 14 NGÀY)
# ==============================================================================
horizons = [1, 2, 3, 5, 7, 10, 14, 21, 28, 35, 42, 56]
h_res = {h: [] for h in horizons}
for t0 in cutoffs:
    for h in horizons:
        fut = baskets[(baskets['DAY'] > t0) & (baskets['DAY'] <= t0 + h)]
        pct = fut['household_key'].nunique() / 2500.0 * 100
        h_res[h].append(pct)

h_means = [np.mean(h_res[h]) for h in horizons]
h_stds = [np.std(h_res[h]) for h in horizons]

fig, ax = plt.subplots(figsize=(10, 5.2), constrained_layout=True)
ax.plot(horizons, h_means, marker='o', color='#1f77b4', linewidth=2.5, label='Tỷ lệ hộ có phát sinh mua sắm (Trung bình 5 điểm chốt sổ)')
ax.fill_between(horizons, np.array(h_means) - np.array(h_stds), np.array(h_means) + np.array(h_stds), color='#1f77b4', alpha=0.15)

# Highlight H = 7, 14, 28
for h_target, col in zip([7, 14, 28], ['#2ca02c', '#d95f02', '#7570b3']):
    idx = horizons.index(h_target)
    val = h_means[idx]
    ax.scatter([h_target], [val], color=col, s=90, zorder=5)
    ax.axvline(h_target, color=col, linestyle=':', alpha=0.7)
    ax.annotate(f'H = {h_target} ngày: {val:.1f}%\n(std ±{h_stds[idx]:.1f}%)',
                xy=(h_target, val), xytext=(h_target + 1.2, val - 7 if h_target == 14 else val + 4),
                fontweight='bold', fontsize=10,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#f7f7f7', edgecolor=col))

ax.axhline(68.34, color='#d95f02', linestyle='--', linewidth=1.2, alpha=0.6)
ax.set_xlabel('Chân trời dự báo H (Số ngày kể từ mốc chốt sổ t_0)', fontweight='bold')
ax.set_ylabel('Tỷ lệ hộ gia đình có >= 1 giỏ hàng (%)', fontweight='bold')
ax.set_title('Đường cong tích lũy hộ gia đình mua sắm theo chân trời dự báo H\n(Trung bình qua 5 mốc quan sát; tập mẫu n = 2,500 hộ)', pad=12)
ax.set_xlim(0, 58)
ax.set_ylim(0, 100)
ax.legend(loc='lower right', frameon=True, facecolor='white', fontsize=10)
plt.savefig(FIG_DIR / '01_horizon_selection_curve.png', dpi=150)
plt.close()
print("✅ Generated 01_horizon_selection_curve.png")


# ==============================================================================
# 2. RECENCY: DAYS SINCE LAST BASKET
# ==============================================================================
rec_results = []
for t0 in cutoffs:
    q = f"""
    WITH last_b AS (
        SELECT household_key, MAX(DAY) AS last_day
        FROM baskets WHERE DAY <= {t0} GROUP BY household_key
    ),
    fut AS (
        SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0 + 14}
    )
    SELECT 
        CASE 
            WHEN ({t0} - l.last_day) <= 3 THEN '1 - 3 ngày'
            WHEN ({t0} - l.last_day) <= 7 THEN '4 - 7 ngày'
            WHEN ({t0} - l.last_day) <= 14 THEN '8 - 14 ngày'
            WHEN ({t0} - l.last_day) <= 30 THEN '15 - 30 ngày'
            ELSE '> 30 ngày'
        END AS recency_bin,
        COUNT(*) AS n_hh,
        ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS p_y1
    FROM last_b l LEFT JOIN fut f ON l.household_key = f.household_key
    GROUP BY 1
    """
    rec_results.append(con.execute(q).df())

df_rec = pd.concat(rec_results).groupby('recency_bin').agg(n=('n_hh', 'mean'), p=('p_y1', 'mean')).reindex(['1 - 3 ngày', '4 - 7 ngày', '8 - 14 ngày', '15 - 30 ngày', '> 30 ngày']).reset_index()
plot_gold_standard_bar(df_rec, 'recency_bin', 'p', 'n',
                       title='Khoảng cách từ lần mua gần nhất và xác suất mua 14 ngày tới\n(Biến: days_since_last_basket | n = 2,500 hộ)',
                       xlabel='Khoảng cách từ chuyến đi chợ gần nhất đến thời điểm t_0',
                       fig_name='02_p_y1_recency.png',
                       delta_idx=(4, 0), delta_label='Chênh lệch (1-3 ngày vs >30 ngày)',
                       bar_color='#3182bd')


# ==============================================================================
# 3. FREQUENCY: BASKETS COUNT 90D
# ==============================================================================
freq_res = []
for t0 in cutoffs:
    q = f"""
    WITH obs AS (
        SELECT household_key, COUNT(*) AS n_baskets
        FROM baskets WHERE DAY <= {t0} AND DAY >= {t0 - 90} GROUP BY household_key
    ),
    all_hh AS (SELECT DISTINCT household_key FROM df_trans),
    fut AS (SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0 + 14})
    SELECT 
        CASE 
            WHEN COALESCE(o.n_baskets, 0) = 0 THEN '0 giỏ'
            WHEN o.n_baskets <= 5 THEN '1 - 5 giỏ'
            WHEN o.n_baskets <= 12 THEN '6 - 12 giỏ'
            WHEN o.n_baskets <= 24 THEN '13 - 24 giỏ'
            ELSE '>= 25 giỏ'
        END AS freq_tier,
        COUNT(*) AS n_hh,
        ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS p_y1
    FROM all_hh a 
    LEFT JOIN obs o ON a.household_key = o.household_key
    LEFT JOIN fut f ON a.household_key = f.household_key
    GROUP BY 1
    """
    freq_res.append(con.execute(q).df())

df_freq = pd.concat(freq_res).groupby('freq_tier').agg(n=('n_hh', 'mean'), p=('p_y1', 'mean')).reindex(['0 giỏ', '1 - 5 giỏ', '6 - 12 giỏ', '13 - 24 giỏ', '>= 25 giỏ']).reset_index()
plot_gold_standard_bar(df_freq, 'freq_tier', 'p', 'n',
                       title='Tần suất mua sắm 90 ngày và xác suất mua 14 ngày tới\n(Biến: baskets_count_90d | n = 2,500 hộ)',
                       xlabel='Số giỏ hàng phát sinh trong cửa sổ quan sát 90 ngày',
                       fig_name='03_p_y1_frequency.png',
                       delta_idx=(0, 4), delta_label='Chênh lệch (>=25 giỏ vs 0 giỏ)',
                       bar_color='#2ca25f')


# ==============================================================================
# 4. SPEND 90D
# ==============================================================================
spend_res = []
for t0 in cutoffs:
    q = f"""
    WITH obs AS (
        SELECT household_key, SUM(basket_spend) AS total_spend
        FROM baskets WHERE DAY <= {t0} AND DAY >= {t0 - 90} GROUP BY household_key
    ),
    all_hh AS (SELECT DISTINCT household_key FROM df_trans),
    fut AS (SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0 + 14})
    SELECT 
        CASE 
            WHEN COALESCE(o.total_spend, 0) = 0 THEN '$0'
            WHEN o.total_spend < 300 THEN '< $300'
            WHEN o.total_spend < 700 THEN '$300 - $700'
            WHEN o.total_spend < 1300 THEN '$700 - $1,300'
            ELSE '>= $1,300'
        END AS spend_tier,
        COUNT(*) AS n_hh,
        ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS p_y1
    FROM all_hh a 
    LEFT JOIN obs o ON a.household_key = o.household_key
    LEFT JOIN fut f ON a.household_key = f.household_key
    GROUP BY 1
    """
    spend_res.append(con.execute(q).df())

df_sp = pd.concat(spend_res).groupby('spend_tier').agg(n=('n_hh', 'mean'), p=('p_y1', 'mean')).reindex(['$0', '< $300', '$300 - $700', '$700 - $1,300', '>= $1,300']).reset_index()
plot_gold_standard_bar(df_sp, 'spend_tier', 'p', 'n',
                       title='Tổng chi tiêu 90 ngày và xác suất mua 14 ngày tới\n(Biến: spend_90d | n = 2,500 hộ)',
                       xlabel='Tổng mức chi tiêu trong 90 ngày quan sát (USD)',
                       fig_name='04_p_y1_spend.png',
                       delta_idx=(0, 4), delta_label='Chênh lệch (>= $1,300 vs $0)',
                       bar_color='#6baed6')


# ==============================================================================
# 5. CATEGORY BREADTH 90D (CẬP NHẬT 24_category_breadth_stickiness.png)
# ==============================================================================
breadth_res = []
for t0 in cutoffs:
    q = f"""
    WITH items AS (
        SELECT t.household_key, t.BASKET_ID, t.DAY, p.DEPARTMENT
        FROM df_trans t JOIN df_prod p ON t.PRODUCT_ID = p.PRODUCT_ID
        WHERE t.DAY <= {t0} AND t.DAY >= {t0 - 90} AND t.SALES_VALUE > 0
    ),
    hh_breadth AS (
        SELECT household_key, COUNT(DISTINCT DEPARTMENT) AS num_depts FROM items GROUP BY household_key
    ),
    fut AS (
        SELECT DISTINCT household_key FROM df_trans WHERE DAY > {t0} AND DAY <= {t0 + 14} AND SALES_VALUE > 0
    )
    SELECT 
        CASE WHEN num_depts >= 12 THEN 'Toàn diện (>=12 ngành)'
             WHEN num_depts BETWEEN 7 AND 11 THEN 'Phổ thông (7-11 ngành)'
             WHEN num_depts BETWEEN 3 AND 6 THEN 'Thứ yếu (3-6 ngành)'
             ELSE 'Đơn ngành (1-2 ngành)' END AS breadth_tier,
        COUNT(*) AS total_hh,
        ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS propensity_pct
    FROM hh_breadth h LEFT JOIN fut f ON h.household_key = f.household_key
    GROUP BY 1
    """
    breadth_res.append(con.execute(q).df())

df_all_breadth = pd.concat(breadth_res).groupby('breadth_tier').agg(n=('total_hh', 'mean'), p=('propensity_pct', 'mean')).reindex([
    'Đơn ngành (1-2 ngành)', 'Thứ yếu (3-6 ngành)', 'Phổ thông (7-11 ngành)', 'Toàn diện (>=12 ngành)'
]).reset_index()

plot_gold_standard_bar(df_all_breadth, 'breadth_tier', 'p', 'n',
                       title='Độ phủ ngành hàng 90 ngày và xác suất mua 14 ngày tới\n(Biến: department_breadth_90d | n = 2,301 hộ có phát sinh giỏ hàng)',
                       xlabel='Số lượng ngành hàng đã mua sắm trong 90 ngày quan sát',
                       fig_name='24_category_breadth_stickiness.png',
                       delta_idx=(0, 3), delta_label='Chênh lệch (Toàn diện vs Đơn ngành)',
                       bar_color='#08519c')


# ==============================================================================
# 6. PERISHABLES RECENCY (DAYS SINCE LAST PERISHABLE)
# ==============================================================================
per_res = []
for t0 in cutoffs:
    q = f"""
    WITH last_p AS (
        SELECT household_key, MAX(DAY) AS last_p_day
        FROM baskets WHERE DAY <= {t0} AND has_perishable = true GROUP BY household_key
    ),
    all_hh AS (SELECT DISTINCT household_key FROM df_trans),
    fut AS (SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0 + 14})
    SELECT 
        CASE 
            WHEN l.last_p_day IS NULL OR ({t0} - l.last_p_day) > 30 THEN '> 30 ngày / Chưa mua'
            WHEN ({t0} - l.last_p_day) <= 3 THEN '1 - 3 ngày'
            WHEN ({t0} - l.last_p_day) <= 7 THEN '4 - 7 ngày'
            WHEN ({t0} - l.last_p_day) <= 14 THEN '8 - 14 ngày'
            ELSE '15 - 30 ngày'
        END AS per_tier,
        COUNT(*) AS n_hh,
        ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS p_y1
    FROM all_hh a 
    LEFT JOIN last_p l ON a.household_key = l.household_key
    LEFT JOIN fut f ON a.household_key = f.household_key
    GROUP BY 1
    """
    per_res.append(con.execute(q).df())

df_per = pd.concat(per_res).groupby('per_tier').agg(n=('n_hh', 'mean'), p=('p_y1', 'mean')).reindex([
    '1 - 3 ngày', '4 - 7 ngày', '8 - 14 ngày', '15 - 30 ngày', '> 30 ngày / Chưa mua'
]).reset_index()

plot_gold_standard_bar(df_per, 'per_tier', 'p', 'n',
                       title='Khoảng cách từ lần mua đồ tươi gần nhất và xác suất mua 14 ngày tới\n(Biến: days_since_last_perishable | n = 2,500 hộ)',
                       xlabel='Số ngày kể từ lần gần nhất mua thực phẩm tươi sống',
                       fig_name='05_p_y1_perishable_recency.png',
                       delta_idx=(4, 0), delta_label='Chênh lệch (1-3 ngày vs >30 ngày)',
                       bar_color='#238b45')


# ==============================================================================
# 7. CAMPAIGN TARGETING AT T0
# ==============================================================================
camp_res = []
for t0 in cutoffs:
    q = f"""
    WITH active_camps AS (
        SELECT c.household_key, d.DESCRIPTION AS camp_type
        FROM df_camp c
        JOIN df_camp_desc d ON c.CAMPAIGN = d.CAMPAIGN
        WHERE d.START_DAY <= {t0} AND d.END_DAY >= {t0}
    ),
    camp_summary AS (
        SELECT 
            household_key,
            MAX(CASE WHEN camp_type = 'TypeA' THEN 1 ELSE 0 END) AS has_type_a,
            MAX(CASE WHEN camp_type = 'TypeB' THEN 1 ELSE 0 END) AS has_type_b,
            MAX(CASE WHEN camp_type = 'TypeC' THEN 1 ELSE 0 END) AS has_type_c
        FROM active_camps GROUP BY household_key
    ),
    all_hh AS (SELECT DISTINCT household_key FROM df_trans),
    fut AS (SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0 + 14})
    SELECT 
        CASE 
            WHEN s.has_type_a = 1 THEN 'Chiến dịch Loại A'
            WHEN s.has_type_b = 1 THEN 'Chiến dịch Loại B'
            WHEN s.has_type_c = 1 THEN 'Chiến dịch Loại C'
            ELSE 'Không có chiến dịch'
        END AS camp_cohort,
        COUNT(*) AS n_hh,
        ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS p_y1
    FROM all_hh a
    LEFT JOIN camp_summary s ON a.household_key = s.household_key
    LEFT JOIN fut f ON a.household_key = f.household_key
    GROUP BY 1
    """
    camp_res.append(con.execute(q).df())

df_cp = pd.concat(camp_res).groupby('camp_cohort').agg(n=('n_hh', 'mean'), p=('p_y1', 'mean')).reindex([
    'Không có chiến dịch', 'Chiến dịch Loại C', 'Chiến dịch Loại B', 'Chiến dịch Loại A'
]).reset_index()

plot_gold_standard_bar(df_cp, 'camp_cohort', 'p', 'n',
                       title='Nhắm mục tiêu chiến dịch tiếp thị tại t_0 và xác suất mua 14 ngày tới\n(Biến: is_targeted_campaign_type | n = 2,500 hộ)',
                       xlabel='Phân loại chiến dịch tiếp thị đang kích hoạt đối với hộ gia đình',
                       fig_name='07_p_y1_campaign_targeting.png',
                       delta_idx=(0, 3), delta_label='Chênh lệch (Loại A vs Không)',
                       bar_color='#756bb1')


# ==============================================================================
# 8. COUPON REDEMPTIONS 180D
# ==============================================================================
cpn_res = []
for t0 in cutoffs:
    q = f"""
    WITH red AS (
        SELECT household_key, COUNT(*) AS n_red
        FROM df_redempt WHERE DAY <= {t0} AND DAY >= {t0 - 180} GROUP BY household_key
    ),
    all_hh AS (SELECT DISTINCT household_key FROM df_trans),
    fut AS (SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0 + 14})
    SELECT 
        CASE 
            WHEN COALESCE(r.n_red, 0) = 0 THEN '0 lần (Chưa dùng)'
            WHEN r.n_red <= 2 THEN '1 - 2 lần'
            ELSE '>= 3 lần'
        END AS red_cohort,
        COUNT(*) AS n_hh,
        ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS p_y1
    FROM all_hh a
    LEFT JOIN red r ON a.household_key = r.household_key
    LEFT JOIN fut f ON a.household_key = f.household_key
    GROUP BY 1
    """
    cpn_res.append(con.execute(q).df())

df_cr = pd.concat(cpn_res).groupby('red_cohort').agg(n=('n_hh', 'mean'), p=('p_y1', 'mean')).reindex([
    '0 lần (Chưa dùng)', '1 - 2 lần', '>= 3 lần'
]).reset_index()

plot_gold_standard_bar(df_cr, 'red_cohort', 'p', 'n',
                       title='Lịch sử đổi phiếu giảm giá 180 ngày và xác suất mua 14 ngày tới\n(Biến: coupon_redemptions_180d | n = 2,500 hộ)',
                       xlabel='Số lần sử dụng coupon giảm giá trong 180 ngày quan sát',
                       fig_name='06_p_y1_coupon_redemptions.png',
                       delta_idx=(0, 2), delta_label='Chênh lệch (>=3 lần vs 0 lần)',
                       bar_color='#31a354')


# ==============================================================================
# 9. STORE LOYALTY 90D
# ==============================================================================
loy_res = []
for t0 in cutoffs:
    q = f"""
    WITH store_spend AS (
        SELECT household_key, STORE_ID, SUM(basket_spend) AS st_spend
        FROM baskets WHERE DAY <= {t0} AND DAY >= {t0 - 90} GROUP BY household_key, STORE_ID
    ),
    hh_tot AS (
        SELECT household_key, SUM(st_spend) AS tot_spend, MAX(st_spend) AS max_st_spend
        FROM store_spend GROUP BY household_key
    ),
    all_hh AS (SELECT DISTINCT household_key FROM df_trans),
    fut AS (SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0 + 14})
    SELECT 
        CASE 
            WHEN h.tot_spend IS NULL OR h.tot_spend = 0 THEN '0 giỏ (Không mua)'
            WHEN (h.max_st_spend * 1.0 / h.tot_spend) >= 0.80 THEN 'Tập trung cao (>=80% tiền)'
            WHEN (h.max_st_spend * 1.0 / h.tot_spend) >= 0.50 THEN 'Trung bình (50-80% tiền)'
            ELSE 'Phân tán (<50% tiền)'
        END AS loyalty_tier,
        COUNT(*) AS n_hh,
        ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS p_y1
    FROM all_hh a 
    LEFT JOIN hh_tot h ON a.household_key = h.household_key
    LEFT JOIN fut f ON a.household_key = f.household_key
    GROUP BY 1
    """
    loy_res.append(con.execute(q).df())

df_loy = pd.concat(loy_res).groupby('loyalty_tier').agg(n=('n_hh', 'mean'), p=('p_y1', 'mean')).reindex([
    '0 giỏ (Không mua)', 'Phân tán (<50% tiền)', 'Trung bình (50-80% tiền)', 'Tập trung cao (>=80% tiền)'
]).reset_index()

plot_gold_standard_bar(df_loy, 'loyalty_tier', 'p', 'n',
                       title='Tỷ trọng chi tiêu tại cửa hàng chính và xác suất mua 14 ngày tới\n(Biến: primary_store_spend_share | n = 2,500 hộ)',
                       xlabel='Mức độ tập trung ngân sách mua sắm tại cửa hàng chính trong 90 ngày',
                       fig_name='08_p_y1_store_loyalty.png',
                       delta_idx=(0, 3), delta_label='Chênh lệch (Tập trung vs 0 giỏ)',
                       bar_color='#e6550d')


# ==============================================================================
# 10. DEMOGRAPHICS: HOUSEHOLD SIZE
# ==============================================================================
demo_res = []
for t0 in cutoffs:
    q = f"""
    WITH all_hh AS (SELECT DISTINCT household_key FROM df_trans),
    fut AS (SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0 + 14})
    SELECT 
        COALESCE(d.classification_4, 'UNKNOWN') AS hh_size,
        COUNT(*) AS n_hh,
        ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END)*100.0/COUNT(*), 2) AS p_y1
    FROM all_hh a
    LEFT JOIN df_demo d ON a.household_key = d.household_key
    LEFT JOIN fut f ON a.household_key = f.household_key
    GROUP BY 1
    """
    demo_res.append(con.execute(q).df())

df_dm = pd.concat(demo_res).groupby('hh_size').agg(n=('n_hh', 'mean'), p=('p_y1', 'mean')).reindex([
    '1', '2', '3', '4', '5+', 'UNKNOWN'
]).reset_index()
df_dm['hh_size_label'] = [
    '1 người', '2 người', '3 người', '4 người', '5+ người', 'Không khai báo\n(UNKNOWN)'
]

plot_gold_standard_bar(df_dm, 'hh_size_label', 'p', 'n',
                       title='Quy mô hộ gia đình và xác suất mua sắm 14 ngày tới\n(Biến: household_size | n = 801 hộ khai báo + 1,699 hộ UNKNOWN)',
                       xlabel='Quy mô thành viên trong hộ gia đình (Theo dữ liệu nhân khẩu học)',
                       fig_name='09_p_y1_demographics.png',
                       delta_idx=(5, 0), delta_label='Chênh lệch (1 người vs UNKNOWN)',
                       bar_color='#41b6c4')


# ==============================================================================
# 11. APPENDIX 1: REVENUE CONCENTRATION CURVE (19_clv_pareto_distribution.png)
# ==============================================================================
hh_clv = baskets.groupby('household_key')['basket_spend'].sum().sort_values(ascending=False).reset_index()
total_spend = hh_clv['basket_spend'].sum()
hh_clv['cum_spend'] = hh_clv['basket_spend'].cumsum()
hh_clv['cum_spend_pct'] = (hh_clv['cum_spend'] / total_spend) * 100
hh_clv['cum_hh_pct'] = (np.arange(1, len(hh_clv) + 1) / len(hh_clv)) * 100

top10_spend_pct = hh_clv.iloc[int(len(hh_clv)*0.10) - 1]['cum_spend_pct']
top20_spend_pct = hh_clv.iloc[int(len(hh_clv)*0.20) - 1]['cum_spend_pct']
top50_spend_pct = hh_clv.iloc[int(len(hh_clv)*0.50) - 1]['cum_spend_pct']

# Gini
x_vals = np.sort(hh_clv['basket_spend'].values)
n_vals = len(x_vals)
gini = (2 * np.sum(np.arange(1, n_vals + 1) * x_vals) - (n_vals + 1) * np.sum(x_vals)) / (n_vals * np.sum(x_vals))

fig, ax = plt.subplots(figsize=(9.5, 5.2), constrained_layout=True)
ax.plot(hh_clv['cum_hh_pct'], hh_clv['cum_spend_pct'], color='#1f77b4', linewidth=2.8, label='Đường cong tập trung doanh thu thực tế')
ax.plot([0, 100], [0, 100], color='gray', linestyle='--', linewidth=1.5, label='Đường phân bổ đồng đều (45° Baseline)')
ax.fill_between(hh_clv['cum_hh_pct'], hh_clv['cum_spend_pct'], hh_clv['cum_hh_pct'], color='#1f77b4', alpha=0.15)

ax.scatter([10, 20, 50], [top10_spend_pct, top20_spend_pct, top50_spend_pct], color='#d62728', s=80, zorder=5)

ax.annotate(f'Top 10% hộ tạo {top10_spend_pct:.1f}% doanh thu\n(${hh_clv.iloc[:250]["basket_spend"].sum():,.0f})',
            xy=(10, top10_spend_pct), xytext=(22, top10_spend_pct - 6),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='#d62728'),
            fontweight='bold', fontsize=9.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#fee8c8', edgecolor='#d62728'))

ax.annotate(f'Top 20% hộ tạo {top20_spend_pct:.1f}% doanh thu\n(${hh_clv.iloc[:500]["basket_spend"].sum():,.0f} | Gini = {gini:.2f})',
            xy=(20, top20_spend_pct), xytext=(35, top20_spend_pct - 6),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='#d62728'),
            fontweight='bold', fontsize=9.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#fee8c8', edgecolor='#d62728'))

ax.annotate(f'Top 50% hộ tạo {top50_spend_pct:.1f}% doanh thu\n(50% hộ còn lại chiếm {100-top50_spend_pct:.1f}%)',
            xy=(50, top50_spend_pct), xytext=(58, top50_spend_pct - 10),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='#d62728'),
            fontweight='bold', fontsize=9.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#fee8c8', edgecolor='#d62728'))

ax.set_xlabel('Tỷ lệ tích lũy hộ gia đình (Sắp xếp từ chi tiêu cao nhất đến thấp nhất) (%)', fontweight='bold')
ax.set_ylabel('Tỷ lệ tích lũy doanh thu thực tế (%)', fontweight='bold')
ax.set_title(f'Mức độ tập trung doanh thu theo hộ gia đình (Tổng 2 năm: ${total_spend:,.2f} | n = 2,500 hộ)\n(Cần 44.0% số hộ để đạt 80% doanh thu - Mức tập trung thấp hơn quy tắc 80/20)', pad=12)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9)
plt.savefig(FIG_DIR / '19_clv_pareto_distribution.png', dpi=150)
plt.close()
print("✅ Generated 19_clv_pareto_distribution.png")


# ==============================================================================
# 12. APPENDIX 2: TWO-TIER PROMOTION STRUCTURE (20_markdown_vs_coupon_spend.png)
# ==============================================================================
total_retail_disc = abs(df_trans['RETAIL_DISC'].sum())
total_coupon_disc = abs(df_trans['COUPON_DISC'].sum())
total_net_sales = df_trans['SALES_VALUE'].sum()
gross_sales = total_net_sales + total_retail_disc + total_coupon_disc
ratio_markdown_coupon = total_retail_disc / total_coupon_disc

baskets_with_retail = (baskets['retail_discount'] < 0).mean() * 100
baskets_with_coupon = (baskets['coupon_discount'] < 0).mean() * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.0), constrained_layout=True)

categories = ['Giảm giá niêm yết tại quầy\n(RETAIL_DISC - Siêu thị)', 'Giảm giá coupon\n(COUPON_DISC - Nhà sản xuất)']
disc_values = [total_retail_disc / 1e6, total_coupon_disc / 1e6]
colors = ['#e6550d', '#31a354']

bars1 = ax1.bar(categories, disc_values, color=colors, edgecolor='black', width=0.45)
ax1.set_ylabel('Tổng ngân sách giảm giá (Triệu USD)', fontweight='bold')
ax1.set_title('Quy mô ngân sách chiết khấu', fontweight='bold', fontsize=12, pad=10)
ax1.set_ylim(0, 1.8)
ax1.text(0, disc_values[0] + 0.05, f'${total_retail_disc:,.2f}\n({total_retail_disc/gross_sales*100:.2f}% gross sales)', ha='center', fontweight='bold', fontsize=10.5)
ax1.text(1, disc_values[1] + 0.05, f'${total_coupon_disc:,.2f}\n({total_coupon_disc/gross_sales*100:.2f}% gross sales)', ha='center', fontweight='bold', fontsize=10.5)
ax1.text(0.5, 0.90, f'Giảm giá tại quầy lớn gấp {ratio_markdown_coupon:.1f} lần so với coupon', transform=ax1.transAxes, ha='center', fontsize=10.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.3', facecolor='#fee8c8', edgecolor='#e6550d'))

coverage_cats = ['Giỏ có giảm giá\ntại quầy', 'Giỏ có áp dụng\ncoupon']
cov_values = [baskets_with_retail, baskets_with_coupon]
bars2 = ax2.bar(coverage_cats, cov_values, color=colors, edgecolor='black', width=0.45)
ax2.set_ylabel('Tỷ lệ giỏ hàng áp dụng (%)', fontweight='bold')
ax2.set_title('Độ phủ trên giỏ hàng (n = 275,542 giỏ)', fontweight='bold', fontsize=12, pad=10)
ax2.set_ylim(0, 105)
ax2.text(0, cov_values[0] + 2.0, f'{cov_values[0]:.2f}%\n({int(len(baskets)*cov_values[0]/100):,} giỏ)', ha='center', fontweight='bold', fontsize=10.5)
ax2.text(1, cov_values[1] + 2.0, f'{cov_values[1]:.2f}%\n({int(len(baskets)*cov_values[1]/100):,} giỏ)', ha='center', fontweight='bold', fontsize=10.5)

fig.suptitle('Cấu trúc chiết khấu 2 tầng: Giảm giá niêm yết tại quầy vs Phiếu giảm giá coupon', fontsize=13, fontweight='bold')
plt.savefig(FIG_DIR / '20_markdown_vs_coupon_spend.png', dpi=150)
plt.close()
print("✅ Generated 20_markdown_vs_coupon_spend.png")


# ==============================================================================
# 13. APPENDIX 3: PRIVATE LABEL PENETRATION (21_private_label_penetration.png)
# ==============================================================================
sku_counts = df_prod['BRAND'].value_counts()
sku_priv_pct = sku_counts.get('Private', 0) / len(df_prod) * 100
sku_nat_pct = sku_counts.get('National', 0) / len(df_prod) * 100

trans_brand = df_trans[['PRODUCT_ID', 'SALES_VALUE', 'QUANTITY']].merge(df_prod[['PRODUCT_ID', 'BRAND']], on='PRODUCT_ID', how='inner')
brand_spend = trans_brand.groupby('BRAND', observed=False)['SALES_VALUE'].sum()
brand_units = trans_brand['BRAND'].value_counts()

spend_priv_pct = brand_spend.get('Private', 0) / brand_spend.sum() * 100
spend_nat_pct = brand_spend.get('National', 0) / brand_spend.sum() * 100

unit_priv_pct = brand_units.get('Private', 0) / brand_units.sum() * 100
unit_nat_pct = brand_units.get('National', 0) / brand_units.sum() * 100

fig, ax = plt.subplots(figsize=(10, 4.8), constrained_layout=True)
categories = ['Tỷ lệ mặt hàng (SKU share)', 'Tỷ lệ doanh thu (Spend share)', 'Tỷ lệ sản lượng (Unit share)']
private_shares = [sku_priv_pct, spend_priv_pct, unit_priv_pct]
national_shares = [sku_nat_pct, spend_nat_pct, unit_nat_pct]

y = np.arange(len(categories))
height = 0.45

p1 = ax.barh(y, private_shares, height, label='Nhãn hàng riêng (Private Label)', color='#2b8cbe', edgecolor='black')
p2 = ax.barh(y, national_shares, height, left=private_shares, label='Thương hiệu quốc gia (National Brand)', color='#fdae6b', edgecolor='black')

ax.set_xlabel('Tỷ trọng đóng góp (%)', fontweight='bold', fontsize=11)
ax.set_yticks(y)
ax.set_yticklabels(categories, fontweight='bold', fontsize=11)
ax.set_xlim(0, 100)
ax.set_title('Tỷ trọng đóng góp của nhãn hàng riêng vs thương hiệu quốc gia\n(Chỉ số doanh thu/SKU của Private Label đạt 1.86x, cao gấp 2.18 lần so với National Brand 0.85x)', fontsize=12, fontweight='bold', pad=12)
# Put legend outside top right to avoid covering the 85.0% bar label
ax.legend(bbox_to_anchor=(0.5, 1.15), loc='upper center', ncol=2, frameon=True, facecolor='white', fontsize=10)

for i in range(len(categories)):
    ax.text(private_shares[i] / 2, y[i], f'{private_shares[i]:.1f}%', ha='center', va='center', color='white', fontweight='bold', fontsize=11)
    ax.text(private_shares[i] + national_shares[i] / 2, y[i], f'{national_shares[i]:.1f}%', ha='center', va='center', color='black', fontweight='bold', fontsize=11)

plt.savefig(FIG_DIR / '21_private_label_penetration.png', dpi=150)
plt.close()
print("✅ Generated 21_private_label_penetration.png")


# ==============================================================================
# 14. APPENDIX 4: TEMPORAL DISTRIBUTION (COMBINED DAY MOD 7 & HOURLY)
# ==============================================================================
day_mod = baskets['DAY'] % 7
day_counts = day_mod.value_counts().sort_index()

hours = (df_trans.groupby(['household_key', 'BASKET_ID'])['TRANS_TIME'].first() // 100).value_counts().sort_index()
hours_11_18 = hours.loc[11:18].sum()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)

# Subplot 1: Day mod 7
days_labels = [f'Ngày {d}' for d in range(7)]
days_pcts = (day_counts / len(baskets)) * 100
bars1 = ax1.bar(days_labels, days_pcts, color='#3182bd', edgecolor='black', width=0.55)
ax1.axhline(100.0/7, color='gray', linestyle='--', label=f'Phân bổ đều ({100/7:.1f}%)')
ax1.set_ylabel('Tỷ lệ giỏ hàng (%)', fontweight='bold')
ax1.set_xlabel('Chỉ số chu kỳ ngày (DAY mod 7)', fontweight='bold')
ax1.set_title('Phân phối giỏ hàng theo chu kỳ 7 ngày\n(Đỉnh rơi vào Ngày 4 và Ngày 5: ~16% mỗi ngày)', fontweight='bold', fontsize=11.5)
ax1.set_ylim(0, 22)
ax1.legend(loc='upper left', frameon=True, facecolor='white')

for bar in bars1:
    h = bar.get_height()
    ax1.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=9.5, fontweight='bold')

# Subplot 2: Hourly
h_x = np.arange(24)
h_y = [hours.get(h, 0) / len(baskets) * 100 for h in h_x]
colors_h = ['#fdae6b' if 11 <= h <= 18 else '#9ecae1' for h in h_x]
bars2 = ax2.bar(h_x, h_y, color=colors_h, edgecolor='black', width=0.7)
ax2.set_xlabel('Khung giờ trong ngày (0h - 23h)', fontweight='bold')
ax2.set_ylabel('Tỷ lệ giỏ hàng (%)', fontweight='bold')
ax2.set_title(f'Phân phối giỏ hàng theo khung giờ\n(Khung 11h - 18h chiếm {hours_11_18/len(baskets)*100:.1f}% tổng số giỏ)', fontweight='bold', fontsize=11.5)
ax2.set_xticks(range(0, 24, 2))
ax2.set_ylim(0, 13)

plt.savefig(FIG_DIR / '03_temporal_combined_rhythm.png', dpi=150)
plt.close()
print("✅ Generated 03_temporal_combined_rhythm.png")

print("🎉 All standardized figures generated successfully!")
