# Kịch bản trình bày báo cáo khám phá dữ liệu & kiểm toán chất lượng (EDA & Data Quality)
## Xây dựng mô hình dự đoán xác suất mua hàng bán lẻ (Purchasing Propensity Model)
### Bộ dữ liệu: Dunnhumby — The Complete Journey (2,500 Hộ gia đình, 2.59 Triệu giao dịch, 8 Bảng, 711 Ngày)

---

## Cấu trúc tổng thể bài trình bày (Narrative Arc)

Bài thuyết trình kéo dài **15 phút** (gồm 12 phút trình bày và 3 phút Q&A), được cấu trúc chặt chẽ qua 4 phần chính tương ứng với 18 slides:

1. **Phần 1: Thiết kế bài toán & Kiểm toán chất lượng dữ liệu (Slides 1 – 3 | 3.0 phút):**
   - Thiết lập bài toán học máy: Đơn vị hộ gia đình ($n = 2,500$ hộ panel), chân trời dự báo $\Delta t = 14$ ngày, kỷ luật thời gian Point-in-Time ($DAY \le t_0$).
   - Kiến trúc 8 bảng dữ liệu Dunnhumby và kết quả kiểm toán làm sạch: Khử trùng 5,164 dòng coupon, chuẩn hóa 1,699 hộ `UNKNOWN`, loại 942 giỏ hàng phi thương mại (chỉ thay đổi 0.016% nhãn).
2. **Phần 2: Căn cứ xác lập chân trời dự báo & Phân tích hành vi (Slides 4 – 13 | 6.5 phút):**
   - Căn cứ thực nghiệm chọn $\Delta t = 14$ ngày (Base rate 68.3%, std $\pm 1.0\%$).
   - Khám phá 9 nhóm đặc trưng học máy cốt lõi (Chuẩn vàng: $P(Y=1)$, cỡ mẫu $n$, Base rate, độ phân tách thực nghiệm, phân tầng kiểm soát).
3. **Phần 3: Ma trận chuyển giao đặc trưng sang Feature Engineering (Slide 14 | 1.5 phút):**
   - Chuyển giao 28 biến đặc trưng đã kiểm chứng thực nghiệm, tuân thủ 100% ranh giới Point-in-Time.
4. **Phần 4: Phụ lục chiến lược bán lẻ & Quản trị vận hành (Slides 15 – 18 | 1.0 phút):**
   - Quy luật Pareto & Hệ số Gini ($0.5028$), cấu trúc chiết khấu 2 tầng, thâm nhập nhãn hàng riêng (Private Label), và nhịp điệu mua sắm theo giờ.
5. **Phần 5: Bộ câu hỏi & trả lời dự phòng cho phần Q&A (3.0 phút).**

---

## Kịch bản chi tiết từng slide (Slide-by-Slide Script)

### Slide 1: Tiêu đề báo cáo
* **Tiêu đề:** Khám phá dữ liệu (EDA) & kiểm toán chất lượng dữ liệu
* **Phụ đề:** Nền tảng thực nghiệm cho bài toán dự đoán xác suất mua hàng bán lẻ
* **Thời lượng:** 30 giây

**Lời thoại trình bày:**
> *"Kính chào quý thầy cô và các bạn. Hôm nay, nhóm chúng em xin trình bày báo cáo: **Khám phá dữ liệu và Kiểm toán chất lượng dữ liệu**, đóng vai trò là nền tảng thực nghiệm cốt lõi để xây dựng mô hình học máy dự đoán xác suất mua hàng cấp hộ gia đình trong ngành bán lẻ.
>
> Nghiên cứu được thực hiện trên bộ dữ liệu Dunnhumby — The Complete Journey với 2,500 hộ gia đình panel, 2.59 triệu dòng giao dịch chi tiết trải dài trên 711 ngày quan sát liên tục. Mục tiêu tối thượng của bài báo cáo là xác lập kỷ luật dữ liệu nghiêm ngặt, thẩm định tính toàn vẹn của 8 bảng quan hệ, và chứng minh bằng thực nghiệm giá trị dự báo của các nhóm đặc trưng hành vi trước khi chuyển giao sang giai đoạn huấn luyện mô hình."*

---

### Slide 2: Thiết kế bài toán và kỷ luật thời gian chống rò rỉ dữ liệu
* **Tiêu đề:** 1. Thiết kế bài toán và kỷ luật thời gian chống rò rỉ dữ liệu
* **Thời lượng:** 60 giây
* **Trực quan:** 2 cột: Cột trái nêu rõ đơn vị dự báo, cửa sổ quan sát, cửa sổ dự báo, và định nghĩa nhãn mục tiêu $Y$; cột phải nêu kỷ luật Point-in-Time và chiến lược chia tập Multi-cutoff.

