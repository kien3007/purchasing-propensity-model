# Kịch bản trình bày báo cáo khám phá dữ liệu & kiểm toán chất lượng (EDA & Data Quality)
## Xây dựng mô hình dự đoán xác suất mua hàng bán lẻ (Purchasing Propensity Model)
### Bộ dữ liệu: Dunnhumby — The Complete Journey (2,500 Hộ gia đình, 2.59 Triệu giao dịch, 8 Bảng, 711 Ngày)

---

## Cấu trúc tổng thể bài trình bày (Narrative Arc)

Bài thuyết trình kéo dài **15 phút** (gồm 12 phút trình bày mạch chính và 3 phút Q&A), được chuẩn hóa theo kiến trúc 16 slides (10 slide mạch chính + 6 slide phụ lục):

1. **Phần 1: Thiết kế bài toán & Kiểm toán chất lượng dữ liệu (Slides 1 – 3 | 2.5 phút):**
   - Thiết lập bài toán học máy: Đơn vị hộ gia đình ($n = 2,500$ hộ panel), chân trời dự báo $\Delta t = 14$ ngày, kỷ luật thời gian Point-in-Time ($DAY \le t_0$).
   - Kết quả kiểm toán 8 bảng dữ liệu: Phân tách rõ ràng đơn vị dòng (2.59M), giỏ (275.5k sạch) và hộ (2,500 panel với 1,699 hộ `UNKNOWN`), kiểm chứng JOIN 100%, kiểm định tác động nhãn của việc loại 942 giỏ hàng phi thương mại (chỉ thay đổi 0.016% nhãn).
2. **Phần 2: Căn cứ xác lập chân trời dự báo & Phân tích tín hiệu hành vi (Slides 4 – 9 | 6.5 phút):**
   - Căn cứ thực nghiệm chọn $\Delta t = 14$ ngày (Base rate 68.3%, std $\pm 1.0\%$).
   - Khám phá các nhóm tín hiệu cốt lõi: Ma trận kết hợp 2D Recency $\times$ Frequency (heatmap), phân tầng kiểm soát Spend & Breadth, chỉ báo chu kỳ thực phẩm tươi sống, tương quan chiến dịch & coupon, cấu trúc mạng lưới cửa hàng và nhóm `UNKNOWN`.
3. **Phần 3: Đề xuất 28 đặc trưng sang Feature Engineering (Slide 10 | 1.5 phút):**
   - Đề xuất 28 biến đặc trưng Point-in-Time (bao gồm biến quan sát trực tiếp và biến dẫn xuất động lượng/tỷ lệ) sẵn sàng cho pipeline mô hình hóa.
4. **Phần 4: Phụ lục chuyên sâu & Quản trị bán lẻ (Slides 11 – 16 | 1.5 phút dùng khi tra cứu hoặc phản biện):**
   - Sơ đồ ERD 8 bảng dữ liệu, phân phối AOV giỏ hàng ($17.18 USD), quy luật Pareto ($53.0\%$) & Gini ($0.5028$), cấu trúc chiết khấu 2 tầng, thâm nhập nhãn hàng riêng (Private Label), và nhịp điệu mua sắm theo giờ.
5. **Phần 5: Bộ câu hỏi & trả lời dự phòng cho phần Q&A (3.0 phút).**

---

## Kịch bản chi tiết từng slide (Slide-by-Slide Script)

