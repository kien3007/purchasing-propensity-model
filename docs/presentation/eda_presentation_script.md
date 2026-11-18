# Kịch bản trình bày báo cáo khám phá dữ liệu & kiểm toán chất lượng (EDA & Data Quality)

**Dự án:** Mô hình dự đoán xác suất mua hàng của hộ gia đình (Purchasing Propensity Model)  
**Tập dữ liệu:** Dunnhumby - The Complete Journey (2.59M dòng giao dịch, 275,542 giỏ hàng sạch, 2,500 hộ gia đình, 711 ngày)  
**Thời lượng dự kiến:** 12 – 14 phút thuyết trình + 5 phút Q&A  

---

## Cấu trúc tổng thể bài trình bày (Narrative Arc)

```
[Mở đầu & Nền tảng dữ liệu] (Slide 1–3, ~2 phút)
   │  • Slide 1: Tiêu đề báo cáo & mục tiêu nghiên cứu
   │  • Slide 2: Mục tiêu & cấu trúc 18 slide (tách bạch ML vs Góc nhìn kinh doanh)
   │  • Slide 3: Kiến trúc 8 bảng & kết quả kiểm toán chất lượng dữ liệu
   │
├──> [Khung dự báo & Phân phối cơ sở] (Slide 4–5, ~2 phút)
   │  • Slide 4: Phân phối giá trị giỏ hàng thực nghiệm (AOV) & độ lệch phải
   │  • Slide 5: Cơ sở khoa học chọn cửa sổ dự báo Δt = 14 ngày (Đường cong Horizon H ∈ [1, 56])
   │
├──> [Phân tích 9 nhóm đặc trưng ML theo chuẩn vàng P(Y=1)] (Slide 6–13, ~6 phút)
   │  • Slide 6: Recency — Số ngày chưa mua hàng vs P(Y=1) (Δ = -64.4 điểm phần trăm)
   │  • Slide 7: Frequency — Tần suất mua sắm 90 ngày vs P(Y=1) (Δ = +85.8 điểm phần trăm)
   │  • Slide 8: Spend / Monetary — Tổng chi tiêu 90 ngày vs P(Y=1) & điểm bão hòa
   │  • Slide 9: Perishables — Chu kỳ cạn thực phẩm tươi sống thúc đẩy chuyến đi kế tiếp
   │  • Slide 10: Category Breadth — Độ rộng ngành hàng 90 ngày vs P(Y=1) (Δ = +64.7 điểm phần trăm)
   │  • Slide 11: Marketing Campaigns — Tác động tiếp cận chiến dịch tại t₀ & phễu đổi phiếu
   │  • Slide 12: Coupon Sensitivity — Lịch sử đổi phiếu giảm giá 180 ngày vs P(Y=1)
   │  • Slide 13: Demographics — Tín hiệu phân tách của nhóm khuyết thiếu UNKNOWN (n = 1,699)
   │
├──> [Ma trận chuyển giao sang mô hình hóa] (Slide 14, ~1.5 phút)
   │  • Slide 14: Bảng đặc trưng Point-in-Time, chiều tác động, bảo đảm không rò rỉ dữ liệu
   │
└──> [Phụ lục: Góc nhìn chiến lược bán lẻ & Vận hành] (Slide 15–18, ~2.5 phút)
      • Slide 15: Phụ lục 1 — Mức độ tập trung doanh thu theo hộ gia đình (Gini = 0.503)
      • Slide 16: Phụ lục 2 — Cấu trúc chiết khấu hai tầng (Giảm giá quầy gấp 32.8 lần coupon)
      • Slide 17: Phụ lục 3 — Tỷ trọng & hiệu suất doanh thu/SKU của nhãn hàng riêng (Private Label)
      • Slide 18: Phụ lục 4 — Phân phối thời gian mua sắm theo chu kỳ ngày và khung giờ
```

---

## Kịch bản chi tiết từng slide (Slide-by-Slide Script)

---

### Slide 1: Tiêu đề báo cáo
* **Tiêu đề:** Khám phá dữ liệu và kiểm toán chất lượng dữ liệu (EDA & Data Quality)
* **Phụ đề:** Cơ sở thực nghiệm xây dựng mô hình dự đoán xác suất mua hàng bán lẻ
* **Thời lượng:** 30 giây
* **Phong thái:** Chuyên nghiệp, trực diện, tự tin.

**Lời thoại trình bày:**
> *"Kính chào quý thầy cô, hội đồng đánh giá và các bạn đồng nghiệp. Hôm nay, tôi xin đại diện nhóm trình bày báo cáo về giai đoạn **Khám phá Dữ liệu (EDA) và Kiểm toán Chất lượng Dữ liệu** cho bài toán Dự đoán xác suất mua hàng của hộ gia đình.*
>
> *Khác với cách tiếp cận mô tả thống kê thuần túy, toàn bộ giai đoạn EDA trong dự án này được thiết kế như **cơ sở thực nghiệm định lượng cho bài toán học máy**: kiểm toán triệt để các nguồn nhiễu nghiệp vụ, chứng minh cơ sở chọn cửa sổ dự báo $\Delta t = 14$ ngày, và kiểm định thực nghiệm từng nhóm đặc trưng bằng mối liên hệ trực tiếp với biến mục tiêu $P(Y=1)$. Đồng thời, chúng tôi tách bạch rõ ràng giữa các đặc trưng phục vụ mô hình học máy và các phân tích phụ lục phục vụ góc nhìn chiến lược kinh doanh."*

---

### Slide 2: Mục tiêu và cấu trúc báo cáo khám phá dữ liệu
* **Tiêu đề:** 1. Mục tiêu và cấu trúc báo cáo khám phá dữ liệu
* **Thời lượng:** 45 giây
* **Trực quan:** 2 khối nội dung: 4 mục tiêu cốt lõi bên trái và cấu trúc 18 slide bên phải.