**Lời thoại trình bày:**
> *"Trước khi bước vào phân tích dữ liệu, nhóm đã xác lập một khung bài toán học máy minh bạch và nhất quán:
> - **Đơn vị dự báo:** Cấp hộ gia đình ($household\_key$). Toàn bộ 2,500 hộ gia đình là một panel khách hàng cố định được siêu thị theo dõi xuyên suốt nghiên cứu.
> - **Cửa sổ quan sát hành vi ($T_{obs}$):** 90 ngày trước mốc chốt sổ $t_0$ ($DAY \le t_0$) để trích xuất các đặc trưng tần suất, chi tiêu và danh mục.
> - **Cửa sổ dự báo ($\Delta t$):** 14 ngày tới ($DAY \in (t_0, t_0 + 14]$).
> - **Nhãn mục tiêu ($Y$):** Biến nhị phân $Y \in \{0, 1\}$. $Y = 1$ nếu hộ có phát sinh ít nhất một giỏ hàng thương mại có chi tiêu dương ($SALES\_VALUE > 0$) trong 14 ngày tiếp theo; ngược lại $Y = 0$.
>
> Về mặt phương pháp luận, chúng em áp dụng triệt để **kỷ luật Point-in-Time**: 100% biến đặc trưng chỉ được tính toán từ các sự kiện phát sinh trước hoặc tại thời điểm $t_0$. Mọi thông tin sau $t_0$ tuyệt đối chỉ được dùng để gán nhãn mục tiêu $Y$, triệt tiêu hoàn toàn nguy cơ rò rỉ dữ liệu từ tương lai.
>
> Để đánh giá mô hình khách quan, nhóm áp dụng chiến lược chia tập **Multi-cutoff**: Tập Huấn luyện gồm 11 mốc chốt sổ trượt $t_0 \in [200, 500]$, Tập Xác thực gồm 3 mốc $t_0 \in [530, 590]$, và Tập Kiểm thử độc lập gồm 2 mốc $t_0 \in [650, 680]$ hoàn toàn tách biệt về mặt thời gian."*

---

### Slide 3: Kiến trúc 8 bảng dữ liệu và kết quả kiểm toán làm sạch
* **Tiêu đề:** 2. Kiến trúc 8 bảng dữ liệu và kết quả kiểm toán làm sạch
* **Thời lượng:** 75 giây
* **Trực quan:** Sơ đồ thực thể liên kết (ERD) 8 bảng dữ liệu bên trái và danh sách 6 kết quả kiểm toán làm sạch ở cột bên phải.

**Lời thoại trình bày:**
> *"Trên màn hình bên trái là sơ đồ kiến trúc 8 bảng dữ liệu trong hệ sinh thái Dunnhumby. Ở cột bên phải là các kết quả kiểm toán chất lượng và xử lý làm sạch then chốt:
> 1. **Bảng giao dịch `transaction_data` (2.59M dòng):** Chúng em kiểm toán và loại bỏ 942 giỏ hàng phi thương mại có chi tiêu $\le \$0$ (chiếm 0.34% tổng số giỏ hàng, đóng góp đúng $0 doanh thu). Kiểm toán định lượng trên toàn bộ 12,500 cặp (hộ, cutoff) qua 5 mốc chốt sổ cho thấy việc loại 942 giỏ này chỉ làm thay đổi đúng 2 nhãn từ 1 sang 0 tại mốc $t_0 = 550$ (tỷ lệ ảnh hưởng chỉ 0.016%), hoàn toàn không gây sai lệch nhãn mục tiêu trong khi giúp dữ liệu giỏ hàng hoàn toàn sạch.
> 2. **Bảng `coupon` (124.5k dòng):** Khử trùng triệt để 5,164 bản ghi trùng lặp 100% (exact duplicates), thu gọn còn 119,384 dòng ánh xạ SKU hợp lệ để ngăn chặn hiện tượng nhân đôi dòng khi kết nối bảng.
> 3. **Bảng nhân khẩu học `hh_demographic` (801 hộ, 32.0%):** Nhóm kiên quyết không drop 68% số hộ thiếu thông tin để tránh sai lệch chọn mẫu (selection bias). Thay vào đó, 1,699 hộ khuyết thiếu được mã hóa thành một nhóm `UNKNOWN` độc lập, bảo toàn trọn vẹn 100% cỡ mẫu 2,500 hộ gia đình.
> 4. **Bảng chiến dịch và đổi coupon:** Chuẩn hóa 3 loại chiến dịch (Loại A, B, C) gửi tới 1,584 hộ; kiểm toán bảng `coupon_redempt` (2,318 lượt đổi thực tế từ 434 hộ) đạt 0 bản ghi trùng lặp và 100% khớp nối khóa ngoại.
> 5. **Bảng sản phẩm `product` (92.4k SKU):** Bóc tách danh mục thực phẩm tươi sống (`perishables`) trên 44 ngành hàng.
> 6. **Bảng `causal_data` (36.8 triệu dòng):** Nhóm chủ động loại bỏ khỏi baseline vì dữ liệu ở cấp cửa hàng/tuần (*store-week*), độ thưa cao và không liên kết được với hành vi dừng chân thực tế của từng hộ gia đình."*

---

### Slide 4: Căn cứ thực nghiệm xác lập chân trời dự báo $\Delta t = 14$ ngày
* **Tiêu đề:** 3. Căn cứ thực nghiệm xác lập chân trời dự báo $\Delta t = 14$ ngày
* **Thời lượng:** 60 giây
* **Biểu đồ:** Đường cong tích lũy hộ gia đình mua sắm theo chân trời dự báo $H \in [1, 56]$ ngày, trung bình qua 5 mốc chốt sổ quan sát.