### Slide 1: Tiêu đề báo cáo
* **Tiêu đề:** Khám phá dữ liệu (EDA) & kiểm toán chất lượng dữ liệu
* **Phụ đề:** Nền tảng thực nghiệm cho bài toán dự đoán xác suất mua hàng bán lẻ (14 ngày)
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
> - **Nhãn mục tiêu ($Y$):** Biến nhị phân $Y \in \{0, 1\}$. $Y = 1$ nếu hộ có phát sinh ít nhất một giỏ hàng sạch có chi tiêu dương ($SALES\_VALUE > 0$) trong 14 ngày tiếp theo; ngược lại $Y = 0$. Tỷ lệ dương toàn mẫu đạt khoảng 68.3%.
>
> Về mặt phương pháp luận, chúng em áp dụng triệt để **kỷ luật Point-in-Time**: 100% biến đặc trưng chỉ được tính toán từ các sự kiện phát sinh trước hoặc tại thời điểm $t_0$. Mọi thông tin sau $t_0$ tuyệt đối chỉ được dùng để gán nhãn mục tiêu $Y$, triệt tiêu hoàn toàn nguy cơ rò rỉ dữ liệu từ tương lai (data leakage).
>
> Để đánh giá mô hình khách quan, nhóm áp dụng chiến lược chia tập **Multi-cutoff**: Tập Huấn luyện gồm 11 mốc chốt sổ trượt $t_0 \in [200, 500]$, Tập Xác thực gồm 3 mốc $t_0 \in [530, 590]$, và Tập Kiểm thử độc lập gồm 2 mốc $t_0 \in [650, 680]$ hoàn toàn tách biệt về mặt thời gian."*

---

### Slide 3: 2. Kiểm toán 8 bảng: Loại bỏ nhiễu, chuẩn hóa khóa nối và bảo toàn mẫu
* **Tiêu đề:** 2. Kiểm toán 8 bảng: Loại bỏ nhiễu, chuẩn hóa khóa nối và bảo toàn mẫu
* **Thời lượng:** 60 giây
* **Trực quan:** Bảng kiểm toán tách bạch theo từng đơn vị (Dòng, Giỏ, Hộ) ở cột trái; 3 kết luận kiểm chứng toàn vẹn & kiểm định nhãn ở cột phải.

**Lời thoại trình bày:**
> *"Để đảm bảo tính minh bạch tuyệt đối, ở bảng bên trái nhóm tách bạch rõ ràng theo từng đơn vị quan sát:
> 1. **Bảng giao dịch `transaction_data`:** Ở cấp dòng, dữ liệu thô có 2,595,732 dòng chi tiết thuộc 276,484 chuyến đi chợ (giỏ hàng). Nhóm kiểm toán và loại bỏ 942 giỏ hàng phi thương mại có tổng chi tiêu $\le \$0$ (hoàn hàng, quẹt thẻ kỹ thuật, quà tặng \$0), tương ứng với 1,054 dòng giao dịch. Sau làm sạch, chúng em thu được đúng 2,594,678 dòng sạch và 275,542 giỏ hàng thương mại sạch.
> 2. **Kiểm định tác động nhãn:** Kiểm toán định lượng trên toàn bộ 12,500 lượt đánh giá qua 5 mốc chốt sổ cho thấy việc loại 942 giỏ này chỉ làm đổi đúng 2 nhãn từ 1 sang 0 tại duy nhất mốc $t_0 = 550$ (tỷ lệ ảnh hưởng chỉ 0.016%), chứng minh việc làm sạch không hề gây sai lệch biến mục tiêu.
> 3. **Bảng nhân khẩu học `hh_demographic`:** Ở cấp hộ gia đình, chỉ có 801 hộ khai báo thông tin. Nhóm kiên quyết không drop 68% số hộ thiếu dữ liệu để tránh sai lệch chọn mẫu (selection bias). Thay vào đó, 1,699 hộ khuyết thiếu được mã hóa thành phân nhóm `UNKNOWN` độc lập, bảo toàn trọn vẹn 100% cỡ mẫu 2,500 hộ panel.
> 4. **Khử trùng và kiểm chứng khóa nối:** Bảng coupon được khử trùng 5,164 bản ghi trùng 100%, thu gọn còn 119,384 dòng ánh xạ; kiểm toán JOIN đạt toàn vẹn 100% không phát sinh SKU lệch; bảng `causal_data` (36.8M dòng store-week) được loại bỏ khỏi baseline do độ thưa cao."*

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
* **Biểu đồ:** Heatmap 2D ma trận kết hợp giữa 5 nhóm Recency và 4 nhóm Frequency 90 ngày; mỗi ô hiển thị xác suất $P(Y=1)$ và số hộ trung bình $n$ qua 5 mốc cutoff (tổng $n=2,500$ hộ).

