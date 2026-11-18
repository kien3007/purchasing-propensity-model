# Kịch bản trình bày báo cáo khám phá dữ liệu & kiểm toán chất lượng (EDA & Data Quality)
## Xây dựng mô hình dự đoán xác suất mua hàng bán lẻ (Purchasing Propensity Model)
### Bộ dữ liệu: Dunnhumby — The Complete Journey (2,500 Hộ gia đình, 2.59 Triệu giao dịch, 8 Bảng, 711 Ngày)

---

## Cấu trúc tổng thể bài trình bày (Narrative Arc)

Bài thuyết trình kéo dài **15 phút** (gồm 12 phút trình bày mạch chính và 3 phút Q&A), được chuẩn hóa theo kiến trúc 16 slides (10 slide mạch chính + 6 slide phụ lục):

1. **Phần 1: Thiết kế bài toán & Kiểm toán chất lượng dữ liệu (Slides 1 – 3 | 2.5 phút):**
   - Thiết lập bài toán học máy: Đơn vị hộ gia đình ($n = 2,500$ hộ panel), chân trời dự báo $\Delta t = 14$ ngày, kỷ luật thời gian Point-in-Time ($DAY \le t_0$).
   - Kết quả kiểm toán 8 bảng dữ liệu Dunnhumby: Khử trùng 5,164 dòng coupon, mã hóa 1,699 hộ `UNKNOWN`, kiểm chứng JOIN đạt 100%, loại 942 giỏ hàng phi thương mại (chỉ làm thay đổi 0.016% nhãn).
2. **Phần 2: Căn cứ xác lập chân trời dự báo & Phân tích tín hiệu hành vi (Slides 4 – 9 | 6.5 phút):**
   - Căn cứ thực nghiệm chọn $\Delta t = 14$ ngày (Base rate 68.3%, std $\pm 1.0\%$).
   - Khám phá 8 nhóm đặc trưng học máy cốt lõi (Recency $\times$ Frequency heatmap, Phân tầng Spend & Breadth, Hàng tươi sống, Chiến dịch & Coupon, Mạng lưới cửa hàng & Nhóm UNKNOWN).
3. **Phần 3: Ma trận chuyển giao 28 đặc trưng sang Feature Engineering (Slide 10 | 1.5 phút):**
   - Chuyển giao 28 biến đặc trưng đã kiểm chứng thực nghiệm, tuân thủ 100% ranh giới Point-in-Time.
4. **Phần 4: Phụ lục chuyên sâu & Quản trị bán lẻ (Slides 11 – 16 | 1.5 phút dùng khi tra cứu hoặc phản biện):**
   - Sơ đồ ERD 8 bảng dữ liệu, phân phối AOV giỏ hàng, quy luật Pareto & Gini ($0.5028$), cấu trúc chiết khấu 2 tầng, thâm nhập nhãn hàng riêng (Private Label), và nhịp điệu mua sắm theo giờ.
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

### Slide 2: 1. Thiết kế bài toán: Dự đoán hộ gia đình có mua hàng trong 14 ngày tới
* **Tiêu đề:** 1. Thiết kế bài toán: Dự đoán hộ gia đình có mua hàng trong 14 ngày tới
* **Thời lượng:** 60 giây
* **Trực quan:** Sơ đồ timeline trực quan hóa dòng thời gian với 3 khối: Cửa sổ lịch sử 90 ngày ($DAY \le t_0$), Điểm chốt sổ $t_0$, và Cửa sổ nhãn 14 ngày ($(t_0, t_0 + 14]$).

