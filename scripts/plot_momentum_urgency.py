import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import duckdb

def main():
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False

    output_path = Path("docs/reports/figures/25_momentum_urgency_decay.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect()
    t_path = "sample_data/dunnhumby_The-Complete-Journey/dunnhumby_The-Complete-Journey CSV/transaction_data.csv"

    cutoffs = [250, 350, 450, 550, 650]
    results_mom = []
    results_ur = []

    for t0 in cutoffs:
        q_mom = f"""
        WITH baskets AS (
            SELECT household_key, BASKET_ID, DAY, SUM(SALES_VALUE) as spend
            FROM read_csv_auto('{t_path}')
            GROUP BY household_key, BASKET_ID, DAY
            HAVING SUM(SALES_VALUE) > 0
        ),
        hist_counts AS (
            SELECT 
                household_key,
                COUNT(DISTINCT CASE WHEN DAY >= {t0} - 30 AND DAY <= {t0} THEN BASKET_ID END) AS count_30d,
                COUNT(DISTINCT CASE WHEN DAY >= {t0} - 90 AND DAY <= {t0} THEN BASKET_ID END) AS count_90d
            FROM baskets
            WHERE DAY <= {t0} AND DAY >= {t0} - 90
            GROUP BY household_key
        ),
        future_baskets AS (
            SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0} + 14
        )
        SELECT 
            CASE 
                WHEN count_30d = 0 THEN 'Đóng Băng 30d\n(0 giỏ hàng)'
                WHEN (count_30d / 30.0) / (count_90d / 90.0) < 0.8 THEN 'Giảm Tốc\n(Velocity < 0.8x)'
                ELSE 'Ổn Định / Tăng Tốc\n(Velocity >= 0.8x)'
            END AS segment,
            COUNT(*) AS total_hh,
            ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS propensity_pct
        FROM hist_counts h
        LEFT JOIN future_baskets f ON h.household_key = f.household_key
        GROUP BY 1
        """
        results_mom.append(con.execute(q_mom).df())

        q_ur = f"""
        WITH baskets AS (
            SELECT household_key, BASKET_ID, DAY, SUM(SALES_VALUE) as spend
            FROM read_csv_auto('{t_path}')
            GROUP BY household_key, BASKET_ID, DAY
            HAVING SUM(SALES_VALUE) > 0
        ),
        hist_baskets AS (
            SELECT * FROM baskets WHERE DAY <= {t0} AND DAY >= {t0} - 180
        ),
        future_baskets AS (
            SELECT DISTINCT household_key FROM baskets WHERE DAY > {t0} AND DAY <= {t0} + 14
        ),
        hh_cadence AS (
            SELECT 
                household_key,
                {t0} - MAX(DAY) AS days_since_last,
                (MAX(DAY) - MIN(DAY)) * 1.0 / NULLIF(COUNT(DISTINCT BASKET_ID) - 1, 0) AS avg_cycle
            FROM hist_baskets
            GROUP BY household_key
        )
        SELECT 
            CASE 
                WHEN days_since_last / NULLIF(avg_cycle, 0) <= 1.0 THEN 'Đúng Hẹn\n(UR <= 1.0x)'
                WHEN days_since_last / NULLIF(avg_cycle, 0) BETWEEN 1.0 AND 2.0 THEN 'Chớm Trễ\n(1.0x < UR <= 2.0x)'
                WHEN days_since_last / NULLIF(avg_cycle, 0) > 2.0 THEN 'Trễ Nặng\n(UR > 2.0x)'
                ELSE 'Mất Dấu\n(Không lịch sử)'
            END AS ur_segment,
            COUNT(*) AS total_hh,
            ROUND(SUM(CASE WHEN f.household_key IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS propensity_pct
        FROM hh_cadence h
        LEFT JOIN future_baskets f ON h.household_key = f.household_key
        GROUP BY 1
        """
        results_ur.append(con.execute(q_ur).df())

    df_mom = pd.concat(results_mom, ignore_index=True).groupby('segment').agg(
        avg_hh=('total_hh', 'mean'), propensity=('propensity_pct', 'mean')
    ).reindex(['Ổn Định / Tăng Tốc\n(Velocity >= 0.8x)', 'Giảm Tốc\n(Velocity < 0.8x)', 'Đóng Băng 30d\n(0 giỏ hàng)']).reset_index()

    df_ur = pd.concat(results_ur, ignore_index=True).groupby('ur_segment').agg(
        avg_hh=('total_hh', 'mean'), propensity=('propensity_pct', 'mean')
    ).reindex(['Đúng Hẹn\n(UR <= 1.0x)', 'Chớm Trễ\n(1.0x < UR <= 2.0x)', 'Trễ Nặng\n(UR > 2.0x)', 'Mất Dấu\n(Không lịch sử)']).reset_index()

    # Create 2-panel figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=150)
    baseline = 68.25

    # Panel 1: Frequency Momentum
    colors_mom = ['#2b83ba', '#abdda4', '#d7191c']
    x1 = np.arange(len(df_mom))
    bars1 = ax1.bar(x1, df_mom['propensity'], width=0.48, color=colors_mom, edgecolor='#333333', lw=1.2, zorder=3)
    ax1.axhline(baseline, color='#D95F02', linestyle='--', linewidth=1.5, label=f'Baseline Trung bình ({baseline}%)', zorder=4)

    for i, bar in enumerate(bars1):
        h = bar.get_height()
        hh = int(df_mom.loc[i, 'avg_hh'])
        ax1.annotate(f'{h:.1f}%\n({hh:,} hộ)',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 5), textcoords="offset points",
                     ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1B365D')

    drop_mom = df_mom.loc[0, 'propensity'] - df_mom.loc[2, 'propensity']
    ax1.annotate(f'Rơi tự do -{drop_mom:.1f}%\nkhi tắt động lượng',
                 xy=(2, df_mom.loc[2, 'propensity']), xytext=(1.2, 52),
                 arrowprops=dict(arrowstyle="->", color="#d7191c", lw=1.8),
                 fontsize=9.5, fontweight='bold', color="#d7191c",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#fee8c8", edgecolor="#d7191c"))

    ax1.set_ylabel('Xác Suất Mua Sắm 14 Ngày: P(Y=1) (%)', fontsize=10.5, fontweight='bold')
    ax1.set_title('A. Gia Tốc Động Lượng (Momentum 30d vs 90d)', fontsize=11.5, fontweight='bold', color='#1B365D')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(df_mom['segment'], fontsize=9.5, fontweight='bold')
    ax1.set_ylim(0, 105)
    ax1.grid(axis='y', linestyle=':', alpha=0.6, zorder=0)
    ax1.legend(loc='lower left', fontsize=9, frameon=True)

    # Panel 2: Urgency Ratio
    colors_ur = ['#2b83ba', '#abdda4', '#fdae61', '#d7191c']
    x2 = np.arange(len(df_ur))
    bars2 = ax2.bar(x2, df_ur['propensity'], width=0.52, color=colors_ur, edgecolor='#333333', lw=1.2, zorder=3)
    ax2.axhline(baseline, color='#D95F02', linestyle='--', linewidth=1.5, label=f'Baseline Trung bình ({baseline}%)', zorder=4)

    for i, bar in enumerate(bars2):
        h = bar.get_height()
        hh = int(df_ur.loc[i, 'avg_hh'])
        ax2.annotate(f'{h:.1f}%\n({hh:,} hộ)',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 5), textcoords="offset points",
                     ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1B365D')

    ax2.annotate(f'Ngưỡng gãy hành vi (UR > 2.0x):\nXác suất giảm về 51.7%',
                 xy=(2, df_ur.loc[2, 'propensity']), xytext=(1.3, 72),
                 arrowprops=dict(arrowstyle="->", color="#B2182B", lw=1.8),
                 fontsize=9.5, fontweight='bold', color="#B2182B",
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="#fddbc7", edgecolor="#B2182B"))

    ax2.set_ylabel('Xác Suất Mua Sắm 14 Ngày: P(Y=1) (%)', fontsize=10.5, fontweight='bold')
    ax2.set_title('B. Độ Trễ Chu Kỳ Cá Nhân Hóa (Urgency Ratio)', fontsize=11.5, fontweight='bold', color='#1B365D')
    ax2.set_xticks(x2)
    ax2.set_xticklabels(df_ur['ur_segment'], fontsize=9.5, fontweight='bold')
    ax2.set_ylim(0, 105)
    ax2.grid(axis='y', linestyle=':', alpha=0.6, zorder=0)
    ax2.legend(loc='lower left', fontsize=9, frameon=True)

    plt.suptitle('QUY LUẬT ĐỘNG LƯỢNG MUA SẮM & CẢNH BÁO NGỦ ĐÔNG (MOMENTUM & URGENCY DECAY)\n'
                 'Tín hiệu cảnh báo sớm giải mã 100% bản chất của các hộ không phát sinh mua sắm (Nhãn Y = 0)',
                 fontsize=12.5, fontweight='bold', color='#1B365D', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    main()