**Lời thoại trình bày:**
> *"Bước sang khám phá các đặc trưng hành vi, Recency và Frequency là cặp biến cốt lõi tạo nên lực phân tách nền tảng của bài toán. Thay vì nhìn đơn lẻ, ma trận Heatmap 2 chiều trên màn hình bóc tách sự tương tác hiệp đồng giữa hai biến:
> - **Xét đơn biến:** Nhìn theo từng chiều biên độ, Recency đơn biến phân tách từ **88.5%** ở nhóm vừa mua 0–3 ngày xuống **24.0%** ở nhóm trên 30 ngày. Tương tự, Frequency đơn biến phân tách từ **12.3%** ở nhóm 0 giỏ lên **95.5%** ở nhóm $\ge 16$ giỏ.
> - **Hiệu ứng hiệp đồng trên ma trận 2D:** Sự kết hợp 2 chiều mang lại lực phân loại vượt trội: Nhóm khách hàng vừa đi chợ gần ($\le 3$ ngày) kết hợp với tần suất cao ($\ge 16$ giỏ) đạt đỉnh xác suất mua lên tới **97.4%** (trung bình 599 hộ mỗi mốc). Ngược lại, nhóm vắng bóng trên 30 ngày và hoàn toàn không có giỏ hàng nào trong 90 ngày rơi về đáy xác suất chỉ còn **12.4%** (199 hộ).
> - **Biên độ phân tách cực đại:** Khoảng cách giữa 2 cực đạt tới **85.0 điểm phần trăm**. Recency đo lường độ trễ ngắn hạn, trong khi Frequency đo quán tính nền tảng dài hạn; sự kết hợp này cung cấp bộ lọc phân loại cơ sở mạnh nhất cho mô hình học máy."*

---

### Slide 6: 5. Spend và Breadth: Tín hiệu bổ trợ trong các phân tầng Tần suất
* **Tiêu đề:** 5. Spend và Breadth: Tín hiệu bổ trợ trong các phân tầng Tần suất
* **Thời lượng:** 65 giây
* **Biểu đồ:** 2 panel phân tầng kiểm soát (Stratified Analysis) trên 2,301 hộ active trong 90 ngày (Base rate tập active: 73.2% vs Base rate toàn mẫu 68.3%): Panel trái là Spend theo tầng Frequency; Panel phải là Breadth theo tầng Frequency.

**Lời thoại trình bày:**
> *"Một câu hỏi phương pháp luận quan trọng là: Mức chi tiêu (Spend) và Độ rộng ngành hàng (Breadth) có mang lại tín hiệu bổ trợ hay chỉ phản ánh việc đi chợ nhiều lần? Để kiểm tra, nhóm thực hiện phân tích phân tầng có điều kiện trên 2,301 hộ gia đình có phát sinh giao dịch trong 90 ngày:
> - **Lưu ý về Base rate:** Tập 2,301 hộ active này có tỷ lệ cơ sở là **73.2%**, cao hơn mức 68.3% của toàn bộ 2,500 hộ panel.
> - **Ở Panel bên trái (Phân tầng Spend):** Khi cố định trong cùng tầng Tần suất thấp (1–5 giỏ), những hộ chi tiêu cao (\$300–\$700) đạt xác suất mua **76.0%**, vượt xa mức **38.4%** của hộ chi tiêu dưới \$100 (chênh lệch $+37.6$ điểm phần trăm). Spend đo lường độ gắn kết ví tiền (share of wallet).
> - **Ở Panel bên phải (Phân tầng Breadth):** Trong cùng tầng Tần suất vừa (6–15 giỏ), hộ mua sắm danh mục rộng ($\ge 11$ ngành) đạt xác suất mua **83.7%**, vượt trội **+19.7 điểm phần trăm** so với hộ chỉ mua 1–4 ngành hàng rời rạc (64.0%).
> - **Ý nghĩa phương pháp:** Trong các phân tầng khảo sát, độ dốc dương được duy trì rõ rệt. Tuy nhiên, nhóm nhấn mạnh đây là phân tích phân tầng có điều kiện; khi chuyển giao sang Feature Engineering, mô hình đa biến sẽ tiếp tục đánh giá trọng số đóng góp thực tế của từng biến."*