**Lời thoại trình bày:**
> *"Trước khi bước vào phân tích dữ liệu, nhóm đã xác lập một khung bài toán học máy minh bạch và nhất quán như thể hiện trên sơ đồ timeline:
> - **Đơn vị dự báo:** Cấp hộ gia đình (`household_key`). Toàn bộ 2,500 hộ gia đình là một panel khách hàng cố định được chuỗi siêu thị theo dõi xuyên suốt nghiên cứu.
> - **Cửa sổ quan sát hành vi ($T_{obs}$):** 90 ngày trước mốc chốt sổ $t_0$ ($DAY \le t_0$) để trích xuất các đặc trưng tần suất, chi tiêu và danh mục.
> - **Cửa sổ dự báo ($\Delta t$):** 14 ngày tới ($DAY \in (t_0, t_0 + 14]$).
> - **Nhãn mục tiêu ($Y$):** Biến nhị phân $Y \in \{0, 1\}$. $Y = 1$ nếu hộ có phát sinh ít nhất một giỏ hàng sạch có chi tiêu dương ($SALES\_VALUE > 0$) trong 14 ngày tiếp theo; ngược lại $Y = 0$.
>
> Về mặt phương pháp luận, chúng em áp dụng triệt để **kỷ luật Point-in-Time**: 100% biến đặc trưng chỉ được tính toán từ các sự kiện phát sinh trước hoặc tại thời điểm $t_0$. Mọi thông tin sau $t_0$ tuyệt đối chỉ được dùng để gán nhãn mục tiêu $Y$, triệt tiêu hoàn toàn nguy cơ rò rỉ dữ liệu từ tương lai (data leakage).
>
> Để đánh giá mô hình khách quan, nhóm áp dụng chiến lược chia tập **Multi-cutoff**: Tập Huấn luyện gồm 11 mốc chốt sổ trượt $t_0 \in [200, 500]$, Tập Xác thực gồm 3 mốc $t_0 \in [530, 590]$, và Tập Kiểm thử độc lập gồm 2 mốc $t_0 \in [650, 680]$ hoàn toàn tách biệt về mặt thời gian."*

---

### Slide 3: 2. Kiểm toán 8 bảng: Loại bỏ nhiễu, chuẩn hóa khóa nối và bảo toàn mẫu
* **Tiêu đề:** 2. Kiểm toán 8 bảng: Loại bỏ nhiễu, chuẩn hóa khóa nối và bảo toàn mẫu
* **Thời lượng:** 60 giây
* **Trực quan:** Bảng kiểm toán số dòng thô vs dòng sạch cho từng bảng ở cột trái; 3 kết luận kiểm chứng toàn vẹn & nhãn ở cột phải.

**Lời thoại trình bày:**
> *"Trên màn hình là kết quả kiểm toán chất lượng và xử lý làm sạch then chốt trên 8 bảng dữ liệu:
> 1. **Bảng giao dịch `transaction_data` (2.59M dòng):** Chúng em kiểm toán và loại bỏ 942 giỏ hàng phi thương mại có chi tiêu $\le \$0$ (chiếm 0.34% tổng số giỏ hàng, đóng góp đúng \$0 doanh thu). Kiểm toán định lượng trên toàn bộ 12,500 cặp (hộ, cutoff) qua 5 mốc chốt sổ cho thấy việc loại 942 giỏ này chỉ làm thay đổi đúng 2 nhãn từ 1 sang 0 tại mốc $t_0 = 550$ (tỷ lệ ảnh hưởng chỉ 0.016%), hoàn toàn không gây sai lệch nhãn mục tiêu trong khi giúp dữ liệu giỏ hàng hoàn toàn sạch (275,542 giỏ hàng sạch).
> 2. **Bảng `coupon` (124.5k dòng):** Khử trùng triệt để 5,164 bản ghi trùng lặp 100% (exact duplicates), thu gọn còn 119,384 dòng ánh xạ SKU hợp lệ để ngăn chặn hiện tượng nhân đôi dòng khi kết nối bảng.
> 3. **Bảng nhân khẩu học `hh_demographic` (801 hộ, 32.0%):** Nhóm kiên quyết không drop 68% số hộ thiếu thông tin để tránh sai lệch chọn mẫu (selection bias). Thay vào đó, 1,699 hộ khuyết thiếu được mã hóa thành một nhóm `UNKNOWN` độc lập, bảo toàn trọn vẹn 100% cỡ mẫu 2,500 hộ gia đình.
> 4. **Kiểm chứng JOIN Audit đạt toàn vẹn 100%:** Khớp nối 2.59M dòng giao dịch sang bảng sản phẩm đạt 100% (0 SKU lệch, 0 nhân đôi dòng). Khớp nối bảng chiến dịch (1,584 hộ) và bảng đổi coupon (2,318 lượt đổi của 434 hộ) hoàn toàn toàn vẹn khóa ngoại.
> 5. **Bảng `causal_data` (36.8 triệu dòng):** Nhóm chủ động loại bỏ khỏi baseline vì dữ liệu ở cấp cửa hàng/tuần (*store-week*), độ thưa cao và không liên kết được với hành vi dừng chân thực tế của từng hộ gia đình."*