**Lời thoại trình bày:**
> *"Báo cáo được triển khai với 4 mục tiêu cốt lõi:
> 1. **Kiểm toán chất lượng dữ liệu:** Làm sạch các giao dịch dị biệt $\le \$0$, khử trùng bản ghi coupon, và xử lý dữ liệu nhân khẩu học khuyết thiếu.
> 2. **Xác lập khung dự báo khoa học:** Chứng minh cơ sở chọn cửa sổ dự báo $\Delta t = 14$ ngày bằng đường cong tỷ lệ hộ gia đình theo horizon thời gian $H \in [1, 56]$.
> 3. **Kiểm định khả năng phân tách của đặc trưng:** Mọi đặc trưng đề xuất đều được kiểm tra thực nghiệm thông qua xác suất mua hàng thực tế $P(Y=1)$ và so sánh với mức trung bình nền tảng (base rate).
> 4. **Tách bạch góc nhìn:** 14 slide đầu tập trung hoàn toàn vào nền tảng bài toán học máy; 4 slide phụ lục cuối dành riêng cho các phân tích chiến lược bán lẻ và vận hành.
>
> Toàn bộ deck gồm 18 slide, đi từ nền tảng dữ liệu đến ma trận chuyển giao đặc trưng cho mô hình LightGBM."*

---

### Slide 3: Kiến trúc dữ liệu và kết quả kiểm toán chất lượng
* **Tiêu đề:** 2. Kiến trúc 8 bảng dữ liệu và kết quả kiểm toán làm sạch
* **Thời lượng:** 60 giây
* **Trực quan:** Sơ đồ thực thể liên kết (ERD) 8 bảng dữ liệu bên trái và danh sách kết quả kiểm toán, xử lý làm sạch ở cột bên phải.

**Lời thoại trình bày:**
> *"Trên màn hình bên trái là sơ đồ kiến trúc tổng thể 8 bảng dữ liệu trong hệ sinh thái Dunnhumby, chia thành hai khối: các bảng dữ liệu phát sinh (Data tables) xoay quanh `transaction_data`, và các bảng danh mục tra cứu (Lookup tables).
>
> Ở cột bên phải là các kết quả xử lý dữ liệu then chốt đã hoàn tất:
> 1. **`transaction_data` (2.6M dòng):** Loại bỏ triệt để 942 giỏ hàng hoàn/hủy/tặng $0 (0.34% giỏ, $0 doanh thu); bảo toàn 275,542 giỏ hàng thương mại sạch cho toàn bộ 2,500 hộ gia đình trong 711 ngày.
> 2. **`coupon` (124.5k dòng):** Khử trùng 5,164 bản ghi trùng lặp 100% (exact duplicates); thu gọn về 119,384 dòng ánh xạ SKU hợp lệ để tránh rủi ro nhân đôi dòng khi join.
> 3. **`hh_demographic` (801 hộ, 32.0%):** Không drop 68% hộ thiếu (tránh sai lệch chọn mẫu); chuẩn hóa thành nhóm `UNKNOWN` độc lập, bảo toàn trọn vẹn 100% tập 2,500 hộ gia đình.
> 4. **`campaigns` & `campaign_desc`:** Chuẩn hóa 3 loại chiến dịch (Loại A, B, C) gửi đến 1,584 hộ; kiểm toán `coupon_redempt` (2,318 lượt đổi) đạt 0 bản ghi trùng lặp.
> 5. **`product` (92.4k SKU):** Bóc tách danh mục thực phẩm tươi sống (`perishables`) cho 44 ngành hàng để xây dựng chỉ báo chu kỳ tiêu dùng nhanh.
> 6. **`causal_data` (36.8 triệu dòng):** Chủ động loại bỏ khỏi baseline mô hình do dữ liệu ở cấp cửa hàng/tuần (*store-week*), độ thưa cao, không đo trực tiếp hành vi cấp hộ gia đình."*

---

### Slide 4: Phân phối giá trị giỏ hàng thực nghiệm (AOV)
* **Tiêu đề:** 3. Phân phối giá trị giỏ hàng thực nghiệm (AOV)
* **Biểu đồ:** Histogram & KDE của giá trị giỏ hàng (Basket Spend) kèm các đường phân vị P25, P50, P75, P90 và Mean.
* **Thời lượng:** 50 giây
* **Trực quan:** Biểu đồ lệch phải rõ rệt; đường trung vị P50 = $17.18 khác xa đường trung bình Mean = $29.24.

**Lời thoại trình bày:**
> *"Bước sang phân tích hành vi, Slide 4 thể hiện phân phối giá trị của toàn bộ 275,542 giỏ hàng sạch trong tập dữ liệu.
>
> Đặc điểm nổi bật nhất là **phân phối lệch phải rất mạnh (Right-skewed)**:
> * Giá trị trung vị (P50) chỉ đạt **\$17.18**, với khoảng liên phân vị IQR là **\$29.40** (từ P25 = \$6.99 đến P75 = \$36.39).
> * Giá trị trung bình bị kéo lên tới **\$29.24** do tác động của đuôi dài các giỏ hàng lớn (P90 đạt **\$70.79**, và các giỏ trên \$150 chiếm khoảng 1.5% tổng số giỏ).
>
> Phát hiện này dẫn tới một nguyên tắc quan trọng: Trong bài toán phân tích giỏ hàng, **trung vị (P50 = \$17.18) phản ánh trung thực hơn quy mô chi tiêu điển hình** của một lần đi chợ so với giá trị trung bình. Đồng thời, mô hình hóa cần các biến quy đổi logarit hoặc phân vị để giảm thiểu ảnh hưởng của các giá trị ngoại lai cực lớn."*

---

### Slide 5: Cơ sở khoa học chọn cửa sổ dự báo nhãn $\Delta t = 14$ ngày
* **Tiêu đề:** 4. Cơ sở khoa học chọn cửa sổ dự báo nhãn $\Delta t = 14$ ngày
* **Biểu đồ:** Tỷ lệ hộ gia đình có $\ge 1$ giao dịch theo độ dài cửa sổ tương lai $H \in [1, 56]$ ngày.
* **Thời lượng:** 60 giây
* **Trực quan:** Đường cong tích lũy tăng nhanh ở 1–14 ngày và thoải dần sau đó; mốc H=14 ngày được đánh dấu nổi bật tại 68.34%.

