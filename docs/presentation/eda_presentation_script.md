# Kịch bản trình bày báo cáo khám phá dữ liệu & kiểm toán chất lượng (EDA & Data Quality)
## Bài toán Dự đoán Xác suất Mua hàng Bán lẻ (14 ngày) & Chiến lược Kinh doanh Chuỗi Siêu thị
### Bộ dữ liệu: Dunnhumby — The Complete Journey (2,500 Hộ gia đình panel, 2.59M Giao dịch, 8 Bảng, 711 Ngày)

---

## Cấu trúc tổng thể bài trình bày (Deck Structure & Narrative Arc)

Bài thuyết trình kéo dài **15 phút** (gồm 12 phút trình bày mạch chính và 3 phút Q&A), được chuẩn hóa thành **2 Phần rõ rệt** tương ứng với 19 slides chuyên nghiệp:

1. **Phần 1: Khám phá dữ liệu cho Bài toán Học máy (Slides 1 – 9 | 6.0 phút):**
   - **Slide 1:** Tiêu đề báo cáo & Định hướng tiếp cận 2 phân hệ (ML Track & Business Track).
   - **Slide 2:** 1. Kiểm toán 8 bảng dữ liệu: Sơ đồ ERD The Complete Journey, bóc tách dòng/giỏ/hộ, kiểm định tác động nhãn của 942 giỏ hàng phi thương mại (0.016%).
   - **Slide 3:** 2. Căn cứ thực nghiệm chọn cửa sổ 14 ngày (Base rate 68.34%, std $\pm 1.04\%$, cân bằng phân hóa & vận hành).
   - **Slide 4:** 3. Heatmap tương tác 2D Recency $\times$ Frequency phân tách quán tính mua sắm.
   - **Slide 5:** 4. Phân tầng kiểm soát Spend & Breadth bổ trợ tín hiệu trong từng tầng tần suất.
   - **Slide 6:** 5. Hàng tươi sống: Chỉ báo chu kỳ tiêu dùng thực phẩm ngắn hạn.
   - **Slide 7:** 6. Tác động kích hoạt của chiến dịch tiếp thị và tỷ lệ đổi coupon Type A/B/C tại $t_0$.
   - **Slide 8:** 7. Cấu trúc mạng lưới cửa hàng (Store Loyalty) và kiểm định tính đại diện của nhóm `UNKNOWN`.
   - **Slide 9:** 8. Đề xuất 28 đặc trưng Point-in-Time chuyển giao sang Feature Engineering.

2. **Phần 2: Khám phá dữ liệu chuyên sâu cho Chiến lược Bán lẻ (Slides 10 – 18 | 6.0 phút):**
   - **Slide 10:** 9. Phân khúc giá trị khách hàng RFM & Ma trận giữ chân (VIP 21.6% tạo 54.3% DT, At-Risk 2.1% tạo 3% DT trễ 83 ngày).
   - **Slide 11:** 10. Ma trận hiệu quả ngành hàng: Nam châm kéo khách (Grocery 78.1% độ phủ, 50.8% DT) vs Tăng giá trị giỏ hàng (Fresh & Drug GM).
   - **Slide 12:** 11. Sức mạnh giỏ hàng đa ngành & Cơ hội bán chéo liên ngành (AOV tăng từ $12 lên $84+; 12.7% giỏ đa ngành tạo 38.0% DT).
   - **Slide 13:** 12. Thâm nhập Nhãn hàng riêng (Private Label) theo ngành hàng (Pastry 51.6% DT, Grocery 27.0% DT; dư địa tăng biên lợi nhuận tại Meat & Drug GM).
   - **Slide 14:** 13. Hành vi tiêu dùng theo Quy mô gia đình & Trẻ em (Hộ $\ge 5$ người đạt AOV $42.06, chi $6,699/năm).
   - **Slide 15:** 14. Cấu trúc chiết khấu hai tầng: Markdown tại quầy ($1.40M) vs Coupon ($42.6K) — đòn bẩy gấp 32.8 lần.
   - **Slide 16:** 15. Mức độ tập trung doanh thu khách hàng: Kiểm định Pareto (Top 20% = 53.0% DT) và Hệ số Gini (0.5028).
   - **Slide 17:** 16. Nhịp điệu thời gian vi mô & Tối ưu hóa vận hành (Khung giờ cao điểm 11h–18h chiếm 62.9% giao dịch).
   - **Slide 18:** 17. Tổng kết chiến lược bán lẻ: 5 hành động thương mại trọng tâm cho ban giám đốc chuỗi.

3. **Phụ lục & Q&A Defense (Slide 19 + 5 Câu hỏi phản biện):**
   - **Slide 19:** Phụ lục: Phân phối giá trị giỏ hàng thực nghiệm (AOV: Trung vị $17.18 USD, Trung bình $29.24 USD).
   - **Phần Q&A:** 5 câu hỏi tình huống hóc búa về rò rỉ dữ liệu, xử lý `UNKNOWN`, phân tầng Spend/Breadth, chiến lược giải cứu At-Risk, và quy luật Pareto FMCG.

---

## Kịch bản chi tiết từng slide (Slide-by-Slide Script)

### Slide 1: Tiêu đề báo cáo
* **Tiêu đề:** Khám phá dữ liệu (EDA) & kiểm toán chất lượng dữ liệu
* **Phụ đề:** Phân tích thực nghiệm đa chiều cho Bài toán Dự đoán Mua hàng & Chiến lược Bán lẻ
* **Thời lượng:** 30 giây