**Lời thoại trình bày:**
> *"Một quyết định thiết kế bài toán then chốt là: Nên dự đoán xác suất mua hàng trong bao nhiêu ngày tới? Để trả lời bằng thực nghiệm, nhóm quét độ dài chân trời dự báo $H$ từ 1 đến 56 ngày qua 5 mốc chốt sổ đại diện:
> - **Nếu chọn $H = 7$ ngày:** Tỷ lệ hộ phát sinh giao dịch chỉ đạt **53.4%**, quá thấp và bỏ sót gần 47% hộ gia đình có chu kỳ đi chợ 2 tuần một lần, tạo áp lực vận hành quá gấp cho đội ngũ tiếp thị.
> - **Nếu chọn $H = 28$ ngày:** Tỷ lệ dương tính lên tới **80.2%**, đường cong bão hòa khiến lớp mục tiêu mất cân bằng nặng và làm suy giảm độ nhạy phân loại của mô hình học máy.
> - **Tại $H = 14$ ngày:** Tỷ lệ hộ có phát sinh mua sắm đạt **68.3%** với độ lệch chuẩn cực kỳ hẹp giữa các cutoff (chỉ $\pm 1.0\%$). Đây là điểm cân bằng lý tưởng: vừa đảm bảo tỷ lệ lớp mục tiêu phân hóa tự nhiên (khoảng 2/3 dương tính, 1/3 âm tính), vừa mang lại khoảng đệm 2 tuần đủ dài để các chiến dịch marketing có thể can thiệp hiệu quả."*

---

### Slide 5: Khoảng cách từ lần mua gần nhất phản ánh độ suy giảm xác suất mua (Recency)
* **Tiêu đề:** 4. Khoảng cách từ lần mua gần nhất phản ánh độ suy giảm xác suất mua
* **Thời lượng:** 50 giây
* **Biểu đồ:** Tỷ lệ $P(Y=1)$ theo 5 nhóm Recency (`0 - 3 ngày`, `4 - 7 ngày`, `8 - 14 ngày`, `15 - 30 ngày`, `> 30 ngày / Chưa mua`).

**Lời thoại trình bày:**
> *"Bước sang khám phá đặc trưng hành vi, Recency — tức số ngày kể từ lần mua cuối cùng đến $t_0$ — là biến đơn lẻ có lực phân tách mạnh nhất:
> - Nhóm khách hàng vừa đi chợ trong **0 đến 3 ngày qua** ($n = 959$ hộ) đạt xác suất mua trong 14 ngày tới lên tới **88.5%**, vượt mức trung bình toàn mẫu 20.2 điểm phần trăm.
> - Ngược lại, với nhóm đã qua **trên 30 ngày chưa mua sắm hoặc chưa có lịch sử** ($n = 468$ hộ), xác suất mua sắm rơi dốc thẳng đứng về mức **24.1%**.
> - Chênh lệch giữa hai nhóm cực trị lên tới **64.4 điểm phần trăm**. Điều này khẳng định quán tính tiêu dùng suy giảm rất nhanh theo thời gian vắng bóng.
> - Nhóm chuyển giao hai biến đại diện: `days_since_last_basket` và `urgency_ratio` (tỷ lệ trễ so với chu kỳ mua trung bình của chính hộ đó)."*

---

### Slide 6: Tần suất mua sắm quá khứ phân hóa khả năng quay lại của khách hàng (Frequency)
* **Tiêu đề:** 5. Tần suất mua sắm quá khứ phân hóa khả năng quay lại của khách hàng
* **Thời lượng:** 50 giây
* **Biểu đồ:** Tỷ lệ $P(Y=1)$ theo số giỏ hàng trong 90 ngày (`0 giỏ`, `1 - 5 giỏ`, `6 - 15 giỏ`, `16 - 25 giỏ`, $\ge 25$ giỏ).

**Lời thoại trình bày:**
> *"Đặc trưng thứ hai là Tần suất mua sắm trong 90 ngày (`baskets_count_90d`):
> - Nhóm hộ hoàn toàn không phát sinh giỏ hàng nào trong 90 ngày ($n = 199$ hộ) chỉ có xác suất mua 14 ngày tới là **12.4%**, phản ánh nhóm khách hàng đã ngừng hoạt động (churn/dormant).
> - Khi số giỏ hàng tăng từ 1–5 giỏ lên 6–15 giỏ, xác suất mua tăng vọt từ **47.2%** lên **77.9%**.
> - Với các hộ đi chợ thường xuyên từ **16 giỏ trở lên** (tương đương hơn 1 lần/tuần), xác suất tái mua tiệm cận mức bão hòa **88.3% đến 92.5%**.
> - Tổng mức phân tách giữa nhóm tích cực nhất và nhóm không hoạt động đạt tới **80.1 điểm phần trăm**.
> - Nhóm chuyển giao biến `baskets_count_90d` và `freq_momentum` (tỷ lệ so sánh tần suất 30 ngày gần nhất so với trung bình 90 ngày)."*

---

### Slide 7: Mức chi tiêu quá khứ đồng biến với khả năng tiếp tục mua sắm (Spend)
* **Tiêu đề:** 6. Mức chi tiêu quá khứ đồng biến với khả năng tiếp tục mua sắm
* **Thời lượng:** 50 giây
* **Biểu đồ:** Tỷ lệ $P(Y=1)$ theo tổng chi tiêu 90 ngày ($0, <$300, $300–$700, $700–$1,300, $\ge $1,300).