---

### Slide 7: 6. Hàng tươi sống: Chỉ báo chu kỳ tiêu dùng thực phẩm ngắn hạn
* **Tiêu đề:** 6. Hàng tươi sống: Chỉ báo chu kỳ tiêu dùng thực phẩm ngắn hạn
* **Thời lượng:** 50 giây
* **Biểu đồ:** Tỷ lệ $P(Y=1)$ theo khoảng cách ngày kể từ lần mua thực phẩm tươi sống gần nhất (`days_since_last_perishable`).

**Lời thoại trình bày:**
> *"Đặc trưng thứ năm là Khoảng cách mua thực phẩm tươi sống (`days_since_last_perishable`):
> - **Chuẩn hóa danh mục:** Nhóm đã phân loại danh mục tươi sống chuẩn mực (Rau củ quả, Thịt tươi, Thịt chế biến, Thủy hải sản, Sữa, Bánh mì tươi, Chế biến sẵn), loại trừ hoàn toàn ngành hàng `GROCERY` khô để nắm bắt đúng chu kỳ bảo quản thực phẩm ngắn hạn.
> - **Quan sát thực nghiệm:** Xác suất mua sắm 14 ngày tới có mối tương quan đơn biến rất chặt chẽ với độ tươi mới của giỏ hàng: Hộ vừa mua đồ tươi trong 0–3 ngày qua đạt xác suất mua **89.7%** ($n = 658$ hộ); khi vắng bóng đồ tươi quá 30 ngày, xác suất rơi dốc về **35.0%** ($n = 712$ hộ, giảm 54.7 điểm phần trăm).
> - **Lưu ý mô hình hóa:** Chúng em lưu ý rằng ở mức độ EDA, đây là một chỉ báo chu kỳ đơn biến mang tính trực quan cao. Vì khoảng cách mua đồ tươi thường có mức độ tương quan cao (collinearity) với khoảng cách mua giỏ hàng chung, pipeline Feature Engineering sẽ cần kiểm soát tương quan này để tránh hiện tượng đa cộng tuyến."*

---

### Slide 8: 7. Chiến dịch & Coupon: Tín hiệu tương quan dự báo tại mốc chốt sổ
* **Tiêu đề:** 7. Chiến dịch & Coupon: Tín hiệu tương quan dự báo tại mốc chốt sổ
* **Thời lượng:** 60 giây
* **Biểu đồ:** 2 panel song song: Panel trái thể hiện xác suất $P(Y=1)$ theo nhóm chiến dịch active tại $t_0$; Panel phải thể hiện xác suất $P(Y=1)$ theo lịch sử đổi coupon 180 ngày.

**Lời thoại trình bày:**
> *"Slide 8 khảo sát hai biến động lực tiếp thị tại mốc chốt sổ $t_0$:
> - **Ở Panel bên trái (Chiến dịch active tại $t_0$):** Hộ có chiến dịch đang có hiệu lực tại $t_0$ đạt xác suất mua **86.7% đến 90.7%**, cao hơn vượt trội **+27 đến +30 điểm phần trăm** so với nhóm không có chiến dịch nào kích hoạt (59.9%, $n = 1,827$ hộ).
> - **Ở Panel bên phải (Lịch sử đổi coupon 180 ngày):** Hộ có lịch sử đổi coupon đạt xác suất mua **92.5% đến 94.7%**, so với mức 67.4% ở nhóm chưa từng đổi coupon (2,406 hộ).
> - **Ranh giới phương pháp luận quan trọng:** Nhóm xin nhấn mạnh đây là **mối liên hệ tương quan mang giá trị dự báo (predictive association)** xuất phát từ việc bộ phận tiếp thị chủ động nhắm mục tiêu vào các hộ khách hàng tiềm năng. Chúng em tuyệt đối **không suy diễn đây là tác động nhân quả (causality hay uplift)** rằng chiến dịch đã làm tăng hành vi mua hàng."*