**Lời thoại trình bày:**
> *"Kính chào quý thầy cô và hội đồng. Hôm nay, nhóm chúng em xin báo cáo kết quả: **Khám phá dữ liệu (EDA) và Kiểm toán chất lượng dữ liệu**, đóng vai trò là nền tảng thực nghiệm khoa học kép: vừa phục vụ trực tiếp cho việc xây dựng **Mô hình học máy dự đoán xác suất mua hàng 14 ngày**, vừa mở rộng thành **Khung phân tích chiến lược bán lẻ chuyên sâu** cho ban điều hành chuỗi siêu thị.
>
> Toàn bộ nghiên cứu được thực hiện trên bộ dữ liệu thực tế Dunnhumby — The Complete Journey gồm 2,500 hộ panel, 2.59 triệu dòng giao dịch trải dài trên 711 ngày quan sát liên tục. Để bài báo cáo đạt độ mạch lạc cao nhất, nhóm đã chia cấu trúc thành 2 phần rõ rệt: **Phần 1: Bài toán học máy** và **Phần 2: Chiến lược bán lẻ**."*

---

### Slide 2: 1. Kiểm toán 8 bảng: Xử lý dữ liệu & chuẩn hóa khóa nối
* **Thời lượng:** 55 giây
* **Trực quan:** Sơ đồ kiến trúc ERD thực tế bên trái (The complete journey: dataset details) và bảng phân tích bóc tách làm sạch 8 bảng bên phải.

**Lời thoại trình bày:**
> *"Mở đầu Phần 1, nhìn vào sơ đồ kiến trúc 8 bảng dữ liệu Dunnhumby bên trái, nhóm đã tiến hành kiểm toán dữ liệu đa cấp độ với các kết quả cụ thể:
> 1. **Bảng giao dịch (`transaction_data`):** Từ 2,595,732 dòng thô, nhóm phát hiện và loại bỏ 1,054 dòng thuộc **942 giỏ hàng lỗi có tổng chi tiêu $\le \$0$** (gồm các giao dịch hoàn trả, quẹt thẻ lỗi hoặc dùng toàn bộ điểm thưởng). Bảo toàn nguyên vẹn **275,542 giỏ hàng thương mại sạch**.
> 2. **Kiểm định tác động nhãn:** Nhóm đã kiểm tra chéo xem việc loại 942 giỏ hàng này có làm sai lệch nhãn học máy hay không. Kết quả trên toàn bộ 12,500 lượt đánh giá qua 5 mốc cutoff chỉ làm đổi đúng **2 nhãn từ 1 sang 0** tại $t_0=550$ (tỷ lệ chỉ **0.016%**), chứng minh việc làm sạch không hề gây biến dạng nhãn mục tiêu.
> 3. **Bảng coupon:** Khử trùng 5,164 bản ghi trùng lặp 100%, chuẩn hóa về đúng **119,384 dòng ánh xạ** duy nhất; bảng đổi quà ghi nhận chính xác **2,318 lượt đổi thực tế** của 434 hộ.
> 4. **Bảng nhân khẩu học:** Chỉ có 801 hộ khai báo (32%). Thay vì loại bỏ 68% số hộ gây sai lệch mẫu tự chọn (selection bias), nhóm mã hóa toàn bộ 1,699 hộ khuyết thành phân lớp **`UNKNOWN`**, bảo toàn 100% cỡ mẫu 2,500 hộ panel.
> 5. **Khớp nối JOIN Audit:** Khớp nối giữa giao dịch và sản phẩm đạt **100% tuyệt đối** (không lệch một SKU nào và không nhân đôi dòng)."*

---

### Slide 3: 2. Căn cứ chọn cửa sổ 14 ngày: Phân hóa & vận hành
* **Thời lượng:** 45 giây
* **Trực quan:** Đồ thị tỷ lệ mẫu dương và độ lệch chuẩn của 3 cửa sổ: 7 ngày, 14 ngày và 30 ngày.

**Lời thoại trình bày:**
> *"Để xác định chân trời dự báo tối ưu, nhóm đã kiểm nghiệm thực nghiệm 3 cửa sổ:
> - **Cửa sổ 7 ngày:** Base rate trung bình chỉ đạt **51.2%**. Tuy cân bằng về tỷ lệ nhãn nhưng lại quá nhạy cảm với nhiễu ngẫu nhiên thời tiết, chu kỳ ngày cuối tuần, và tạo áp lực vận hành tiếp thị quá dồn dập cho đội ngũ in ấn gửi thư.
> - **Cửa sổ 30 ngày:** Base rate tăng vọt lên **84.1%**, khiến nhãn bị bão hòa, làm mất tính phân tách giữa khách hàng năng động và khách hàng vãng lai.
> - **Cửa sổ 14 ngày:** Base rate đạt **68.34%** với độ lệch chuẩn cực kỳ ổn định giữa các mốc cutoff ($\pm 1.04\%$). Khoảng thời gian 2 tuần này vừa bao trọn chu kỳ nhận lương của người tiêu dùng, vừa khớp hoàn hảo với chu kỳ 14 ngày lên kế hoạch và phát hành chiến dịch CRM của siêu thị. Riêng trên nhóm 2,301 hộ active trong 90 ngày gần nhất, tỷ lệ mua đạt 73.20%."*

---

### Slide 4: 3. Recency & Frequency: Phân tách quán tính mua sắm
* **Thời lượng:** 45 giây
* **Trực quan:** Heatmap 2D màu sắc phân tách xác suất mua theo tương tác giữa Recency và Frequency.

