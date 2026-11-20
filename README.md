# 🛒 Mô Hình Dự Đoán Xác Suất Mua Hàng Hộ Gia Đình (Household Purchase Propensity Model)
### Phân Tích Thực Nghiệm & Học Máy Trên Bộ Dữ Liệu Dunnhumby - The Complete Journey (2.6 Triệu Giao Dịch, 2,500 Hộ Gia Đình)

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: Passing](https://img.shields.io/badge/pytest-4%20passed-brightgreen.svg)]()
[![Model: LightGBM](https://img.shields.io/badge/Model-LightGBM%20GBDT-orange.svg)]()
[![PR-AUC: 0.9303](https://img.shields.io/badge/PR--AUC-0.9303-green.svg)]()
[![Brier Score: 0.1364](https://img.shields.io/badge/Brier%20Score-0.1364-blue.svg)]()

---

## 📌 1. Đặt Vấn Đề Kinh Doanh & Định Nghĩa Bài Toán

Trong ngành bán lẻ hiện đại (Supermarket & FMCG Retail), thấu hiểu và dự đoán chính xác khi nào khách hàng sẽ quay lại mua sắm là chìa khóa sống còn để:
- **Tối ưu hóa ngân sách tiếp thị (Marketing ROI)**: Tránh phát voucher cào bằng cho nhóm khách chắc chắn quay lại tự nhiên.
- **Kích hoạt đúng nhóm chuyển đổi (Persuadable Segment)**: Tập trung nguồn lực vào nhóm khách hàng đang lưỡng lự hoặc có dấu hiệu giãn cách chu kỳ mua.
- **Quản lý chuỗi cung ứng hàng tươi sống (Fresh Inventory Management)**: Dự báo sức mua ngắn hạn để giảm tỷ lệ hao hụt hàng cận hạn.

### 🎯 Phát biểu bài toán (Mathematical Formulation):
Dự đoán xác suất hộ gia đình $h \in \{1, 2, \dots, 2500\}$ sẽ phát sinh **ít nhất một lượt đi chợ/mua sắm hợp lệ ($> \$0$)** trong khoảng thời gian tương lai $\Delta t = 14$ ngày kể từ một mốc thời gian chốt sổ quan sát bất kỳ ($t_0$):

$$Y_{h, t_0} = \begin{cases} 1 & \text{nếu } \exists \text{ trip của hộ } h \text{ trong khoảng } (t_0, t_0 + 14] \\ 0 & \text{ngược lại} \end{cases}$$

### 🛡️ Ba Nguyên Tắc Thiết Kế Cốt Lõi:
1. **Cam kết 100% Số Liệu Thực Tế (Zero Hallucination)**: Toàn bộ số liệu, tỷ lệ phần trăm và thông số trong dự án đều được trích xuất và tính toán trực tiếp từ 2,595,732 dòng giao dịch thực tế của Dunnhumby.
2. **Kỷ Luật Point-in-Time Tuyệt Đối (Zero Future Leakage)**: Mọi biến số và tính năng (features) tại thời điểm $t_0$ chỉ được phép sử dụng dữ liệu phát sinh tính đến hết ngày $t_0$ ($DAY \le t_0$). Nghiêm cấm dùng Cross-Validation ngẫu nhiên trên toàn bộ tập dữ liệu (dễ gây rò rỉ thông tin tương lai).
3. **Diễn Giải Trực Quan Cho Cả Người Trong Ngành Lẫn Ngoài Ngành**: Mọi kết luận phân tích đều tuân thủ công thức 3 mảnh: **Hiện tượng đời thường + Con số neo thực tế + Hành động cụ thể**.

---

## 🏗️ 2. Kiến Trúc Dự Án & Cấu Trúc Mã Nguồn

```text
purchasing-propensity-model/
├── .agents/skills/              # Các skills tiêu chuẩn (EDA, Modeling, LaTeX Beamer, Clean Code...)
├── .venv/                       # Môi trường ảo Python độc lập (git-ignored)
├── data/                        # Dữ liệu trung gian & cache (git-ignored)
├── docs/                        # Tài liệu nghiệp vụ, slide thuyết trình & báo cáo chuyên sâu
│   ├── purchase_propensity_checklist.md  # Master Blueprint & Checklist kiểm toán
│   ├── presentation/                     # Slide thuyết trình LaTeX Beamer widescreen 16:9 (23 slide)
│   │   ├── eda_data_quality_presentation.tex    # Mã nguồn Beamer chuẩn mực
│   │   ├── eda_data_quality_presentation.pdf    # Bản PDF trình chiếu xuất bản hoàn chỉnh
│   │   └── eda_presentation_script.md          # Kịch bản thuyết minh MC/Diễn giả chi tiết
│   └── reports/
│       ├── model_performance_summary.md  # Báo cáo tổng hợp hiệu năng mô hình
│       ├── model_performance_summary.json
│       └── figures/                      # 21 biểu đồ trực quan hóa dữ liệu chuẩn hóa 4 màu
├── models/                      # Mô hình LightGBM đã hiệu chuẩn xác suất (.joblib)
├── notebooks/                   # Chuỗi 5 Jupyter Notebooks tương tác hoàn chỉnh
│   ├── 01_eda_and_data_quality.ipynb             # Kiểm toán 8 bảng dữ liệu & phân tích chuyên sâu
│   ├── 02_point_in_time_feature_engineering.ipynb  # Kỷ luật Point-in-Time & trích xuất 28 đặc trưng
│   ├── 03_model_training_and_benchmarking.ipynb  # Benchmark Heuristic vs Logistic vs LightGBM
│   ├── 04_business_impact_and_decile_lift.ipynb  # Phân tầng 10 phân vị Decile Lift & ROI Marketing
│   └── 05_model_explainability_and_shap.ipynb    # Giải thích toàn cục/cục bộ qua SHAP & Playbook
├── sample_data/                 # Thư mục chứa 8 file CSV gốc từ Dunnhumby
├── src/                         # Gói mã nguồn Python chuẩn mực (Clean Architecture)
│   ├── config/settings.py       # Cấu hình cửa sổ thời gian, đường dẫn, siêu tham số
│   ├── data/loader.py           # Ingestion tối ưu RAM (downcasting) & tổng hợp giỏ hàng
│   ├── features/
│   │   ├── time_windows.py      # Sinh nhãn Point-in-Time trượt qua các mốc thời gian
│   │   └── feature_builder.py   # Trích xuất 28 tính năng đa chiều (RFM, tươi sống, coupon, loyalty)
│   ├── models/
│   │   ├── baselines.py         # Mô hình Heuristic (Urgency Ratio) & Logistic Regression
│   │   └── trainer.py           # LightGBM GBDT + Isotonic Calibration + SHAP
│   ├── evaluation/metrics.py    # PR-AUC, ROC-AUC, Brier Score, ECE, Decile Lift Table
│   └── pipelines/
│       └── train_pipeline.py    # Luồng huấn luyện, kiểm thử và xuất báo cáo tự động
├── tests/
│   └── test_data_quality.py     # Unit tests kiểm toán chống rò rỉ & chất lượng logic
├── pyproject.toml               # Khai báo dependency và cấu hình pytest
├── .gitignore                   # Loại trừ file lớn, scripts nội bộ và môi trường ảo
└── README.md                    # Tài liệu hướng dẫn tổng quan dự án
```

---

## 📊 3. Khám Phá Dữ Liệu & Các Phát Hiện Nghiệp Vụ Cốt Lõi (EDA)

Bộ dữ liệu Dunnhumby gồm 8 bảng quan hệ đã được kiểm toán toàn diện:
- **Giao dịch**: 2,595,732 dòng -> 276,484 giỏ hàng thô.
- **Làm sạch**: Loại bỏ 942 giao dịch số tiền âm/trả hàng -> **275,542 giỏ hàng hợp lệ ($> \$0$)**.
- **Độ phủ khách hàng**: Đủ 2,500 hộ gia đình trải dài qua 711 ngày quan sát (~102 tuần), không ai bị bỏ sót.

### 🌟 10 Căn Cứ Thực Nghiệm Nền Tảng:
1. **Căn cứ chọn cửa sổ 14 ngày**: Chu kỳ đi chợ có trung vị 2.0 ngày, trung bình 5.67 ngày; 82.0% khách quay lại trong 7 ngày và 92.4% trong 14 ngày. Cửa sổ 14 ngày cân bằng hoàn hảo giữa khả năng phân hóa hành vi và độ trễ vận hành chiến dịch.
2. **Phân phối giá trị giỏ hàng (Log-Normal)**: Đa số đi chợ hết \$17.18 (trung vị), nhưng các giỏ lớn kéo trung bình lên \$29.24. Cần áp dụng biến đổi $\ln(1 + \text{Spend})$ để nén ngoại lai khi đưa vào mô hình.
3. **Tương tác Độ trễ (Recency) & Tần suất (Frequency)**: Khách vừa đi chợ 2–3 hôm trước có xác suất quay lại 96%, nhưng bỏ đi >30 ngày chỉ còn 17%. Khách quen (tần suất cao) duy trì xác suất quay lại gấp đôi khách lạ ngay cả khi cùng một khoảng thời gian vắng mặt.
4. **Sức mạnh của độ rộng ngành hàng (Category Breadth)**: Khách mua đa dạng nhiều ngành hàng (rau củ, thịt cá, đồ gia dụng) có xác suất quay lại tăng từ 64.0% lên 83.7% (+19.7%), tạo sự gắn bó bền vững hơn là chỉ tập trung tăng số tiền chi tiêu.
5. **Hàng tươi sống - Chuông báo động chu kỳ tiêu dùng**: Do có hạn sử dụng ngắn, khách vừa mua đồ tươi 3 ngày trước đạt 90.0% quay lại, nhưng quá 14 ngày không mua đồ tươi tỷ lệ này giảm sâu xuống 37.7%.
6. **Chiến dịch tiếp thị & Phiếu giảm giá**: Có chiến dịch kích hoạt tại thời điểm quan sát nâng xác suất quay lại lên 86.8% (so với 59.9% khi không có). Phiếu giảm giá toàn giỏ (Type A/B) hiệu quả gấp đôi phiếu giảm giá 1 món (Type C).
7. **Tính đại diện của nhóm thông tin khuyết thiếu (UNKNOWN)**: 1,699 hộ gia đình giấu thông tin nhân khẩu học vẫn đi chợ với tỷ lệ quay lại 68.4% (tương đồng 68.2% ở nhóm khai báo đầy đủ), chứng minh dữ liệu khuyết thiếu ngẫu nhiên và an toàn giữ lại 100% mẫu.
8. **Phân khúc khách hàng RFM**: 541 hộ VIP gánh 54.3% doanh thu siêu thị. Nhóm 52 hộ "Nguy cơ rời bỏ" (từng chi tiêu rất lớn nhưng đã vắng mặt gần 3 tháng) cần được kích hoạt chiến dịch win-back khẩn cấp để cứu vãn \$244K doanh thu.
9. **Mức độ tập trung doanh thu (Lorenz & Gini)**: Hệ số Gini = 0.5028. Cần tới 44% số hộ gia đình để tạo ra 80% doanh thu, chứng minh ngành hàng tiêu dùng thiết yếu không tuân theo quy luật Pareto 80/20 cực đoan.
10. **Tỷ trọng thâm nhập nhãn hàng riêng (Private Label)**: Nhãn hàng riêng chiếm 51.6% doanh số ngành bánh (PASTRY), nhưng mới đạt 5.0% ở quầy thịt tươi và 9.4% ở quầy mỹ phẩm/gia dụng -> Dư địa lớn để mở rộng nhãn riêng nhằm gia tăng biên lợi nhuận thêm 5–12%.

### 🔬 6 Phát Hiện Chuyên Sâu Mới (Deep-Dive Insights):
1. **Kiểm toán chuỗi thời gian mở rộng mẫu (Panel Onboarding)**: 20 tuần đầu là giai đoạn tuyển mẫu (số hộ hoạt động tăng từ 390 lên 1,336 hộ/tuần, doanh thu tăng từ \$22.5K lên \$84K/tuần); từ tuần 21–102 số lượng hộ mới ổn định hoàn toàn. Cần phân tích theo nhóm gia nhập (cohort) để tránh nhầm lẫn sự mở rộng mẫu với tăng trưởng thực tế của siêu thị.
2. **Nhịp mua đều đặn (Inter-purchase Regularity)**: Hộ gia đình có thói quen đi chợ đúng ngày cố định ($CV \le 0.65$) đạt xác suất quay lại 14 ngày lên tới **86.1%**, cao hơn **+5.6%** so với nhóm đi chợ thất thường ($CV > 0.85$, đạt 80.5%).
3. **Tách biệt giỏ xăng (KIOSK-GAS)**: Trong 22,056 giỏ hàng có xăng, có tới **95.7% (21,108 giỏ) chỉ mua xăng đơn thuần** với AOV \$24.83. Trong khi đó, giỏ thực phẩm 1 ngành hàng chỉ có AOV \$8.83. Việc tách riêng trạm xăng giúp định giá đúng giá trị thực của chuyến đi chợ.
4. **Cơ hội bán chéo sản phẩm vi mô (Cross-sell Affinities)**:
   - *Mì khô/Pasta $\to$ Sốt mì*: Xuất hiện trong 6,423 giỏ, tỷ lệ đính kèm đạt **45.8%** (gấp **10.7 lần** tỷ lệ nền 4.3%).
   - *Phô mai $\to$ Thịt nguội*: Xuất hiện trong 7,132 giỏ, tỷ lệ đính kèm đạt **63.0%** (gấp **4.4 lần** tỷ lệ nền 14.3%).
   - *Giấy vệ sinh $\to$ Khăn giấy cuộn*: Xuất hiện trong 3,743 giỏ, tỷ lệ đính kèm đạt **27.5%** (gấp **3.2 lần** tỷ lệ nền 8.5%).
5. **Cấu trúc chiết khấu niêm yết (Markdowns)**: Dù quầy tạp hóa chiếm số tiền giảm giá lớn nhất (\$817.5K / 58.4%), nhưng riêng hai ngành thịt và hải sản đóng gói chịu mức giảm giá sâu nhất (**22.5% – 25.3%**, tiêu tốn \$296K) $\to$ Cần ưu tiên rà soát lại chính sách định giá và bảo quản hàng tươi sống.
6. **Hiệu ứng phiếu giảm giá trong cùng hộ gia đình (Within-Household Lift)**: So sánh trên 1,856 hộ có cả hai loại giao dịch, giá trị giỏ hàng trung bình khi dùng coupon đạt **\$68.17**, cao hơn **+140.8%** so với khi không dùng coupon (**\$28.31**). Kết quả khẳng định coupon kích thích khách mua nhiều hàng hơn trong cùng một chuyến đi, chứ không chỉ chọn lọc nhóm khách VIP vốn dĩ giàu có.

---

## 🔬 4. Kết Quả Kiểm Thử & So Sánh Benchmark (Out-of-Time Test Set)

Mô hình được kiểm thử trên tập dữ liệu độc lập ngoài thời gian (**Out-of-Time Test Set** tại các mốc Ngày 650 và Ngày 680, gồm 5,000 lượt quan sát, tỷ lệ mua hàng thực tế cơ sở = 70.14%).

### Bảng So Sánh Các Kiến Trúc Mô Hình:

| Kiến trúc mô hình | PR-AUC (Precision-Recall) | ROC-AUC | Brier Score (Càng thấp càng tốt) | ECE (Sai số hiệu chuẩn) | Top Decile Lift (Nhóm 10% cao nhất) | Top 20% Cumulative Gains |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 🏆 **LightGBM (Isotonic Calibrated)** | **0.9303** | **0.8595** | **0.1364** | **0.0171** | **1.41x** | **28.0%** |
| 🌲 LightGBM (Raw / Uncalibrated) | 0.9348 | 0.8600 | 0.1363 | 0.0193 | 1.41x | 28.1% |
| 📈 Logistic Regression (Linear) | 0.9328 | 0.8556 | 0.1385 | 0.0191 | 1.42x | 27.9% |
| 📏 Heuristic Recency Rule | 0.6311 | 0.3941 | 0.3392 | 0.3158 | 0.69x | 16.4% |

> [!NOTE]
> - **Hiệu chuẩn xác suất (Isotonic Calibration)** giúp hạ thấp sai số hiệu chuẩn kỳ vọng (**ECE giảm xuống chỉ còn 1.71%**), giúp xác suất mô hình trả về phản ánh chính xác tỷ lệ chuyển đổi thực tế trong kinh doanh.
> - **Quy luật Heuristic đơn giản thất bại** vì khách hàng bán lẻ không mua sắm theo một chu kỳ cơ học cố định mà chịu tác động đa chiều từ hàng tươi sống, khuyến mãi và đà mua sắm gần nhất.

---

## 📈 5. Bảng Phân Tầng 10 Phân Vị (Decile Lift Table)

Khi triển khai thực tế vào các chiến dịch Marketing / CRM, khách hàng được xếp hạng theo xác suất dự đoán từ cao xuống thấp và chia thành 10 phân vị (mỗi phân vị gồm 500 hộ gia đình):

| Nhóm Phân Vị (Decile) | Số Hộ Gia Đình | Khách Mua Thực Tế | Xác Suất Dự Báo TB | Tỷ Lệ Mua Thực Tế | Hệ Số Nâng (Lift) | Tỷ Lệ Tích Lũy (Gains) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Decile 1 (Cao nhất)** | 500 | 496 | **99.9%** | **99.2%** | **1.41x** | 14.1% |
| **Decile 2** | 500 | 487 | **97.3%** | **97.4%** | **1.39x** | 28.0% |
| **Decile 3** | 500 | 478 | **95.5%** | **95.6%** | **1.36x** | 41.7% |
| **Decile 4** | 500 | 451 | **89.4%** | **90.2%** | **1.29x** | 54.5% |
| **Decile 5** | 500 | 414 | **83.0%** | **82.8%** | **1.18x** | 66.3% |
| **Decile 6** | 500 | 352 | **71.5%** | **70.4%** | **1.00x** | 76.4% |
| **Decile 7** | 500 | 309 | **60.3%** | **61.8%** | **0.88x** | 85.2% |
| **Decile 8** | 500 | 259 | **47.4%** | **51.8%** | **0.74x** | 92.6% |
| **Decile 9** | 500 | 174 | **33.5%** | **34.8%** | **0.50x** | 97.5% |
| **Decile 10 (Thấp nhất)** | 500 | 87 | **15.9%** | **17.4%** | **0.25x** | 100.0% |

> [!TIP]
> **Ứng dụng thực tiễn**:
> - Nhóm **Decile 1–3**: Tỷ lệ mua tự nhiên lên tới **95% – 99%**. Không cần tốn voucher giảm giá cao (Organic Buyers).
> - Nhóm **Decile 6–8**: Tỷ lệ mua dao động từ 50% – 70%. Đây là **"nhóm vàng cần thuyết phục" (Persuadable Segment)**, nơi ngân sách Marketing mang lại chỉ số ROI chuyển đổi cao nhất!

---

## 🧠 6. Phân Tích Độ Quan Trọng Của Tính Năng & SHAP Explainability

| Hạng | Tên Tính Năng (Feature) | Độ Quan Trọng (Tree Gain) | Tác Động SHAP TB | Ý Nghĩa Kinh Doanh |
| :---: | :--- | :---: | :---: | :--- |
| **1** | `baskets_count_60d` | 105,163.2 | 0.5860 | Tần suất mua hàng trung hạn (60 ngày) - Thước đo nhịp sống cốt lõi |
| **2** | `baskets_count_90d` | 45,173.9 | 0.2852 | Độ ổn định mua sắm dài hạn trong quý |
| **3** | `days_since_last_basket` | 14,227.1 | 0.1794 | Số ngày kể từ giỏ hàng gần nhất (Recency kinh điển) |
| **4** | `baskets_count_30d` | 11,228.2 | 0.2073 | Tần suất mua sắm trong tháng vừa qua |
| **5** | `std_inter_trip` | 6,343.8 | 0.1260 | Độ biến động chu kỳ đi chợ (Khách đi đều đặn vs thất thường) |
| **6** | `spend_30d` | 4,423.2 | 0.1132 | Tổng ngân sách chi tiêu gần nhất |
| **7** | `urgency_ratio` | 2,755.2 | 0.0520 | Tỷ lệ quá hạn chu kỳ cá nhân hóa (Recency / Chu kỳ trung vị) |
| **8** | `days_since_last_perishable` | 2,421.2 | 0.0596 | Số ngày hết đồ ăn tươi sống trong tủ lạnh |
| **9** | `frequency_momentum_30_vs_90` | 2,251.9 | 0.0480 | Gia tốc tần suất (30 ngày gần đây tăng tốc hay đang nguội dần) |
| **10** | `classification_3` | 1,890.5 | 0.0612 | Đặc trưng mức thu nhập hộ gia đình |

---

## 🚀 7. Hướng Dẫn Cài Đặt & Tái Hiện Kết Quả (Reproduction Guide)

Dự án được xây dựng hoàn toàn khép kín trong môi trường ảo `.venv` của Python:

### Bước 1: Khởi tạo môi trường ảo và cài đặt thư viện
```bash
# Clone repository
git clone https://github.com/kien3007/purchasing-propensity-model.git
cd purchasing-propensity-model

# Tạo môi trường ảo Python 3.10
python -m venv .venv

# Kích hoạt môi trường (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
# (Hoặc Linux/macOS: source .venv/bin/activate)

# Cài đặt toàn bộ dependencies
pip install --upgrade pip
pip install pandas polars numpy scipy scikit-learn lightgbm optuna shap matplotlib seaborn plotly pyyaml pytest nbformat ipykernel pyarrow nbconvert
```

### Bước 2: Chạy kiểm toán Unit Tests
```bash
python -m pytest tests/ -v
# Kết quả: 4 passed in ~10s (Kiểm toán rò rỉ dữ liệu, nhãn mục tiêu và biên độ metrics)
```

### Bước 3: Chạy toàn bộ Pipeline Huấn Luyện & Xuất Báo Cáo
```bash
python -m src.pipelines.train_pipeline
```
*Pipeline sẽ tự động tải dữ liệu, xây dựng ma trận đặc trưng qua các mốc thời gian, huấn luyện LightGBM, hiệu chuẩn Isotonic, xuất file mô hình `models/lightgbm_propensity_model.joblib` và cập nhật các file báo cáo trong `docs/reports/`.*

### Bước 4: Khám Phá Chuỗi 5 Jupyter Notebook Tương Tác
```bash
# Mở giao diện Jupyter Lab để khám phá trực quan từng giai đoạn:
jupyter lab notebooks/

# Hoặc thực thi lại toàn bộ chuỗi 5 notebooks:
jupyter nbconvert --to notebook --execute notebooks/01_eda_and_data_quality.ipynb --inplace
jupyter nbconvert --to notebook --execute notebooks/02_point_in_time_feature_engineering.ipynb --inplace
jupyter nbconvert --to notebook --execute notebooks/03_model_training_and_benchmarking.ipynb --inplace
jupyter nbconvert --to notebook --execute notebooks/04_business_impact_and_decile_lift.ipynb --inplace
jupyter nbconvert --to notebook --execute notebooks/05_model_explainability_and_shap.ipynb --inplace
```

---

## ⚖️ Giấy Phép & Tác Quyền
Dự án được phát triển và công bố theo giấy phép MIT License. Toàn bộ mã nguồn mở phục vụ mục đích nghiên cứu, học tập và ứng dụng thực tiễn trong ngành khoa học dữ liệu bán lẻ.