**Lời thoại trình bày:**
> *"Đặc trưng thứ ba là Tổng mức chi tiêu tích lũy trong 90 ngày (`spend_90d`):
> - Xác suất mua đồng biến rõ rệt với quy mô dòng tiền: Hộ chi tiêu dưới \$300 chỉ đạt xác suất mua **52.2%**, trong khi hộ chi tiêu trên \$1,300 đạt xác suất lên tới **91.1%** (chênh lệch +38.9 điểm phần trăm).
> - **Phân tầng kiểm soát (Stratified Analysis):** Một câu hỏi phương pháp luận quan trọng là: Chi tiêu có thực sự mang lại tín hiệu độc lập, hay chỉ là hệ quả của việc đi chợ nhiều lần? Khi kiểm soát cố định trong cùng tầng Frequency (1–5 giỏ), hộ có mức chi tiêu cao ($300–$700) đạt xác suất mua **76.0%**, cao hơn vượt bậc so với hộ chi tiêu thấp (<\$100, đạt **38.4%**, chênh lệch +37.6 pp).
> - Điều này chứng minh Spend chứa đựng thông tin độc lập về độ gắn kết ngân sách, không bị triệt tiêu hoàn toàn bởi tần suất đi chợ."*

---

### Slide 8: Độ phủ ngành hàng phản ánh mức độ gắn kết với siêu thị (Category Breadth)
* **Tiêu đề:** 7. Độ phủ ngành hàng phản ánh mức độ gắn kết với siêu thị
* **Thời lượng:** 50 giây
* **Biểu đồ:** Tỷ lệ $P(Y=1)$ theo số ngành hàng đã mua trong 90 ngày (0 ngành, 1–2 ngành, 3–6 ngành, 7–11 ngành, $\ge 12$ ngành).

**Lời thoại trình bày:**
> *"Đặc trưng thứ tư là Độ phủ ngành hàng (`department_breadth_90d`):
> - Khách hàng mua sắm giỏ hàng đơn ngành (1–2 ngành hàng) chỉ đạt xác suất mua **31.8%** ($n = 160$ hộ). Họ chỉ ghé siêu thị để mua một vài mặt hàng tiện lợi rời rạc.
> - Ngược lại, nhóm khách hàng đại siêu thị mua sắm toàn diện từ **12 ngành hàng trở lên** ($n = 241$ hộ) đạt xác suất quay lại lên tới **96.5%**.
> - Biên độ phân tách đạt tới **84.2 điểm phần trăm** trên toàn bộ tập mẫu 2,500 hộ gia đình.
> - Kiểm tra phân tầng cho thấy trong cùng tầng Frequency trung bình (6–15 giỏ), hộ mua danh mục rộng đạt xác suất mua cao hơn hộ mua hẹp tới **19.7 điểm phần trăm** (83.7% vs 64.0%). Độ rộng danh mục là minh chứng thực nghiệm cho thấy hộ đã xem siêu thị là điểm đến mua sắm trọn gói chính yếu của gia đình."*

---

### Slide 9: Thời gian chưa mua thực phẩm tươi sống kích thích chuyến đi chợ mới (Perishables)
* **Tiêu đề:** 8. Thời gian chưa mua thực phẩm tươi sống kích thích chuyến đi chợ mới
* **Thời lượng:** 50 giây
* **Biểu đồ:** Tỷ lệ $P(Y=1)$ theo số ngày kể từ lần mua thực phẩm tươi sống gần nhất (`0 - 3 ngày`, `4 - 7 ngày`, `8 - 14 ngày`, `15 - 30 ngày`, `> 30 ngày / Chưa mua`).

**Lời thoại trình bày:**
> *"Đặc trưng thứ năm là Khoảng cách mua thực phẩm tươi sống (`days_since_last_perishable`).
> - **Làm rõ ranh giới danh mục:** Nhóm đã chuẩn hóa danh mục hàng tươi sống chuẩn mực (gồm Rau củ quả, Thịt tươi, Thịt đóng gói, Thủy hải sản, Sữa, Bánh mì tươi, Thực phẩm chín chế biến sẵn), loại bỏ hoàn toàn ngành hàng `GROCERY` khô thông thường để tránh méo mó chu kỳ bảo quản.
> - Kết quả thực nghiệm cho thấy: Hộ vừa mua thực phẩm tươi sống trong **0–3 ngày qua** đạt xác suất mua **89.7%** ($n = 658$ hộ), phản ánh nhóm khách hàng có thói quen đi chợ nấu ăn đều đặn hàng tuần.
> - Khi thời gian vắng bóng đồ tươi vượt quá **30 ngày**, xác suất mua rơi về **35.0%** (giảm 54.7 điểm phần trăm). Nhu cầu bổ sung thực phẩm tươi sống chính là xung lực tự nhiên thúc đẩy nhịp điệu quay lại siêu thị."*

---

### Slide 10: Tác động của việc nhắm mục tiêu chiến dịch tiếp thị (Campaigns)
* **Tiêu đề:** 9. Tác động của việc nhắm mục tiêu chiến dịch tiếp thị
* **Thời lượng:** 50 giây
* **Biểu đồ:** Xác suất $P(Y=1)$ theo trạng thái chiến dịch active tại $t_0$ (Không có chiến dịch: 59.9%, Loại C: 88.5%, Loại B: 90.7%, Loại A: 86.7%).