**Lời thoại trình bày:**
> *"Trên biểu đồ heatmap tương tác 2 chiều giữa Recency (độ trễ) và Frequency (tần suất), chúng ta thấy rõ sức mạnh phân tách quán tính mua sắm:
> - **Hiệu ứng Recency là áp đảo:** Nhóm hộ vừa mua hàng trong vòng $0-3$ ngày trước $t_0$ đạt xác suất mua tiếp lên tới **95.6%** ($n=794$ hộ). Khi độ trễ vượt quá 30 ngày, xác suất mua rơi tự do xuống chỉ còn **16.7%** ($n=366$ hộ).
> - **Frequency đóng vai trò điều tiết mức độ phân rã:** Ở cùng một khoảng trễ $15-30$ ngày, nếu hộ có lịch sử mua thường xuyên ($\ge 7$ giỏ trong 90 ngày) thì xác suất mua vẫn giữ vững ở mức **67.2%**; trong khi hộ chỉ ghé $1-2$ lần thì xác suất tụt dốc về **31.0%**.
>
> Kết quả này là bằng chứng thực nghiệm để tạo ra biến tương tác phi tuyến $\text{Recency} \times \text{Frequency}$ trong bộ đặc trưng học máy."*

---

### Slide 5: 4. Spend & Breadth: Tín hiệu bổ trợ trong phân tầng Tần suất
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ phân tầng kiểm soát tần suất, so sánh hiệu ứng của Spend và Breadth trên tầng tần suất trung bình (3–6 chuyến).

**Lời thoại trình bày:**
> *"Một vấn đề kinh điển trong học máy bán lẻ là: Liệu quy mô chi tiêu (Spend) và độ rộng ngành hàng (Breadth) có cung cấp tín hiệu độc lập hay chỉ là bản sao của Frequency?
>
> Để trả lời, nhóm tiến hành phân tầng kiểm soát tần suất. Tại tầng trung bình từ $3-6$ chuyến đi chợ:
> - **Độ rộng ngành hàng (Basket Breadth) tạo bước nhảy vọt:** Hộ mua từ $\ge 11$ ngành hàng đạt xác suất mua **83.7%**, so với chỉ **64.0%** ở hộ mua hẹp $1-4$ ngành hàng — chênh lệch tới **+19.7 điểm phần trăm** mà không phụ thuộc vào số chuyến đi.
> - **Quy mô chi tiêu (Spend):** Tầng chi tiêu cao đạt **76.8%** so với **68.3%** ở tầng chi tiêu thấp ($\Delta = +8.5\%$).
>
> Như vậy, Breadth và Spend bổ sung tín hiệu gia tăng nội tầng rất mạnh mẽ, phản ánh mức độ gắn kết đa nhu cầu của hộ gia đình."*

---

### Slide 6: 5. Hàng tươi sống: Chỉ báo chu kỳ tiêu dùng thực phẩm ngắn hạn
* **Thời lượng:** 40 giây
* **Trực quan:** Biểu đồ phân rã xác suất mua theo số ngày kể từ lần cuối mua rau củ (`PRODUCE`) hoặc thịt tươi (`MEAT`).

**Lời thoại trình bày:**
> *"Hàng tươi sống là nhóm sản phẩm đặc thù có hạn sử dụng ngắn ($3-5$ ngày).
> - Phân tích thực nghiệm cho thấy: Hộ gia đình vừa mua hàng tươi sống trong $0-3$ ngày gần nhất có xác suất tái ghé thăm siêu thị đạt **89.7%**.
> - Khi không phát sinh mua đồ tươi $>14$ ngày, xác suất giảm nhanh về **42.5%**.
> - Tuy biến tươi sống có độ tương quan vừa phải với Recency chung ($r \approx 0.62$), việc tách riêng đặc trưng `days_since_last_fresh` giúp mô hình nắm bắt trạng thái cạn kiệt nguồn thực phẩm thiết yếu tại gia đình, đóng vai trò một chiếc đồng hồ đếm ngược cho chuyến đi chợ tiếp theo."*

---

### Slide 7: 6. Chiến dịch & Coupon: Tín hiệu tương quan dự báo tại $t_0$
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ xác suất mua theo trạng thái chiến dịch active và tỷ lệ chuyển đổi đổi coupon theo 3 loại chiến dịch Type A, B, C.

**Lời thoại trình bày:**
> *"Về các yếu tố tiếp thị ngoại sinh:
> - Hộ đang nằm trong danh sách mục tiêu của một chiến dịch còn hiệu lực tại $t_0$ đạt xác suất mua từ **86.8% đến 90.3%**, vượt trội hoàn toàn so với mức **59.9%** ở hộ không có chiến dịch active — chênh lệch từ **+27 đến +30 điểm phần trăm**.
> - Khi phân tích tỷ lệ đổi coupon theo loại chiến dịch, có sự phân hóa sâu sắc:
>   - **Chiến dịch Loại A (Đa ngành hàng):** Đạt tỷ lệ đổi coupon lên tới **15.96%** (635 lượt đổi trên 3,979 cặp hộ-chiến dịch).
>   - **Chiến dịch Loại B (Chuyên ngành):** Đạt **7.91%**.
>   - **Chiến dịch Loại C (Ngắn hạn):** Đạt **7.67%**.
> - Chiến dịch Loại A có tỷ lệ đổi quà gấp **2.08 lần** so với Loại B và C, chứng minh rằng các ưu đãi giỏ hàng bao trùm nhiều danh mục kích hoạt hành vi mua sắm mạnh mẽ hơn nhiều so với ưu đãi đơn ngành."*

