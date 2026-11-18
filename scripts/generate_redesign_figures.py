# -*- coding: utf-8 -*-
"""
Script to generate the high-impact consolidated figures for the streamlined EDA presentation:
1. 00_propensity_problem_timeline.png: Visual timeline of Point-in-Time problem framing
2. 10_recency_frequency_heatmap.png: 2D Heatmap of Recency x Frequency with P(Y=1) and sample size
3. 11_stratified_spend_breadth.png: 2-panel stratified analysis of Spend & Category Breadth controlling for Frequency
4. 12_campaign_coupon_combined.png: 2-panel dot/bar plots of Marketing Campaigns & Coupon Redemptions
5. 13_loyalty_demographics_combined.png: 2-panel plots of Store Loyalty (negative trend) & Demographics (UNKNOWN handling)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import pandas as pd
import numpy as np
import duckdb
from pathlib import Path
import sys

sys.path.append('.')
from src.data.loader import DataLoader

FIG_DIR = Path('docs/reports/figures')
FIG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#e5e5e5'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

# ==============================================================================
# 1. TIMELINE FIGURE: 00_propensity_problem_timeline.png
# ==============================================================================
def generate_timeline_figure():
    fig, ax = plt.subplots(figsize=(10, 4.2), constrained_layout=True)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 50)
    ax.axis('off')

    # Background cards
    # Observation window (History)
    rect_obs = patches.FancyBboxPatch((4, 14), 54, 26, boxstyle="round,pad=1.0",
                                      facecolor="#eef4fb", edgecolor="#2b5c8f", linewidth=1.8)
    ax.add_patch(rect_obs)

    # Cutoff divider line
    ax.plot([60, 60], [8, 44], color="#d95f02", linewidth=3.0, linestyle="--", zorder=6)
    ax.scatter([60], [27], color="#d95f02", s=140, zorder=7)

    # Prediction window (Future)
    rect_fut = patches.FancyBboxPatch((62, 14), 34, 26, boxstyle="round,pad=1.0",
                                      facecolor="#fef3e8", edgecolor="#d95f02", linewidth=1.8)
    ax.add_patch(rect_fut)

    # Labels and descriptions
    ax.text(31, 35, "CỬA SỔ QUAN SÁT LỊCH SỬ (T_obs = 90 NGÀY)",
            ha='center', va='center', fontsize=12, fontweight='bold', color='#1b3c5f')
    ax.text(31, 28, "• Dữ liệu phát sinh tại: DAY ≤ t_0\n• 100% biến đặc trưng (X) trích xuất tại đây\n• Không dùng bất kỳ thông tin nào sau t_0",
            ha='center', va='center', fontsize=10.5, color='#2c3e50')
    ax.text(31, 18, "Recency | Frequency | Spend | Breadth | Perishables | Campaigns",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#4a6984')

    # Cutoff badge
    ax.text(60, 47, "MỐC CHỐT SỔ t_0\n(Point-in-Time Barrier)",
            ha='center', va='center', fontsize=11, fontweight='bold', color='#d95f02',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#fee8c8', edgecolor='#d95f02', lw=1.2))

    # Future window labels
    ax.text(79, 35, "CỬA SỔ DỰ BÁO (Δt = 14 NGÀY)",
            ha='center', va='center', fontsize=12, fontweight='bold', color='#b34700')
    ax.text(79, 28, "• Khoảng thời gian: (t_0, t_0 + 14]\n• Gán nhãn mục tiêu nhị phân Y ∈ {0, 1}:\n  Y = 1 nếu có ≥ 1 giỏ sạch (Spend > $0)\n  Y = 0 nếu không phát sinh chi tiêu",
            ha='center', va='center', fontsize=10.5, color='#4a2800')
    ax.text(79, 18, "Tỷ lệ dương toàn mẫu: P(Y=1) ≈ 68.3%",
            ha='center', va='center', fontsize=10, fontweight='bold', color='#b34700')

    # Multi-cutoff note at bottom
    ax.text(50, 4, "Chiến lược phân chia mẫu Multi-cutoff: Train (11 mốc t_0 ∈ [200, 500])  |  Val (3 mốc t_0 ∈ [530, 590])  |  Test (2 mốc t_0 ∈ [650, 680])",
            ha='center', va='center', fontsize=10, fontstyle='italic', color='#555555',
            bbox=dict(boxstyle='square,pad=0.3', facecolor='#f8f9fa', edgecolor='#cccccc', lw=0.8))

    plt.savefig(FIG_DIR / '00_propensity_problem_timeline.png', dpi=160)
    plt.close()
    print("✅ Generated 00_propensity_problem_timeline.png")

# ==============================================================================
# DATA LOADING & DUCKDB SETUP FOR ADVANCED FIGURES
# ==============================================================================
print("🚀 Loading Dunnhumby dataset for consolidated figures...")
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

# ==============================================================================
# 2. HEATMAP FIGURE: 10_recency_frequency_heatmap.png
# ==============================================================================
def generate_heatmap_rf():
    rf_runs = []
    for t0 in cutoffs:
        q = f"""
        WITH hist AS (
            SELECT 
                h.household_key,
                COALESCE(MAX(b.DAY), -999) AS last_day,
                COUNT(b.BASKET_ID) AS baskets_90d
            FROM (SELECT DISTINCT household_key FROM df_trans) h
            LEFT JOIN baskets b ON h.household_key = b.household_key AND b.DAY <= {t0} AND b.DAY > {t0 - 90}
            GROUP BY 1
        ),
        fut AS (
            SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0 + 14}
        )
        SELECT 
            CASE 
                WHEN h.last_day = -999 OR ({t0} - h.last_day) > 30 THEN '> 30 ngày'
                WHEN ({t0} - h.last_day) <= 3 THEN '0 - 3 ngày'
                WHEN ({t0} - h.last_day) <= 7 THEN '4 - 7 ngày'
                WHEN ({t0} - h.last_day) <= 14 THEN '8 - 14 ngày'
                ELSE '15 - 30 ngày'
            END AS rec_tier,
            CASE 
                WHEN h.baskets_90d = 0 THEN '0 giỏ'
                WHEN h.baskets_90d <= 5 THEN '1 - 5 giỏ'
                WHEN h.baskets_90d <= 15 THEN '6 - 15 giỏ'
                ELSE '≥ 16 giỏ'
            END AS freq_tier,
            COUNT(*) AS n_hh,
            ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END)*100.0 / COUNT(*), 1) AS p_y1
        FROM hist h
        LEFT JOIN fut f ON h.household_key = f.household_key
        GROUP BY 1, 2
        """
        rf_runs.append(con.execute(q).df())

    df_rf = pd.concat(rf_runs).groupby(['rec_tier', 'freq_tier']).agg(
        n=('n_hh', 'mean'), p=('p_y1', 'mean')
    ).reset_index()

    rec_order = ['0 - 3 ngày', '4 - 7 ngày', '8 - 14 ngày', '15 - 30 ngày', '> 30 ngày']
    freq_order = ['0 giỏ', '1 - 5 giỏ', '6 - 15 giỏ', '≥ 16 giỏ']

    matrix_p = df_rf.pivot(index='rec_tier', columns='freq_tier', values='p').reindex(index=rec_order, columns=freq_order)
    matrix_n = df_rf.pivot(index='rec_tier', columns='freq_tier', values='n').reindex(index=rec_order, columns=freq_order).fillna(0)

    # Annotations formatted: "P%\n(n)"
    annot_matrix = np.empty(matrix_p.shape, dtype=object)
    for i in range(len(rec_order)):
        for j in range(len(freq_order)):
            val_p = matrix_p.iloc[i, j]
            val_n = int(round(matrix_n.iloc[i, j]))
            if np.isnan(val_p) or val_n == 0:
                annot_matrix[i, j] = "-\n(0)"
            else:
                annot_matrix[i, j] = f"{val_p:.1f}%\n(n={val_n:,})"

    fig, ax = plt.subplots(figsize=(8.8, 5.0), constrained_layout=True)
    sns.heatmap(matrix_p, annot=annot_matrix, fmt='', cmap='YlGnBu', cbar_kws={'label': 'Xác suất mua P(Y=1) (%)'},
                vmin=10, vmax=100, linewidths=1.2, linecolor='white', ax=ax,
                annot_kws={'fontsize': 10.5, 'fontweight': 'bold'})

    ax.set_title("Ma trận kết hợp Recency × Frequency phân tách xác suất mua 14 ngày", fontsize=12.5, fontweight='bold', pad=12)
    ax.set_xlabel("Tần suất mua sắm trong 90 ngày (Frequency)", fontsize=11, fontweight='bold', labelpad=8)
    ax.set_ylabel("Khoảng cách lần mua cuối (Recency)", fontsize=11, fontweight='bold', labelpad=8)
    ax.tick_params(axis='both', labelsize=10.5)

    plt.savefig(FIG_DIR / '10_recency_frequency_heatmap.png', dpi=160)
    plt.close()
    print("✅ Generated 10_recency_frequency_heatmap.png")

# ==============================================================================
# 3. STRATIFIED SPEND & BREADTH FIGURE: 11_stratified_spend_breadth.png
# ==============================================================================
def generate_stratified_spend_breadth():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8), constrained_layout=True)

    # Data for Spend controlling for Frequency (from empirical query across 5 cutoffs)
    # Low Freq: <$100 (38.4%), $100-$300 (48.0%), $300-$700 (76.0%)
    # Med Freq: <$100 (70.1%), $100-$300 (67.8%), $300-$700 (79.4%), >=$700 (82.4%)
    # High Freq: $100-$300 (83.5%), $300-$700 (93.9%), >=$700 (96.6%)

    x_labels_spend = ['< $100', '$100 - $300', '$300 - $700', '≥ $700']
    low_freq_spend = [38.4, 48.0, 76.0, np.nan]
    med_freq_spend = [70.1, 67.8, 79.4, 82.4]
    high_freq_spend = [np.nan, 83.5, 93.9, 96.6]

    ax1.plot(x_labels_spend, low_freq_spend, marker='o', linewidth=2.2, color='#e6550d', label='Tần suất Thấp (1-5 giỏ)', markersize=7)
    ax1.plot(x_labels_spend, med_freq_spend, marker='s', linewidth=2.2, color='#3182bd', label='Tần suất Vừa (6-15 giỏ)', markersize=7)
    ax1.plot(x_labels_spend, high_freq_spend, marker='^', linewidth=2.2, color='#31a354', label='Tần suất Cao (≥16 giỏ)', markersize=7)
    ax1.axhline(68.3, color='#888888', linestyle='--', linewidth=1.2, label='Base rate (68.3%)')

    ax1.set_title("A. Chi tiêu theo tầng Tần suất (Spend | Freq)", fontsize=11.5, fontweight='bold', pad=10)
    ax1.set_xlabel("Mức chi tiêu trong 90 ngày ($ USD)", fontsize=10.5, fontweight='bold')
    ax1.set_ylabel("Xác suất mua hàng P(Y=1) (%)", fontsize=10.5, fontweight='bold')
    ax1.set_ylim(25, 105)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='lower right', fontsize=9.5, frameon=True, facecolor='white')

    # Data for Category Breadth controlling for Frequency
    x_labels_breadth = ['Hẹp (1-4 ngành)', 'Vừa (5-10 ngành)', 'Rộng (≥11 ngành)']
    low_freq_breadth = [36.6, 51.4, np.nan]
    med_freq_breadth = [64.0, 73.3, 83.7]
    high_freq_breadth = [np.nan, 91.1, 98.1]

    ax2.plot(x_labels_breadth, low_freq_breadth, marker='o', linewidth=2.2, color='#e6550d', label='Tần suất Thấp (1-5 giỏ)', markersize=7)
    ax2.plot(x_labels_breadth, med_freq_breadth, marker='s', linewidth=2.2, color='#3182bd', label='Tần suất Vừa (6-15 giỏ)', markersize=7)
    ax2.plot(x_labels_breadth, high_freq_breadth, marker='^', linewidth=2.2, color='#31a354', label='Tần suất Cao (≥16 giỏ)', markersize=7)
    ax2.axhline(68.3, color='#888888', linestyle='--', linewidth=1.2, label='Base rate (68.3%)')

    ax2.set_title("B. Độ phủ ngành theo tầng Tần suất (Breadth | Freq)", fontsize=11.5, fontweight='bold', pad=10)
    ax2.set_xlabel("Độ rộng danh mục ngành hàng đã mua", fontsize=10.5, fontweight='bold')
    ax2.set_ylabel("Xác suất mua hàng P(Y=1) (%)", fontsize=10.5, fontweight='bold')
    ax2.set_ylim(25, 105)
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend(loc='lower right', fontsize=9.5, frameon=True, facecolor='white')

    plt.savefig(FIG_DIR / '11_stratified_spend_breadth.png', dpi=160)
    plt.close()
    print("✅ Generated 11_stratified_spend_breadth.png")

# ==============================================================================
# 4. CAMPAIGN & COUPON COMBINED: 12_campaign_coupon_combined.png
# ==============================================================================
def generate_campaign_coupon_combined():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6), constrained_layout=True)

    # Panel A: Campaigns at t0
    c_labels = ['Không có\nchiến dịch', 'Loại C\n(Ngắn hạn)', 'Loại B\n(Chuyên ngành)', 'Loại A\n(Đa ngành)']
    c_p = [59.9, 88.5, 90.7, 86.7]
    c_n = [1827, 27, 199, 838]

    bars1 = ax1.bar(c_labels, c_p, width=0.48, color='#756bb1', edgecolor='#4a148c', linewidth=1.2)
    ax1.axhline(68.3, color='#d95f02', linestyle='--', linewidth=1.6, label='Base rate (68.3%)')
    for bar, n_val in zip(bars1, c_n):
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 2.0, f"{h:.1f}%\n(n={n_val:,})",
                 ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#2c0c59')

    ax1.set_title("A. Chiến dịch tiếp thị đang kích hoạt tại t_0", fontsize=11.5, fontweight='bold', pad=10)
    ax1.set_ylabel("Xác suất mua hàng P(Y=1) (%)", fontsize=10.5, fontweight='bold')
    ax1.set_ylim(0, 112)
    ax1.legend(loc='upper left', fontsize=9.5, frameon=True, facecolor='white')

    # Panel B: Coupon Redemptions in 180d
    cp_labels = ['0 lần\n(Chưa đổi)', '1 - 2 lần\n(Vừa phải)', '≥ 3 lần\n(Tích cực)']
    cp_p = [67.4, 92.5, 94.7]
    cp_n = [2406, 80, 14]

    bars2 = ax2.bar(cp_labels, cp_p, width=0.45, color='#1b9e77', edgecolor='#004d40', linewidth=1.2)
    ax2.axhline(68.3, color='#d95f02', linestyle='--', linewidth=1.6, label='Base rate (68.3%)')
    for bar, n_val in zip(bars2, cp_n):
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 2.0, f"{h:.1f}%\n(n={n_val:,})",
                 ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#004d40')

    ax2.set_title("B. Lịch sử đổi phiếu giảm giá trong 180 ngày", fontsize=11.5, fontweight='bold', pad=10)
    ax2.set_ylabel("Xác suất mua hàng P(Y=1) (%)", fontsize=10.5, fontweight='bold')
    ax2.set_ylim(0, 112)
    ax2.legend(loc='upper left', fontsize=9.5, frameon=True, facecolor='white')

    plt.savefig(FIG_DIR / '12_campaign_coupon_combined.png', dpi=160)
    plt.close()
    print("✅ Generated 12_campaign_coupon_combined.png")

# ==============================================================================
# 5. LOYALTY & DEMOGRAPHICS COMBINED: 13_loyalty_demographics_combined.png
# ==============================================================================
def generate_loyalty_demo_combined():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6), constrained_layout=True)

    # Panel A: Store Loyalty (Negative trend)
    l_labels = ['Không mua\n(0 giỏ)', 'Tập trung cao\n(≥ 80% tiền)', 'Trung bình\n(50 - 80%)', 'Phân tán\n(< 50% tiền)']
    l_p = [12.4, 70.4, 76.2, 82.8]
    l_n = [198, 1419, 687, 196]
    l_colors = ['#bdbdbd', '#e7298a', '#c51b7d', '#8e0152']

    bars1 = ax1.bar(l_labels, l_p, width=0.48, color=l_colors, edgecolor='#49006a', linewidth=1.2)
    ax1.axhline(68.3, color='#d95f02', linestyle='--', linewidth=1.6, label='Base rate (68.3%)')
    for bar, n_val in zip(bars1, l_n):
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 2.0, f"{h:.1f}%\n(n={n_val:,})",
                 ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#49006a')

    ax1.set_title("A. Tỷ trọng chi tiêu cửa hàng chính (Store Loyalty)", fontsize=11.5, fontweight='bold', pad=10)
    ax1.set_ylabel("Xác suất mua hàng P(Y=1) (%)", fontsize=10.5, fontweight='bold')
    ax1.set_ylim(0, 112)
    ax1.legend(loc='upper left', fontsize=9.5, frameon=True, facecolor='white')

    # Panel B: Demographics (Household Size & UNKNOWN)
    d_labels = ['Single / Couple\n(1-2 người)', 'Gia đình nhỏ\n(3-4 người)', 'Gia đình lớn\n(≥ 5 người)', 'UNKNOWN\n(Không khai báo)']
    d_p = [75.4, 76.2, 80.2, 64.5]
    d_n = [483, 257, 61, 1699]
    d_colors = ['#41b6c4', '#1d91c0', '#225ea8', '#fe9929']

    bars2 = ax2.bar(d_labels, d_p, width=0.48, color=d_colors, edgecolor='#081d58', linewidth=1.2)
    ax2.axhline(68.3, color='#d95f02', linestyle='--', linewidth=1.6, label='Base rate (68.3%)')
    for bar, n_val in zip(bars2, d_n):
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 2.0, f"{h:.1f}%\n(n={n_val:,})",
                 ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#081d58')

    ax2.set_title("B. Quy mô hộ gia đình & Phân nhóm UNKNOWN", fontsize=11.5, fontweight='bold', pad=10)
    ax2.set_ylabel("Xác suất mua hàng P(Y=1) (%)", fontsize=10.5, fontweight='bold')
    ax2.set_ylim(0, 112)
    ax2.legend(loc='upper left', fontsize=9.5, frameon=True, facecolor='white')

    plt.savefig(FIG_DIR / '13_loyalty_demographics_combined.png', dpi=160)
    plt.close()
    print("✅ Generated 13_loyalty_demographics_combined.png")

if __name__ == '__main__':
    generate_timeline_figure()
    generate_heatmap_rf()
    generate_stratified_spend_breadth()
    generate_campaign_coupon_combined()
    generate_loyalty_demo_combined()
    print("🎉 All 5 consolidated figures generated successfully!")