**Lời thoại trình bày:**
> *"Đặc trưng thứ sáu là Tình trạng nhắm mục tiêu của các chiến dịch tiếp thị đang kích hoạt tại $t_0$:
> - Nhóm hộ gia đình có ít nhất một chiến dịch đang có hiệu lực tại mốc chốt sổ đạt xác suất mua sắm trong 14 ngày tới từ **86.7% đến 90.7%**, vượt trội **27 đến 30 điểm phần trăm** so với nhóm không có chiến dịch nào kích hoạt (59.9%, $n = 1,827$ hộ).
> - Đào sâu vào hiệu quả chuyển đổi đổi phiếu coupon trên 7,208 cặp (hộ, chiến dịch): Chiến dịch **Loại A (Đa ngành hàng)** có tỷ lệ đổi coupon đạt **15.96%**, cao gấp 2.08 lần so với Loại B (7.91%) và Loại C (7.67%).
> - **Lưu ý phương pháp luận:** Đây là mối liên hệ mang giá trị dự báo (predictive association), phản ánh bộ phận tiếp thị của siêu thị đã nhắm mục tiêu vào nhóm khách hàng tiềm năng; phân tích này không suy diễn quan hệ nhân quả (causality).
> - Nhóm chuyển giao các biến chỉ báo nhị phân: `is_targeted_type_A`, `type_B`, `type_C`."*

---

### Slide 11: Lịch sử sử dụng phiếu giảm giá gắn liền với xác suất tái mua (Coupons)
* **Tiêu đề:** 10. Lịch sử sử dụng phiếu giảm giá gắn liền với xác suất tái mua
* **Thời lượng:** 45 giây
* **Biểu đồ:** Xác suất $P(Y=1)$ theo số lần đổi coupon trong 180 ngày (0 lần, 1–2 lần, $\ge 3$ lần).

**Lời thoại trình bày:**
> *"Đặc trưng thứ bảy là Lịch sử đổi phiếu giảm giá coupon trong 180 ngày (`coupon_redemptions_180d`):
> - Trong 2,500 hộ gia đình, có 434 hộ từng thực hiện ít nhất 1 lần đổi coupon với 2,318 lượt đổi thực tế.
> - Hộ gia đình có lịch sử đổi **1–2 lần coupon** đạt xác suất mua **92.5%** ($n = 80$ hộ). Với nhóm đổi tích cực từ **3 lần trở lên**, xác suất mua đạt tới **94.7%** ($n = 14$ hộ).
> - Ngược lại, nhóm không đổi coupon nào ($n = 2,406$ hộ) chỉ đạt xác suất mua trung bình **67.4%**.
> - Chênh lệch đạt **27.3 điểm phần trăm**. Hành vi cất công sưu tầm và xuất trình coupon tại quầy thanh toán là một chỉ báo hành vi mạnh mẽ cho thấy sự gắn bó và chủ động lên kế hoạch mua sắm của khách hàng."*

---

### Slide 12: Mức độ tập trung chi tiêu tại cửa hàng chính (Store Loyalty)
* **Tiêu đề:** 11. Mức độ tập trung chi tiêu tại cửa hàng chính
* **Thời lượng:** 50 giây
* **Biểu đồ:** Xác suất $P(Y=1)$ theo tỷ trọng chi tiêu tại cửa hàng chính trong 90 ngày (Phân tán <50%, Trung bình 50–80%, Tập trung $\ge 80\%$, Không mua).

**Lời thoại trình bày:**
> *"Đặc trưng thứ tám là Mức độ tập trung chi tiêu tại cửa hàng chính (`primary_store_spend_share`):
> - Hơn **91% hộ gia đình** có phát sinh chi tiêu dồn quá nửa ngân sách vào một cửa hàng duy nhất; trong đó nhóm tập trung cao ($\ge 80\%$ tiền) chiếm tới **61.7% số hộ** ($n = 1,419$ hộ).
> - **Mối liên hệ nghịch (-) thú vị:** Nhóm dồn toàn bộ ngân sách vào một cửa hàng chính có xác suất mua 14 ngày tới là **70.4%**. Trong khi đó, nhóm khách hàng phân tán chi tiêu ghé nhiều siêu thị khác nhau (<50% tiền, $n = 196$ hộ) lại có xác suất mua cao hơn, đạt **82.8%** (chênh lệch +12.4 pp).
> - Kiểm tra phân tầng theo Frequency xác nhận hiện tượng này: Khách hàng mua sắm tại nhiều chi nhánh là những khách hàng có tần suất đi chợ cao và mức độ năng động tiêu dùng lớn. Do đó trong ma trận đặc trưng, biến này mang mối quan hệ nghịch (-) với xác suất mua."*

---

### Slide 13: Thông tin nhân khẩu học và giá trị của nhóm không khai báo (Demographics)
* **Tiêu đề:** 12. Thông tin nhân khẩu học và giá trị của nhóm không khai báo
* **Thời lượng:** 50 giây
* **Biểu đồ:** Xác suất $P(Y=1)$ theo quy mô hộ gia đình (1–2 người, 3–4 người, 5+ người) và nhóm `UNKNOWN`.