---

### Slide 8: 7. Mạng lưới cửa hàng & Phân nhóm UNKNOWN: Cấu trúc
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ tương quan tỷ trọng cửa hàng chính và tính ổn định của nhóm `UNKNOWN`.

**Lời thoại trình bày:**
> *"Hai phát hiện cấu trúc quan trọng cuối cùng của Phần 1:
> 1. **Nghịch lý độ trung thành cửa hàng đơn lẻ:** Những hộ dồn 100% chi tiêu vào một cửa hàng duy nhất lại có xác suất mua 14 ngày thấp hơn (**63.0%**) so với nhóm mua sắm linh hoạt tại 2–3 cửa hàng khác nhau trong chuỗi (**79.0%**). Điều này phản ánh rằng những người đi nhiều cửa hàng là nhóm khách hàng năng động, gắn bó toàn diện với thương hiệu siêu thị trên các tuyến đường sinh hoạt hàng ngày.
> 2. **Tính đại diện của nhóm `UNKNOWN`:** Nhóm 1,699 hộ không khai báo nhân khẩu học đạt tỷ lệ mua **68.4%**, tương đồng gần như tuyệt đối với mức **68.2%** của nhóm có khai báo. Điều này khẳng định nhóm khuyết không có sự sai lệch tự chọn, việc gán nhãn `UNKNOWN` hoàn toàn giữ vững tính khách quan cho mô hình."*

---

### Slide 9: 8. Đề xuất 28 đặc trưng Point-in-Time sang Feature Engineering
* **Thời lượng:** 45 giây
* **Trực quan:** Bảng ma trận 9 nhóm đặc trưng (28 biến) với cửa sổ tính toán, kiểu dữ liệu và căn cứ thực nghiệm từ EDA.

**Lời thoại trình bày:**
> *"Khép lại Phần 1, toàn bộ phát hiện EDA được cô đọng thành **ma trận đề xuất 28 đặc trưng Point-in-Time** chia làm 9 nhóm cốt lõi:
> - Từ nhóm Recency (độ trễ chung và hàng tươi sống), Frequency đa cửa sổ (14d, 30d, 90d), biến tương tác phi tuyến `recency_x_frequency_90d`, quy mô chi tiêu Spend và AOV, độ rộng danh mục Breadth, tỷ trọng hàng tươi sống, chỉ báo chiến dịch Type A/B/C, độ phân tán cửa hàng, cho đến nhóm nhân khẩu học an toàn.
> - Toàn bộ 28 đặc trưng đều tuân thủ nguyên tắc $DAY \le t_0$, sẵn sàng chuyển giao làm đầu vào chuẩn hóa cho mô hình phân loại **LightGBM Calibrated Classifier**."*

---

### Slide 10: 9. Phân khúc khách hàng RFM & Ma trận giữ chân
* **Thời lượng:** 50 giây
* **Trực quan:** Biểu đồ cột kép so sánh tỷ lệ số hộ trong Panel (%) và tỷ lệ đóng góp Doanh thu thực tế (%) trên 6 phân khúc RFM.

**Lời thoại trình bày:**
> *"Bước sang **Phần 2: Góc nhìn Chiến lược Kinh doanh Bán lẻ**, nhóm tiến hành phân khúc 2,500 hộ gia đình panel theo phương pháp RFM định lượng kết hợp mức chi tiêu thực tế $8.06M USD:
> - **Nhóm VIP / Champions (21.6% số hộ):** 541 hộ gia đình nhưng đóng góp tới **54.3% tổng doanh thu** (\$4.38M USD), giá trị giỏ hàng trung bình AOV đạt \$40, và độ trễ cực thấp chỉ 2.7 ngày. Đây là xương sống dòng tiền của cả hệ thống.
> - **Khách thân thiết (Loyal - 46.3% số hộ):** 1,157 hộ, tạo **35.1% doanh thu** (\$2.83M USD), độ trễ 7.3 ngày.
> - **Cảnh báo khẩn cấp — Nhóm Nguy cơ rời bỏ (At-Risk - 2.1% số hộ):** Chỉ có 52 hộ gia đình nhưng đóng góp tới **3.0% tổng doanh thu** (\$244 nghìn USD). Đây là những khách hàng từng chi tiêu rất lớn với AOV lên tới \$43.8, nhưng hiện tại độ trễ đã lên tới **83.2 ngày**! Nếu không có chương trình can thiệp cứu vãn (Win-back) kịp thời, siêu thị sẽ mất trắng một phân khúc có giá trị vòng đời cực cao.
> - **Khách ngủ đông (Dormant - 9.2% số hộ):** Độ trễ 167 ngày, chỉ đóng góp 1.9% doanh thu."*

---

### Slide 11: 10. Ma trận ngành hàng: Hút khách vs Tăng giỏ
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ ngang Panel A (Doanh thu vs Độ phủ giỏ của Top 8 ngành) và Panel B (Chi tiêu bình quân mỗi chuyến AOV ngành).

