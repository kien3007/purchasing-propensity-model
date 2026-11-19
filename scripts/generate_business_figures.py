# -*- coding: utf-8 -*-
"""
Script to generate the high-impact visual figures for the Business Strategy track:
1. 22_rfm_customer_segmentation.png: RFM Customer Tiers (% Households vs % Revenue Share, AOV)
2. 23_department_performance_matrix.png: Top 10 Departments (Revenue, Basket Penetration, Category Spend)
3. 24_basket_category_breadth_aov.png: Multi-category Basket Affinity & AOV Multiplier
4. 25_private_label_by_department.png: Private Label Revenue Share across Departments
5. 26_demographics_family_basket_spend.png: Spend & AOV by Household Size & Kids Category
"""

import sys
sys.path.append('.')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import duckdb
from pathlib import Path

from src.data.loader import DataLoader

FIG_DIR = Path('docs/reports/figures')
FIG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#e5e5e5'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

print("🚀 Loading data for business figures...")
data = DataLoader.load_all()
df_trans = data['transactions']
df_prod = data['products']
df_demo = data['demographics']
baskets = DataLoader.build_trip_level_baskets(df_trans, df_prod)

con = duckdb.connect()
con.register('df_trans', df_trans)
con.register('df_prod', df_prod)
con.register('df_demo', df_demo)
con.register('baskets', baskets)

# ==============================================================================
# 1. 22_rfm_customer_segmentation.png
# ==============================================================================
def generate_rfm_figure():
    q_rfm = """
    WITH hh_stats AS (
        SELECT 
            household_key,
            MAX(DAY) AS max_day,
            COUNT(DISTINCT BASKET_ID) AS total_baskets,
            SUM(basket_spend) AS total_spend,
            AVG(basket_spend) AS avg_spend_per_basket
        FROM baskets
        GROUP BY household_key
    )
    SELECT 
        household_key,
        (711 - max_day) AS recency_days,
        total_baskets AS frequency,
        total_spend AS monetary,
        avg_spend_per_basket AS aov
    FROM hh_stats
    """
    df_rfm = con.execute(q_rfm).df()

    def assign_tier(row):
        r, f, m = row['recency_days'], row['frequency'], row['monetary']
        if m >= 4500 and r <= 14 and f >= 80:
            return 'VIP / Champions'
        elif f >= 40 and r <= 30:
            return 'Thân thiết (Loyal)'
        elif r <= 14:
            return 'Tiềm năng (Promising)'
        elif m >= 2500 and r > 30:
            return 'Nguy cơ rời bỏ (At-Risk)'
        elif r > 60:
            return 'Ngủ đông (Dormant)'
        else:
            return 'Vãng lai (Attention)'

    df_rfm['segment'] = df_rfm.apply(assign_tier, axis=1)
    seg = df_rfm.groupby('segment').agg(
        hh_count=('household_key', 'count'),
        total_spend=('monetary', 'sum'),
        avg_aov=('aov', 'mean'),
        avg_rec=('recency_days', 'mean')
    ).reset_index()

    tot_hh = len(df_rfm)
    tot_rev = df_rfm['monetary'].sum()
    seg['hh_pct'] = seg['hh_count'] * 100.0 / tot_hh
    seg['spend_pct'] = seg['total_spend'] * 100.0 / tot_rev

    order = ['VIP / Champions', 'Thân thiết (Loyal)', 'Vãng lai (Attention)', 
             'Nguy cơ rời bỏ (At-Risk)', 'Tiềm năng (Promising)', 'Ngủ đông (Dormant)']
    seg['order'] = seg['segment'].map(lambda x: order.index(x) if x in order else 99)
    seg = seg.sort_values('order').reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10.5, 4.8), constrained_layout=True)
    x = np.arange(len(seg))
    width = 0.38

    b1 = ax.bar(x - width/2, seg['hh_pct'], width, label='Tỷ lệ số hộ trong Panel (%)', color='#2b5c8f', alpha=0.9)
    b2 = ax.bar(x + width/2, seg['spend_pct'], width, label='Tỷ lệ đóng góp Doanh thu (%)', color='#d95f02', alpha=0.9)

    for bar in b1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.8, f"{h:.1f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#2b5c8f')
    for bar in b2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.8, f"{h:.1f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#d95f02')

    # Annotate AOV and Recency badges below x labels
    labels = [f"{row['segment']}\nAOV: ${row['avg_aov']:.0f} | Trễ: {row['avg_rec']:.0f}d" for _, row in seg.iterrows()]
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8.8, fontweight='medium')
    ax.set_ylim(0, 65)
    ax.set_ylabel("Tỷ lệ (%)", fontsize=11, fontweight='bold')
    ax.set_title("Phân khúc giá trị khách hàng RFM & Đóng góp doanh thu thực tế (2,500 Hộ)", fontsize=12.5, fontweight='bold', pad=12)
    ax.legend(frameon=True, facecolor='white', loc='upper right', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5, axis='y')

    plt.savefig(FIG_DIR / '22_rfm_customer_segmentation.png', dpi=160)
    plt.close()
    print("✅ Generated 22_rfm_customer_segmentation.png")