**Lời thoại trình bày:**
> *"Đặc trưng thứ chín là Thông tin nhân khẩu học (`hh_demographic`):
> - Trong số 801 hộ có khai báo thông tin, xác suất mua tăng dần theo quy mô hộ: Từ **75.4%** ở hộ 1–2 người ($n = 483$ hộ), lên **76.2%** ở hộ 3–4 người ($n = 257$ hộ), và đạt **80.2%** ở hộ gia đình đông nhân khẩu từ 5 người trở lên ($n = 61$ hộ). Quy mô gia đình càng lớn thì nhu cầu tái bổ sung nhu yếu phẩm càng diễn ra thường xuyên.
> - **Giá trị của nhóm `UNKNOWN`:** Chiếm tới 68% tập mẫu ($n = 1,699$ hộ) với xác suất mua sắm đạt **64.5%**. Việc không loại bỏ mà giữ nguyên nhóm `UNKNOWN` làm một phân lớp độc lập giúp mô hình học máy vừa tận dụng được tín hiệu phân hóa của nhóm có dữ liệu, vừa duy trì đầy đủ tính bao phủ trên toàn bộ khách hàng của chuỗi bán lẻ."*

---

### Slide 14: Ma trận chuyển giao đặc trưng sang giai đoạn mô hình hóa
* **Tiêu đề:** 13. Ma trận chuyển giao đặc trưng sang giai đoạn mô hình hóa
* **Thời lượng:** 60 giây
* **Bảng:** Ma trận tổng hợp 9 nhóm đặc trưng, cửa sổ thời gian, tên biến đại diện trong pipeline `feature_builder.py`, chiều quan hệ thực nghiệm với $Y$, và ý nghĩa vật lý.

**Lời thoại trình bày:**
> *"Từ toàn bộ các kết quả khám phá thực nghiệm, nhóm đúc kết thành **Ma trận chuyển giao 9 nhóm đặc trưng cốt lõi** cho pipeline mô hình hóa `feature_builder.py`:
> 1. **Recency:** Cửa sổ $\le t_0$, quan hệ nghịch (-), biến `days_since_last_basket`, `urgency_ratio`.
> 2. **Frequency:** Cửa sổ 90d, quan hệ đồng (+), biến `baskets_count_90d`, `freq_momentum`.
> 3. **Spend & AOV:** Cửa sổ 90d, quan hệ đồng (+), biến `spend_90d`, `aov_90d`.
> 4. **Breadth:** Cửa sổ 90d, quan hệ đồng (+), biến `department_breadth_90d`.
> 5. **Perishables:** Cửa sổ $\le t_0$, quan hệ nghịch (-), biến `days_since_last_perishable`.
> 6. **Campaigns:** Tại $t_0$, quan hệ đồng (+), biến `is_targeted_type_A`, `type_B`, `type_C`.
> 7. **Coupons:** Cửa sổ 180d, quan hệ đồng (+), biến `coupon_redemptions_180d`.
> 8. **Store Loyalty:** Cửa sổ 90d, quan hệ nghịch (-), biến `primary_store_spend_share`.
> 9. **Demographics:** Cố định, biến phân nhóm quy mô hộ và cờ nhị phân `is_demographics_unknown`.
>
> 100% các biến đều tuân thủ nghiêm ngặt nguyên tắc Point-in-Time, sẵn sàng đưa vào huấn luyện mô hình LightGBM, XGBoost và CatBoost."*

---

### Slide 15: Phụ lục: Mức độ tập trung doanh thu theo hộ gia đình (Pareto & Gini)
* **Tiêu đề:** 14. Phụ lục: Mức độ tập trung doanh thu theo hộ gia đình
* **Thời lượng:** 40 giây
* **Biểu đồ:** Đường cong Lorenz biểu diễn mức độ tập trung doanh thu tích lũy của 2,500 hộ gia đình so với đường phân bổ bình đẳng.

**Lời thoại trình bày:**
> *"Ở phần Phụ lục dành cho góc nhìn kinh doanh, biểu đồ đường cong Lorenz chứng minh mức độ tập trung doanh thu bán lẻ:
> - **Quy luật Pareto:** Top **20% hộ gia đình chi tiêu nhiều nhất** (500 hộ) đóng góp tới **73.1% tổng doanh thu** của toàn bộ chuỗi siêu thị (tương đương 5.89 triệu USD trên tổng số 8.06 triệu USD).
> - **Hệ số Gini:** Được tính toán chuẩn xác theo công thức hình thang giải tích đạt **0.5028**, phản ánh mức độ tập trung doanh thu ở mức trung bình cao trong phân tích hành vi khách hàng bán lẻ.
> - Đây là căn cứ để bộ phận kinh doanh phân tầng chiến lược CRM: ưu tiên giữ chân top 20% khách hàng cốt lõi."*

---

### Slide 16: Phụ lục: Cấu trúc chiết khấu niêm yết tại quầy vs phiếu giảm giá
* **Tiêu đề:** 15. Phụ lục: Cấu trúc chiết khấu niêm yết tại quầy vs phiếu giảm giá
* **Thời lượng:** 40 giây
* **Biểu đồ:** Đối sánh ngân sách chiết khấu và tỷ lệ bao phủ giỏ hàng giữa Giảm giá tại quầy (`RETAIL_DISC`) và Phiếu giảm giá (`COUPON_DISC`).