---

### Slide 4: 3. Căn cứ chọn cửa sổ 14 ngày: Điểm cân bằng giữa phân hóa và vận hành
* **Tiêu đề:** 3. Căn cứ chọn cửa sổ 14 ngày: Điểm cân bằng giữa phân hóa và vận hành
* **Thời lượng:** 60 giây
* **Biểu đồ:** Đường cong tích lũy hộ gia đình mua sắm theo chân trời dự báo $H \in [1, 56]$ ngày, trung bình qua 5 mốc chốt sổ quan sát kèm dải biến thiên độ lệch chuẩn.

**Lời thoại trình bày:**
> *"Một quyết định thiết kế bài toán then chốt là: Nên dự đoán xác suất mua hàng trong bao nhiêu ngày tới? Để trả lời bằng thực nghiệm, nhóm quét độ dài chân trời dự báo $H$ từ 1 đến 56 ngày qua 5 mốc chốt sổ đại diện:
> - **Nếu chọn $H = 7$ ngày:** Tỷ lệ hộ phát sinh giao dịch chỉ đạt **53.4%**, quá thấp và bỏ sót gần 47% hộ gia đình có chu kỳ đi chợ 2 tuần một lần, tạo áp lực vận hành quá gấp cho đội ngũ tiếp thị.
> - **Nếu chọn $H = 28$ ngày:** Tỷ lệ dương tính lên tới **80.2%**, đường cong bão hòa khiến lớp mục tiêu mất cân bằng nặng và làm suy giảm độ nhạy phân loại của mô hình học máy.
> - **Tại $H = 14$ ngày:** Tỷ lệ hộ có phát sinh mua sắm đạt **68.3%** với độ lệch chuẩn cực kỳ hẹp giữa các cutoff (chỉ $\pm 1.0\%$). Đây là điểm cân bằng lý tưởng: vừa đảm bảo tỷ lệ lớp mục tiêu phân hóa tự nhiên (khoảng 2/3 dương tính, 1/3 âm tính), vừa mang lại khoảng đệm 2 tuần đủ dài để các chiến dịch marketing có thể can thiệp hiệu quả."*

---

### Slide 5: 4. Recency và Frequency: Cặp bài trùng phân tách quán tính mua sắm
* **Tiêu đề:** 4. Recency và Frequency: Cặp bài trùng phân tách quán tính mua sắm
* **Thời lượng:** 65 giây
* **Biểu đồ:** Heatmap 2D đồng thời biểu diễn xác suất $P(Y=1)$ và cỡ mẫu $n$ trên lưới giao thoa giữa 5 nhóm Recency và 5 nhóm Frequency 90 ngày.