# ==============================================================================
# 2. 23_department_performance_matrix.png
# ==============================================================================
def generate_dept_matrix_figure():
    q_dept = """
    WITH dept_trans AS (
        SELECT 
            p.DEPARTMENT,
            t.BASKET_ID,
            t.SALES_VALUE
        FROM df_trans t
        JOIN df_prod p ON t.PRODUCT_ID = p.PRODUCT_ID
        WHERE t.SALES_VALUE > 0
    ),
    tot_b AS (
        SELECT COUNT(DISTINCT BASKET_ID) AS n_baskets FROM df_trans WHERE SALES_VALUE > 0
    )
    SELECT 
        d.DEPARTMENT,
        COUNT(DISTINCT d.BASKET_ID) * 100.0 / (SELECT n_baskets FROM tot_b) AS penetration_pct,
        SUM(d.SALES_VALUE) / 1e3 AS revenue_k,
        SUM(d.SALES_VALUE) * 100.0 / (SELECT SUM(SALES_VALUE) FROM df_trans WHERE SALES_VALUE > 0) AS rev_share_pct,
        SUM(d.SALES_VALUE) / COUNT(DISTINCT d.BASKET_ID) AS dept_aov
    FROM dept_trans d
    GROUP BY d.DEPARTMENT
    ORDER BY revenue_k DESC
    LIMIT 8;
    """
    df_d = con.execute(q_dept).df()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8), constrained_layout=True)

    # Panel A: Revenue Share vs Basket Penetration
    y_pos = np.arange(len(df_d))
    ax1.barh(y_pos - 0.2, df_d['rev_share_pct'], height=0.38, color='#2b5c8f', label='Tỷ trọng Doanh thu (%)')
    ax1.barh(y_pos + 0.2, df_d['penetration_pct'], height=0.38, color='#31a354', label='Tỷ lệ thâm nhập Giỏ hàng (%)')
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(df_d['DEPARTMENT'], fontsize=10, fontweight='bold')
    ax1.invert_yaxis()
    ax1.set_xlabel("Tỷ lệ (%)", fontsize=10.5, fontweight='bold')
    ax1.set_title("A. Doanh thu vs Độ phủ giỏ hàng (Top 8 Ngành)", fontsize=11.5, fontweight='bold', pad=10)
    ax1.legend(loc='lower right', fontsize=9.5, frameon=True, facecolor='white')
    ax1.grid(True, linestyle='--', alpha=0.5, axis='x')

    # Panel B: Category AOV (Dept spend per trip)
    bars = ax2.bar(df_d['DEPARTMENT'], df_d['dept_aov'], color='#d95f02', width=0.55, edgecolor='#8c2d04', lw=1.1)
    ax2.set_xticks(range(len(df_d)))
    ax2.set_xticklabels(df_d['DEPARTMENT'], rotation=35, ha='right', fontsize=9.5, fontweight='bold')
    ax2.set_ylabel("Chi tiêu trung bình mỗi chuyến ($ USD)", fontsize=10.5, fontweight='bold')
    ax2.set_title("B. Giá trị giỏ ngành hàng (Category Basket Size)", fontsize=11.5, fontweight='bold', pad=10)
    ax2.grid(True, linestyle='--', alpha=0.5, axis='y')
    for b in bars:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 0.5, f"${h:.1f}", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#8c2d04')
    ax2.set_ylim(0, 30)

    plt.savefig(FIG_DIR / '23_department_performance_matrix.png', dpi=160)
    plt.close()
    print("✅ Generated 23_department_performance_matrix.png")