**Lời thoại trình bày:**
> *"Để tối ưu hóa quản trị danh mục (Category Management), nhóm phân tích ma trận 44 ngành hàng để phân định vai trò chiến lược:
> - **Nam châm kéo khách (Traffic Driver) — Ngành `GROCERY`:** Xuất hiện ở **78.1% tổng số giỏ hàng**, tạo ra **50.8% doanh thu toàn hệ thống** (\$4.09M USD), với chi tiêu trung bình \$19.03/chuyến. Khách hàng đến siêu thị trước hết là để mua hàng tạp hóa nhu yếu phẩm.
> - **Ngành mở rộng giỏ (Basket Builder) — `DRUG GM`:** Độ phủ **42.8% giỏ hàng**, đóng góp **13.1% doanh thu** (\$1.05M USD).
> - **Nhóm giữ chân định kỳ — Hàng tươi sống (`FRESH` - Produce + Meat + Packaged Meat):** Đóng góp tổng cộng **18.9% doanh thu**.
>
> Chiến lược thương mại ở đây là: Sử dụng `GROCERY` làm mồi kéo lưu lượng khách hàng vào cửa hàng, sau đó tối ưu hóa luồng di chuyển và biển chỉ dẫn để dẫn dắt họ mua chéo sang các quầy Fresh và Drug GM có biên lợi nhuận cao hơn."*

---

### Slide 12: 11. Sức mạnh giỏ hàng đa ngành & Đòn bẩy bán chéo
* **Thời lượng:** 45 giây
* **Trực quan:** Đồ thị cột AOV giỏ hàng theo số lượng ngành hàng trong giỏ, kèm đường tỷ trọng doanh thu tích lũy.

**Lời thoại trình bày:**
> *"Phân tích giỏ hàng đa ngành mang lại một phát hiện kinh doanh đột phá về đòn bẩy AOV:
> - Giỏ hàng chỉ mua **1 ngành đơn lẻ** chiếm tới 36.7% số lượt mua, nhưng AOV chỉ đạt vỏn vẹn **\$12.22**, chỉ đóng góp 15.3% doanh thu.
> - Khi khách hàng mua chéo từ **3–4 ngành**, AOV nhảy vọt gấp 3 lần lên **\$36.78** (đóng góp 32.9% doanh thu).
> - Đặc biệt, với những giỏ hàng đa ngành lớn từ **$\ge 5$ ngành hàng**, AOV đạt đỉnh **\$84.12** — gấp gần **7 lần** giỏ đơn lẻ.
> - **Điểm tựa doanh số vàng:** Chỉ có **12.7% số giỏ hàng** có từ $\ge 5$ ngành, nhưng nhóm này tạo ra tới **38.0% tổng doanh thu** của chuỗi!
>
> Khuyến nghị hành động: Triển khai chiến lược trưng bày liên kết (Cross-merchandising), ví dụ đặt bơ và mứt ngay cạnh quầy bánh mì nướng, hoặc xếp gia vị ướp ngay quầy thịt tươi để kích thích giỏ hàng đa ngành."*

---

### Slide 13: 12. Thâm nhập Nhãn riêng (Private Label) theo ngành
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ tỷ trọng Doanh thu và Sản lượng tiêu thụ của Nhãn hàng riêng (Private Label) trên 7 ngành hàng chủ lực.

**Lời thoại trình bày:**
> *"Nhãn hàng riêng (Private Label) là vũ khí chiến lược giúp các chuỗi bán lẻ gia tăng biên lợi nhuận gộp từ 5% đến 12% so với phân phối nhãn hàng quốc gia:
> - **Thống trị tuyệt đối tại ngành Bánh nướng (`PASTRY`):** Nhãn riêng chiếm tới **51.6% doanh thu** và 39.7% sản lượng tiêu thụ. Khách hàng hoàn toàn tin tưởng vào chất lượng bánh tự sản xuất của siêu thị.
> - **Chiếm lĩnh vững chắc tại Tạp hóa (`GROCERY`):** Đạt **27.0% doanh thu** và **36.4% sản lượng tiêu thụ** (hơn 1/3 tổng lượng hàng bán ra).
> - Các ngành chế biến sẵn như `DELI` và `MEAT-PCKGD` cũng đạt tỷ trọng ấn tượng quanh mức **23%**.
> - **Dư địa mở rộng:** Nhãn riêng tại quầy Hóa mỹ phẩm (`DRUG GM` - 9.5%) và Quầy thịt tươi sống (`MEAT` - 5.0%) còn rất khiêm tốn. Đây là cơ hội vàng để siêu thị hợp tác gia công nhằm đa dạng hóa dải sản phẩm nhãn riêng có tỷ suất lợi nhuận cao."*

---

### Slide 14: 13. Tiêu dùng theo Quy mô gia đình & Trẻ em
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ so sánh AOV và mức chi tiêu bình quân hàng năm theo Quy mô hộ gia đình (Panel A) và Số lượng trẻ em (Panel B).

**Lời thoại trình bày:**
> *"Phân tích 801 hộ gia đình có khai báo nhân khẩu học cho thấy chân dung khách hàng có sức mua lớn nhất:
> - **Quy mô hộ gia đình:** Hộ độc thân (1 người) chi tiêu \$5,032/năm với AOV \$27.83; trong khi các hộ gia đình lớn ($\ge 5$ người) chi tiêu tới **\$6,699/năm** (tăng +33.1%) và AOV mỗi lần đi chợ đạt **\$42.06** (tăng +51.1%).
> - **Tác động của trẻ em:** Sự xuất hiện của con cái làm thay đổi hoàn toàn quy mô giỏ hàng. Hộ có 2 con chi tiêu trung bình **\$6,764/năm** (AOV \$36.36); hộ có $\ge 3$ con đạt AOV **\$41.10** và chi tiêu \$6,742/năm.
> - **Định hướng tiếp thị:** Siêu thị cần thiết kế các gói sản phẩm combo gia đình dung tích lớn (Family pack / Bulk size) nhắm trực tiếp vào phân khúc hộ đông người và có con nhỏ để tối đa hóa chi tiêu mỗi chuyến."*