---

### Slide 9: 8. Mạng lưới cửa hàng & Phân nhóm UNKNOWN: Đặc trưng cấu trúc
* **Tiêu đề:** 8. Mạng lưới cửa hàng & Phân nhóm UNKNOWN: Đặc trưng cấu trúc
* **Thời lượng:** 60 giây
* **Biểu đồ:** 2 panel: Panel trái thể hiện xác suất theo tỷ trọng chi tiêu tại cửa hàng chính (Primary Store Share 90d); Panel phải thể hiện xác suất theo quy mô hộ và nhóm `UNKNOWN`.

**Lời thoại trình bày:**
> *"Slide 9 phân tích hai đặc trưng cấu trúc về mạng lưới bán lẻ và hộ gia đình:
> - **Ở Panel bên trái (Xu hướng ghé nhiều siêu thị):** Quan hệ mang chiều **nghịch (-)**: Hộ phân tán chi tiêu ghé nhiều chi nhánh (<50% tiền) có xác suất mua trong 14 ngày tới đạt **82.8%**, cao hơn so với hộ dồn $\ge 80\%$ ngân sách vào một cửa hàng duy nhất (**70.4%**, chênh lệch +12.4 pp). Nhóm xin lưu ý: Hiện tượng này phản ánh khách hàng có hành vi mua sắm tại nhiều địa điểm thường có tần suất sinh hoạt và đi lại dày đặc trong ngắn hạn, làm tăng xác suất xuất hiện giỏ hàng trong 14 ngày; chúng em không suy diễn rằng họ kém trung thành thương hiệu trong dài hạn. Tương tự, nhóm 0 giỏ trong 90 ngày có xác suất mua thấp (12.3%) phản ánh trạng thái ngừng hoạt động tạm thời trong cửa sổ quan sát, không quy kết đã rời bỏ vĩnh viễn.
> - **Ở Panel bên phải (Nhân khẩu học & Nhóm `UNKNOWN`):** Nhóm 1,699 hộ khuyết thiếu (`UNKNOWN`, chiếm 68% panel) đạt xác suất mua ổn định **64.5%**. Việc giữ nguyên phân nhóm `UNKNOWN` độc lập giúp mô hình học máy tận dụng trọn vẹn thông tin mà không tạo ra bất kỳ thiên lệch chọn mẫu nào."*

---

### Slide 10: 9. Đề xuất 28 đặc trưng Point-in-Time từ EDA sang Feature Engineering
* **Tiêu đề:** 9. Đề xuất 28 đặc trưng Point-in-Time từ EDA sang Feature Engineering
* **Thời lượng:** 60 giây
* **Bảng:** Ma trận tổng hợp 9 nhóm đặc trưng, cửa sổ thời gian, biến đại diện đề xuất, chiều quan hệ thực nghiệm với $Y$, và bằng chứng thực nghiệm.

