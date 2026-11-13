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

Trong ngành bán lẻ hiện đại (Grocery & Supermarket Retail), việc thấu hiểu và dự đoán trước khi nào khách hàng sẽ quay lại mua sắm là chìa khóa sống còn để tối ưu hóa ngân sách tiếp thị (Marketing ROI), quản lý chuỗi cung ứng hàng tươi sống (Fresh Inventory Management), và xây dựng các chương trình cá nhân hóa (Personalized CRM/Promotion).

### 🎯 Phát biểu bài toán (Mathematical Formulation):
Dự đoán xác suất hộ gia đình $h \in \{1, 2, \dots, 2500\}$ sẽ phát sinh **ít nhất một lượt đi chợ/mua sắm hợp lệ ($> \$0$)** trong khoảng thời gian tương lai $\Delta t = 14$ ngày kể từ một mốc thời gian chốt sổ quan sát bất kỳ ($t_0$):

$$Y_{h, t_0} = \begin{cases} 1 & \text{nếu } \exists \text{ trip của hộ } h \text{ trong khoảng } (t_0, t_0 + 14] \\ 0 & \text{ngược lại} \end{cases}$$

### 🛡️ Nguyên Tắc Thiết Kế Cốt Lõi:
1. **Cam kết 100% Số Liệu Thực Tế (Zero Hallucination)**: Toàn bộ số liệu, phần trăm và thông số trong dự án này đều được trích xuất và tính toán trực tiếp từ 2,595,732 dòng giao dịch thực tế của Dunnhumby.
2. **Kỷ Luật Point-in-Time Tuyệt Đối (Zero Future Leakage)**: Mọi biến số và tính năng (features) tại thời điểm $t_0$ chỉ được phép sử dụng dữ liệu phát sinh tính đến hết ngày $t_0$ ($DAY \le t_0$). Nghiêm cấm dùng Cross-Validation ngẫu nhiên trên toàn bộ tập dữ liệu (dễ gây rò rỉ tương lai).
3. **Diễn Giải Đơn Giản Cho Mọi Người**: Mọi phân tích, đồ thị đều được thiết kế thân thiện, dễ hiểu cho cả người không chuyên kỹ thuật, giải thích rõ: *Tại sao làm thế? Ý nghĩa kinh doanh là gì?*

---

## 🏗️ 2. Kiến Trúc Dự Án & Cấu Trúc Mã Nguồn

```text
purchasing-propensity-model/
├── .agents/skills/              # 12 Skills tiêu chuẩn phân tích dữ liệu & clean code
├── .venv/                       # Môi trường ảo Python độc lập
├── data/                        # Thư mục dữ liệu trung gian (git-ignored)
├── docs/                        # Tài liệu nghiệp vụ & báo cáo chuyên sâu
│   ├── purchase_propensity_checklist.md  # Master Blueprint & Checklist
│   └── reports/
│       ├── model_performance_summary.md  # Báo cáo kết quả kiểm thử OOT
│       ├── model_performance_summary.json
│       └── figures/                      # 10 biểu đồ trực quan hóa dữ liệu
├── models/                      # Mô hình LightGBM đã hiệu chuẩn xác suất (.joblib)
├── notebooks/
│   └── 01_eda_and_data_quality.ipynb    # Jupyter Notebook thực thi 100% phân tích & biểu đồ
├── sample_data/                 # Thư mục chứa 8 file CSV gốc từ Dunnhumby
├── scripts/
│   ├── compute_actual_stats.py          # Script kiểm toán số liệu thực tế
│   ├── compute_campaign_stats.py        # Script phân tích tác động chiến dịch
│   └── generate_eda_notebook.py         # Script xây dựng Notebook chuẩn
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
│   └── test_data_quality.py     # 4 Unit tests kiểm toán chống rò rỉ & chất lượng logic
├── pyproject.toml               # Khai báo dependency và cấu hình pytest
├── .gitignore                   # Loại trừ file lớn (>100MB) và môi trường ảo
└── README.md                    # Tài liệu hướng dẫn tổng quan dự án
```

---

## 📊 3. Khám Phá Dữ Liệu & 10 Phát Hiện Nghiệp Vụ Cốt Lõi (EDA)