**Lời thoại trình bày:**
> *"Phụ lục tiếp theo bóc tách cấu trúc giảm giá hai tầng trong bán lẻ:
> - **Giảm giá niêm yết tại quầy (`RETAIL_DISC`):** Đạt quy mô **1.40 triệu USD**, xuất hiện trong **83.67% tổng số giỏ hàng** (230,554 giỏ hàng).
> - **Phiếu giảm giá coupon (`COUPON_DISC`):** Đạt quy mô **42.6 nghìn USD**, chỉ bao phủ **6.08% số giỏ hàng** (16,741 giỏ hàng).
> - Quy mô giảm giá tại quầy lớn gấp **32.8 lần** so với ngân sách coupon. Điều này chỉ ra rằng giảm giá niêm yết là chi phí thương mại đại trà trên kệ, trong khi coupon đóng vai trò là công cụ tiếp thị cá nhân hóa nhắm chọn lọc vào nhóm khách hàng nhạy cảm giá."*

---

### Slide 17: Phụ lục: Tỷ trọng danh mục và doanh thu của nhãn hàng riêng (Private Label)
* **Tiêu đề:** 16. Phụ lục: Tỷ trọng danh mục và doanh thu của nhãn hàng riêng
* **Thời lượng:** 40 giây
* **Biểu đồ:** Đối sánh tỷ trọng SKU (15.0%) vs Tỷ trọng Doanh thu (27.8%) và Tỷ trọng Sản lượng (28.8%) của nhãn hàng riêng.

**Lời thoại trình bày:**
> *"Phụ lục thứ ba phân tích hiệu quả thương hiệu riêng của siêu thị (Private Label):
> - Mặt hàng nhãn riêng chỉ chiếm **14.96% số lượng SKU trên kệ** (13,812 / 92,353 SKU).
> - Tuy nhiên, nhãn riêng lại đóng góp tới **27.77% tổng doanh thu** (2.24 triệu USD) và **28.75% tổng sản lượng** hàng hóa bán ra.
> - Hiệu suất doanh thu trên mỗi SKU nhãn riêng đạt **1.86x**, cao gấp **2.18 lần** so với thương hiệu quốc gia thông thường (0.85x). Nhãn riêng chính là nhóm hàng thiết yếu có hiệu suất doanh số và biên lợi nhuận cao nhất của chuỗi."*

---

### Slide 18: Phụ lục: Nhịp điệu thời gian theo chu kỳ ngày và khung giờ mua sắm
* **Tiêu đề:** 17. Phụ lục: Nhịp điệu thời gian theo chu kỳ ngày và khung giờ mua sắm
* **Thời lượng:** 40 giây
* **Biểu đồ:** Phân phối giỏ hàng theo chu kỳ 7 ngày (`DAY mod 7`, bên trái) và Khung giờ mua sắm trong ngày (bên phải).

**Lời thoại trình bày:**
> *"Phụ lục cuối cùng khảo sát nhịp điệu thời gian của 275,542 giỏ hàng sạch:
> - **Chu kỳ ngày:** Phân phối ngày trong tuần cho thấy lượng giỏ hàng đạt đỉnh vào Ngày 4 và Ngày 5 ($pprox 16.0\%$ mỗi ngày), các ngày còn lại duy trì ổn định từ 13.3% đến 14.0%.
> - **Khung giờ mua sắm:** Toàn bộ hoạt động mua sắm tập trung cao độ vào khung từ **11 giờ trưa đến 18 giờ chiều**, chiếm tới **62.93% tổng số giỏ hàng** (hơn 173,000 giỏ), với đỉnh cao nhất rơi vào khoảng 16h–17h.
> - Phát hiện này hỗ trợ trực tiếp cho vận hành: Siêu thị có thể tối ưu ca trực quầy thu ngân và nhân sự châm hàng tươi sống vào khung giờ cao điểm buổi chiều.
>
> Em xin chân thành cảm ơn quý thầy cô và các bạn đã lắng nghe. Nhóm xin sẵn sàng tiếp nhận các câu hỏi phản biện."*

---

## Bộ câu hỏi & trả lời dự phòng cho phần Q&A (Anticipated Q&A)

### Câu hỏi 1: Tại sao nhóm chọn chân trời dự báo $\Delta t = 14$ ngày dựa trên tỷ lệ hộ thay vì khoảng cách giữa các chuyến đi chợ?
> **Trả lời:**  
> *"Thưa thầy cô, khoảng cách trung bình giữa các chuyến đi chợ của toàn bộ các hộ hoạt động là khoảng 6–7 ngày. Tuy nhiên, nếu đặt cửa sổ dự báo là 7 ngày thì chỉ có 53.4% số hộ phát sinh giao dịch. Điều này xuất phát từ việc phân phối chu kỳ đi chợ có phương sai lớn: rất nhiều hộ đi chợ 10–14 ngày một lần.  
> Nếu chọn $H = 7$ ngày, mô hình sẽ gắn nhãn 0 cho gần một nửa số hộ khách hàng hoàn toàn khỏe mạnh chỉ vì chu kỳ của họ là 10 ngày, tạo ra nhiều nhãn âm giả (false negative). Cửa sổ $\Delta t = 14$ ngày đạt tỷ lệ dương tính ổn định 68.3% với độ lệch chuẩn cực kỳ hẹp ($\pm 1.0\%$), đảm bảo tính ổn định thời gian và cho phép bộ phận marketing có đủ thời gian 2 tuần để triển khai các chương trình CRM can thiệp."*