**Lời thoại trình bày:**
> *"Bước sang khám phá các đặc trưng hành vi, Recency và Frequency là cặp biến quan trọng bậc nhất tạo nên lực phân tách nền tảng của mô hình. Trên màn hình là biểu đồ Heatmap tương tác 2 chiều:
> - **Hiệu ứng biên Recency:** Giảm từ **88.5%** ở nhóm vừa đi chợ trong 1–3 ngày qua ($n = 959$ hộ) xuống chỉ còn **24.1%** ở nhóm trên 30 ngày chưa mua sắm ($n = 465$ hộ). Biên độ phân tách đơn lẻ đạt tới **64.4 điểm phần trăm**.
> - **Hiệu ứng biên Frequency:** Nhóm hoàn toàn không có giao dịch trong 90 ngày ($n = 199$ hộ) chỉ đạt xác suất mua **12.4%** (nhóm khách hàng đã rời bỏ hoặc ngủ đông). Khi tần suất tăng lên $\ge 25$ giỏ, xác suất mua đạt tới **92.5%** (chênh lệch tới **80.1 điểm phần trăm**).
> - **Tương tác 2 chiều trên Heatmap:** Ngay cả trong cùng nhóm khách hàng vừa mua cách đây 1–3 ngày, nếu tần suất 90 ngày thấp (1–5 giỏ), xác suất mua chỉ là 66.7%; nhưng nếu tần suất cao ($\ge 25$ giỏ), xác suất vọt lên tới 93.6%. Ngược lại, hộ có tần suất cao nhưng đã quá 30 ngày chưa quay lại thì xác suất rơi về 40.0%. Hai biến số bổ trợ khăng khít cho nhau để nhận diện độ tươi mới và độ bền vững của quán tính mua sắm."*

---

### Slide 6: 5. Spend và Breadth: Tín hiệu gia tăng độc lập ngoài Tần suất
* **Tiêu đề:** 5. Spend và Breadth: Tín hiệu gia tăng độc lập ngoài Tần suất
* **Thời lượng:** 65 giây
* **Biểu đồ:** 2 panel phân tầng kiểm soát (Stratified Analysis): Panel trái biểu diễn Spend theo tầng Frequency; Panel phải biểu diễn Breadth theo tầng Frequency.

**Lời thoại trình bày:**
> *"Một câu hỏi phương pháp luận lớn đặt ra là: Chi tiêu (Spend) và Độ rộng ngành hàng (Breadth) có thực sự mang lại tín hiệu dự báo độc lập hay chỉ là hệ quả phái sinh của việc đi chợ nhiều lần? Để chứng minh, nhóm thực hiện phân tích phân tầng cố định theo Tần suất:
> - **Ở Panel bên trái (Phân tầng Spend):** Khi kiểm soát cố định trong cùng tầng Frequency thấp (1–5 giỏ hàng), những hộ chi tiêu cao (\$300–\$700) đạt xác suất mua **76.0%**, vượt xa mức **38.4%** của những hộ chỉ tiêu dưới \$100 (chênh lệch độc lập lên tới **+37.6 điểm phần trăm**). Spend đo lường độ gắn kết về mặt ví tiền (share of wallet), không bị tần suất triệt tiêu.
> - **Ở Panel bên phải (Phân tầng Breadth):** Trong cùng tầng Frequency trung bình (6–15 giỏ), hộ mua sắm đa ngành ($\ge 7$ ngành) đạt xác suất mua **83.7%**, vượt trội **+19.7 điểm phần trăm** so với hộ chỉ mua 1–2 ngành hàng tiện lợi rời rạc (64.0%). Độ phủ ngành hàng phản ánh hộ đã xem siêu thị là điểm đến trọn gói (one-stop shop) của gia đình."*

---

### Slide 7: 6. Hàng tươi sống: Chỉ báo chu kỳ tiêu dùng thực phẩm ngắn hạn
* **Tiêu đề:** 6. Hàng tươi sống: Chỉ báo chu kỳ tiêu dùng thực phẩm ngắn hạn
* **Thời lượng:** 50 giây
* **Biểu đồ:** Tỷ lệ $P(Y=1)$ theo 5 nhóm Recency của danh mục hàng tươi sống (`days_since_last_perishable`).