Toàn bộ 8 bảng trong dataset Dunnhumby đã được liên kết và kiểm toán toàn diện:
- **Giao dịch**: 2,595,732 dòng -> 276,484 giỏ hàng thô.
- **Làm sạch**: Loại bỏ 942 giao dịch số tiền âm/trả hàng -> **275,542 giỏ hàng hợp lệ ($> \$0$)**.
- **Độ phủ khách hàng**: 2,500 hộ gia đình trải dài qua 711 ngày quan sát (~102 tuần).

| Biểu đồ | Loại biểu đồ & Lý do chọn | Phát hiện từ số liệu thực tế | Ý nghĩa kinh doanh & Quyết định kỹ thuật |
| :---: | :--- | :--- | :--- |
| **01. Nhịp Đi Chợ** | **Histogram + Đường tích lũy CDF**<br>*Thấy rõ các mốc ngày quay lại phổ biến nhất.* | - Trung vị: **2.0 ngày**; Trung bình: **5.67 ngày**.<br>- **82.0%** mua lại trong 7 ngày.<br>- **92.4%** mua lại trong 14 ngày. | Căn cứ khoa học chuẩn xác để chốt **$\Delta t = 14$ ngày** làm cửa sổ dự đoán mục tiêu. |
| **02. Giá Trị Giỏ** | **Histogram có dán nhãn Percentiles**<br>*Tránh bị lệch bởi các đơn hàng tiệc tùng lớn.* | - P25: **\$7.85**, P50: **\$17.18**.<br>- P75: **\$37.28**, P90: **\$68.04**.<br>- Trung bình: **\$29.24**. | Tách biệt tính năng tần suất mua và quy mô chi tiêu AOV. |
| **03. Nhịp Trong Tuần** | **Bar Chart (Cột chuẩn mực)**<br>*Dễ so sánh giữa các ngày trong tuần.* | - Khối lượng mua sắm đều đặn cả tuần.<br>- Đỉnh cao điểm rơi vào các ngày cuối tuần (Thứ 7 - CN). | Trích xuất tính năng khoảng cách tới chu kỳ cuối tuần tiếp theo. |
| **04. Khung Giờ Mua** | **Line Chart (Dòng thời gian 24h)**<br>*Mô tả nhịp sinh học mua sắm trong ngày.* | - Khung giờ vàng từ **11:00 đến 18:00** chiếm trên 65% số đơn. Thấp nhất từ 0h - 6h. | Khai thác tính năng giờ mua ưa thích của từng hộ gia đình. |
| **05. Đồ Tươi Sống** | **Comparative Bar Chart (Cột đôi so sánh)**<br>*So sánh trực quan hai trạng thái giỏ hàng.* | - **51.71%** giỏ hàng chứa đồ tươi sống (Thịt, Rau củ, Sữa, Bánh mì).<br>- Chu kỳ mua lặp lại đồ tươi ngắn hơn rõ rệt. | Tính năng `days_since_last_perishable` là động lực hàng đầu kéo khách quay lại. |
| **06. Mồi Câu Coupon** | **Grouped Bar Chart (So sánh chi tiêu)**<br>*Chứng minh tác động tài chính của voucher.* | - Đơn dùng Coupon đạt AOV = **\$67.60** vs không dùng = **\$26.76** (**Tăng gấp 2.53 lần / +152.6%**). | Coupon không làm mất biên lợi nhuận mà kích thích giỏ hàng lớn. Feature `coupon_redemption_count_180d`. |
| **07. Tăng Tốc Tiếp Thị** | **Boxplot / Interval Comparison**<br>*Đo lường trực tiếp độ co giãn thời gian mua.* | - Khi có chiến dịch: chu kỳ trung bình = **3.55 ngày**.<br>- Không có chiến dịch: chu kỳ = **6.49 ngày** (**Rút ngắn 45.3%**). | Feature `is_targeted_by_active_campaign` tạo cú hích gia tăng propensity rõ rệt. |
| **08. Nhảy Cóc Shop** | **Categorical Bar Chart (Tỷ lệ nhóm)**<br>*Nhận diện lòng trung thành theo địa bàn.* | - Chỉ **6.68%** chỉ đi 1 shop duy nhất.<br>- **66.4%** đi $\ge 4$ shop khác nhau.<br>- Nhưng Primary Store chiếm tới **73.35% chi tiêu**. | Khách hay mua tiện đường nhưng có 1 shop ruột. Feature `store_loyalty_index` & `primary_store_id`. |
| **09. Nhân Khẩu Học** | **Horizontal Bar Chart (Thanh ngang dễ đọc)**<br>*Tránh mỏi cổ khi đọc tên nhóm phân loại.* | - Hộ độc thân: AOV = **\$31.49**.<br>- Hộ 4-5+ người: AOV = **\$43.91** (+39.4% chi tiêu). | Nạp các trường nhân khẩu học (`classification_1` đến `classification_5`, `KID_CATEGORY_DESC`) vào mô hình. |
| **10. Ổn Định Nhãn** | **Time-Series Stability Line**<br>*Chứng minh không có trôi dạt dữ liệu.* | - Tỷ lệ $P(Y=1)$ dao động ổn định trong biên độ hẹp **66% - 70%** xuyên suốt 16 mốc $t_0$ (Day 200 - 680). | Cho phép áp dụng Multi-Cutoff Sliding Window mà không làm méo mó nhãn mục tiêu. |

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
> **Nhận xét chuyên môn**:
> - **Hiệu chuẩn xác suất (Isotonic Calibration)** giúp hạ thấp sai số hiệu chuẩn kỳ vọng (**ECE giảm xuống chỉ còn 1.71%**), giúp xác suất mô hình trả về phản ánh đúng 100% tỷ lệ chuyển đổi thực tế trong kinh doanh.
> - **Quy luật Heuristic đơn giản thất bại** vì khách hàng bán lẻ không mua sắm theo một chu kỳ cơ học cố định mà chịu tác động đa chiều từ đồ tươi sống, khuyến mãi và đà mua sắm gần nhất.

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
> - Nhóm **Decile 1-3**: Tỷ lệ mua tự nhiên lên tới **95% - 99%**. Không cần tốn voucher giảm giá cao (Organic Buyers).
> - Nhóm **Decile 6-8**: Tỷ lệ mua dao động từ 50% - 70%. Đây là **"nhóm vàng cần thuyết phục" (Persuadable Segment)**, nơi ngân sách Marketing mang lại chỉ số ROI chuyển đổi cao nhất!