**Lời thoại trình bày:**
> *"Từ toàn bộ các phát hiện thực nghiệm trong giai đoạn EDA, nhóm đúc kết thành **Danh mục đề xuất 28 đặc trưng Point-in-Time thuộc 9 nhóm cốt lõi** để chuyển giao sang pipeline Feature Engineering:
> - Danh mục bao gồm các biến quan sát trực tiếp đã kiểm chứng trong EDA (như `days_since_last_basket`, `baskets_count_90d`, `spend_90d`, `department_breadth_90d`, cờ chiến dịch `is_targeted_type_A/B/C`, số lần đổi coupon, tỷ trọng cửa hàng chính) kết hợp với các biến dẫn xuất logic (như tỷ lệ trễ chu kỳ `urgency_ratio`, xung lượng tần suất 30d/90d `freq_momentum`, và xu hướng dòng tiền `spend_trend`).
> - **Kỷ luật Point-in-Time:** 100% các biến đều được trích xuất nghiêm ngặt tại $DAY \le t_0$, hoàn toàn sẵn sàng đưa vào huấn luyện các thuật toán Gradient Boosting như LightGBM, XGBoost và CatBoost."*

---

### Slide 11: Phụ lục 1 — Kiến trúc chi tiết 8 bảng dữ liệu Dunnhumby
* **Tiêu đề:** Phụ lục 1: Kiến trúc chi tiết 8 bảng dữ liệu Dunnhumby
* **Thời lượng:** 20 giây (dùng khi phản biện kiến trúc dữ liệu)
* **Trực quan:** Sơ đồ quan hệ thực thể (ERD) chi tiết 8 bảng dữ liệu với đầy đủ các trường khóa chính, khóa ngoại và quan hệ kết nối.

**Lời thoại trình bày:**
> *"Ở phần phụ lục, đây là sơ đồ ERD chi tiết thể hiện toàn bộ 8 bảng dữ liệu Dunnhumby cùng hệ thống khóa liên kết: `HOUSEHOLD_KEY`, `BASKET_ID`, `PRODUCT_ID`, `CAMPAIGN`, `COUPON_UPC`, và `STORE_ID`. Mọi truy vấn trích xuất đặc trưng của nhóm đều tuân thủ chính xác lược đồ quan hệ chuẩn hóa này."*

---

### Slide 12: Phụ lục 2 — Phân phối giá trị giỏ hàng thực nghiệm (AOV)
* **Tiêu đề:** Phụ lục 2: Phân phối giá trị giỏ hàng thực nghiệm (AOV)
* **Thời lượng:** 20 giây (dùng khi phản biện AOV và phân phối chi tiêu)
* **Biểu đồ:** Biểu đồ histogram kết hợp KDE thể hiện phân phối giá trị giỏ hàng thực nghiệm trên 275,542 giỏ hàng sạch.

**Lời thoại trình bày:**
> *"Phụ lục 2 khảo sát phân phối giá trị giỏ hàng sạch (`basket_spend`): Phân phối có dạng lệch phải điển hình của ngành bán lẻ với trung vị đạt **17.18 USD**, trung bình đạt **29.24 USD**, phân vị 75 đạt **36.39 USD**, phân vị 90 đạt **70.79 USD**, và khoảng liên phân vị IQR là **29.40 USD**. Đây là cơ sở thực nghiệm để nhóm áp dụng biến đổi logarit cho các biến chi tiêu trong quá trình tiền xử lý mô hình hóa."*

---

### Slide 13: Phụ lục 3 — Mức độ tập trung doanh thu theo hộ gia đình (Pareto & Gini)
* **Tiêu đề:** Phụ lục 3: Mức độ tập trung doanh thu theo hộ gia đình (Pareto & Gini)
* **Thời lượng:** 20 giây (dùng khi phản biện chiến lược kinh doanh và CLV)
* **Biểu đồ:** Đường cong Lorenz biểu diễn mức độ tập trung doanh thu tích lũy của 2,500 hộ gia đình so với đường phân bổ bình đẳng.