**Lời thoại trình bày:**
> *"Đặc trưng thứ năm là Khoảng cách mua thực phẩm tươi sống (`days_since_last_perishable`):
> - **Làm rõ ranh giới danh mục:** Nhóm đã chuẩn hóa danh mục hàng tươi sống chuẩn mực (gồm Rau củ quả, Thịt tươi, Thịt đóng gói, Thủy hải sản, Sữa, Bánh mì tươi, Thực phẩm chín chế biến sẵn), loại bỏ hoàn toàn ngành hàng `GROCERY` khô thông thường để tránh méo mó chu kỳ bảo quản thực phẩm.
> - Kết quả thực nghiệm cho thấy: Hộ vừa mua thực phẩm tươi sống trong **0–3 ngày qua** đạt xác suất mua **89.7%** ($n = 658$ hộ), phản ánh nhóm khách hàng có thói quen đi chợ nấu ăn đều đặn hàng tuần.
> - Khi thời gian vắng bóng đồ tươi vượt quá **30 ngày**, xác suất mua rơi về **35.0%** (giảm 54.7 điểm phần trăm). Nhu cầu bổ sung thực phẩm tươi sống chính là xung lực tự nhiên thúc đẩy nhịp điệu quay lại siêu thị."*

---

### Slide 8: 7. Chiến dịch & Coupon: Tín hiệu tương quan dự báo tại mốc chốt sổ
* **Tiêu đề:** 7. Chiến dịch & Coupon: Tín hiệu tương quan dự báo tại mốc chốt sổ
* **Thời lượng:** 60 giây
* **Biểu đồ:** 2 panel: Panel trái thể hiện xác suất $P(Y=1)$ theo nhóm chiến dịch active tại $t_0$; Panel phải thể hiện xác suất $P(Y=1)$ theo lịch sử đổi coupon 180 ngày.

**Lời thoại trình bày:**
> *"Slide 8 khám phá các biến động lực tiếp thị tại mốc chốt sổ $t_0$:
> - **Ở Panel bên trái (Chiến dịch active tại $t_0$):** Hộ có chiến dịch đang có hiệu lực tại $t_0$ đạt xác suất mua **86.7% đến 90.7%**, cao hơn vượt bậc **+27 đến +30 điểm phần trăm** so với nhóm không có chiến dịch nào kích hoạt (59.9%, $n = 1,827$ hộ). Chiến dịch Loại A (Đa ngành hàng) có tỷ lệ chuyển đổi đổi coupon đạt 15.96%, cao gấp đôi Loại B và C.
> - **Ở Panel bên phải (Lịch sử đổi coupon 180 ngày):** Hộ gia đình có lịch sử đổi 1–2 lần coupon đạt xác suất mua **92.5%** ($n = 80$ hộ). Với nhóm đổi từ 3 lần trở lên, xác suất mua đạt tới **94.7%** ($n = 14$ hộ), so với mức 67.4% ở nhóm chưa từng đổi coupon.
> - **Ranh giới phương pháp luận:** Nhóm xin nhấn mạnh đây là **mối liên hệ tương quan mang giá trị dự báo (predictive association)** do bộ phận marketing chủ động nhắm hộ tích cực; chúng em tuyệt đối không diễn giải đây là tác động nhân quả (causality hay uplift)."*

---

### Slide 9: 8. Mạng lưới cửa hàng & Phân nhóm UNKNOWN: Đặc trưng cấu trúc
* **Tiêu đề:** 8. Mạng lưới cửa hàng & Phân nhóm UNKNOWN: Đặc trưng cấu trúc
* **Thời lượng:** 60 giây
* **Biểu đồ:** 2 panel: Panel trái thể hiện xác suất $P(Y=1)$ theo tỷ trọng chi tiêu tại cửa hàng chính (Primary Store Share 90d); Panel phải thể hiện xác suất theo quy mô hộ gia đình và nhóm `UNKNOWN`.