**Lời thoại trình bày:**
> *"Một câu hỏi nền tảng của bài toán: **Tại sao lại chọn cửa sổ nhãn $\Delta t = 14$ ngày mà không phải 7 hay 28 ngày?**
>
> Để trả lời chặt chẽ, chúng tôi không chỉ nhìn vào khoảng cách giữa các chuyến đi vốn bị chi phối bởi các hộ mua nhiều, mà tính toán **tỷ lệ hộ gia đình có phát sinh $\ge 1$ giao dịch trong $H$ ngày tới**, trung bình qua nhiều mốc quan sát $t_0$:
> * Tại **$H = 7$ ngày**: Chỉ có **53.36%** số hộ phát sinh giao dịch. Cửa sổ này quá ngắn, làm sót những hộ có chu kỳ đi chợ 10–14 ngày theo kỳ lương bán nguyệt, đồng thời gây áp lực quá lớn cho quy trình vận hành chiến dịch tiếp thị.
> * Tại **$H = 28$ ngày**: Tỷ lệ dương tính lên tới **80.18%**. Tỷ lệ này quá cao khiến mô hình mất đi tính phân loại và khả năng chọn lọc khách hàng cần can thiệp.
> * Tại **$H = 14$ ngày**: Tỷ lệ dương tính đạt **68.34%**, với độ lệch chuẩn giữa các mốc thời gian chỉ **$\pm 1.04\%$**.
>
> Mốc 14 ngày tạo ra điểm cân bằng tối ưu: vừa đủ bao quát chu kỳ tiêu dùng tự nhiên của đại đa số hộ gia đình, vừa mang lại cửa sổ 2 tuần đủ dài để bộ phận tiếp thị thiết kế và triển khai các chương trình kích cầu."*

---

### Slide 6: Thời gian chưa mua hàng vs Xác suất mua lại (Recency)
* **Tiêu đề:** 5. Mối quan hệ giữa thời gian chưa mua hàng và xác suất mua lại
* **Biểu đồ:** Xác suất $P(Y=1)$ theo các nhóm `days_since_last_basket` (Chuẩn vàng: cột xác suất, cỡ mẫu $n$, đường base rate 68.3%, độ chênh điểm phần trăm).
* **Thời lượng:** 50 giây
* **Trực quan:** Xu hướng giảm đơn điệu từ 88.5% xuống 24.1%; độ chênh -64.4 điểm phần trăm.

**Lời thoại trình bày:**
> *"Từ Slide 6 đến Slide 13, chúng tôi áp dụng một **khuôn mẫu trực quan chuẩn mực thống nhất**: Trục hoành là phân nhóm giá trị của đặc trưng, trục tung là xác suất mua hàng thực tế $P(Y=1)$ trong 14 ngày tới, trên mỗi cột hiển thị rõ tỷ lệ phần trăm và cỡ mẫu $n$, cùng đường tham chiếu mức trung bình nền tảng 68.3%.
>
> Slide 6 kiểm định đặc trưng **Recency (Số ngày kể từ lần mua gần nhất)**:
> * Hộ vừa mua trong vòng **0–3 ngày qua ($n = 959$)** có xác suất mua lại trong 14 ngày tới lên tới **88.5%** (cao hơn 20.2 điểm phần trăm so với mức trung bình).
> * Khi thời gian chưa mua kéo dài ra **4–7 ngày ($n = 436$)**, xác suất đạt **79.8%**; **8–14 ngày ($n = 337$)** đạt **69.9%**; **15–30 ngày ($n = 300$)** rơi xuống **54.9%**; và với nhóm **trên 30 ngày hoặc chưa mua ($n = 468$)**, xác suất sụt giảm mạnh về **24.0%**.
>
> Mức độ chênh lệch lên tới **-64.5 điểm phần trăm**. Đây là tín hiệu đơn điệu mạnh mẽ nhất trong dữ liệu, khẳng định `days_since_last_basket` là đặc trưng rường cột của mô hình."*

---

### Slide 7: Tần suất mua sắm trong 90 ngày vs Xác suất mua lại (Frequency)
* **Tiêu đề:** 6. Mối quan hệ giữa tần suất mua sắm trong 90 ngày và xác suất mua lại
* **Biểu đồ:** Xác suất $P(Y=1)$ theo các nhóm `baskets_count_90d` (0, 1–5, 6–12, 13–24, $\ge 25$).
* **Thời lượng:** 50 giây
* **Trực quan:** Xu hướng tăng đơn điệu vọt từ 12.3% lên 98.1%; độ chênh +85.8 điểm phần trăm.

**Lời thoại trình bày:**
> *"Slide 7 kiểm định đặc trưng **Frequency (Tần suất số giỏ hàng trong 90 ngày qua)**.
>
> Kết quả cho thấy mối quan hệ đồng biến hoàn hảo và biên độ phân tách rộng nhất toàn bộ nghiên cứu:
> * Nhóm hộ **không phát sinh giao dịch nào ($n = 198$)** có xác suất mua trong 14 ngày tới chỉ là **12.3%** — phản ánh nhóm khách hàng đã rời bỏ hoặc không hoạt động.
> * Xác suất tăng đều qua từng nấc: 1–5 giỏ đạt **41.1%**, 6–12 giỏ đạt **70.4%**, 13–24 giỏ đạt **89.8%**, và chạm ngưỡng **98.1%** ở nhóm đi chợ thường xuyên $\ge 25$ giỏ ($n = 477$).
>
> Biên độ phân tách đạt tới **+85.8 điểm phần trăm**. Điều này khẳng định tần suất mua sắm trong quá khứ gần là thước đo đáng tin cậy nhất về mức độ duy trì gắn kết của hộ gia đình."*

---