---

### Slide 15: 14. Chiết khấu hai tầng: Markdown tại quầy vs Coupon
* **Thời lượng:** 40 giây
* **Trực quan:** Biểu đồ so sánh Quy mô dòng tiền chiết khấu ($ Triệu USD) và Tỷ lệ giỏ hàng được áp dụng (%) giữa Markdown tại quầy và Phiếu Coupon.

**Lời thoại trình bày:**
> *"Bóc tách cơ cấu ngân sách khuyến mại, chúng ta thấy sự chênh lệch khổng lồ giữa hai công cụ:
> - **Giảm giá niêm yết tại quầy (`RETAIL_DISC`):** Đạt tới **\$1.40 Triệu USD** (chiếm 14.8% tổng doanh thu gộp), xuất hiện ở **83.67% tổng số giỏ hàng** (230,554 giỏ).
> - **Phiếu giảm giá coupon (`COUPON_DISC`):** Chỉ đạt vỏn vẹn **\$42.6 nghìn USD** (0.53% doanh thu gộp), chỉ bao phủ **6.08% giỏ hàng** (16,741 giỏ).
> - **Tỷ lệ đòn bẩy:** Ngân sách giảm giá niêm yết gấp tới **32.8 lần** chi phí coupon!
>
> Ý nghĩa chiến lược: Markdown tại quầy là chi phí cạnh tranh trên kệ diện rộng để giữ chân lượng khách chung; trong khi Coupon là công cụ đòn bẩy chi phí thấp nhưng mang tính nhắm chọn mục tiêu cực cao vào nhóm khách hàng nhạy cảm về giá."*

---

### Slide 16: 15. Mức độ tập trung doanh thu khách hàng: Pareto & Gini
* **Thời lượng:** 45 giây
* **Trực quan:** Đường cong Lorenz thực tế (Gini = 0.5028) so sánh với đường bình đẳng tuyệt đối 45°, định vị điểm tích lũy Top 20% và mốc 80% doanh thu.

**Lời thoại trình bày:**
> *"Khảo sát mức độ tập trung doanh thu qua đường cong Lorenz trên tổng chi tiêu $8.06M USD của 2,500 hộ panel:
> - **Quy luật Pareto trong bán lẻ FMCG:** Top **20% hộ gia đình chi tiêu nhiều nhất** (500 hộ) đóng góp **53.0% tổng doanh thu** (\$4.27M USD).
> - Để đạt được **80% doanh thu tích lũy**, siêu thị cần tới **44.0% số hộ gia đình** (1,100 hộ). Con số này phản ánh đặc thù thực phẩm thiết yếu có mức độ phân hóa ít cực đoan hơn so với thương mại điện tử hay thời trang xa xỉ, nơi 20% khách thường tạo 80% doanh số.
> - **Hệ số Gini đạt 0.5028:** Thể hiện mức độ tập trung doanh thu ở mức trung bình cao, củng cố tầm quan trọng của việc cá nhân hóa chính sách CRM để chăm sóc chặt chẽ nhóm 20% khách hàng đóng góp hơn một nửa doanh số."*

---

### Slide 17: 16. Nhịp điệu thời gian vi mô & Tối ưu hóa vận hành
* **Thời lượng:** 40 giây
* **Trực quan:** Biểu đồ phân phối ngày trong tuần (`DAY mod 7`) và biểu đồ đường phân bố khung giờ mua sắm trong ngày (`TRANS_TIME`).

**Lời thoại trình bày:**
> *"Phân tích nhịp điệu vi mô cung cấp căn cứ trực tiếp để tối ưu hóa vận hành chuỗi:
> - **Chu kỳ ngày trong tuần:** Hai ngày cuối tuần đạt tỷ trọng giỏ hàng vượt trội (**16.2% đến 17.5%**), trong khi các ngày giữa tuần phân bổ đều đặn từ 12.1% đến 13.0%.
> - **Khung giờ vàng trong ngày:** Khung giờ từ **11h trưa đến 18h chiều** chiếm tới **62.9% tổng lượng giao dịch** trong ngày, với đỉnh điểm rơi vào khoảng 13h–16h.
> - **Ứng dụng vận hành:**
>   - Bố trí tăng cường nhân sự quầy thu ngân và nhân viên hỗ trợ đóng gói vào khung giờ 11h–18h và hai ngày cuối tuần.
>   - Hoàn tất việc sắp xếp và kiểm tra chất lượng quầy rau củ, thịt tươi trước 10h sáng.
>   - Thời điểm vàng để gửi tin nhắn thông báo đẩy (Push Notification / SMS) ưu đãi là trước 11h sáng để đón đầu quyết định đi chợ của khách hàng."*

---

### Slide 18: 17. Tổng kết: 5 hành động chiến lược bán lẻ
* **Thời lượng:** 50 giây
* **Trực quan:** 5 khối màu tổng kết 5 trụ cột hành động thương mại trọng tâm cho Ban Giám đốc.