**Lời thoại trình bày:**
> *"Slide 9 phân tích hai đặc trưng cấu trúc về mạng lưới bán lẻ và nhân khẩu học:
> - **Ở Panel bên trái (Mức độ tập trung cửa hàng - Store Loyalty):** Một hiện tượng thú vị là mối quan hệ mang chiều **nghịch (-)**: Nhóm dồn $\ge 80\%$ ngân sách vào 1 cửa hàng đạt xác suất mua **70.4%**. Trong khi đó, nhóm khách hàng phân tán ghé nhiều siêu thị (<50% tiền, $n = 196$ hộ) lại có xác suất mua cao hơn, đạt **82.8%** (chênh lệch +12.4 pp). Khách hàng ghé nhiều chi nhánh là những khách hàng có tần suất đi chợ cao và mức độ năng động sinh hoạt lớn.
> - **Ở Panel bên phải (Nhân khẩu học & Nhóm `UNKNOWN`):** Trong nhóm 801 hộ có khai báo, xác suất mua tăng dần theo quy mô hộ (từ 75.4% ở hộ 1–2 người lên 80.2% ở hộ 5+ người). Đặc biệt, nhóm 1,699 hộ khuyết thiếu (`UNKNOWN`, chiếm 68% panel) đạt xác suất mua ổn định **64.5%**. Việc giữ nguyên nhóm `UNKNOWN` độc lập giúp mô hình học máy tận dụng tín hiệu mà không tạo ra bất kỳ thiên lệch chọn mẫu nào."*

---

### Slide 10: 9. Ma trận chuyển giao 28 đặc trưng Point-in-Time sang mô hình hóa
* **Tiêu đề:** 9. Ma trận chuyển giao 28 đặc trưng Point-in-Time sang mô hình hóa
* **Thời lượng:** 60 giây
* **Bảng:** Ma trận tổng hợp 9 nhóm đặc trưng, cửa sổ thời gian, tên biến đại diện trong pipeline `feature_builder.py`, chiều quan hệ thực nghiệm với $Y$, và bằng chứng thực nghiệm.

**Lời thoại trình bày:**
> *"Từ toàn bộ các kết quả khám phá thực nghiệm, nhóm đúc kết thành **Ma trận chuyển giao 28 đặc trưng thuộc 9 nhóm cốt lõi** cho pipeline mô hình hóa:
> 1. **Recency ($\le t_0$, Nghịch -):** Lực phân tách mạnh nhất, delta 64.4 pp (88.5% vs 24.1%). Biến: `days_since_last_basket`, `urgency_ratio`.
> 2. **Frequency (90d, Đồng +):** Phân tách 80.1 pp (92.5% vs 12.4%). Biến: `baskets_count_90d`, `freq_momentum`.
> 3. **Spend (90d, Đồng +):** Giữ độ dốc dương khi cố định frequency (+37.6 pp). Biến: `spend_90d`, `spend_trend`.
> 4. **Breadth (90d, Đồng +):** Tín hiệu độc lập ngoài frequency (+19.7 pp). Biến: `department_breadth_90d`.
> 5. **Perishables ($\le t_0$, Nghịch -):** Đo chu kỳ cạn thực phẩm tươi (89.7% vs 35.0%). Biến: `days_since_last_perishable`.
> 6. **Campaigns (Tại $t_0$, Đồng +):** Hộ có chiến dịch active đạt 86.7%–90.7%. Biến: `is_targeted_type_A`, `type_B`, `type_C`.
> 7. **Coupons (180d, Đồng +):** Đổi coupon là chỉ báo gắn kết (92.5% vs 67.4%). Biến: `coupon_redemptions_180d`.
> 8. **Store Loyalty (90d, Nghịch -):** Hộ ghé nhiều siêu thị năng động hơn (82.8% vs 70.4%). Biến: `primary_store_spend_share`.
> 9. **Demographics (Cố định, Phân nhóm):** Phân loại cấu trúc hộ và bảo toàn 1,699 hộ UNKNOWN. Biến: `household_size`, `is_unknown`.
>
> 100% các biến đều tuân thủ nghiêm ngặt nguyên tắc Point-in-Time, sẵn sàng đưa vào huấn luyện mô hình LightGBM, XGBoost và CatBoost."*

---

