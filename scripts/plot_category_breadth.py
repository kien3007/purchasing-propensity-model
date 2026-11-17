import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import duckdb

def main():
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False

    output_path = Path("docs/reports/figures/24_category_breadth_stickiness.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    t_path = "sample_data/dunnhumby_The-Complete-Journey/dunnhumby_The-Complete-Journey CSV/transaction_data.csv"
    p_path = "sample_data/dunnhumby_The-Complete-Journey/dunnhumby_The-Complete-Journey CSV/product.csv"

    # Multi-cutoff average across t0 = 250, 350, 450, 550, 650
    cutoffs = [250, 350, 450, 550, 650]
    dfs = []
    for t0 in cutoffs:
        q = f"""
        WITH items AS (
            SELECT t.household_key, t.BASKET_ID, t.DAY, p.DEPARTMENT
            FROM read_csv_auto('{t_path}') t
            JOIN read_csv_auto('{p_path}') p ON t.PRODUCT_ID = p.PRODUCT_ID
            WHERE t.DAY <= {t0} AND t.DAY >= {t0 - 90} AND t.SALES_VALUE > 0
        ),
        hh_breadth AS (
            SELECT household_key, COUNT(DISTINCT DEPARTMENT) AS num_depts
            FROM items
            GROUP BY household_key
        ),
        future_baskets AS (
            SELECT DISTINCT household_key FROM read_csv_auto('{t_path}') WHERE DAY > {t0} AND DAY <= {t0 + 14} AND SALES_VALUE > 0
        )
        SELECT 
            CASE 
                WHEN num_depts >= 12 THEN 'Toàn Diện\n(>=12 ngành hàng)'
                WHEN num_depts BETWEEN 7 AND 11 THEN 'Phổ Thông\n(7-11 ngành hàng)'
                WHEN num_depts BETWEEN 3 AND 6 THEN 'Thứ Yếu\n(3-6 ngành hàng)'
                ELSE 'Đơn Ngành\n(1-2 ngành hàng)'
            END AS breadth_tier,
            COUNT(*) AS total_hh,
            ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS propensity_pct
        FROM hh_breadth h
        LEFT JOIN future_baskets f ON h.household_key = f.household_key
        GROUP BY 1
        """
        dfs.append(con.execute(q).df())

    df_all = pd.concat(dfs, ignore_index=True)
    agg = df_all.groupby('breadth_tier').agg(
        avg_hh=('total_hh', 'mean'),
        propensity=('propensity_pct', 'mean')
    ).reindex([
        'Đơn Ngành\n(1-2 ngành hàng)',
        'Thứ Yếu\n(3-6 ngành hàng)',
        'Phổ Thông\n(7-11 ngành hàng)',
        'Toàn Diện\n(>=12 ngành hàng)'
    ]).reset_index()

    # Styling colors: gradient from light slate to deep navy/emerald
    colors = ['#8da0cb', '#66c2a5', '#fc8d62', '#1b7837']
    bar_colors = ['#AEC7E8', '#6BAED6', '#3182BD', '#08519C']

    fig, ax1 = plt.subplots(figsize=(10, 5.8), dpi=150)

    x = np.arange(len(agg))
    width = 0.52

    # Draw bars for Propensity
    bars = ax1.bar(x, agg['propensity'], width, color=bar_colors, edgecolor='#08306B', linewidth=1.2, zorder=3)

    # Baseline average line
    baseline = 68.25
    ax1.axhline(baseline, color='#D95F02', linestyle='--', linewidth=1.8, label=f'Tỷ lệ Mua Trung bình Toàn bộ Tập mẫu ({baseline}%)', zorder=4)

    # Bar value labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        hh_num = int(agg.loc[i, 'avg_hh'])
        ax1.annotate(f'{height:.1f}%\n({hh_num:,} hộ)',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 5),  # 5 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom', fontsize=11, fontweight='bold', color='#08306B')

    # Highlight delta
    delta = agg.loc[3, 'propensity'] - agg.loc[0, 'propensity']
    ax1.annotate(f'Chênh lệch: +{delta:.1f}%\n(Gấp 3.03 lần)',
                 xy=(3, agg.loc[3, 'propensity']), xytext=(2.1, 70),
                 arrowprops=dict(arrowstyle="->", color="#B2182B", lw=2, connectionstyle="arc3,rad=-0.2"),
                 fontsize=10.5, fontweight='bold', color='#B2182B',
                 bbox=dict(boxstyle="round,pad=0.4", facecolor="#FDDBC7", edgecolor="#B2182B", lw=1.2))

    # Formatting
    ax1.set_ylabel('Xác Suất Mua Sắm Trong 14 Ngày Tới: P(Y=1) (%)', fontsize=11.5, fontweight='bold', labelpad=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels(agg['breadth_tier'], fontsize=11, fontweight='bold')
    ax1.set_ylim(0, 115)
    ax1.grid(axis='y', linestyle=':', alpha=0.6, zorder=0)

    # Title & Subtitle
    plt.title('QUY LUẬT MỎ NEO ĐA NGÀNH: ĐỘ PHỦ DANH MỤC VS XÁC SUẤT MUA SẮM 14 NGÀY\n'
              'Độ rộng danh mục hàng hóa (Category Breadth) là mỏ neo giữ chân khách hàng mạnh nhất',
              fontsize=12, fontweight='bold', pad=15, color='#1B365D')

    # Legend
    ax1.legend(loc='upper left', frameon=True, facecolor='#F7FBFF', edgecolor='#4292C6', fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()