**Lời thoại trình bày:**
> *"Tổng kết toàn bộ chuỗi phát hiện thực nghiệm, nhóm đề xuất **5 hành động chiến lược bán lẻ trọng tâm** cho ban lãnh đạo chuỗi siêu thị:
> 1. **Bảo vệ Top 20% & Cứu vãn At-Risk:** Dành đặc quyền chăm sóc cho 541 hộ VIP đang nắm giữ 54.3% doanh số; đồng thời kích hoạt chiến dịch giải cứu khẩn cấp cho 52 hộ At-Risk (\$244K doanh thu, giỏ hàng \$43.8 nhưng đã trễ 83 ngày).
> 2. **Khai thác Nam châm Grocery để Bán chéo:** Dùng ngành Tạp hóa khô (78% độ phủ) kéo khách vào cửa hàng; bố trí trưng bày liên kết sang Fresh và Drug GM nhằm nâng tỷ trọng giỏ hàng đa ngành $\ge 5$ ngành để hưởng đòn bẩy AOV gấp 7 lần.
> 3. **Mở rộng Nhãn hàng riêng (Private Label):** Phát huy vị thế dẫn đầu tại Bánh nướng (51.6% DT) và Tạp hóa (27% DT), từng bước thâm nhập vào Quầy thịt tươi sống và Hóa mỹ phẩm để cải thiện biên lợi nhuận gộp từ 5% đến 12%.
> 4. **Tái cấu trúc Ngân sách Khuyến mãi:** Cắt giảm ngân sách giảm giá niêm yết cào bằng diện rộng (\$1.40M USD) để tái đầu tư vào các chiến dịch coupon Loại A có tính nhắm chọn cá nhân hóa cao (đạt tỷ lệ chuyển đổi đổi quà 15.96%, gấp đôi Loại B và C).
> 5. **Vận hành linh hoạt theo Thời gian thực:** Tối ưu hóa ca trực thu ngân và chuẩn bị quầy hàng tươi sống tập trung vào khung giờ cao điểm 11h–18h và hai ngày cuối tuần."*

---

### Slide 19: Phụ lục: Phân phối giá trị giỏ hàng thực nghiệm (AOV)
* **Thời lượng:** 30 giây (Dùng khi tra cứu hoặc phản biện)
* **Trực quan:** Biểu đồ phân phối chi tiêu giỏ hàng với đường Median, Mean và vùng IQR.

**Lời thoại trình bày:**
> *"Tại phần phụ lục, biểu đồ mô tả phân phối chi tiêu giỏ hàng trên toàn bộ **275,542 giỏ hàng sạch**:
> - **Giá trị trung vị (Median):** Đạt **\$17.18 USD**, phản ánh chính xác nhất quy mô của một chuyến đi chợ điển hình của hộ gia đình.
> - **Giá trị trung bình (Mean):** Đạt **\$29.24 USD**, bị kéo lệch về phía phải do những giỏ hàng mua sắm gia đình lớn hoặc kỳ nghỉ lễ (lên tới hơn \$100).
> - **Khoảng tứ phân vị (IQR):** Đạt **\$29.40 USD** với $Q_1 = \$7.22$ và $Q_3 = \$36.62$.
> - Khuyến nghị kỹ thuật: Trước khi đưa biến chi tiêu vào mô hình học máy, bắt buộc phải áp dụng hàm biến đổi phi tuyến logarit $\log(1 + \text{Spend})$ để ổn định phương sai và triệt tiêu ảnh hưởng của các giá trị ngoại lai cực lớn."*

---

## Bộ câu hỏi & trả lời dự phòng cho phần Q&A (Defense Strategy)

### Câu hỏi 1: Tại sao nhóm không loại bỏ 68% số hộ gia đình bị khuyết thông tin nhân khẩu học trong bảng `hh_demographic` để dữ liệu được sạch hoàn toàn?
**Câu trả lời:**
> *"Dạ thưa quý thầy cô, trong khai phá dữ liệu bán lẻ, việc loại bỏ các mẫu khuyết chỉ phù hợp khi dữ liệu khuyết ngẫu nhiên hoàn toàn (MCAR) và tỷ lệ khuyết nhỏ. Ở đây, có tới 1,699 trên 2,500 hộ (68%) không có thông tin nhân khẩu học.
> Nếu chúng ta loại bỏ 68% số hộ này, chúng ta sẽ phạm phải sai lầm nghiêm trọng về **sai lệch chọn mẫu (Selection Bias)**: mô hình sẽ chỉ học được hành vi của nhóm khách hàng chịu cung cấp thông tin cá nhân.
> Thực nghiệm kiểm tra nhãn của nhóm đã chứng minh: Nhóm không khai báo (`UNKNOWN`) có tỷ lệ phát sinh mua hàng trong 14 ngày là **68.4%**, gần như tương đồng hoàn hảo với mức **68.2%** của nhóm có khai báo. Do đó, giải pháp khoa học chuẩn mực nhất là giữ nguyên 2,500 hộ và mã hóa nhóm khuyết thành một danh mục riêng mang tên `UNKNOWN`. Cách làm này vừa bảo toàn 100% dung lượng mẫu nghiên cứu, vừa cho phép mô hình tự khai thác tín hiệu từ hành vi không khai báo thông tin."*

