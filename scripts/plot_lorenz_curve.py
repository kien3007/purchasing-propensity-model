import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
from src.data.loader import load_raw_transactions, build_basket_dataset

def main():
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False

    trans = load_raw_transactions()
    baskets = build_basket_dataset(trans)

    # Group CLV
    hh_clv = baskets.groupby('household_key')['basket_spend'].sum().reset_index()
    hh_clv = hh_clv.sort_values('basket_spend', ascending=False).reset_index(drop=True)
    total_spend = hh_clv['basket_spend'].sum()
    hh_clv['cum_spend'] = hh_clv['basket_spend'].cumsum()
    hh_clv['cum_spend_pct'] = (hh_clv['cum_spend'] / total_spend) * 100
    hh_clv['cum_hh_pct'] = ((hh_clv.index + 1) / len(hh_clv)) * 100

    top10_spend_pct = hh_clv.iloc[249]['cum_spend_pct']
    top20_spend_pct = hh_clv.iloc[499]['cum_spend_pct']
    top50_spend_pct = hh_clv.iloc[1249]['cum_spend_pct']

    # Exact point reaching 80% spend
    idx_80 = (hh_clv['cum_spend_pct'] >= 80.0).idxmax()
    hh_80_pct = hh_clv.iloc[idx_80]['cum_hh_pct']

    # Gini coefficient
    spend_arr = hh_clv['basket_spend'].values
    diffsum = np.abs(np.subtract.outer(spend_arr, spend_arr)).sum()
    gini = diffsum / (2 * len(spend_arr) * spend_arr.sum())

    fig, ax = plt.subplots(figsize=(12, 6.5), dpi=150)

    # Lorenz curve
    ax.plot(hh_clv['cum_hh_pct'], hh_clv['cum_spend_pct'], color='#1f77b4', linewidth=3, label='Đường cong Doanh thu Thực tế (Lorenz Curve)')
    ax.plot([0, 100], [0, 100], color='gray', linestyle='--', linewidth=1.5, label='Đường Bình đẳng Tuyệt đối (45° Baseline)')

    # Theoretical Pareto 80/20 point
    ax.scatter([20], [80], color='#2ca02c', marker='X', s=130, zorder=6, label='Điểm Pareto 80/20 Lý thuyết (Top 20% Hộ = 80% Doanh thu)')
    ax.annotate('Mốc Pareto 80/20 Lý thuyết\n(Thực tế bán lẻ FMCG không đạt được)',
                xy=(20, 80), xytext=(5, 87),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#2ca02c'),
                fontweight='bold', fontsize=9.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#e5f5e0', edgecolor='#2ca02c'))

    # Fill area
    ax.fill_between(hh_clv['cum_hh_pct'], hh_clv['cum_spend_pct'], hh_clv['cum_hh_pct'], color='#1f77b4', alpha=0.12)

    # Actual points
    ax.scatter([10, 20, hh_80_pct, 50], [top10_spend_pct, top20_spend_pct, 80.0, top50_spend_pct], color='#d62728', s=70, zorder=5)

    # Annotate Top 10%
    spend_top10 = hh_clv.iloc[:250]['basket_spend'].sum()
    ax.annotate(f'Top 10% Hộ tạo ra {top10_spend_pct:.1f}% Doanh thu\n(${spend_top10:,.0f})',
                xy=(10, top10_spend_pct), xytext=(18, top10_spend_pct - 10),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#d62728'),
                fontweight='bold', fontsize=9.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#fee8c8', edgecolor='#d62728'))

    # Annotate Top 20%
    spend_top20 = hh_clv.iloc[:500]['basket_spend'].sum()
    ax.annotate(f'Thực tế: Top 20% Hộ tạo ra {top20_spend_pct:.1f}% Doanh thu\n(${spend_top20:,.0f} - Khác biệt so với 80% lý thuyết)',
                xy=(20, top20_spend_pct), xytext=(30, top20_spend_pct - 10),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#d62728'),
                fontweight='bold', fontsize=9.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#fee8c8', edgecolor='#d62728'))

    # Annotate 80% revenue point
    ax.annotate(f'Cần tới {hh_80_pct:.1f}% Hộ (1,100 hộ) để đạt 80% Doanh thu\n(Đặc thù hàng tiêu dùng thiết yếu FMCG)',
                xy=(hh_80_pct, 80.0), xytext=(hh_80_pct - 4, 65),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='#d62728'),
                fontweight='bold', fontsize=9.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff7bc', edgecolor='#d95f02'))

    ax.set_xlabel('Tỷ lệ tích lũy hộ gia đình (Sắp xếp từ chi nhiều nhất -> ít nhất) (%)', fontweight='bold', fontsize=11)
    ax.set_ylabel('Tỷ lệ tích lũy doanh thu thực tế (%)', fontweight='bold', fontsize=11)
    ax.set_title(f'Biểu đồ 11: Mức Độ Tập Trung Doanh Thu & Đường Cong Lorenz (CLV)\n(Tổng chi tiêu: ${total_spend:,.2f} | 2,500 Hộ gia đình | Hệ số Gini = {gini:.3f})', pad=15, fontsize=12, fontweight='bold')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)

    plt.tight_layout()
    out_path = Path('docs/reports/figures/19_clv_pareto_distribution.png')
    plt.savefig(out_path, dpi=150)
    print('Saved updated figure to:', out_path)

if __name__ == '__main__':
    main()