### Slide 11: Phụ lục 1 — Kiến trúc chi tiết 8 bảng dữ liệu Dunnhumby
* **Tiêu đề:** Phụ lục 1: Kiến trúc chi tiết 8 bảng dữ liệu Dunnhumby
* **Thời lượng:** 20 giây (dùng khi phản biện kiến trúc dữ liệu)
* **Trực quan:** Sơ đồ quan hệ thực thể (ERD) chi tiết 8 bảng dữ liệu với đầy đủ các trường khóa chính, khóa ngoại và quan hệ kết nối.

**Lời thoại trình bày:**
> *"Ở phần phụ lục, đây là sơ đồ ERD chi tiết thể hiện toàn bộ 8 bảng dữ liệu Dunnhumby cùng hệ thống khóa liên kết: `HOUSEHOLD_KEY`, `BASKET_ID`, `PRODUCT_ID`, `CAMPAIGN`, `COUPON_UPC`, và `STORE_ID`. Mọi truy vấn trích xuất đặc trưng của nhóm đều tuân thủ chính xác lược đồ quan hệ chuẩn hóa này."*

---

### Slide 12: Phụ lục 2 — Phân phối giá trị giỏ hàng thực nghiệm
* **Tiêu đề:** Phụ lục 2: Phân phối giá trị giỏ hàng thực nghiệm
* **Thời lượng:** 20 giây (dùng khi phản biện AOV và phân phối chi tiêu)
* **Biểu đồ:** Biểu đồ histogram kết hợp KDE thể hiện phân phối giá trị giỏ hàng thực nghiệm trên 275,542 giỏ hàng sạch.

**Lời thoại trình bày:**
> *"Phụ lục 2 khảo sát phân phối giá trị giỏ hàng sạch (`basket_spend`): Phân phối có dạng lệch phải điển hình (right-skewed) với trung vị đạt 17.03 USD, trung bình đạt 29.24 USD, và phân vị 95 đạt 92.56 USD. Đây là cơ sở để nhóm áp dụng biến đổi logarit cho các biến chi tiêu trong quá trình tiền xử lý mô hình hóa."*

---

### Slide 13: Phụ lục 3 — Mức độ tập trung doanh thu theo hộ gia đình (Pareto & Gini)
* **Tiêu đề:** Phụ lục 3: Mức độ tập trung doanh thu theo hộ gia đình
* **Thời lượng:** 20 giây (dùng khi phản biện chiến lược kinh doanh và CLV)
* **Biểu đồ:** Đường cong Lorenz biểu diễn mức độ tập trung doanh thu tích lũy của 2,500 hộ gia đình so với đường phân bổ bình đẳng.

**Lời thoại trình bày:**
> *"Phụ lục 3 chứng minh mức độ tập trung doanh thu bán lẻ: Top 20% hộ gia đình chi tiêu nhiều nhất (500 hộ) đóng góp tới 73.1% tổng doanh thu của toàn bộ chuỗi siêu thị. Hệ số Gini được tính toán chuẩn xác theo công thức hình thang giải tích đạt **0.5028**, phản ánh mức độ tập trung doanh thu ở mức trung bình cao trong phân tích bán lẻ."*

---

### Slide 14: Phụ lục 4 — Cấu trúc chiết khấu niêm yết tại quầy vs Phiếu giảm giá
* **Tiêu đề:** Phụ lục 4: Cấu trúc chiết khấu niêm yết tại quầy vs Phiếu giảm giá
* **Thời lượng:** 20 giây (dùng khi phản biện về chính sách khuyến mại)
* **Biểu đồ:** Đối sánh ngân sách chiết khấu và tỷ lệ bao phủ giỏ hàng giữa Giảm giá tại quầy (`RETAIL_DISC`) và Phiếu giảm giá (`COUPON_DISC`).

**Lời thoại trình bày:**
> *"Phụ lục 4 bóc tách cấu trúc giảm giá hai tầng: Giảm giá niêm yết tại quầy (`RETAIL_DISC`) đạt quy mô 1.40 triệu USD (bao phủ 83.67% giỏ hàng); trong khi phiếu giảm giá coupon (`COUPON_DISC`) đạt 42.6 nghìn USD (bao phủ 6.08% giỏ hàng). Giảm giá tại quầy lớn gấp 32.8 lần coupon, cho thấy coupon là công cụ tiếp thị cá nhân hóa nhắm chọn lọc vào nhóm khách hàng nhạy cảm giá."*