### Slide 8: Tổng chi tiêu 90 ngày vs Xác suất mua lại (Spend / Monetary)
* **Tiêu đề:** 7. Mối quan hệ giữa tổng chi tiêu 90 ngày và xác suất mua lại
* **Biểu đồ:** Xác suất $P(Y=1)$ theo các nhóm `spend_90d` ($0, <$300, $300–$700, $700–$1,300, $\ge $1,300).
* **Thời lượng:** 45 giây
* **Trực quan:** Đường cong tăng nhanh rồi bão hòa tiệm cận sau mốc $700.

**Lời thoại trình bày:**
> *"Slide 8 kiểm định thành tố thứ ba của bộ khung RFM: **Tổng chi tiêu tích lũy trong 90 ngày (`spend_90d`)**.
>
> Tương tự như tần suất, chi tiêu có quan hệ đồng biến mạnh với xác suất mua lại:
> * Hộ có chi tiêu \$0 chỉ có xác suất **12.3%**, nhóm dưới \$300 đạt **55.2%**.
> * Nhóm \$300–\$700 vọt lên **85.3%**, và nhóm chi tiêu cao $\ge \$1,300 ($n = 188$) đạt tới **98.7%**.
>
> Tuy nhiên, biểu đồ chỉ ra hiện tượng **bão hòa tiệm cận (Diminishing returns)**: Sau ngưỡng \$700, mức tăng xác suất chậm lại rõ rệt (từ 85.3% lên 94.0% và 98.7%). Khám phá này gợi ý việc áp dụng biến đổi phi tuyến như hàm căn bậc hai hoặc logarit cho các biến chi tiêu khi đưa vào mô hình học máy."*

---

### Slide 9: Chu kỳ mua thực phẩm tươi sống thúc đẩy lượt ghé thăm (Perishables)
* **Tiêu đề:** 8. Chu kỳ mua hàng thực phẩm tươi sống thúc đẩy lượt ghé thăm
* **Biểu đồ:** Xác suất $P(Y=1)$ theo số ngày kể từ lần mua đồ tươi gần nhất (`days_since_last_perishable`).
* **Thời lượng:** 50 giây
* **Trực quan:** Cột 1–3 ngày đạt 89.7%, giảm dần xuống 35.0% ở nhóm >30 ngày / chưa từng mua; độ chênh -54.7 điểm phần trăm.

**Lời thoại trình bày:**
> *"Slide 9 giải quyết một vấn đề quan trọng từng gây tranh cãi: **Vai trò thực sự của ngành hàng tươi sống (thịt, sữa, rau củ quả)**.
>
> Trong phân tích cấp giỏ hàng trước đây, những giỏ có đồ tươi thường là các chuyến đi chợ lớn nên khoảng cách đến lần mua sau có vẻ dài hơn. Để chứng minh đúng cơ chế vật lý của ngành hàng, chúng tôi theo dõi biến `days_since_last_perishable` tại cấp hộ gia đình:
> * Hộ gia đình vừa mua đồ tươi trong **1–3 ngày qua ($n = 658$)** có xác suất mua lại đạt **89.7%**.
> * Tỷ lệ này giảm dần theo thời gian: 4–7 ngày đạt **84.3%**, 8–14 ngày đạt **78.6%**, và nhóm trên 30 ngày hoặc chưa từng mua đồ tươi chỉ đạt **35.0%**.
>
> Độ chênh lệch đạt **-54.7 điểm phần trăm**. Do thực phẩm tươi sống có thời hạn bảo quản ngắn (3–5 ngày), nhu cầu tái bổ sung thực phẩm đóng vai trò như một chiếc 'đồng hồ đếm ngược' kéo khách hàng quay lại siêu thị. Đây là căn cứ để tạo biến `days_since_last_perishable`."*

---

### Slide 10: Tác động của độ rộng ngành hàng đối với xác suất mua lại (Category Breadth)
* **Tiêu đề:** 9. Tác động của độ rộng ngành hàng đối với xác suất mua lại
* **Biểu đồ:** Xác suất $P(Y=1)$ theo số ngành hàng đã mua trong 90 ngày (`department_breadth_90d`).
* **Thời lượng:** 50 giây
* **Trực quan:** 5 cột bao quát đủ 2,500 hộ: 0 ngành đạt 12.3%, 1–2 ngành đạt 31.8%, tăng dần lên 96.5% ở nhóm $\ge 12$ ngành; độ phân tách đạt 84.2 điểm phần trăm.

**Lời thoại trình bày:**
> *"Slide 10 phân tích mức độ đa dạng danh mục mua sắm thông qua biến `department_breadth_90d`.
>
> Biểu đồ bao quát trọn vẹn 100% tập mẫu 2,500 hộ gia đình phân theo 5 mức độ rộng danh mục:
> * Nhóm **không mua gì trong 90 ngày (0 ngành, $n = 198$)** có xác suất mua 14 ngày tới chỉ đạt **12.3%**.
> * Nhóm **đơn ngành (1–2 ngành, $n = 160$)** đạt **31.8%** — phản ánh những khách hàng chỉ ghé tiện đường mua một vài món đồ lẻ.
> * Khi danh mục mở rộng lên **thứ yếu (3–6 ngành, $n = 723$)**, xác suất đạt **57.8%**; **phổ thông (7–11 ngành, $n = 1,178$)** đạt **83.5%**; và nhóm mua **toàn diện ($\ge 12$ ngành, $n = 241$)** đạt tới **96.5%**.
>
> Toàn bộ 2,500 hộ được bảo toàn nguyên vẹn, không có hộ nào biến mất; độ phân tách giữa nhóm toàn diện và nhóm không mua lên tới **84.2 điểm phần trăm** (96.5% so với 12.3%). Khi một gia đình mua sắm đa ngành, siêu thị đã trở thành điểm đến mua sắm thiết yếu trọn gói của họ."*

---