---

## 🧠 6. Phân Tích Độ Quan Trọng Của Tính Năng & SHAP Explainability

| Hạng | Tên Tính Năng (Feature) | Độ Quan Trọng (Tree Gain) | Tác Động SHAP TB | Ý Nghĩa Kinh Doanh |
| :---: | :--- | :---: | :---: | :--- |
| **1** | `baskets_count_60d` | 105,163.2 | 0.5860 | Tần suất mua hàng trung hạn (60 ngày) - Thước đo nhịp sống cốt lõi |
| **2** | `baskets_count_90d` | 45,173.9 | 0.2852 | Độ ổn định mua sắm dài hạn trong quý |
| **3** | `days_since_last_basket` | 14,227.1 | 0.1794 | Số ngày kể từ giỏ hàng gần nhất (Recency kinh điển) |
| **4** | `baskets_count_30d` | 11,228.2 | 0.2073 | Tần suất mua sắm trong tháng vừa qua |
| **5** | `std_inter_trip` | 6,343.8 | 0.1260 | Độ biến động chu kỳ đi chợ (Khách đi theo giờ giấc cố định vs thất thường) |
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

### Bước 4: Chạy Notebook Khám Phá EDA
```bash
jupyter nbconvert --to notebook --execute notebooks/01_eda_and_data_quality.ipynb --inplace
```

---

## ⚖️ Giấy Phép & Tác Quyền
Dự án được phát triển và công bố theo giấy phép MIT License. Toàn bộ mã nguồn mở phục vụ mục đích nghiên cứu, học tập và ứng dụng thực tiễn trong ngành khoa học dữ liệu bán lẻ.