# ==============================================================================
# 3. 24_basket_category_breadth_aov.png
# ==============================================================================
def generate_basket_breadth_figure():
    q_b = """
    WITH b_dept AS (
        SELECT 
            t.BASKET_ID,
            SUM(t.SALES_VALUE) AS basket_spend,
            COUNT(DISTINCT p.DEPARTMENT) AS num_depts
        FROM df_trans t
        JOIN df_prod p ON t.PRODUCT_ID = p.PRODUCT_ID
        WHERE t.SALES_VALUE > 0
        GROUP BY t.BASKET_ID
    )
    SELECT 
        CASE 
            WHEN num_depts = 1 THEN '1 ngành hàng\\n(Đơn lẻ)'
            WHEN num_depts = 2 THEN '2 ngành hàng'
            WHEN num_depts <= 4 THEN '3 - 4 ngành hàng'
            WHEN num_depts <= 7 THEN '5 - 7 ngành hàng'
            ELSE '≥ 8 ngành\\n(Đại siêu thị)'
        END AS dept_tier,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM b_dept) AS basket_share_pct,
        AVG(basket_spend) AS avg_aov,
        SUM(basket_spend) * 100.0 / (SELECT SUM(basket_spend) FROM b_dept) AS spend_share_pct
    FROM b_dept
    GROUP BY 1
    ORDER BY avg_aov ASC;
    """
    df_b = con.execute(q_b).df()

    fig, ax1 = plt.subplots(figsize=(10.5, 4.8), constrained_layout=True)
    x = np.arange(len(df_b))

    color_aov = '#d95f02'
    bars = ax1.bar(x, df_b['avg_aov'], width=0.48, color=color_aov, alpha=0.9, edgecolor='#8c2d04', lw=1.2, label='AOV Giá trị giỏ hàng ($ USD)')
    ax1.set_ylabel("Giá trị giỏ hàng trung bình AOV ($ USD)", fontsize=11, fontweight='bold', color=color_aov)
    ax1.tick_params(axis='y', labelcolor=color_aov)
    ax1.set_ylim(0, 175)

    for b in bars:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, h + 3.0, f"${h:.1f}", ha='center', va='bottom', fontsize=10.5, fontweight='bold', color=color_aov)

    # Line for Spend share
    ax2 = ax1.twinx()
    color_share = '#2b5c8f'
    ax2.plot(x, df_b['spend_share_pct'], color=color_share, marker='o', linewidth=2.5, markersize=8, label='Tỷ trọng Đóng góp Doanh thu (%)')
    ax2.set_ylabel("Tỷ trọng Doanh thu tích lũy (%)", fontsize=11, fontweight='bold', color=color_share)
    ax2.tick_params(axis='y', labelcolor=color_share)
    ax2.set_ylim(0, 45)
    ax2.grid(False)

    for i, (_, row) in enumerate(df_b.iterrows()):
        ax2.annotate(f"{row['spend_share_pct']:.1f}% DT\n({row['basket_share_pct']:.1f}% Giỏ)",
                     xy=(i, row['spend_share_pct']), xytext=(i, row['spend_share_pct'] + 4.5),
                     ha='center', fontsize=9.0, fontweight='bold', color=color_share,
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#f0f4f8', edgecolor=color_share, lw=0.8))

    ax1.set_xticks(x)
    ax1.set_xticklabels(df_b['dept_tier'], fontsize=10, fontweight='bold')
    ax1.set_title("Sức mạnh của Giỏ hàng đa ngành: AOV tăng gấp 12 lần khi mua chéo ngành hàng", fontsize=12.5, fontweight='bold', pad=12)
    ax1.grid(True, linestyle='--', alpha=0.5, axis='y')

    plt.savefig(FIG_DIR / '24_basket_category_breadth_aov.png', dpi=160)
    plt.close()
    print("✅ Generated 24_basket_category_breadth_aov.png")

# ==============================================================================
# 4. 25_private_label_by_department.png
# ==============================================================================
def generate_pl_department_figure():
    q_pl = """
    SELECT 
        p.DEPARTMENT,
        SUM(CASE WHEN p.BRAND = 'Private' THEN t.SALES_VALUE ELSE 0 END) * 100.0 / SUM(t.SALES_VALUE) AS pl_spend_pct,
        SUM(CASE WHEN p.BRAND = 'Private' THEN t.QUANTITY ELSE 0 END) * 100.0 / SUM(t.QUANTITY) AS pl_units_pct,
        SUM(t.SALES_VALUE) / 1e3 AS rev_k
    FROM df_trans t
    JOIN df_prod p ON t.PRODUCT_ID = p.PRODUCT_ID
    WHERE t.SALES_VALUE > 0 AND p.DEPARTMENT IN ('PASTRY', 'GROCERY', 'DELI', 'MEAT-PCKGD', 'PRODUCE', 'DRUG GM', 'MEAT')
    GROUP BY p.DEPARTMENT
    ORDER BY pl_spend_pct DESC;
    """
    df_pl = con.execute(q_pl).df()

    fig, ax = plt.subplots(figsize=(10.0, 4.6), constrained_layout=True)
    y = np.arange(len(df_pl))
    height = 0.36

    b1 = ax.barh(y - height/2, df_pl['pl_spend_pct'], height, label='Tỷ trọng Doanh thu Nhãn riêng (%)', color='#d95f02', alpha=0.9)
    b2 = ax.barh(y + height/2, df_pl['pl_units_pct'], height, label='Tỷ trọng Sản lượng Tiêu thụ (%)', color='#2b5c8f', alpha=0.9)

    ax.set_yticks(y)
    ax.set_yticklabels(df_pl['DEPARTMENT'], fontsize=10.5, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlim(0, 65)
    ax.set_xlabel("Tỷ trọng của Nhãn hàng riêng trong ngành (%)", fontsize=10.5, fontweight='bold')
    ax.set_title("Thâm nhập của Nhãn hàng riêng (Private Label) theo từng ngành hàng chủ lực", fontsize=12.5, fontweight='bold', pad=12)
    ax.legend(loc='lower right', fontsize=10, frameon=True, facecolor='white')
    ax.grid(True, linestyle='--', alpha=0.5, axis='x')

    for bar in b1:
        w = bar.get_width()
        ax.text(w + 1.0, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va='center', fontsize=9.5, fontweight='bold', color='#d95f02')
    for bar in b2:
        w = bar.get_width()
        ax.text(w + 1.0, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va='center', fontsize=9.5, fontweight='bold', color='#2b5c8f')

    plt.savefig(FIG_DIR / '25_private_label_by_department.png', dpi=160)
    plt.close()
    print("✅ Generated 25_private_label_by_department.png")

# ==============================================================================
# 5. 26_demographics_family_basket_spend.png
# ==============================================================================
def generate_demographics_family_figure():
    q_size = """
    SELECT 
        d.classification_4 AS hh_size,
        COUNT(DISTINCT t.household_key) AS hh_count,
        SUM(t.SALES_VALUE) / COUNT(DISTINCT t.household_key) AS spend_per_hh,
        SUM(t.SALES_VALUE) / COUNT(DISTINCT t.BASKET_ID) AS aov
    FROM df_trans t
    JOIN df_demo d ON t.household_key = d.household_key
    WHERE t.SALES_VALUE > 0
    GROUP BY 1
    ORDER BY CASE hh_size WHEN '1' THEN 1 WHEN '2' THEN 2 WHEN '3' THEN 3 WHEN '4' THEN 4 ELSE 5 END;
    """
    df_s = con.execute(q_size).df()

    q_kids = """
    SELECT 
        d.KID_CATEGORY_DESC AS kid_cat,
        COUNT(DISTINCT t.household_key) AS hh_count,
        SUM(t.SALES_VALUE) / COUNT(DISTINCT t.household_key) AS spend_per_hh,
        SUM(t.SALES_VALUE) / COUNT(DISTINCT t.BASKET_ID) AS aov
    FROM df_trans t
    JOIN df_demo d ON t.household_key = d.household_key
    WHERE t.SALES_VALUE > 0
    GROUP BY 1
    ORDER BY CASE kid_cat WHEN 'None/Unknown' THEN 1 WHEN '1' THEN 2 WHEN '2' THEN 3 ELSE 4 END;
    """
    df_k = con.execute(q_kids).df()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6), constrained_layout=True)

    # Panel A: HH Size
    size_labels = [f"{s} người" if s != '5+' else "≥ 5 người" for s in df_s['hh_size']]
    bars1 = ax1.bar(size_labels, df_s['aov'], color='#3182bd', width=0.52, edgecolor='#08519c', lw=1.1)
    ax1.set_ylabel("Giá trị giỏ hàng AOV ($ USD)", fontsize=10.5, fontweight='bold')
    ax1.set_title("A. AOV theo Quy mô hộ gia đình", fontsize=11.5, fontweight='bold', pad=10)
    ax1.grid(True, linestyle='--', alpha=0.5, axis='y')
    ax1.set_ylim(0, 52)
    for b, s_val in zip(bars1, df_s['spend_per_hh']):
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, h + 1.0, f"${h:.1f}\n(${s_val:,.0f}/năm)", ha='center', va='bottom', fontsize=9.0, fontweight='bold', color='#08519c')

    # Panel B: Kids Category
    kid_labels = ['Không có', '1 trẻ', '2 trẻ', '≥ 3 trẻ']
    bars2 = ax2.bar(kid_labels, df_k['aov'], color='#756bb1', width=0.52, edgecolor='#54278f', lw=1.1)
    ax2.set_ylabel("Giá trị giỏ hàng AOV ($ USD)", fontsize=10.5, fontweight='bold')
    ax2.set_title("B. AOV theo Số lượng trẻ em trong hộ", fontsize=11.5, fontweight='bold', pad=10)
    ax2.grid(True, linestyle='--', alpha=0.5, axis='y')
    ax2.set_ylim(0, 52)
    for b, s_val in zip(bars2, df_k['spend_per_hh']):
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 1.0, f"${h:.1f}\n(${s_val:,.0f}/năm)", ha='center', va='bottom', fontsize=9.0, fontweight='bold', color='#54278f')

    plt.savefig(FIG_DIR / '26_demographics_family_basket_spend.png', dpi=160)
    plt.close()
    print("✅ Generated 26_demographics_family_basket_spend.png")

if __name__ == '__main__':
    generate_rfm_figure()
    generate_dept_matrix_figure()
    generate_basket_breadth_figure()
    generate_pl_department_figure()
    generate_demographics_family_figure()
    print("🎉 All business strategy figures generated successfully!")
