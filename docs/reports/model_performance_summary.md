# Purchase Propensity Model - Performance & Benchmark Report

## 1. Executive Summary & Benchmark Comparison (Out-of-Time Test Set)

| Model Architecture | PR-AUC (Precision-Recall) | ROC-AUC | Brier Score (Lower is better) | ECE (Calibration Error) | Top Decile Lift | Top 20% Cumulative Gains |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **LightGBM (Isotonic Calibrated)** | **0.9303** | **0.8595** | **0.1364** | **0.0171** | **1.41x** | **28.0%** |
| LightGBM (Raw / Uncalibrated) | 0.9348 | 0.8600 | 0.1363 | 0.0193 | 1.41x | 28.1% |
| Logistic Regression (Linear) | 0.9328 | 0.8556 | 0.1385 | 0.0191 | 1.42x | 27.9% |
| Heuristic Recency Rule | 0.6311 | 0.3941 | 0.3392 | 0.3158 | 0.69x | 16.4% |

*Base rate on Out-Of-Time Test set: 70.14%.*

---

## 2. Decile Lift Table (LightGBM Calibrated)

| Decile | Households | Actual Buyers | Predicted Prob | Actual Conversion | Lift vs Base Rate | Cumulative Gains (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Decile 1 | 500 | 496 | 99.9% | 99.2% | 1.41x | 14.1% |
| Decile 2 | 500 | 487 | 97.3% | 97.4% | 1.39x | 28.0% |
| Decile 3 | 500 | 478 | 95.5% | 95.6% | 1.36x | 41.7% |
| Decile 4 | 500 | 451 | 89.4% | 90.2% | 1.29x | 54.5% |
| Decile 5 | 500 | 414 | 83.0% | 82.8% | 1.18x | 66.3% |
| Decile 6 | 500 | 352 | 71.5% | 70.4% | 1.00x | 76.4% |
| Decile 7 | 500 | 309 | 60.3% | 61.8% | 0.88x | 85.2% |
| Decile 8 | 500 | 259 | 47.4% | 51.8% | 0.74x | 92.6% |
| Decile 9 | 500 | 174 | 33.5% | 34.8% | 0.50x | 97.5% |
| Decile 10 | 500 | 87 | 15.9% | 17.4% | 0.25x | 100.0% |

---

## 3. Top 10 Feature Importance (Tree Split Gain)

| Rank | Feature Name | Total Gain Importance | Business Interpretation |
| :---: | :--- | :---: | :--- |
| 1 | `baskets_count_60d` | 105,163.2 | Chỉ số hành vi / nhân khẩu học |
| 2 | `baskets_count_90d` | 45,173.9 | Chỉ số hành vi / nhân khẩu học |
| 3 | `days_since_last_basket` | 14,227.1 | Số ngày trôi qua kể từ giỏ hàng gần nhất |
| 4 | `baskets_count_30d` | 11,228.2 | Tần suất mua sắm 30 ngày gần nhất |
| 5 | `baskets_count_180d` | 7,085.0 | Chỉ số hành vi / nhân khẩu học |
| 6 | `std_inter_trip` | 6,343.8 | Chỉ số hành vi / nhân khẩu học |
| 7 | `spend_30d` | 4,423.2 | Tổng chi tiêu 30 ngày gần nhất |
| 8 | `urgency_ratio` | 2,755.2 | Tỷ lệ quá hạn chu kỳ cá nhân (Recency / Chu kỳ trung vị) |
| 9 | `days_since_last_perishable` | 2,421.2 | Số ngày kể từ lần mua thực phẩm tươi sống cuối |
| 10 | `frequency_momentum_30_vs_90` | 2,251.9 | Gia tốc tần suất (30 ngày gần đây tăng hay chậm) |

---

## 4. Top 10 SHAP Explanations (Mean Absolute SHAP Value)

| Rank | Feature | Mean |SHAP| (Log-odds Impact) |
| :---: | :--- | :---: |
| 1 | `baskets_count_60d` | 0.5860 |
| 2 | `baskets_count_90d` | 0.2852 |
| 3 | `baskets_count_30d` | 0.2073 |
| 4 | `days_since_last_basket` | 0.1794 |
| 5 | `std_inter_trip` | 0.1260 |
| 6 | `spend_30d` | 0.1132 |
| 7 | `baskets_count_180d` | 0.1000 |
| 8 | `classification_3` | 0.0612 |
| 9 | `baskets_count_14d` | 0.0604 |
| 10 | `days_since_last_perishable` | 0.0596 |