### Slide 11: Tác động của việc tiếp cận chiến dịch tiếp thị tới xác suất mua lại (Campaigns)
* **Tiêu đề:** 10. Tác động của việc tiếp cận chiến dịch tiếp thị tới xác suất mua lại
* **Biểu đồ:** Xác suất $P(Y=1)$ theo nhóm chiến dịch đang nhắm mục tiêu tại $t_0$ (Type A: 86.8%, Type B: 90.3%, Type C: 89.1% vs Không có chiến dịch: 59.9%).
* **Thời lượng:** 55 giây
* **Trực quan:** Các cột chiến dịch đều quanh mức 87%–90%, vượt trội so với mức 59.9% của nhóm không có chiến dịch.

**Lời thoại trình bày:**
> *"Slide 11 kiểm tra tác động của các chiến dịch gửi thư tiếp thị trực tiếp (Direct Mail) được kích hoạt tại thời điểm quan sát $t_0$.
>
> Khi hộ gia đình nằm trong danh sách nhắm mục tiêu của bất kỳ chiến dịch nào, xác suất mua hàng trong 14 ngày tới duy trì ở mức rất cao: **86.8% đối với Chiến dịch Loại A, 90.3% đối với Loại B, và 89.1% đối với Loại C**, so với mức chỉ **59.9%** ở nhóm không có chiến dịch nào đang hoạt động.
>
> Về tỷ lệ chuyển đổi thực tế (tính theo số cặp hộ gia đình – chiến dịch có $\ge 1$ lần đổi phiếu): **Loại A đạt 15.96% (635/3,979 cặp)**, cao gấp hơn **2 lần** so với Loại B (7.91%) và Loại C (7.67%).
>
> *Lưu ý về mặt nhân quả:* Cần nhìn nhận khách quan rằng những hộ được nhắm mục tiêu vốn đã là nhóm có lịch sử mua sắm tích cực hơn. Tuy nhiên, về mặt học máy, cờ trạng thái `is_targeted_by_active_campaign` tại $t_0$ là một đặc trưng ngoại sinh hoàn toàn hợp lệ, nắm bắt sự kết hợp giữa mức độ ưu tiên của bộ phận tiếp thị và hành vi của hộ."*

---

### Slide 12: Tác động của lịch sử đổi coupon tới xác suất mua lại (Coupons)
* **Tiêu đề:** 11. Tác động của lịch sử đổi coupon tới xác suất mua lại
* **Biểu đồ:** Xác suất $P(Y=1)$ theo số lần đổi coupon trong 180 ngày (0 lần, 1–2 lần, $\ge 3$ lần).
* **Thời lượng:** 45 giây
* **Trực quan:** 0 lần (Chưa đổi) = 66.3% ($n=2,317$), 1–2 lần = 93.2% ($n=94$), $\ge 3$ lần = 93.6% ($n=90$).

**Lời thoại trình bày:**
> *"Slide 12 kiểm định hành vi sử dụng phiếu giảm giá trong cửa sổ 180 ngày qua biến `coupon_redemptions_180d`.
>
> Dữ liệu chỉ ra một đặc điểm rất thú vị:
> * Hành vi đổi coupon khá hiếm: Chỉ có **7.3% số hộ (183/2,500 hộ)** từng có ít nhất 1 lần đổi coupon trong 6 tháng qua.
> * Tuy nhiên, nhóm 183 hộ này có xác suất mua lại vượt trội: Đạt **93.2% ở nhóm đổi 1–2 lần** và **93.6% ở nhóm đổi $\ge 3$ lần**, cao hơn gần **27 điểm phần trăm** so với nhóm chưa từng đổi phiếu (66.3%).
>
> Dù chỉ là nhóm thiểu số, việc chủ động lưu giữ và đổi phiếu giảm giá là chỉ báo rõ ràng của nhóm khách hàng rất gắn bó. Đặc trưng này mang lại giá trị gia tăng rõ rệt cho mô hình."*

---

### Slide 13: Thông tin nhân khẩu học và giá trị của nhóm không khai báo (Demographics)
* **Tiêu đề:** 12. Thông tin nhân khẩu học và giá trị của nhóm không khai báo
* **Biểu đồ:** Xác suất $P(Y=1)$ theo quy mô hộ gia đình (1, 2, 3, 4, 5+ người) và nhóm UNKNOWN.
* **Thời lượng:** 50 giây
* **Trực quan:** 5 cột có khai báo đều phẳng ở mức 90%–92%, cột UNKNOWN sụt xuống 57.7% ($n = 1,699$).

**Lời thoại trình bày:**
> *"Slide 13 làm rõ giá trị thực sự của bảng nhân khẩu học đối với bài toán học máy:
>
> Trong số **801 hộ gia đình có khai báo thông tin**, xác suất mua hàng hầu như không có sự khác biệt theo quy mô hộ: 1 người đạt **92.4%**, 2 người đạt **89.7%**, 3 người đạt **90.8%**, 4 người đạt **92.1%**, và 5+ người đạt **90.3%**. Như vậy, số lượng thành viên trong gia đình không tạo ra sự phân tách về xác suất mua.
>
> Ngược lại, **tín hiệu phân tách mạnh nhất lại nằm ở chính 1,699 hộ khuyết thiếu (UNKNOWN)**: Xác suất mua hàng của nhóm này rơi xuống **57.7%**, thấp hơn từ **32 đến 34 điểm phần trăm** so với nhóm có khai báo.
>
> *Ý nghĩa thực tế:* Những hộ đăng ký làm thẻ thành viên và cung cấp thông tin nhân khẩu học vốn là nhóm khách hàng cốt lõi; trong khi nhóm không khai báo chứa nhiều khách vãng lai. Quyết định kỹ thuật của chúng tôi là **giữ nguyên nhóm `UNKNOWN` dưới dạng một biến danh mục độc lập**, không điền khuyết nhân tạo, giúp thuật toán cây tận dụng tối đa tín hiệu phân tách này."*

---

