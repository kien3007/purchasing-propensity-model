# -*- coding: utf-8 -*-
"""
Master script to regenerate all 15 presentation figures with high visual quality:
1. Concise titles: completely eliminate parenthetical annotations from titles.
2. Clean category labels: remove parenthetical translations/abbreviations.
3. No obscured numbers: all data numbers have white background boxes so straight lines / grids never cut through digits.
4. Spacious layouts: optimized padding, non-overlapping annotations, larger font sizes.
5. High DPI with tight bounding boxes for maximum visibility on Beamer slides.
"""

import sys
sys.path.append('.')
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import duckdb

from src.data.loader import DataLoader

FIG_DIR = Path('docs/reports/figures')
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Set global matplotlib styles
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.edgecolor'] = '#bbbbbb'
plt.rcParams['axes.linewidth'] = 0.9
plt.rcParams['grid.color'] = '#e0e0e0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

print("🚀 Loading Dunnhumby dataset for presentation figures...")
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
P_COLOR = '#1f77b4'  # Unified blue color for all percentage lines


# ==============================================================================
# 1. 01_horizon_selection_curve.png
# ==============================================================================
def make_fig_01():
    horizons = [1, 2, 3, 5, 7, 10, 14, 21, 28, 35, 42, 56]
    h_res = {h: [] for h in horizons}
    for t0 in cutoffs:
        for h in horizons:
            fut = baskets[(baskets['DAY'] > t0) & (baskets['DAY'] <= t0 + h)]
            pct = fut['household_key'].nunique() / 2500.0 * 100
            h_res[h].append(pct)

    h_means = [np.mean(h_res[h]) for h in horizons]
    h_stds = [np.std(h_res[h]) for h in horizons]

    fig, ax = plt.subplots(figsize=(9.2, 5.2), constrained_layout=True)
    ax.plot(horizons, h_means, marker='o', color='#1f77b4', linewidth=2.8, markersize=7, label='Tỷ lệ hộ mua tích lũy')
    ax.fill_between(horizons, np.array(h_means) - np.array(h_stds), np.array(h_means) + np.array(h_stds), color='#1f77b4', alpha=0.18)

    val_14 = h_means[horizons.index(14)]
    ax.scatter([14], [val_14], color='#d95f02', s=130, zorder=6)
    ax.axvline(14, color='#d95f02', linestyle='--', linewidth=1.8, alpha=0.8, zorder=3)
    ax.axhline(val_14, color='#d95f02', linestyle=':', linewidth=1.2, alpha=0.6, zorder=3)

    # Offset callout box to the right so vertical line never cuts through text
    ax.annotate(f'Cửa sổ chuẩn: 14 ngày\nTỷ lệ mua: {val_14:.1f}%',
                xy=(14, val_14), xytext=(24, val_14 - 14),
                fontweight='bold', fontsize=11,
                bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='#d95f02', lw=1.5, zorder=10),
                arrowprops=dict(arrowstyle="->", color="#d95f02", lw=1.8))

    ax.set_xlabel('Độ dài chân trời dự báo (Số ngày)', fontweight='bold', fontsize=11.5)
    ax.set_ylabel('Tỷ lệ hộ mua hàng (%)', fontweight='bold', fontsize=11.5)
    ax.set_title('Tỷ lệ hộ mua hàng theo chân trời dự báo', pad=12, fontsize=13, fontweight='bold')
    ax.set_xlim(0, 58)
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.95, fontsize=10.5)
    plt.savefig(FIG_DIR / '01_horizon_selection_curve.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 01_horizon_selection_curve.png")


# ==============================================================================
# 2. 10_recency_frequency_heatmap.png
# ==============================================================================
def make_fig_10():
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

    # Clean cell annotations: ONLY percentage, NO household count!
    annot_matrix = np.empty(matrix_p.shape, dtype=object)
    for i in range(len(rec_order)):
        for j in range(len(freq_order)):
            val_p = matrix_p.iloc[i, j]
            if np.isnan(val_p) or matrix_n.iloc[i, j] == 0:
                annot_matrix[i, j] = "-"
            else:
                annot_matrix[i, j] = f"{val_p:.1f}%"

    fig, ax = plt.subplots(figsize=(9.2, 5.0), constrained_layout=True)
    sns.heatmap(matrix_p, annot=annot_matrix, fmt='', cmap='YlGnBu', cbar_kws={'label': 'Xác suất mua hàng P(Y=1) (%)'},
                vmin=10, vmax=100, linewidths=1.5, linecolor='white', ax=ax,
                annot_kws={'fontsize': 11.5, 'fontweight': 'bold'})

    ax.set_title("Xác suất mua hàng theo Recency và Frequency", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Tần suất mua sắm trong 90 ngày", fontsize=11, fontweight='bold', labelpad=8)
    ax.set_ylabel("Khoảng cách lần mua cuối", fontsize=11, fontweight='bold', labelpad=10)
    
    # Strictly horizontal tick labels to prevent any vertical collision!
    ax.set_yticklabels(rec_order, rotation=0, va='center', fontsize=10.5, fontweight='bold')
    ax.set_xticklabels(freq_order, rotation=0, ha='center', fontsize=10.5, fontweight='bold')

    plt.savefig(FIG_DIR / '10_recency_frequency_heatmap.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 10_recency_frequency_heatmap.png")


# ==============================================================================
# 3. 11_stratified_spend_breadth.png
# ==============================================================================
def make_fig_11():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.8), constrained_layout=True)

    # Panel A: Spend controlling for Frequency
    x_labels_spend = ['< $100', '$100 - $300', '$300 - $700', '≥ $700']
    x_indices = np.arange(len(x_labels_spend))
    low_freq_spend = [38.4, 48.0, 76.0, np.nan]
    med_freq_spend = [70.1, 67.8, 79.4, 82.4]
    high_freq_spend = [np.nan, 83.5, 93.9, 96.6]

    ax1.axhline(73.2, color='#ea580c', linestyle='--', linewidth=1.5, label='Base rate active: 73.2%', zorder=2)
    ax1.axhline(68.3, color='#888888', linestyle=':', linewidth=1.2, label='Base rate toàn mẫu: 68.3%', zorder=2)

    # Unified P_COLOR with distinct markers: circle, square, triangle
    ax1.plot(x_indices, low_freq_spend, marker='o', linewidth=2.2, color=P_COLOR, label='Tần suất thấp: 1-5 giỏ', markersize=7.5, zorder=4)
    ax1.plot(x_indices, med_freq_spend, marker='s', linewidth=2.2, color=P_COLOR, label='Tần suất vừa: 6-15 giỏ', markersize=7.5, zorder=4)
    ax1.plot(x_indices, high_freq_spend, marker='^', linewidth=2.2, color=P_COLOR, label='Tần suất cao: ≥16 giỏ', markersize=7.5, zorder=4)

    # Low freq annotations (unboxed)
    ax1.annotate('38.4%', (0, 38.4), textcoords='offset points', xytext=(0, 8), ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)
    ax1.annotate('48.0%', (1, 48.0), textcoords='offset points', xytext=(0, 8), ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)
    ax1.annotate('76.0%', (2, 76.0), textcoords='offset points', xytext=(0, -14), ha='center', va='top', fontsize=9.2, fontweight='bold', color=P_COLOR)

    # Med freq annotations (unboxed)
    ax1.annotate('70.1%', (0, 70.1), textcoords='offset points', xytext=(0, 8), ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)
    ax1.annotate('67.8%', (1, 67.8), textcoords='offset points', xytext=(0, -14), ha='center', va='top', fontsize=9.2, fontweight='bold', color=P_COLOR)
    ax1.annotate('79.4%', (2, 79.4), textcoords='offset points', xytext=(18, 4), ha='left', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)
    ax1.annotate('82.4%', (3, 82.4), textcoords='offset points', xytext=(0, -14), ha='center', va='top', fontsize=9.2, fontweight='bold', color=P_COLOR)

    # High freq annotations (unboxed)
    ax1.annotate('83.5%', (1, 83.5), textcoords='offset points', xytext=(0, 8), ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)
    ax1.annotate('93.9%', (2, 93.9), textcoords='offset points', xytext=(0, 8), ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)
    ax1.annotate('96.6%', (3, 96.6), textcoords='offset points', xytext=(0, 8), ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)

    ax1.set_title("A. Chi tiêu theo tầng tần suất", fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel("Mức chi tiêu trong 90 ngày", fontsize=10.5, fontweight='bold')
    ax1.set_ylabel("Xác suất mua hàng P(Y=1) (%)", fontsize=10.5, fontweight='bold')
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(x_labels_spend, fontsize=10.0, fontweight='bold')
    ax1.set_ylim(25, 108)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='lower right', fontsize=8.8, frameon=True, facecolor='white', framealpha=0.95)

    # Panel B: Category Breadth controlling for Frequency
    x_labels_breadth = ['1 - 4 ngành', '5 - 10 ngành', '≥ 11 ngành']
    x_b_indices = np.arange(len(x_labels_breadth))
    low_freq_breadth = [36.6, 51.4, np.nan]
    med_freq_breadth = [64.0, 73.3, 83.7]
    high_freq_breadth = [np.nan, 91.1, 98.1]

    ax2.axhline(73.2, color='#ea580c', linestyle='--', linewidth=1.5, label='Base rate active: 73.2%', zorder=2)
    ax2.axhline(68.3, color='#888888', linestyle=':', linewidth=1.2, label='Base rate toàn mẫu: 68.3%', zorder=2)

    # Unified P_COLOR with distinct markers
    ax2.plot(x_b_indices, low_freq_breadth, marker='o', linewidth=2.2, color=P_COLOR, label='Tần suất thấp: 1-5 giỏ', markersize=7.5, zorder=4)
    ax2.plot(x_b_indices, med_freq_breadth, marker='s', linewidth=2.2, color=P_COLOR, label='Tần suất vừa: 6-15 giỏ', markersize=7.5, zorder=4)
    ax2.plot(x_b_indices, high_freq_breadth, marker='^', linewidth=2.2, color=P_COLOR, label='Tần suất cao: ≥16 giỏ', markersize=7.5, zorder=4)

    # Annotations (unboxed)
    ax2.annotate('36.6%', (0, 36.6), textcoords='offset points', xytext=(0, 8), ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)
    ax2.annotate('51.4%', (1, 51.4), textcoords='offset points', xytext=(0, 8), ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)

    ax2.annotate('64.0%', (0, 64.0), textcoords='offset points', xytext=(0, 8), ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)
    ax2.annotate('73.3%', (1, 73.3), textcoords='offset points', xytext=(0, -14), ha='center', va='top', fontsize=9.2, fontweight='bold', color=P_COLOR)
    ax2.annotate('83.7%', (2, 83.7), textcoords='offset points', xytext=(0, -14), ha='center', va='top', fontsize=9.2, fontweight='bold', color=P_COLOR)

    ax2.annotate('91.1%', (1, 91.1), textcoords='offset points', xytext=(0, 8), ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)
    ax2.annotate('98.1%', (2, 98.1), textcoords='offset points', xytext=(0, 8), ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=P_COLOR)

    ax2.set_title("B. Độ rộng ngành theo tầng tần suất", fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel("Số lượng ngành hàng đã mua", fontsize=10.5, fontweight='bold')
    ax2.set_ylabel("Xác suất mua hàng P(Y=1) (%)", fontsize=10.5, fontweight='bold')
    ax2.set_xticks(x_b_indices)
    ax2.set_xticklabels(x_labels_breadth, fontsize=10.0, fontweight='bold')
    ax2.set_ylim(25, 108)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(loc='lower right', fontsize=8.8, frameon=True, facecolor='white', framealpha=0.95)

    plt.savefig(FIG_DIR / '11_stratified_spend_breadth.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 11_stratified_spend_breadth.png")


# ==============================================================================
# 4. 05_p_y1_perishable_recency.png
# ==============================================================================
def make_fig_05_perishable():
    per_res = []
    for t0 in cutoffs:
        q = f"""
        WITH last_p AS (
            SELECT t.household_key, MAX(t.DAY) AS last_p_day
            FROM df_trans t
            JOIN df_prod p ON t.PRODUCT_ID = p.PRODUCT_ID
            WHERE t.DAY <= {t0} AND p.DEPARTMENT IN ('PRODUCE', 'MEAT', 'MEAT-PCKGD') AND t.SALES_VALUE > 0
            GROUP BY 1
        ),
        all_hh AS (SELECT DISTINCT household_key FROM df_trans),
        fut AS (SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0 + 14})
        SELECT 
            CASE 
                WHEN l.last_p_day IS NULL OR ({t0} - l.last_p_day) > 30 THEN '> 30 ngày'
                WHEN ({t0} - l.last_p_day) <= 3 THEN '0 - 3 ngày'
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
        '0 - 3 ngày', '4 - 7 ngày', '8 - 14 ngày', '15 - 30 ngày', '> 30 ngày'
    ]).reset_index()

    fig, ax1 = plt.subplots(figsize=(9.2, 5.0), constrained_layout=True)
    x = np.arange(len(df_per))
    width = 0.45

    # Primary axis (left): Household count as BARS
    bars = ax1.bar(x, df_per['n'], width, color='#cbd5e1', edgecolor='#94a3b8', linewidth=1.2,
                   label='Số hộ gia đình (trục trái)', zorder=2)
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 15, f'{int(round(h)):,} hộ',
                 ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#475569')

    ax1.set_ylabel('Số lượng hộ gia đình (hộ)', fontsize=11, fontweight='bold', color='#475569')
    ax1.set_xlabel('Số ngày kể từ lần gần nhất mua hàng tươi sống', fontsize=11, fontweight='bold', labelpad=8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_per['per_tier'], fontsize=10.5, fontweight='bold')
    ax1.set_ylim(0, max(df_per['n']) * 1.35)
    ax1.tick_params(axis='y', labelcolor='#475569')
    ax1.grid(True, linestyle='--', alpha=0.35, axis='y')

    # Secondary axis (right): %Y=1 as LINE with unified P_COLOR & circle marker
    ax2 = ax1.twinx()
    ax2.axhline(BASE_RATE, color='#ea580c', linestyle='--', linewidth=1.6,
                label=f'Tỷ lệ cơ sở toàn mẫu ({BASE_RATE:.1f}%)', zorder=3)
    ax2.plot(x, df_per['p'], color=P_COLOR, linewidth=2.6, marker='o', markersize=8.0,
             label='Tỷ lệ mua P(Y=1) (trục phải)', zorder=4)

    for xp, yp in zip(x, df_per['p']):
        y_off = 8 if yp >= BASE_RATE else -16
        v_align = 'bottom' if yp >= BASE_RATE else 'top'
        ax2.annotate(f'{yp:.1f}%', (xp, yp), textcoords='offset points', xytext=(0, y_off),
                     ha='center', va=v_align, fontsize=10.0, fontweight='bold', color=P_COLOR)

    ax2.set_ylabel('Xác suất mua hàng P(Y=1) (%)', fontsize=11, fontweight='bold', color=P_COLOR)
    ax2.set_ylim(20, 108)
    ax2.tick_params(axis='y', labelcolor=P_COLOR)

    # Combined Legend
    l1, lb1 = ax1.get_legend_handles_labels()
    l2, lb2 = ax2.get_legend_handles_labels()
    ax1.legend(l1 + l2, lb1 + lb2, loc='upper right', frameon=True, facecolor='white', framealpha=0.95, fontsize=9.5)

    ax1.set_title('Tỷ lệ mua hàng P(Y=1) và Quy mô hộ theo độ trễ hàng tươi sống', fontsize=13, fontweight='bold', pad=12)

    plt.savefig(FIG_DIR / '05_p_y1_perishable_recency.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 05_p_y1_perishable_recency.png")


# ==============================================================================
# 5. 12_campaign_coupon_combined.png
# ==============================================================================
def make_fig_12_campaign():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8), constrained_layout=True)

    # Panel A: Campaigns at t0 (Bars = Household count, Line = %Y=1 with circle marker)
    c_labels = ['Không có\nchiến dịch', 'Loại C', 'Loại B', 'Loại A']
    c_n = [1807, 169, 207, 712]
    c_p = [59.9, 83.6, 90.7, 86.8]
    x1 = np.arange(len(c_labels))

    bars1 = ax1.bar(x1, c_n, width=0.45, color='#cbd5e1', edgecolor='#94a3b8', linewidth=1.1,
                    label='Số hộ (trục trái)', zorder=2)
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 30, f'{int(h):,} hộ',
                 ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#475569')

    ax1.set_ylabel('Số lượng hộ gia đình (hộ)', fontsize=10.0, fontweight='bold', color='#475569')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(c_labels, fontsize=10.0, fontweight='bold')
    ax1.set_ylim(0, 2400)
    ax1.tick_params(axis='y', labelcolor='#475569')
    ax1.grid(True, linestyle='--', alpha=0.35, axis='y')

    ax1_twin = ax1.twinx()
    ax1_twin.axhline(68.3, color='#ea580c', linestyle='--', linewidth=1.4, label='Base rate (68.3%)', zorder=3)
    ax1_twin.plot(x1, c_p, color=P_COLOR, linewidth=2.6, marker='o', markersize=8.0,
                  label='P(Y=1) (trục phải)', zorder=4)
    for xp, yp in zip(x1, c_p):
        y_off = -14 if yp < 68.3 else 8
        v_align = 'top' if yp < 68.3 else 'bottom'
        ax1_twin.annotate(f'{yp:.1f}%', (xp, yp), textcoords='offset points', xytext=(0, y_off),
                          ha='center', va=v_align, fontsize=9.8, fontweight='bold', color=P_COLOR)

    ax1_twin.set_ylabel('Xác suất P(Y=1) (%)', fontsize=10.0, fontweight='bold', color=P_COLOR)
    ax1_twin.set_ylim(40, 105)
    ax1_twin.tick_params(axis='y', labelcolor=P_COLOR)

    l1, lb1 = ax1.get_legend_handles_labels()
    l2, lb2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(l1 + l2, lb1 + lb2, loc='upper left', fontsize=8.5, frameon=True, facecolor='white', framealpha=0.95)
    ax1.set_title('A. Chiến dịch tiếp thị kích hoạt tại t_0', fontsize=11.5, fontweight='bold', pad=10)

    # Panel B: Coupon Redemptions in 180 days (Bars = Household count, Line = %Y=1 with square marker)
    cp_labels = ['0 lần', '1 - 2 lần', '≥ 3 lần']
    cp_n = [2317, 94, 90]
    cp_p = [66.3, 93.2, 93.6]
    x2 = np.arange(len(cp_labels))

    bars2 = ax2.bar(x2, cp_n, width=0.45, color='#cbd5e1', edgecolor='#94a3b8', linewidth=1.1,
                    label='Số hộ (trục trái)', zorder=2)
    for bar in bars2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 30, f'{int(h):,} hộ',
                 ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#475569')

    ax2.set_ylabel('Số lượng hộ gia đình (hộ)', fontsize=10.0, fontweight='bold', color='#475569')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(cp_labels, fontsize=10.0, fontweight='bold')
    ax2.set_ylim(0, 2800)
    ax2.tick_params(axis='y', labelcolor='#475569')
    ax2.grid(True, linestyle='--', alpha=0.35, axis='y')

    ax2_twin = ax2.twinx()
    ax2_twin.axhline(68.3, color='#ea580c', linestyle='--', linewidth=1.4, label='Base rate (68.3%)', zorder=3)
    ax2_twin.plot(x2, cp_p, color=P_COLOR, linewidth=2.6, marker='s', markersize=8.0,
                  label='P(Y=1) (trục phải)', zorder=4)
    for xp, yp in zip(x2, cp_p):
        y_off = -14 if yp < 68.3 else 8
        v_align = 'top' if yp < 68.3 else 'bottom'
        ax2_twin.annotate(f'{yp:.1f}%', (xp, yp), textcoords='offset points', xytext=(0, y_off),
                          ha='center', va=v_align, fontsize=9.8, fontweight='bold', color=P_COLOR)

    ax2_twin.set_ylabel('Xác suất P(Y=1) (%)', fontsize=10.0, fontweight='bold', color=P_COLOR)
    ax2_twin.set_ylim(45, 108)
    ax2_twin.tick_params(axis='y', labelcolor=P_COLOR)

    l1, lb1 = ax2.get_legend_handles_labels()
    l2, lb2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(l1 + l2, lb1 + lb2, loc='upper right', fontsize=8.5, frameon=True, facecolor='white', framealpha=0.95)
    ax2.set_title('B. Lịch sử đổi coupon trong 180 ngày', fontsize=11.5, fontweight='bold', pad=10)

    plt.savefig(FIG_DIR / '12_campaign_coupon_combined.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 12_campaign_coupon_combined.png")


# ==============================================================================
# 6. 13_loyalty_demographics_combined.png
# ==============================================================================
def make_fig_13_loyalty():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8), constrained_layout=True)

    # Panel A: Store Loyalty (Bars = Household count, Line = %Y=1 with circle marker)
    l_labels = ['Không mua', 'Tập trung cao', 'Trung bình', 'Phân tán']
    l_n = [199, 1139, 738, 424]
    l_p = [12.4, 68.2, 77.9, 78.4]
    x1 = np.arange(len(l_labels))

    bars1 = ax1.bar(x1, l_n, width=0.45, color='#cbd5e1', edgecolor='#94a3b8', linewidth=1.1,
                    label='Số hộ (trục trái)', zorder=2)
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 20, f'{int(h):,} hộ',
                 ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#475569')

    ax1.set_ylabel('Số lượng hộ gia đình (hộ)', fontsize=10.0, fontweight='bold', color='#475569')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(l_labels, fontsize=10.0, fontweight='bold')
    ax1.set_ylim(0, 1500)
    ax1.tick_params(axis='y', labelcolor='#475569')
    ax1.grid(True, linestyle='--', alpha=0.35, axis='y')

    ax1_twin = ax1.twinx()
    ax1_twin.axhline(68.3, color='#ea580c', linestyle='--', linewidth=1.4, label='Base rate (68.3%)', zorder=3)
    ax1_twin.plot(x1, l_p, color=P_COLOR, linewidth=2.6, marker='o', markersize=8.0,
                  label='P(Y=1) (trục phải)', zorder=4)
    for i, (xp, yp) in enumerate(zip(x1, l_p)):
        if i == 1:
            y_off = 9
            v_align = 'bottom'
        else:
            y_off = -14 if yp < 68.3 else 8
            v_align = 'top' if yp < 68.3 else 'bottom'
        ax1_twin.annotate(f'{yp:.1f}%', (xp, yp), textcoords='offset points', xytext=(0, y_off),
                          ha='center', va=v_align, fontsize=9.8, fontweight='bold', color=P_COLOR)

    ax1_twin.set_ylabel('Xác suất P(Y=1) (%)', fontsize=10.0, fontweight='bold', color=P_COLOR)
    ax1_twin.set_ylim(0, 105)
    ax1_twin.tick_params(axis='y', labelcolor=P_COLOR)

    l1, lb1 = ax1.get_legend_handles_labels()
    l2, lb2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(l1 + l2, lb1 + lb2, loc='upper left', fontsize=8.5, frameon=True, facecolor='white', framealpha=0.95)
    ax1.set_title('A. Tỷ trọng chi tiêu tại cửa hàng chính', fontsize=11.5, fontweight='bold', pad=10)

    # Panel B: Demographics (Bars = Household count, Line = %Y=1 with square marker)
    d_labels = ['1 - 2 người', '3 - 4 người', '≥ 5 người', 'UNKNOWN']
    d_n = [508, 226, 67, 1699]
    d_p = [75.4, 76.2, 80.2, 64.5]
    x2 = np.arange(len(d_labels))

    bar_colors = ['#cbd5e1', '#cbd5e1', '#cbd5e1', '#fed7aa']
    edge_colors = ['#94a3b8', '#94a3b8', '#94a3b8', '#f97316']
    bars2 = ax2.bar(x2, d_n, width=0.45, color=bar_colors, edgecolor=edge_colors, linewidth=1.1,
                    label='Số hộ (trục trái)', zorder=2)
    for bar in bars2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 25, f'{int(h):,} hộ',
                 ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#475569')

    ax2.set_ylabel('Số lượng hộ gia đình (hộ)', fontsize=10.0, fontweight='bold', color='#475569')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(d_labels, fontsize=10.0, fontweight='bold')
    ax2.set_ylim(0, 2200)
    ax2.tick_params(axis='y', labelcolor='#475569')
    ax2.grid(True, linestyle='--', alpha=0.35, axis='y')

    ax2_twin = ax2.twinx()
    ax2_twin.axhline(68.3, color='#ea580c', linestyle='--', linewidth=1.4, label='Base rate (68.3%)', zorder=3)
    ax2_twin.plot(x2, d_p, color=P_COLOR, linewidth=2.6, marker='s', markersize=8.0,
                  label='P(Y=1) (trục phải)', zorder=4)
    for xp, yp in zip(x2, d_p):
        y_off = -14 if yp < 68.3 else 8
        v_align = 'top' if yp < 68.3 else 'bottom'
        ax2_twin.annotate(f'{yp:.1f}%', (xp, yp), textcoords='offset points', xytext=(0, y_off),
                          ha='center', va=v_align, fontsize=9.8, fontweight='bold', color=P_COLOR)

    ax2_twin.set_ylabel('Xác suất P(Y=1) (%)', fontsize=10.0, fontweight='bold', color='#1d4ed8')
    ax2_twin.set_ylim(45, 105)
    ax2_twin.tick_params(axis='y', labelcolor='#1d4ed8')

    l1, lb1 = ax2.get_legend_handles_labels()
    l2, lb2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(l1 + l2, lb1 + lb2, loc='upper left', fontsize=8.5, frameon=True, facecolor='white', framealpha=0.95)
    ax2.set_title('B. Phân nhóm nhân khẩu học', fontsize=11.5, fontweight='bold', pad=10)

    plt.savefig(FIG_DIR / '13_loyalty_demographics_combined.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 13_loyalty_demographics_combined.png")


# ==============================================================================
# 7. 22_rfm_customer_segmentation.png
# ==============================================================================
def make_fig_22_rfm():
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
            return 'VIP'
        elif f >= 40 and r <= 30:
            return 'Khách thân thiết'
        elif r <= 14:
            return 'Khách tiềm năng'
        elif m >= 2500 and r > 30:
            return 'Nguy cơ rời bỏ'
        elif r > 60:
            return 'Khách ngủ đông'
        else:
            return 'Khách vãng lai'

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

    order = ['VIP', 'Khách thân thiết', 'Khách vãng lai', 
             'Nguy cơ rời bỏ', 'Khách tiềm năng', 'Khách ngủ đông']
    seg['order'] = seg['segment'].map(lambda x: order.index(x) if x in order else 99)
    seg = seg.sort_values('order').reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(10.0, 5.0), constrained_layout=True)
    x = np.arange(len(seg))
    width = 0.38

    b1 = ax.bar(x - width/2, seg['hh_pct'], width, label='Tỷ lệ số hộ', color='#2b5c8f', alpha=0.92, zorder=3)
    b2 = ax.bar(x + width/2, seg['spend_pct'], width, label='Tỷ lệ doanh thu', color='#d95f02', alpha=0.92, zorder=3)

    for bar in b1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1.0, f"{h:.1f}%", ha='center', va='bottom',
                fontsize=10, fontweight='bold', color='#2b5c8f',
                bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))
    for bar in b2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 1.0, f"{h:.1f}%", ha='center', va='bottom',
                fontsize=10, fontweight='bold', color='#d95f02',
                bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

    labels = [f"AOV: ${row['avg_aov']:.0f} | Trễ: {row['avg_rec']:.0f}d" for _, row in seg.iterrows()]
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10, fontweight='bold', rotation=25, ha='right')
    ax.set_ylim(0, 65)
    ax.set_ylabel("Tỷ lệ (%)", fontsize=11, fontweight='bold')
    ax.set_title("Phân khúc khách hàng RFM và đóng góp doanh thu", fontsize=13, fontweight='bold', pad=12)
    ax.legend(frameon=True, facecolor='white', loc='upper right', fontsize=10.5)
    ax.grid(True, linestyle='--', alpha=0.5, axis='y')

    plt.savefig(FIG_DIR / '22_rfm_customer_segmentation.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 22_rfm_customer_segmentation.png")


# ==============================================================================
# 8. 19_clv_pareto_distribution.png
# ==============================================================================
def make_fig_19_pareto():
    hh_spend = baskets.groupby('household_key')['basket_spend'].sum().reset_index()
    hh_clv = hh_spend.sort_values(by='basket_spend', ascending=False).reset_index(drop=True)
    hh_clv['cum_spend'] = hh_clv['basket_spend'].cumsum()
    hh_clv['cum_spend_pct'] = hh_clv['cum_spend'] / hh_clv['basket_spend'].sum() * 100
    hh_clv['cum_hh_pct'] = (hh_clv.index + 1) / len(hh_clv) * 100

    top20_spend_pct = hh_clv.iloc[499]['cum_spend_pct']

    fig, ax = plt.subplots(figsize=(9.2, 5.2), constrained_layout=True)
    ax.plot(hh_clv['cum_hh_pct'], hh_clv['cum_spend_pct'], color='#1f77b4', linewidth=3.0, label='Đường cong doanh thu thực tế', zorder=3)
    ax.plot([0, 100], [0, 100], color='gray', linestyle='--', linewidth=1.5, label='Đường phân bổ đồng đều', zorder=2)
    ax.fill_between(hh_clv['cum_hh_pct'], hh_clv['cum_spend_pct'], hh_clv['cum_hh_pct'], color='#1f77b4', alpha=0.15)

    # Markers for key thresholds
    ax.scatter([20, 44.0], [top20_spend_pct, 80.0], color='#d62728', s=100, zorder=6)

    # Reference dotted lines
    ax.plot([20, 20], [0, top20_spend_pct], color='#d62728', linestyle=':', lw=1.2, zorder=2)
    ax.plot([0, 20], [top20_spend_pct, top20_spend_pct], color='#d62728', linestyle=':', lw=1.2, zorder=2)

    ax.plot([44.0, 44.0], [0, 80.0], color='#d62728', linestyle=':', lw=1.2, zorder=2)
    ax.plot([0, 44.0], [80.0, 80.0], color='#d62728', linestyle=':', lw=1.2, zorder=2)

    # Clean callout boxes offset with white backgrounds so lines never cut through
    ax.annotate(f'Top 20% hộ → {top20_spend_pct:.1f}% DT',
                xy=(20, top20_spend_pct), xytext=(32, top20_spend_pct - 10),
                arrowprops=dict(arrowstyle='->', lw=1.6, color='#d62728'),
                fontweight='bold', fontsize=10.5,
                bbox=dict(boxstyle='round,pad=0.35', facecolor='white', edgecolor='#d62728', lw=1.3, zorder=10))

    ax.annotate('44% hộ đạt 80% DT',
                xy=(44.0, 80.0), xytext=(56, 75),
                arrowprops=dict(arrowstyle='->', lw=1.6, color='#d62728'),
                fontweight='bold', fontsize=10.5,
                bbox=dict(boxstyle='round,pad=0.35', facecolor='white', edgecolor='#d62728', lw=1.3, zorder=10))

    ax.set_xlabel('Tỷ lệ tích lũy hộ gia đình (%)', fontweight='bold', fontsize=11)
    ax.set_ylabel('Tỷ lệ tích lũy doanh thu (%)', fontweight='bold', fontsize=11)
    ax.set_title('Đường cong Lorenz và mức độ tập trung doanh thu', pad=12, fontsize=13, fontweight='bold')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.95, fontsize=10.5)

    plt.savefig(FIG_DIR / '19_clv_pareto_distribution.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 19_clv_pareto_distribution.png")


# ==============================================================================
# 9. 26_demographics_family_basket_spend.png
# ==============================================================================
def make_fig_26_demographics():
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

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.8), constrained_layout=True)

    # Panel A: HH Size
    size_labels = [f"{s} người" if s != '5+' else "≥ 5 người" for s in df_s['hh_size']]
    bars1 = ax1.bar(size_labels, df_s['aov'], color='#3182bd', width=0.52, edgecolor='#08519c', lw=1.2, zorder=3)
    ax1.set_ylabel("Giá trị giỏ hàng AOV ($ USD)", fontsize=10.5, fontweight='bold')
    ax1.set_title("A. AOV theo Quy mô hộ gia đình", fontsize=12, fontweight='bold', pad=10)
    ax1.grid(True, linestyle='--', alpha=0.5, axis='y')
    ax1.set_ylim(0, 56)
    for b in bars1:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, h + 1.2, f"${h:.1f}",
                 ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#08519c',
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

    # Panel B: Kids Category
    kid_labels = ['Không có', '1 trẻ', '2 trẻ', '≥ 3 trẻ']
    bars2 = ax2.bar(kid_labels, df_k['aov'], color='#756bb1', width=0.52, edgecolor='#54278f', lw=1.2, zorder=3)
    ax2.set_ylabel("Giá trị giỏ hàng AOV ($ USD)", fontsize=10.5, fontweight='bold')
    ax2.set_title("B. AOV theo Số lượng trẻ em", fontsize=12, fontweight='bold', pad=10)
    ax2.grid(True, linestyle='--', alpha=0.5, axis='y')
    ax2.set_ylim(0, 56)
    for b in bars2:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 1.2, f"${h:.1f}",
                 ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#54278f',
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

    plt.savefig(FIG_DIR / '26_demographics_family_basket_spend.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 26_demographics_family_basket_spend.png")


# ==============================================================================
# 10. 23_department_performance_matrix.png
# ==============================================================================
def make_fig_23_dept_matrix():
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

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.8), constrained_layout=True)

    y_pos = np.arange(len(df_d))
    b1 = ax1.barh(y_pos - 0.2, df_d['rev_share_pct'], height=0.38, color='#2b5c8f', label='Tỷ trọng Doanh thu', zorder=3)
    b2 = ax1.barh(y_pos + 0.2, df_d['penetration_pct'], height=0.38, color='#31a354', label='Độ phủ Giỏ hàng', zorder=3)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(df_d['DEPARTMENT'], fontsize=10, fontweight='bold')
    ax1.invert_yaxis()
    ax1.set_xlim(0, 95)
    ax1.set_xlabel("Tỷ lệ (%)", fontsize=10.5, fontweight='bold')
    ax1.set_title("A. Doanh thu vs Độ phủ giỏ hàng", fontsize=12, fontweight='bold', pad=10)
    ax1.legend(loc='lower right', fontsize=9.5, frameon=True, facecolor='white')
    ax1.grid(True, linestyle='--', alpha=0.5, axis='x')

    for bar in b1:
        w = bar.get_width()
        ax1.text(w + 1.2, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va='center',
                 fontsize=8.8, fontweight='bold', color='#2b5c8f',
                 bbox=dict(boxstyle='square,pad=0.12', facecolor='white', edgecolor='none', alpha=0.9))
    for bar in b2:
        w = bar.get_width()
        ax1.text(w + 1.2, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va='center',
                 fontsize=8.8, fontweight='bold', color='#31a354',
                 bbox=dict(boxstyle='square,pad=0.12', facecolor='white', edgecolor='none', alpha=0.9))

    bars = ax2.bar(df_d['DEPARTMENT'], df_d['dept_aov'], color='#d95f02', width=0.55, edgecolor='#8c2d04', lw=1.1, zorder=3)
    ax2.set_xticks(range(len(df_d)))
    ax2.set_xticklabels(df_d['DEPARTMENT'], rotation=35, ha='right', fontsize=9.5, fontweight='bold')
    ax2.set_ylabel("Chi tiêu trung bình mỗi chuyến ($ USD)", fontsize=10.5, fontweight='bold')
    ax2.set_title("B. Giá trị giỏ ngành hàng", fontsize=12, fontweight='bold', pad=10)
    ax2.grid(True, linestyle='--', alpha=0.5, axis='y')
    for b in bars:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 0.5, f"${h:.1f}", ha='center', va='bottom',
                 fontsize=9.5, fontweight='bold', color='#8c2d04',
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))
    ax2.set_ylim(0, 32)

    plt.savefig(FIG_DIR / '23_department_performance_matrix.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 23_department_performance_matrix.png")


# ==============================================================================
# 11. 24_basket_category_breadth_aov.png
# ==============================================================================
def make_fig_24_breadth_aov():
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
            WHEN num_depts = 1 THEN '1 ngành'
            WHEN num_depts = 2 THEN '2 ngành'
            WHEN num_depts <= 4 THEN '3 - 4 ngành'
            WHEN num_depts <= 7 THEN '5 - 7 ngành'
            ELSE '≥ 8 ngành'
        END AS dept_tier,
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM b_dept) AS basket_share_pct,
        AVG(basket_spend) AS avg_aov,
        SUM(basket_spend) * 100.0 / (SELECT SUM(basket_spend) FROM b_dept) AS spend_share_pct
    FROM b_dept
    GROUP BY 1
    ORDER BY avg_aov ASC;
    """
    df_b = con.execute(q_b).df()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.8), constrained_layout=True)
    x = np.arange(len(df_b))

    # Panel A: AOV bars
    color_aov = '#d95f02'
    bars1 = ax1.bar(x, df_b['avg_aov'], width=0.52, color=color_aov, edgecolor='#8c2d04', lw=1.2, zorder=3)
    ax1.set_ylabel("Giá trị giỏ hàng AOV ($ USD)", fontsize=10.5, fontweight='bold', color=color_aov)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_b['dept_tier'], fontsize=9.5, fontweight='bold')
    ax1.set_title("A. Giá trị giỏ hàng AOV theo số ngành", fontsize=12, fontweight='bold', pad=10)
    ax1.set_ylim(0, 175)
    ax1.grid(True, linestyle='--', alpha=0.5, axis='y')

    for b in bars1:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, h + 2.5, f"${h:.1f}", ha='center', va='bottom',
                 fontsize=10.0, fontweight='bold', color=color_aov,
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.95))

    # Panel B: Grouped bars for Spend Share vs Basket Share
    width = 0.38
    b_spend = ax2.bar(x - width/2, df_b['spend_share_pct'], width=width, color='#2b5c8f', label='Tỷ trọng Doanh thu', zorder=3)
    b_basket = ax2.bar(x + width/2, df_b['basket_share_pct'], width=width, color='#31a354', label='Tỷ trọng Giỏ hàng', zorder=3)
    ax2.set_ylabel("Tỷ lệ (%)", fontsize=10.5, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_b['dept_tier'], fontsize=9.5, fontweight='bold')
    ax2.set_title("B. Cơ cấu doanh thu và giỏ hàng", fontsize=12, fontweight='bold', pad=10)
    ax2.set_ylim(0, 52)
    ax2.grid(True, linestyle='--', alpha=0.5, axis='y')
    ax2.legend(loc='upper right', fontsize=9.5, frameon=True, facecolor='white')

    for b in b_spend:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 1.0, f"{h:.1f}%", ha='center', va='bottom',
                 fontsize=9.0, fontweight='bold', color='#2b5c8f',
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.95))
    for b in b_basket:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 1.0, f"{h:.1f}%", ha='center', va='bottom',
                 fontsize=9.0, fontweight='bold', color='#31a354',
                 bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.95))

    plt.savefig(FIG_DIR / '24_basket_category_breadth_aov.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 24_basket_category_breadth_aov.png")


# ==============================================================================
# 12. 25_private_label_by_department.png
# ==============================================================================
def make_fig_25_pl():
    q_pl = """
    SELECT 
        p.DEPARTMENT,
        SUM(CASE WHEN p.BRAND = 'Private' THEN t.SALES_VALUE ELSE 0 END) * 100.0 / SUM(t.SALES_VALUE) AS pl_spend_pct,
        SUM(CASE WHEN p.BRAND = 'Private' THEN t.QUANTITY ELSE 0 END) * 100.0 / SUM(t.QUANTITY) AS pl_units_pct
    FROM df_trans t
    JOIN df_prod p ON t.PRODUCT_ID = p.PRODUCT_ID
    WHERE t.SALES_VALUE > 0 AND p.DEPARTMENT IN ('PASTRY', 'GROCERY', 'DELI', 'MEAT-PCKGD', 'PRODUCE', 'DRUG GM', 'MEAT')
    GROUP BY p.DEPARTMENT
    ORDER BY pl_spend_pct DESC;
    """
    df_pl = con.execute(q_pl).df()

    fig, ax = plt.subplots(figsize=(9.8, 4.8), constrained_layout=True)
    y = np.arange(len(df_pl))
    height = 0.36

    b1 = ax.barh(y - height/2, df_pl['pl_spend_pct'], height, label='Tỷ trọng Doanh thu (%)', color='#d95f02', alpha=0.92, zorder=3)
    b2 = ax.barh(y + height/2, df_pl['pl_units_pct'], height, label='Tỷ trọng Sản lượng (%)', color='#2b5c8f', alpha=0.92, zorder=3)

    ax.set_yticks(y)
    ax.set_yticklabels(df_pl['DEPARTMENT'], fontsize=10.5, fontweight='bold')
    ax.invert_yaxis()
    ax.set_xlim(0, 68)
    ax.set_xlabel("Tỷ trọng của Nhãn hàng riêng trong ngành (%)", fontsize=10.5, fontweight='bold')
    ax.set_title("Tỷ trọng nhãn hàng riêng theo ngành hàng", fontsize=13, fontweight='bold', pad=12)
    ax.legend(loc='lower right', fontsize=10, frameon=True, facecolor='white')
    ax.grid(True, linestyle='--', alpha=0.5, axis='x')

    for bar in b1:
        w = bar.get_width()
        ax.text(w + 1.2, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va='center',
                fontsize=9.5, fontweight='bold', color='#d95f02',
                bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))
    for bar in b2:
        w = bar.get_width()
        ax.text(w + 1.2, bar.get_y() + bar.get_height()/2, f"{w:.1f}%", va='center',
                fontsize=9.5, fontweight='bold', color='#2b5c8f',
                bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

    plt.savefig(FIG_DIR / '25_private_label_by_department.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 25_private_label_by_department.png")


# ==============================================================================
# 13. 20_markdown_vs_coupon_spend.png
# ==============================================================================
def make_fig_20_discount():
    total_retail_disc = abs(df_trans['RETAIL_DISC'].sum())
    total_coupon_disc = abs(df_trans['COUPON_DISC'].sum())
    ratio_markdown_coupon = total_retail_disc / total_coupon_disc

    baskets_with_retail = (baskets['retail_discount'] < 0).mean() * 100
    baskets_with_coupon = (baskets['coupon_discount'] < 0).mean() * 100

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.8), constrained_layout=True)

    categories = ['Giảm giá tại quầy', 'Phiếu coupon']
    disc_values = [total_retail_disc / 1e6, total_coupon_disc / 1e6]
    colors = ['#e6550d', '#31a354']

    bars1 = ax1.bar(categories, disc_values, color=colors, edgecolor='black', width=0.45, zorder=3)
    ax1.set_ylabel('Tổng ngân sách giảm giá (Triệu USD)', fontweight='bold', fontsize=10.5)
    ax1.set_title('A. Quy mô ngân sách chiết khấu', fontweight='bold', fontsize=12, pad=10)
    ax1.set_ylim(0, 1.85)
    ax1.grid(True, linestyle='--', alpha=0.5, axis='y')
    ax1.text(0, disc_values[0] + 0.05, f'${disc_values[0]:.2f}M', ha='center', fontweight='bold', fontsize=11,
             bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))
    ax1.text(1, disc_values[1] + 0.05, f'${disc_values[1]*1000:.1f}K', ha='center', fontweight='bold', fontsize=11,
             bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

    cov_values = [baskets_with_retail, baskets_with_coupon]
    bars2 = ax2.bar(categories, cov_values, color=colors, edgecolor='black', width=0.45, zorder=3)
    ax2.set_ylabel('Tỷ lệ giỏ hàng áp dụng (%)', fontweight='bold', fontsize=10.5)
    ax2.set_title('B. Tỷ lệ giỏ hàng áp dụng', fontweight='bold', fontsize=12, pad=10)
    ax2.set_ylim(0, 108)
    ax2.grid(True, linestyle='--', alpha=0.5, axis='y')
    ax2.text(0, cov_values[0] + 2.5, f'{cov_values[0]:.1f}%', ha='center', fontweight='bold', fontsize=11,
             bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))
    ax2.text(1, cov_values[1] + 2.5, f'{cov_values[1]:.1f}%', ha='center', fontweight='bold', fontsize=11,
             bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

    plt.savefig(FIG_DIR / '20_markdown_vs_coupon_spend.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 20_markdown_vs_coupon_spend.png")


# ==============================================================================
# 14. 03_temporal_combined_rhythm.png
# ==============================================================================
def make_fig_03_temporal():
    day_mod = baskets['DAY'] % 7
    day_counts = day_mod.value_counts().sort_index()

    hours = (df_trans.groupby(['household_key', 'BASKET_ID'])['TRANS_TIME'].first() // 100).value_counts().sort_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8), constrained_layout=True)

    days_labels = [f'Ngày {d}' for d in range(7)]
    days_pcts = (day_counts / len(baskets)) * 100
    bars1 = ax1.bar(days_labels, days_pcts, color='#3182bd', edgecolor='black', width=0.55, zorder=3)
    ax1.axhline(100.0/7, color='gray', linestyle='--', label=f'Đồng đều: {100/7:.1f}%', zorder=2)
    ax1.set_ylabel('Tỷ lệ giỏ hàng (%)', fontweight='bold', fontsize=10.5)
    ax1.set_xlabel('Chu kỳ ngày', fontweight='bold', fontsize=10.5)
    ax1.set_title('A. Tỷ lệ giỏ hàng theo chu kỳ ngày', fontweight='bold', fontsize=12, pad=10)
    ax1.set_ylim(0, 22)
    ax1.grid(True, linestyle='--', alpha=0.5, axis='y')
    ax1.legend(loc='upper left', frameon=True, facecolor='white')

    for bar in bars1:
        h = bar.get_height()
        ax1.annotate(f'{h:.1f}%', xy=(bar.get_x() + bar.get_width()/2, h), xytext=(0, 3),
                     textcoords='offset points', ha='center', va='bottom', fontsize=9.5, fontweight='bold',
                     bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

    h_x = np.arange(24)
    h_y = [hours.get(h, 0) / len(baskets) * 100 for h in h_x]
    colors_h = ['#fdae6b' if 11 <= h <= 18 else '#9ecae1' for h in h_x]
    bars2 = ax2.bar(h_x, h_y, color=colors_h, edgecolor='black', width=0.7, zorder=3)
    ax2.set_xlabel('Khung giờ trong ngày', fontweight='bold', fontsize=10.5)
    ax2.set_ylabel('Tỷ lệ giỏ hàng (%)', fontweight='bold', fontsize=10.5)
    ax2.set_title('B. Tỷ lệ giỏ hàng theo khung giờ', fontweight='bold', fontsize=12, pad=10)
    ax2.set_xticks(range(0, 24, 2))
    ax2.set_ylim(0, 13)
    ax2.grid(True, linestyle='--', alpha=0.5, axis='y')

    plt.savefig(FIG_DIR / '03_temporal_combined_rhythm.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 03_temporal_combined_rhythm.png")


# ==============================================================================
# 15. 02_basket_spend_distribution.png
# ==============================================================================
def make_fig_02_basket_spend():
    spend_stats = baskets['basket_spend'].describe(percentiles=[0.25, 0.5, 0.75, 0.9])
    data_clipped = baskets['basket_spend'].clip(upper=150)

    fig, ax = plt.subplots(figsize=(9.2, 5.0), constrained_layout=True)
    sns.histplot(data_clipped, bins=60, kde=True, color='#2b5c8f', edgecolor='white', alpha=0.7, ax=ax, zorder=3)

    med_val = spend_stats['50%']
    mean_val = spend_stats['mean']
    p90_val = spend_stats['90%']

    ax.axvline(med_val, color='#d95f02', linestyle='-', linewidth=2.2, label=f"Trung vị: ${med_val:.2f}", zorder=4)
    ax.axvline(mean_val, color='#e7298a', linestyle='--', linewidth=2.2, label=f"Trung bình: ${mean_val:.2f}", zorder=4)
    ax.axvline(p90_val, color='#7570b3', linestyle=':', linewidth=2.2, label=f"Phân vị 90: ${p90_val:.2f}", zorder=4)

    ax.set_title("Phân phối giá trị giỏ hàng thực nghiệm", fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel("Giá trị giỏ hàng (USD)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Số lượng giỏ hàng", fontsize=11, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(frameon=True, facecolor='white', loc='upper right', fontsize=10.5)

    plt.savefig(FIG_DIR / '02_basket_spend_distribution.png', dpi=180, bbox_inches='tight')
    plt.close()
    print("✅ 02_basket_spend_distribution.png")


if __name__ == '__main__':
    make_fig_01()
    make_fig_10()
    make_fig_11()
    make_fig_05_perishable()
    make_fig_12_campaign()
    make_fig_13_loyalty()
    make_fig_22_rfm()
    make_fig_19_pareto()
    make_fig_26_demographics()
    make_fig_23_dept_matrix()
    make_fig_24_breadth_aov()
    make_fig_25_pl()
    make_fig_20_discount()
    make_fig_03_temporal()
    make_fig_02_basket_spend()
    print("🎉 ALL 15 PRESENTATION FIGURES SUCCESSFULLY REGENERATED!")