### Câu hỏi 2: Mối quan hệ giữa tiếp cận chiến dịch tiếp thị (Campaigns) và xác suất mua lại có phải là quan hệ nhân quả (Causality) không?
> **Trả lời:**  
> *"Thưa thầy cô, chúng em khẳng định đây hoàn toàn là **mối liên hệ tương quan mang giá trị dự báo (predictive association)**, chứ **không phải quan hệ nhân quả (causality hay uplift)**.  
> Trong dữ liệu quan sát bán lẻ, bộ phận marketing thường chủ động lựa chọn các hộ gia đình có lịch sử mua sắm tích cực để gửi chiến dịch. Do đó, việc nhóm nhận chiến dịch có xác suất mua cao hơn (+27 đến +30 điểm phần trăm) một phần phản ánh bản thân họ đã là nhóm khách hàng trung thành từ trước. Đối với bài toán dự đoán xác suất Propensity ($Y \in \{0, 1\}$), tín hiệu này có giá trị phân tách mạnh và hoàn toàn hợp lệ khi tuân thủ Point-in-Time; nhưng chúng em không diễn giải rằng chiến dịch đã kích thích hay gây ra hành vi mua hàng đó."*

### Câu hỏi 3: Tại sao biến Mức độ tập trung cửa hàng chính (Store Loyalty) lại có quan hệ nghịch (-) với xác suất mua hàng?
> **Trả lời:**  
> *"Thưa thầy cô, trên biểu đồ đơn biến, nhóm hộ phân tán chi tiêu ghé nhiều cửa hàng (<50% tiền) có xác suất mua là 82.8%, cao hơn so với nhóm dồn $\ge 80\%$ ngân sách vào 1 cửa hàng (70.4%).  
> Để kiểm chứng hiện tượng này, nhóm đã thực hiện phân tích phân tầng (stratified analysis) kiểm soát theo Tần suất (Frequency). Kết quả cho thấy trong cùng tầng Frequency, các hộ ghé nhiều cửa hàng vẫn có xác suất mua cao hơn hoặc tương đương. Lý do là trong mạng lưới bán lẻ Dunnhumby, những khách hàng ghé nhiều chi nhánh thường là những người có mức độ năng động sinh hoạt cao, di chuyển nhiều giữa nơi làm việc và nơi cư trú, và có nhu cầu mua sắm liên tục. Do đó, tỷ trọng dồn vào cửa hàng chính càng thấp thì xác suất có ít nhất một chuyến mua sắm trong 14 ngày tới càng cao."*

### Câu hỏi 4: Việc loại bỏ 942 giỏ hàng chi tiêu $\le \$0$ có làm thiên lệch hoặc rò rỉ nhãn mục tiêu không?
> **Trả lời:**  
> *"Thưa thầy cô, hoàn toàn không làm thiên lệch nhãn. Chúng em đã thực hiện kiểm toán định lượng nghiêm ngặt trên toàn bộ 12,500 cặp (hộ, cutoff) trải qua 5 mốc chốt sổ quan sát:  
> Khi so sánh nhãn $Y$ tính trên dữ liệu thô và nhãn $Y$ tính trên 275,542 giỏ hàng sạch, chỉ có đúng **2 nhãn bị chuyển từ 1 sang 0** tại duy nhất mốc $t_0 = 550$ (tỷ lệ thay đổi chỉ 0.016%), và 0 nhãn bị thay đổi tại 4 mốc còn lại.  
> Việc loại bỏ 942 giỏ hàng này loại bỏ các giao dịch quẹt thẻ kỹ thuật, sửa lỗi thu ngân và quà tặng $0, bảo đảm nhãn $Y$ phản ánh đúng bản chất giao dịch thương mại sạch mà không làm méo mó phân phối nhãn."*

### Câu hỏi 5: Tại sao nhóm không điền khuyết (impute) cho 68% số hộ thiếu thông tin nhân khẩu học?
> **Trả lời:**  
> *"Thưa thầy cô, trong bán lẻ, dữ liệu nhân khẩu học khuyết thiếu thường là Missing Not At Random (MNAR) — khách hàng từ chối cung cấp thông tin thường có đặc điểm hành vi khác biệt so với nhóm chủ động khai báo. Nếu chúng em dùng các phương pháp điền khuyết như mode, mean hay KNN, chúng ta sẽ áp đặt giả định nhân tạo làm biến dạng cấu trúc phân phối tự nhiên.  
> Thay vào đó, việc mã hóa 1,699 hộ thành nhóm `UNKNOWN` độc lập cho phép các mô hình cây quyết định như LightGBM hay XGBoost tự động tìm điểm phân nhánh tối ưu dựa trên chính trạng thái 'không khai báo', bảo toàn trọn vẹn 100% tập mẫu mà không tạo ra sai lệch chọn mẫu (selection bias)."*