### Slide 14: Ma trận chuyển giao đặc trưng sang giai đoạn mô hình hóa
* **Tiêu đề:** 13. Ma trận chuyển giao đặc trưng sang giai đoạn mô hình hóa
* **Bảng:** Ma trận tổng hợp 9 nhóm đặc trưng, cửa sổ thời gian, tên biến đại diện, chiều quan hệ với $Y$, và ý nghĩa vật lý trong mô hình.
* **Thời lượng:** 60 giây
* **Trực quan:** Bảng hệ thống hóa khoa học; dòng cam bảo đảm kỹ thuật không rò rỉ dữ liệu.

**Lời thoại trình bày:**
> *"Trên Slide 14 là **Ma trận chuyển giao toàn diện** đúc kết từ 9 phát hiện thực nghiệm phía trước sang giai đoạn kỹ thuật đặc trưng (Feature Engineering):
>
> Hệ thống gồm 9 nhóm biến chủ đạo:
> 1. **Recency:** `days_since_last_basket`, `urgency_ratio` (Nghịch).
> 2. **Frequency:** `baskets_count_90d`, `freq_momentum` (Đồng).
> 3. **Spend & AOV:** `spend_90d`, `aov_90d`, `spend_trend` (Đồng).
> 4. **Category Breadth:** `department_breadth_90d`, `avg_items` (Đồng).
> 5. **Perishables:** `days_since_perishable`, `perish_ratio` (Nghịch).
> 6. **Campaigns:** `is_targeted_type_A`, `type_B`, `type_C` (Đồng).
> 7. **Coupons:** `coupon_redemptions_180d` (Đồng).
> 8. **Store Loyalty:** `primary_store_spend_share`, `store_id` (Đồng).
> 9. **Demographics:** `household_size`, `income`, `UNKNOWN` (Phân nhóm).
>
> *Bảo đảm kỹ thuật tối thượng:* **100% đặc trưng đều được tính toán nghiêm ngặt tại thời điểm $DAY \le t_0$**, tuyệt đối không sử dụng bất kỳ thông tin nào trong cửa sổ tương lai, loại bỏ hoàn toàn nguy cơ rò rỉ dữ liệu (data leakage) trước khi bước vào huấn luyện mô hình LightGBM."*

---

### Slide 15: Phụ lục 1 — Mức độ tập trung doanh thu theo hộ gia đình (Góc nhìn kinh doanh)
* **Tiêu đề:** 14. Phụ lục: Mức độ tập trung doanh thu theo hộ gia đình
* **Biểu đồ:** Đường cong tập trung doanh thu thực tế so với đường phân bổ bình đẳng ($45^\circ$) cho 2,500 hộ gia đình.
* **Thời lượng:** 45 giây
* **Trực quan:** Đường cong tập trung màu xanh nằm trên đường chéo; mốc Top 20% đạt 53.05% doanh thu; hệ số Gini = 0.503.

**Lời thoại trình bày:**
> *"Bây giờ, chúng ta bước vào 4 slide phụ lục dành cho các phân tích phục vụ góc nhìn chiến lược kinh doanh và vận hành bán lẻ.
>
> Slide 15 kiểm định **mức độ tập trung doanh thu của 2,500 hộ gia đình** qua tổng doanh số \$8.06 Triệu USD trong 2 năm:
> * Hệ số Gini đạt **0.503**, cho thấy mức độ bất bình đẳng vừa phải.
> * Top 10% hộ đóng góp **34.29% tổng doanh thu** (\$2.76 Triệu USD).
> * Top 20% hộ đóng góp **53.05% tổng doanh thu** (\$4.27 Triệu USD).
> * Để tích lũy được 80% tổng doanh thu, chuỗi siêu thị cần tới **44.0% số hộ gia đình**.
>
> Kết quả thực nghiệm cho thấy mức độ tập trung doanh thu trong bán lẻ thực phẩm thiết yếu thấp hơn nhiều so với quy tắc 80/20 lý thuyết hay các ngành hàng xa xỉ. Điều này khẳng định doanh nghiệp không thể chỉ dựa vào một nhóm nhỏ khách hàng siêu VIP, mà cần duy trì độ phủ phục vụ trên diện rộng."*

---

### Slide 16: Phụ lục 2 — Cấu trúc chiết khấu hai tầng trong bán lẻ (Góc nhìn kinh doanh)
* **Tiêu đề:** 15. Phụ lục: Cấu trúc chiết khấu hai tầng trong bán lẻ
* **Biểu đồ:** Đối sánh ngân sách và tỷ lệ bao phủ giỏ hàng giữa Giảm giá tại quầy (`RETAIL_DISC`) và Phiếu giảm giá (`COUPON_DISC`).
* **Thời lượng:** 45 giây
* **Trực quan:** Cột cam \$1.40M áp đảo cột xanh \$42.6k; tỷ lệ bao phủ 83.67% vs 6.08%.

**Lời thoại trình bày:**
> *"Slide 16 phân tích cấu trúc ngân sách chiết khấu của chuỗi siêu thị:
>
> Kết quả bóc tách hai nguồn giảm giá cho thấy:
> * **Giảm giá niêm yết tại quầy (`RETAIL_DISC`):** Đạt tới **\$1,398,352 USD**, chiếm **14.79% tổng doanh thu gộp**, và xuất hiện trong **83.67% tổng số giỏ hàng**.
> * **Giảm giá bằng phiếu coupon (`COUPON_DISC`):** Chỉ đạt **\$42,612 USD**, chiếm **0.53% doanh thu gộp**, và chỉ bao phủ **6.08% số giỏ hàng**.
>
> Ngân sách giảm giá tại quầy **gấp tới 32.8 lần** ngân sách coupon. Điều này cho thấy siêu thị sử dụng giảm giá niêm yết làm công cụ cạnh tranh giá đại trà hàng ngày; trong khi coupon chỉ đóng vai trò kích hoạt có chủ đích đối với một bộ phận khách hàng nhạy cảm về giá."*

---