**Lời thoại trình bày:**
> *"Phụ lục 3 định lượng mức độ tập trung doanh thu bán lẻ:
> - **Thực tế so với lý thuyết:** Trong ngành hàng tiêu dùng nhanh (FMCG), quy luật Pareto 80/20 lý thuyết không diễn ra cực đoan: Top **20% hộ gia đình chi tiêu nhiều nhất** (500 hộ) đóng góp **53.0% tổng doanh thu** của toàn bộ chuỗi siêu thị (tương đương 4.27 triệu USD trên tổng số 8.06 triệu USD).
> - **Độ phân tán nhu yếu phẩm:** Để đạt được 80% doanh thu tích lũy, siêu thị cần tới **44.0% số hộ khách hàng** (1,100 hộ); và Top 50% số hộ tạo ra **84.3%** tổng doanh thu.
> - **Hệ số Gini:** Được tính toán chuẩn xác theo công thức hình thang giải tích đạt **0.5028**, phản ánh mức độ tập trung doanh thu vừa phải, đặc trưng của ngành hàng bán lẻ thiết yếu."*

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
> Để kiểm chứng hiện tượng này, nhóm đã thực hiện phân tích phân tầng (stratified analysis) kiểm soát theo Tần suất (Frequency). Kết quả cho thấy trong cùng tầng Frequency, các hộ ghé nhiều cửa hàng vẫn có xác suất mua cao hơn hoặc tương đương. Lý do là trong mạng lưới bán lẻ Dunnhumby, những khách hàng ghé nhiều chi nhánh thường là những người có mức độ năng động sinh hoạt cao, di chuyển nhiều giữa nơi làm việc và nơi cư trú, và có nhu cầu mua sắm liên tục. Do đó, tỷ trọng dồn vào cửa hàng chính càng thấp thì xác suất có ít nhất một chuyến mua sắm trong 14 ngày tới càng cao. Điều này thuần túy phản ánh nhịp điệu mua sắm ngắn hạn trong 14 ngày, chúng em không suy diễn về độ trung thành thương hiệu dài hạn."*

### Câu hỏi 4: Việc loại bỏ 942 giỏ hàng chi tiêu $\le \$0$ có làm thiên lệch hoặc rò rỉ nhãn mục tiêu không?
> **Trả lời:**  
> *"Thưa thầy cô, hoàn toàn không làm thiên lệch nhãn. Chúng em đã thực hiện kiểm toán định lượng nghiêm ngặt trên toàn bộ 12,500 lượt đánh giá trải qua 5 mốc chốt sổ quan sát:  
> Khi so sánh nhãn $Y$ tính trên dữ liệu thô và nhãn $Y$ tính trên 275,542 giỏ hàng sạch, chỉ có đúng **2 nhãn bị chuyển từ 1 sang 0** tại duy nhất mốc $t_0 = 550$ (tỷ lệ thay đổi chỉ 0.016%), và 0 nhãn bị thay đổi tại 4 mốc còn lại.  
> Việc loại bỏ 942 giỏ hàng này loại bỏ các giao dịch quẹt thẻ kỹ thuật, sửa lỗi thu ngân và quà tặng \$0 (tương ứng 1,054 dòng giao dịch), bảo đảm nhãn $Y$ phản ánh đúng bản chất giao dịch thương mại sạch mà không làm méo mó phân phối nhãn."*

### Câu hỏi 5: Tại sao nhóm không điền khuyết (impute) cho 68% số hộ thiếu thông tin nhân khẩu học?
> **Trả lời:**  
> *"Thưa thầy cô, trong bán lẻ, dữ liệu nhân khẩu học khuyết thiếu thường là Missing Not At Random (MNAR) — khách hàng từ chối cung cấp thông tin thường có đặc điểm hành vi khác biệt so với nhóm chủ động khai báo. Nếu chúng em dùng các phương pháp điền khuyết như mode, mean hay KNN, chúng ta sẽ áp đặt giả định nhân tạo làm biến dạng cấu trúc phân phối tự nhiên.  
> Thay vào đó, việc mã hóa 1,699 hộ thành nhóm `UNKNOWN` độc lập cho phép các mô hình cây quyết định như LightGBM hay XGBoost tự động tìm điểm phân nhánh tối ưu dựa trên chính trạng thái 'không khai báo', bảo toàn trọn vẹn 100% tập mẫu mà không tạo ra sai lệch chọn mẫu (selection bias)."*