### Câu hỏi 2: Có hiện tượng rò rỉ dữ liệu (Data Leakage) khi tính toán các đặc trưng Recency, Frequency và Campaign tại mốc chốt sổ $t_0$ hay không?
**Câu trả lời:**
> *"Dạ hoàn toàn không có rò rỉ dữ liệu. Nhóm chúng em tuân thủ nghiêm ngặt nguyên lý **Point-in-Time Discipline**:
> - Toàn bộ 28 đặc trưng đầu vào chỉ được phép truy vấn dữ liệu giao dịch và chiến dịch thỏa mãn điều kiện $DAY \le t_0$.
> - Cụ thể: Với đặc trưng `has_active_camp`, nhóm kiểm tra điều kiện $START\_DAY \le t_0 \le END\_DAY$, nghĩa là tại đúng ngày $t_0$, siêu thị đã biết rõ hộ đó đang có chiến dịch gửi đến nhà hay chưa.
> - Cửa sổ tính toán nhãn mục tiêu là khoảng thời gian tương lai độc lập hoàn toàn: $DAY \in (t_0, t_0 + 14]$.
> - Nhóm đã viết unit test kiểm tra tự động (`test_data_quality.py`) để khẳng định không có bất kỳ bản ghi nào sau $t_0$ được sử dụng trong ma trận đặc trưng."*

### Câu hỏi 3: Tại sao nhóm lại khẳng định Spend và Breadth cung cấp tín hiệu bổ trợ độc lập cho Frequency? Nhóm đã chứng minh như thế nào?
**Câu trả lời:**
> *"Dạ thưa quý thầy cô, trong toàn bộ tập dữ liệu, Frequency, Spend và Breadth đều có tương quan dương với nhau. Tuy nhiên, nếu chỉ nhìn tương quan đơn biến thì không thể biết liệu Spend và Breadth có giá trị gia tăng (incremental value) hay chỉ là bản sao của Frequency.
> Để bóc tách, nhóm đã sử dụng phương pháp **phân tầng kiểm soát (Stratified Control)**:
> Cố định nhóm hộ gia đình có cùng mức tần suất đi chợ trung bình ($3-6$ chuyến trong 90 ngày). Khi số chuyến đi đã cố định, nhóm phân hóa tiếp theo độ rộng ngành hàng (Breadth). Kết quả cho thấy: Những hộ mua $\ge 11$ ngành hàng đạt xác suất mua **83.7%**, cao hơn rất nhiều so với mức **64.0%** ở hộ chỉ mua $1-4$ ngành hàng ($\Delta = +19.7\%$).
> Tương tự, tầng chi tiêu cao đạt **76.8%** so với **68.3%** ở tầng chi tiêu thấp. Điều này chứng minh thực nghiệm rằng: Ngay cả khi hai khách hàng có số lần đi chợ như nhau, người mua sắm đa ngành và chi tiêu lớn vẫn có xác suất quay lại cao hơn hẳn, mang lại tín hiệu dự báo độc lập cho mô hình."*

### Câu hỏi 4: Nhóm At-Risk trong ma trận RFM chỉ có 52 hộ (2.1%), tại sao lại xem đây là trọng tâm cứu vãn kinh doanh khẩn cấp?
**Câu trả lời:**
> *"Dạ thưa thầy cô, tuy về số lượng chỉ có 52 hộ (chiếm 2.1% panel), nhưng về mặt tài chính, nhóm này đóng góp tới **\$244,000 USD** — chiếm **3.0% tổng doanh thu** của chuỗi siêu thị.
> Đặc điểm của 52 hộ này là: Giá trị giỏ hàng trung bình AOV của họ rất cao (**\$43.8 USD** — cao hơn cả nhóm VIP thông thường), chứng tỏ đây là những khách hàng gia đình lớn, từng gắn bó và chi tiêu rất đậm tại siêu thị. Tuy nhiên, độ trễ hiện tại của họ đã lên tới **83.2 ngày** (gần 3 tháng chưa quay lại).
> Theo lý thuyết CLV và giữ chân khách hàng bán lẻ, chi phí để thu hút một khách hàng mới có giá trị tương đương cao gấp 5 đến 7 lần chi phí gửi một voucher giải cứu cá nhân hóa (Win-back campaign). Do quy mô chỉ 52 hộ, chi phí gửi thư hay gọi điện chăm sóc trực tiếp là vô cùng nhỏ, nhưng doanh thu bảo vệ được lên tới gần một phần tư triệu USD."*

### Câu hỏi 5: Tại sao đường cong Lorenz của siêu thị lại cho thấy Top 20% hộ chỉ đóng góp 53.0% doanh thu, trong khi quy luật Pareto kinh điển thường là 80/20?
**Câu trả lời:**
> *"Dạ thưa hội đồng, đây là một phát hiện thực nghiệm rất đặc trưng của ngành bán lẻ hàng tiêu dùng nhanh (FMCG) và siêu thị thực phẩm:
> - Quy luật Pareto kinh điển 80/20 (20% khách tạo 80% doanh thu) thường xuất hiện phổ biến trong ngành thời trang xa xỉ, thương mại điện tử, hoặc dịch vụ B2B, nơi có những khách hàng cá biệt chi tiêu gấp hàng trăm lần người bình thường.
> - Ngược lại, trong siêu thị bán lẻ thực phẩm, hàng hóa chủ yếu là nhu yếu phẩm thiết yếu (gạo, sữa, thịt, rau củ). Một gia đình dù giàu có đến đâu thì nhu cầu ăn uống hàng ngày cũng có giới hạn sinh học tự nhiên, không thể ăn gấp 100 lần hộ khác được.
> - Do đó, mức phân hóa doanh thu trong bán lẻ thực phẩm có xu hướng thoái triển về mức trung bình cao: Top 20% hộ đóng góp **53.0% doanh thu**, và cần **44.0% số hộ** để tích lũy 80% doanh thu. Hệ số Gini đạt **0.5028** phản ánh chính xác cấu trúc kinh tế phân hóa tự nhiên của ngành FMCG."*