### Slide 17: Phụ lục 3 — Tỷ trọng và vai trò của nhãn hàng riêng (Private Label) (Góc nhìn kinh doanh)
* **Tiêu đề:** 16. Phụ lục: Tỷ trọng và vai trò của nhãn hàng riêng
* **Biểu đồ:** Đối sánh tỷ trọng SKU (15.0%) vs Tỷ trọng Doanh thu (27.8%) và Tỷ trọng Sản lượng (28.8%).
* **Thời lượng:** 45 giây
* **Trực quan:** Cột xanh 15% SKU vươn lên gánh gần 28% doanh số và 29% sản lượng.

**Lời thoại trình bày:**
> *"Slide 17 cung cấp góc nhìn về quản trị danh mục mặt hàng qua hiệu suất của **Nhãn hàng riêng (Private Label)**:
>
> Trong tổng số hơn 92,000 mã hàng hóa, nhãn hàng riêng của siêu thị chỉ chiếm khiêm tốn **14.96% danh mục SKU** (13,812 SKU), nhường 85% danh mục cho các thương hiệu quốc gia.
>
> Thế nhưng, nhóm sản phẩm này đóng góp tới **27.77% tổng doanh thu** (\$2.24 Triệu USD) và chiếm **28.75% tổng sản lượng hàng hóa bán ra**. Chỉ số doanh thu trên mỗi SKU của nhãn hàng riêng đạt **1.86x**, cao gấp **2.18 lần** so với thương hiệu quốc gia (0.85x).
>
> *Lưu ý:* Tập dữ liệu không ghi nhận biên lợi nhuận, nên chúng tôi không kết luận về lợi nhuận ròng. Tuy nhiên, hiệu suất doanh thu vượt trội trên từng SKU chứng minh các dòng sản phẩm Private Label được quy hoạch danh mục rất hiệu quả và được người tiêu dùng đón nhận nồng nhiệt."*

---

### Slide 18: Phụ lục 4 — Phân phối thời gian mua sắm theo ngày và giờ (Góc nhìn kinh doanh)
* **Tiêu đề:** 17. Phụ lục: Phân phối thời gian mua sắm theo ngày và giờ
* **Biểu đồ:** Biểu đồ kết hợp: Phân phối theo chu kỳ ngày (`DAY mod 7`, bên trái) và Khung giờ mua sắm trong ngày (bên phải).
* **Thời lượng:** 45 giây
* **Trực quan:** Đỉnh chu kỳ ngày rơi vào Ngày 4 và Ngày 5 (~16% mỗi ngày); dải giờ vàng 11h–18h chiếm gần 65% giao dịch.

**Lời thoại trình bày:**
> *"Slide cuối cùng của phần phụ lục mô tả nhịp điệu thời gian vi mô trong hoạt động vận hành:
>
> * **Chu kỳ ngày (`DAY mod 7`):** Đỉnh giao dịch rơi vào Ngày 4 và Ngày 5, chiếm khoảng **16% mỗi ngày**. Hai ngày cuối chu kỳ chiếm **27.3%** tổng giao dịch (thấp hơn tỷ lệ lý thuyết 2/7 ≈ 28.6%). Cần lưu ý quan trọng: Dữ liệu Dunnhumby chỉ đánh số thứ tự ngày `DAY` từ 1 đến 711 mà không có mốc lịch dương thực tế; vì vậy không thể kết luận cảm tính đây là 'thứ Bảy hay Chủ Nhật'.
> * **Khung giờ trong ngày:** Giao dịch tập trung đậm đặc từ **11 giờ trưa đến 18 giờ chiều**, chiếm tới **64.9% tổng số giao dịch**, đạt đỉnh vào khoảng 16h–17h (9.3%/giờ).
>
> Thông tin này hỗ trợ công tác quản trị vận hành như điều phối ca trực quầy thu ngân và tiếp tế hàng hóa vào các khung giờ cao điểm.
>
> Toàn bộ 18 slide đã khép lại bức tranh thực nghiệm hoàn chỉnh của giai đoạn EDA. Xin chân thành cảm ơn quý thầy cô và các bạn đã chú ý lắng nghe. Nhóm chúng tôi xin sẵn sàng đón nhận các câu hỏi thảo luận ạ!"*

---

## Bộ câu hỏi & trả lời dự phòng cho phần Q&A (Anticipated Q&A)

### Câu hỏi 1: Tại sao nhóm chọn cửa sổ nhãn $\Delta t = 14$ ngày dựa trên tỷ lệ hộ thay vì khoảng cách giữa các chuyến đi chợ?
* **Trả lời:**
  > *"Khoảng cách giữa các chuyến đi chợ (Inter-trip interval) được tính trên từng cặp giao dịch liên tiếp. Cách tính này bị thiên lệch nặng nề (weighted) bởi những hộ đi chợ nhiều lần: một hộ đi 100 lần sẽ đóng góp 99 khoảng cách ngắn, trong khi hộ đi 2 lần chỉ đóng góp 1 khoảng cách. Kết luận cửa sổ dựa trên inter-trip sẽ đánh đồng tần suất giỏ hàng với tần suất hộ gia đình.
  >
  > Ngược lại, bài toán của chúng ta dự đoán ở **cấp độ hộ gia đình**: 'Hộ này có mua trong $H$ ngày tới hay không?'. Vì vậy, việc quét horizon $H \in [1, 56]$ ngày để đếm chính xác bao nhiêu phần trăm hộ gia đình có $\ge 1$ giao dịch qua nhiều mốc chốt sổ $t_0$ là cách tiếp cận khoa học và chuẩn xác nhất. Kết quả thực nghiệm cho thấy tại $H = 14$ ngày, tỷ lệ dương tính là 68.34% với độ ổn định rất cao ($\pm 1.04\%$), tạo điều kiện lý tưởng cho cả mô hình hóa và vận hành CRM."*