---

### Slide 15: Phụ lục 5 — Tỷ trọng danh mục và doanh thu của Nhãn hàng riêng
* **Tiêu đề:** Phụ lục 5: Tỷ trọng danh mục và doanh thu của Nhãn hàng riêng
* **Thời lượng:** 20 giây (dùng khi phản biện hiệu quả thương hiệu riêng)
* **Biểu đồ:** Đối sánh tỷ trọng SKU (15.0%) vs Tỷ trọng Doanh thu (27.8%) và Tỷ trọng Sản lượng (28.8%) của nhãn hàng riêng.

**Lời thoại trình bày:**
> *"Phụ lục 5 phân tích hiệu quả thương hiệu riêng (Private Label): Dù chỉ chiếm 14.96% số lượng SKU trên kệ, nhãn hàng riêng đóng góp tới 27.77% doanh thu (2.24 triệu USD) và 28.75% sản lượng hàng hóa bán ra. Hiệu suất doanh thu trên mỗi SKU nhãn riêng đạt 1.86x, cao gấp 2.18 lần so với thương hiệu quốc gia thông thường (0.85x)."*

---

### Slide 16: Phụ lục 6 — Nhịp điệu thời gian theo chu kỳ ngày và khung giờ mua sắm
* **Tiêu đề:** Phụ lục 6: Nhịp điệu thời gian theo chu kỳ ngày và khung giờ mua sắm
* **Thời lượng:** 20 giây (dùng khi phản biện tính mùa vụ và vận hành cửa hàng)
* **Biểu đồ:** Phân phối giỏ hàng theo chu kỳ 7 ngày (`DAY mod 7`) và Khung giờ mua sắm trong ngày (`TRANS_TIME`).

**Lời thoại trình bày:**
> *"Phụ lục 6 khảo sát nhịp điệu thời gian: Lượng giỏ hàng đạt đỉnh vào Ngày 4 và Ngày 5 ($\approx 16.0\%$ mỗi ngày). Toàn bộ hoạt động mua sắm tập trung cao độ vào khung từ 11 giờ trưa đến 18 giờ chiều, chiếm tới 62.93% tổng số giỏ hàng sạch (hơn 173,000 giỏ), với đỉnh cao nhất rơi vào 16h–17h.
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
> Việc loại bỏ 942 giỏ hàng này loại bỏ các giao dịch quẹt thẻ kỹ thuật, sửa lỗi thu ngân và quà tặng \$0, bảo đảm nhãn $Y$ phản ánh đúng bản chất giao dịch thương mại sạch mà không làm méo mó phân phối nhãn."*

### Câu hỏi 5: Tại sao nhóm không điền khuyết (impute) cho 68% số hộ thiếu thông tin nhân khẩu học?
> **Trả lời:**  
> *"Thưa thầy cô, trong bán lẻ, dữ liệu nhân khẩu học khuyết thiếu thường là Missing Not At Random (MNAR) — khách hàng từ chối cung cấp thông tin thường có đặc điểm hành vi khác biệt so với nhóm chủ động khai báo. Nếu chúng em dùng các phương pháp điền khuyết như mode, mean hay KNN, chúng ta sẽ áp đặt giả định nhân tạo làm biến dạng cấu trúc phân phối tự nhiên.  
> Thay vào đó, việc mã hóa 1,699 hộ thành nhóm `UNKNOWN` độc lập cho phép các mô hình cây quyết định như LightGBM hay XGBoost tự động tìm điểm phân nhánh tối ưu dựa trên chính trạng thái 'không khai báo', bảo toàn trọn vẹn 100% tập mẫu mà không tạo ra sai lệch chọn mẫu (selection bias)."*