### Câu hỏi 2: Mối quan hệ giữa tiếp cận chiến dịch tiếp thị (Campaigns) và xác suất mua lại có phải là quan hệ nhân quả (Causality) không?
* **Trả lời:**
  > *"Hoàn toàn không thể khẳng định đây là quan hệ nhân quả thuần túy chỉ từ dữ liệu quan sát. Trong thực tế bán lẻ, các thuật toán tiếp thị thường chủ động lựa chọn những hộ gia đình có tần suất mua sắm và chi tiêu cao trong quá khứ để gửi thư mời tham gia chiến dịch (selection bias). Do đó, những hộ được nhắm mục tiêu vốn đã có xác suất mua lại tự nhiên cao hơn.
  >
  > Tuy nhiên, trong bài toán dự báo xu hướng mua (Propensity Modeling), mục tiêu của chúng ta là tối đa hóa độ chính xác dự báo tại thời điểm $t_0$. Biến `is_targeted_by_active_campaign` tại $t_0$ là một đặc trưng quan sát hoàn toàn hợp lệ, không vi phạm rò rỉ dữ liệu, và phản ánh đồng thời cả tín hiệu hành vi tích cực của khách hàng lẫn sự can thiệp tiếp thị ngoại sinh của doanh nghiệp."*

### Câu hỏi 3: Tại sao trước đây phân tích thực phẩm tươi sống cho thấy khoảng cách mua dài hơn, nhưng ở Slide 9 xác suất mua lại lại cao hơn?
* **Trả lời:**
  > *"Đó chính là bài học kinh điển về việc chọn đúng đơn vị phân tích (Unit of Analysis):
  > * Khi phân tích ở **cấp giỏ hàng**: Một giỏ hàng chứa nhiều đồ tươi sống (thịt, cá, rau củ) thường là một chuyến đi chợ lớn tích trữ (stock-up trip). Sau một chuyến mua sắm lớn, hộ gia đình cần tiêu thụ hết lượng thực phẩm đó nên khoảng cách đến chuyến đi tiếp theo đo được ở cấp giỏ thường dài hơn một chuyến đi mua lẻ vài món đồ uống.
  > * Nhưng khi đưa vào bài toán dự báo học máy ở **cấp hộ gia đình**: Đặc trưng cần đo là 'Đã bao lâu kể từ lần cuối hộ này mua đồ tươi sống?' (`days_since_last_perishable`). Thực phẩm tươi sống có chu kỳ bảo quản và hạn sử dụng ngắn (3–5 ngày). Dữ liệu ở Slide 9 chứng minh rõ: Hộ vừa mua đồ tươi trong 1–3 ngày qua có $P(Y=1)$ lên tới 89.7%, và giảm liên tục xuống 35.0% ở nhóm lâu không mua. Nhu cầu bổ sung thực phẩm tươi sống chính là động lực kéo khách hàng quay lại siêu thị."*

### Câu hỏi 4: Nhóm xử lý dữ liệu nhân khẩu học khuyết thiếu (68%) như thế nào và tại sao không dùng các kỹ thuật điền khuyết (Imputation)?
* **Trả lời:**
  > *"Trong dữ liệu bán lẻ thực tế, việc 68% hộ gia đình không có dữ liệu nhân khẩu học không phải là khuyết ngẫu nhiên (Missing Completely at Random - MCAR). Dữ liệu này chỉ xuất hiện khi khách hàng tự nguyện đăng ký làm thẻ thành viên thân thiết và điền phiếu khảo sát.
  >
  > Slide 13 chứng minh một phát hiện quan trọng: 801 hộ có khai báo có xác suất mua lại rất cao và đồng đều quanh 90%–92%, bất kể quy mô gia đình 1 người hay 5 người. Trong khi đó, 1,699 hộ khuyết thiếu có xác suất mua rơi xuống 57.7% (thấp hơn 32–34 điểm phần trăm). Trạng thái khuyết thiếu chính là một tín hiệu hành vi phân tách mạnh mẽ giữa khách hàng thân thiết và khách hàng vãng lai.
  >
  > Nếu chúng ta áp dụng các phương pháp điền khuyết như Mean, KNN hay MICE, chúng ta sẽ xóa nhòa ranh giới phân tách tự nhiên này và đưa thêm giả định sai lệch vào mô hình. Do đó, giải pháp chuẩn mực nhất là giữ nguyên nhóm `UNKNOWN` dạng danh mục độc lập để mô hình LightGBM tự động khai thác."*

### Câu hỏi 5: Tại sao nhóm lại tách các phân tích về Pareto, Chiết khấu quầy, Nhãn hàng riêng và Phân phối giờ vào phần Phụ lục?
* **Trả lời:**
  > *"Đây là sự phân định rạch ròi giữa hai mục tiêu:
  > * **Phục vụ mô hình học máy (Slides 4–14):** Các biểu đồ bắt buộc phải kết nối trực tiếp với biến mục tiêu $Y$ thông qua xác suất $P(Y=1)$, chứng minh khả năng phân tách của từng đặc trưng tại thời điểm $t_0$, và bảo đảm nguyên tắc không rò rỉ dữ liệu tương lai.
  > * **Phục vụ chiến lược kinh doanh và vận hành (Slides 15–18):** Các phân tích như hệ số Gini 0.503, tỷ lệ ngân sách chiết khấu quầy gấp 32.8 lần coupon, hiệu suất SKU của nhãn riêng 1.86x, hay khung giờ cao điểm 11h–18h là những phát hiện vĩ mô rất có giá trị cho ban giám đốc và bộ phận vận hành siêu thị. Tuy nhiên, chúng không thể chuyển hóa trực tiếp thành đặc trưng dự báo nhị phân cấp hộ tại thời điểm $t_0$ (ví dụ: CLV 2 năm là biến tương lai rò rỉ dữ liệu; khung giờ mua sắm xảy ra sau khi khách đã đến siêu thị).
  >
  > Việc đưa các nội dung này vào phần phụ lục giúp giữ cho trục lập luận chính của bài toán học máy sắc bén, mạch lạc, đồng thời vẫn bảo toàn trọn vẹn giá trị tư vấn kinh doanh của giai đoạn EDA."*

---
*Tài liệu được chuẩn hóa và lưu trữ tại `docs/presentation/eda_presentation_script.md`.*
