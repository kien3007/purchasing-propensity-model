# KỊCH BẢN TRÌNH BÀY BÁO CÁO KHÁM PHÁ DỮ LIỆU & KIỂM TOÁN CHẤT LƯỢNG (EDA & DATA QUALITY)

**Dự án:** Dự Đoán Xác Suất Mua Hàng Của Hộ Gia Đình (Purchasing Propensity Model)  
**Tập dữ liệu:** Dunnhumby - The Complete Journey (2.6M giao dịch, 2,500 hộ, 711 ngày)  
**Thời lượng dự kiến:** 12 – 15 phút thuyết trình + 5 phút Q&A  

---

## CẤU TRÚC TỔNG THỂ BÀI TRÌNH BÀY (NARRATIVE ARC)

```
[Mở Đầu] Thách thức dữ liệu thực tế & Sứ mệnh của EDA (Slide 1-2)
   │
   ├──> [Phần 1: Kiểm Toán & Làm Sạch Dữ Liệu] Kiến trúc 8 bảng & Tiêu chuẩn sạch (Slide 3)
   │
   ├──> [Phần 2: 15 Quy Luật Thực Nghiệm Hành Vi] Nhịp sinh học & Bản chất mua sắm (Slide 4-18)
   │      • Nhịp đi chợ & Giá trị giỏ hàng (Slide 4-5)
   │      • Nhịp sinh học tuần & 24 giờ (Slide 6-7)
   │      • Đồ tươi sống & Hiệu ứng lan tỏa coupon (Slide 8-9)
   │      • Gia tốc tiếp thị & Địa bàn đa cửa hàng (Slide 10-11)
   │      • Tác động nhân khẩu & Ổn định nhãn mục tiêu (Slide 12-13)
   │      • Kiểm định Pareto & Chiết khấu hai tầng (Slide 14-15)
   │      • Nhãn hàng riêng & Phễu tiếp thị (Slide 16-17)
   │
   └──> [Phần 3: Chuyển Giao Sang Học Máy] Ma trận đặc trưng & Kỷ luật thời gian (Slide 18-19)
```

---

## KỊCH BẢN CHI TIẾT TỪNG SLIDE (SLIDE-BY-SLIDE SCRIPT)

---

### SLIDE 1: TIÊU ĐỀ BÁO CÁO
* **Tiêu đề:** Khám Phá Dữ Liệu (EDA) & Kiểm Toán Chất Lượng Dữ Liệu
* **Phụ đề:** Nền Tảng Thực Nghiệm Cho Bài Toán Dự Đoán Xác Suất Mua Hàng Bán Lẻ
* **Thời lượng:** 30 giây
* **Điểm nhấn trực quan:** Phong thái tự tin, mắt nhìn thẳng vào hội đồng/người nghe.

**Lời thoại trình bày:**
> *"Kính chào quý thầy cô, các anh chị đồng nghiệp và các bạn. Hôm nay, tôi xin đại diện nhóm trình bày báo cáo về giai đoạn **Khám phá Dữ liệu (EDA) và Kiểm toán Chất lượng Dữ liệu** cho bài toán Dự đoán xác suất mua hàng của hộ gia đình.*
>
> *Trong các dự án máy học thực tế, EDA không đơn thuần chỉ là vẽ các biểu đồ mô tả thống kê, mà chính là **la bàn định hướng toàn bộ bài toán**: từ việc phát hiện và làm sạch nhiễu nghiệp vụ, xác lập cửa sổ dự báo khoa học, cho đến việc thiết kế hệ thống đặc trưng chống rò rỉ dữ liệu trước khi đưa vào mô hình học máy."*

---

### SLIDE 2: BỐI CẢNH THỰC NGHIỆM & MỤC TIÊU KHÁM PHÁ DỮ LIỆU
* **Tiêu đề:** 1. Bối Cảnh Thực Nghiệm & Mục Tiêu Khám Phá Dữ Liệu
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** Chỉ vào 2 cột đối sánh: Thách thức dữ liệu gốc (bên trái) vs. 2 Khối mục tiêu kiểm toán & khám phá (bên phải).

**Lời thoại trình bày:**
> *"Trước hết, chúng ta nhìn vào bức tranh thực tế của dữ liệu bán lẻ. Tập dữ liệu Dunnhumby bao gồm hơn 2.59 triệu dòng giao dịch từ 2,500 hộ gia đình trải dài liên tục trong 711 ngày.*
>
> *Thách thức lớn nhất ở đây là dữ liệu thực tế luôn chứa đầy **nhiễu nghiệp vụ**: từ các thao tác hủy quẹt thẻ tại quầy POS, các giỏ hàng quà tặng 0 đồng, cho đến độ khuyết thiếu lớn về nhân khẩu học. Đặc biệt, để xây dựng mô hình dự báo hành vi trong tương lai, chúng ta phải tuân thủ nghiêm ngặt **kỷ luật thời gian**, phân định rạch ròi giữa quá khứ quan sát và tương lai dự báo.*
>
> *Từ thách thức đó, giai đoạn EDA của chúng tôi tập trung vào 2 mục tiêu cốt lõi: Thứ nhất, kiểm toán và bảo toàn 100% tập mẫu dữ liệu sạch; Thứ hai, bóc tách **14 quy luật thực nghiệm** để làm cơ sở toán học xác định cửa sổ dự báo và sinh đặc trưng cho mô hình."*

---

### SLIDE 3: KIẾN TRÚC 8 BẢNG DỮ LIỆU & KIỂM TOÁN CHẤT LƯỢNG
* **Tiêu đề:** 2. Kiến Trúc 8 Bảng Dữ Liệu & Kiểm Toán Chất Lượng
* **Thời lượng:** 60 giây
* **Điểm nhấn trực quan:** Bảng tổng hợp 8 bảng dữ liệu, lướt qua các số liệu kiểm toán ở cột ngoài cùng bên phải (`transactions`, `coupons`, `demographics`).

**Lời thoại trình bày:**
> *"Trên màn hình là kiến trúc tổng thể của 8 bảng dữ liệu trong hệ thống. Quá trình kiểm toán chất lượng đã xử lý triệt để 3 vấn đề then chốt:*
>
> 1. *Tại bảng `transactions`: Chúng tôi phát hiện và loại bỏ **942 giỏ hàng dị biệt có giá trị chi tiêu $\le \$0$**. Bóc tách thực tế cho thấy hơn 62% các giỏ này thực chất là thao tác quét thẻ hội viên hoặc quẹt mã coupon đơn lẻ tại máy POS, và gần 38% là hàng tặng dùng thử 0 đồng. Việc loại bỏ này giúp triệt tiêu hoàn toàn nhiễu nhãn (label noise) và bảo toàn đúng **275,542 giỏ hàng thương mại thuần túy**.*
> 2. *Tại bảng `coupons`: Chúng tôi khử trùng **5,164 bản ghi trùng lặp 100%**, triệt tiêu nguy cơ nổ dòng (cartesian explosion) khi kết nối sang bảng giao dịch.*
> 3. *Tại bảng `demographics`: Dữ liệu nhân khẩu học khuyết thiếu ở 68% số hộ gia đình. Thay vì xóa bỏ gây mất mát mẫu, chúng tôi chuẩn hóa gán nhãn `UNKNOWN` để đưa vào mô hình dưới dạng một nhóm danh mục độc lập, bảo toàn trọn vẹn 100% tập 2,500 hộ gia đình.*
>
> *Sau khi nền tảng dữ liệu đã đạt chuẩn sạch, chúng ta cùng bước vào 15 quy luật hành vi thực nghiệm."*

---

### SLIDE 4: CÂU CHUYỆN 1 - NHỊP SINH HỌC ĐI CHỢ & CHU KỲ MUA SẮM
* **Tiêu đề:** 3. Nhịp Sinh Học Đi Chợ & Chu Kỳ Mua Sắm Của Hộ Gia Đình
* **Biểu đồ:** Phân phối khoảng cách thời gian giữa các chuyến đi chợ liên tiếp (Inter-trip Days).
* **Thời lượng:** 60 giây
* **Điểm nhấn trực quan:** Chỉ vào đường tích lũy màu đỏ đạt 82.3% tại mốc 7 ngày và đạt 92.4% tại mốc 14 ngày.

**Lời thoại trình bày:**
> *"Biểu đồ đầu tiên trả lời câu hỏi cốt lõi: **Khách hàng đi chợ bao lâu một lần?** Phân phối cho thấy một độ lệch phải điển hình. Trung vị khoảng cách giữa hai lần đi chợ liên tiếp là **2 ngày** và giá trị trung bình là 5.6 ngày.*
>
> *Nhìn vào đường tích lũy màu đỏ: Hơn **82.3%** các lượt mua sắm tái diễn trong vòng 7 ngày – tức nhịp mua sắm hàng tuần thiết yếu. Đến mốc **14 ngày**, tỷ lệ tích lũy đạt tới **92.4%**. Sau mốc 14 ngày, đường cong bão hòa rõ rệt; những hộ không phát sinh giao dịch sau 2 tuần thường là khách vãng lai hoặc có nguy cơ rời bỏ.*
>
> *Chính phát hiện định lượng này là **cơ sở khoa học vững chắc để chúng tôi chọn cửa sổ nhãn dự báo $\Delta t = 14$ ngày**. Đồng thời, chúng tôi sinh ra các đặc trưng quan trọng như `urgency_ratio` (tỷ số giữa số ngày chưa mua so với chu kỳ bình quân) và `days_since_last_basket`."*

---

### SLIDE 5: CÂU CHUYỆN 2 - CẤU TRÚC GIÁ TRỊ GIỎ HÀNG THỰC NGHIỆM (AOV)
* **Tiêu đề:** 4. Cấu Trúc Giá Trị Giỏ Hàng Thực Nghiệm (AOV)
* **Biểu đồ:** Phân phối giá trị giỏ hàng (Basket Spend) với đường trung bình và các mức phân vị.
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** Khoảng cách giữa P50 (\$17.20) và Giá trị trung bình (\$29.24).

**Lời thoại trình bày:**
> *"Khi phân tích giá trị chi tiêu mỗi giỏ hàng, ta nhận thấy hiện tượng phân hóa mạnh mẽ: Trung vị một giỏ hàng chỉ là **\$17.20**, nhưng giá trị trung bình (AOV) lại lên tới **\$29.24** – chênh lệch tới 70%.*
>
> *Điều này phản ánh đúng thực tế bán lẻ: Phần lớn các chuyến đi chợ là mua lẻ bổ sung hàng ngày, nhưng dòng tiền thực sự lại được gánh vác bởi các giỏ hàng lớn cuối tuần hoặc mua sắm tiệc tùng.*
>
> *Hàm ý máy học ở đây là: **Khách hàng chi nhiều tiền chưa chắc đã đi chợ thường xuyên**. Do đó, mô hình bắt buộc phải tách bạch giữa nhóm đặc trưng về **Tần suất** (`frequency`) và nhóm đặc trưng về **Quy mô dòng tiền** (`spend_30d`, `aov_90d`)."*

---

### SLIDE 6: CÂU CHUYỆN 3 - PHÂN BỔ NHỊP MUA SẮM THEO CÁC NGÀY TRONG TUẦN
* **Tiêu đề:** 5. Phân Bổ Nhịp Mua Sắm Theo Các Ngày Trong Tuần
* **Biểu đồ:** Số lượng giỏ hàng phân bổ từ Thứ Hai đến Chủ Nhật.
* **Thời lượng:** 40 giây
* **Điểm nhấn trực quan:** Đáy vào Thứ Ba - Thứ Tư và hai cột đỉnh vọt lên ở Thứ Bảy - Chủ Nhật.

**Lời thoại trình bày:**
> *"Quy luật ngày trong tuần bộc lộ rõ nhịp sống của các hộ gia đình: Giữa tuần (Thứ Ba, Thứ Tư) là điểm đáy tiêu dùng khi mọi người bận rộn đi làm. Ngược lại, Thứ Bảy và Chủ Nhật bùng nổ nhu cầu mua sắm tích trữ với lượng giao dịch tăng vọt **30% đến 35%**.*
>
> *Vì hành vi tiêu dùng gắn chặt với chu kỳ tuần, chúng tôi đưa đặc trưng `day_of_week` tại thời điểm quan sát $t_0$ và `days_to_weekend` vào mô hình, giúp thuật toán nắm bắt được xung lực mua sắm trước kỳ nghỉ."*

---

### SLIDE 7: CÂU CHUYỆN 4 - NHỊP SINH HỌC MUA SẮM SUỐT 24 GIỜ
* **Tiêu đề:** 6. Nhịp Sinh Học Mua Sắm Suốt 24 Giờ Trong Ngày
* **Biểu đồ:** Phân phối giờ mua sắm trong ngày (Hourly Rhythm).
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** Hai đỉnh: Đỉnh trưa (11h--13h) và Đỉnh chiều tối (16h--18h).

**Lời thoại trình bày:**
> *"Mổ xẻ sâu hơn vào 24 giờ trong ngày, dữ liệu xuất hiện **cấu trúc hai đỉnh nhịp sinh học rất rõ nét**: Đỉnh 1 vào giờ nghỉ trưa (11h--13h) và Đỉnh 2 mạnh nhất vào lúc tan sở (16h--18h) khi khách hàng ghé mua thực phẩm chuẩn bị bữa tối. Hơn 65% tổng hóa đơn tập trung trong khung 7 tiếng này.*
>
> *Từ góc độ vận hành tiếp thị và CRM, phát hiện này chỉ ra **'khung giờ vàng' để gửi thông báo ưu đãi hoặc email nhắc nhở là khoảng 9h đến 10h sáng** – đón đầu đúng trước khi nhu cầu đi chợ buổi trưa và buổi chiều phát sinh."*

---

### SLIDE 8: CÂU CHUYỆN 5 - ĐỒ TƯƠI SỐNG: ĐỘNG LỰC THÚC ĐẨY MUA SẮM
* **Tiêu đề:** 7. Thực Phẩm Tươi Sống & Động Lực Thúc Đẩy Mua Sắm
* **Biểu đồ:** So sánh chu kỳ quay lại giữa giỏ có đồ tươi (Perishable) và giỏ chỉ có đồ khô.
* **Thời lượng:** 50 giây
* **Điểm nhấn trực quan:** Đường phân phối của giỏ có đồ tươi lệch hẳn về bên trái (chu kỳ ngắn hơn 1.8 ngày).

**Lời thoại trình bày:**
> *"Một trong những phát hiện thú vị nhất về mặt tâm lý tiêu dùng là **hiệu ứng chiếc đồng hồ đếm ngược của thực phẩm tươi sống** (thịt, rau củ, sữa tươi).*
>
> *Do hạn sử dụng ngắn (chỉ 2 đến 5 ngày), hộ gia đình mua đồ tươi có khoảng cách quay lại siêu thị ngắn hơn gần **1.8 ngày** so với các giỏ hàng chỉ mua đồ khô hoặc hóa mỹ phẩm. Chiếc tủ lạnh hết thức ăn tươi chính là động lực tự nhiên mạnh nhất thúc đẩy chuyến đi kế tiếp.*
>
> *Vì vậy, các đặc trưng như `days_since_last_perishable` và `perishable_ratio_90d` trở thành nhóm tín hiệu dự báo có trọng số cực cao trong mô hình."*

---

### SLIDE 9: CÂU CHUYỆN 6 - HIỆU ỨNG MỒI CÂU & ĐỘ LAN TỎA COUPON
* **Tiêu đề:** 8. Hiệu Ứng Mồi Câu & Độ Lan Tỏa Của Phiếu Giảm Giá
* **Biểu đồ:** Cấu trúc chi tiêu của giỏ hàng có dùng Coupon (Spend with vs. without Coupon).
* **Thời lượng:** 50 giây
* **Điểm nhấn trực quan:** Cột giá trị giỏ hàng có coupon cao gấp 2.5 lần (\$67.60 vs \$26.70).

**Lời thoại trình bày:**
> *"Slide 8 minh họa **Hiệu ứng Mồi câu (Halo Effect)** của các phiếu giảm giá. Khách hàng sử dụng coupon có giá trị giỏ hàng trung bình lên tới **\$67.60**, cao gấp **2.53 lần** so với giỏ hàng thông thường (\$26.70).*
>
> *Mặc dù phiếu ưu đãi chỉ giảm cho một vài món cụ thể, nhưng khi đã cầm coupon đến siêu thị, khách hàng dạo qua các quầy hàng khác và mua sắm chéo rất nhiều. Hơn **80%** giá trị giỏ hàng có coupon đến từ các sản phẩm nguyên giá đi kèm.*
>
> *Điều này khẳng định: Nhóm khách hàng chủ động dùng coupon là nhóm khách hàng có giá trị cao nhất (VIP), và tần suất dùng phiếu `coupon_redempt_count` là tín hiệu vàng của lòng trung thành."*

---

### SLIDE 10: CÂU CHUYỆN 7 - SỨC BẬT CHU KỲ TỪ CHIẾN DỊCH TIẾP THỊ
* **Tiêu đề:** 9. Sức Bật Chu Kỳ Từ Các Chiến Dịch Tiếp Thị
* **Biểu đồ:** So sánh chu kỳ tái mua trong đợt chiến dịch (Active Campaign) vs. ngoài chiến dịch.
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** Chu kỳ tái mua bị rút ngắn gần 3 ngày khi chiến dịch được kích hoạt.

**Lời thoại trình bày:**
> *"Bên cạnh động lực tự nhiên, các chiến dịch gửi thư tiếp thị trực tiếp (Direct Mail) đóng vai trò là **chất xúc tác ngoại sinh phá vỡ độ ì mua sắm**.*
>
> *Trong các giai đoạn chiến dịch hoạt động, thời gian chờ mua hàng của hộ gia đình được rút ngắn gần **3 ngày** so với giai đoạn thông thường, đồng thời tần suất mua sắm tăng gần gấp đôi.*
>
> *Do đó, biến cờ `is_targeted_by_campaign` tại thời điểm quan sát là một đặc trưng ngoại sinh quan trọng giúp mô hình bắt được sự gia tốc hành vi."*

---

### SLIDE 11: CÂU CHUYỆN 8 - HÀNH VI MUA SẮM ĐA CỬA HÀNG & LÒNG TRUNG THÀNH
* **Tiêu đề:** 10. Hành Vi Mua Sắm Đa Cửa Hàng & Lòng Trung Thành
* **Biểu đồ:** Tỷ lệ phân bổ chi tiêu giữa Cửa hàng chính (Primary Store) và các cửa hàng phụ.
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** Miếng bánh 73.4% ngân sách tập trung vào 1 cửa hàng duy nhất.

**Lời thoại trình bày:**
> *"Khám phá về mặt địa lý cho thấy hơn **66.4%** hộ gia đình có ghé mua sắm ở nhiều hơn một chi nhánh (tiện đường đi làm, đón con hoặc du lịch).*
>
> *Tuy nhiên, họ không phân bổ tiền đồng đều: Gần **3/4 ngân sách (73.4%)** vẫn dồn trọn vẹn vào một 'cửa hàng ruột' duy nhất. Các chi nhánh còn lại chỉ đóng vai trò mua sắm phát sinh lẻ.*
>
> *Từ phát hiện này, mô hình được bổ sung chỉ số trung thành `store_loyalty_index` và `primary_store_id`, giúp phân biệt rõ đâu là địa bàn tiêu dùng cốt lõi của khách hàng."*

---

### SLIDE 12: CÂU CHUYỆN 9 - QUY MÔ HỘ GIA ĐÌNH & GIÁ TRỊ GIỎ HÀNG
* **Tiêu đề:** 11. Quy Mô Hộ Gia Đình & Tác Động Lên Giá Trị Giỏ Hàng
* **Biểu đồ:** Tương quan giữa Quy mô hộ gia đình (1, 2, 3, 4, 5+ thành viên) và AOV.
* **Thời lượng:** 40 giây
* **Điểm nhấn trực quan:** Đường bậc thang đi lên vững chắc từ \$22 lên tới \$36/giỏ hàng.

**Lời thoại trình bày:**
> *"Mối liên hệ giữa nhân khẩu học và quy mô giỏ hàng diễn ra theo quan hệ tuyến tính rất đẹp: Số miệng ăn trong gia đình quy định trực tiếp giá trị hóa đơn. Các hộ gia đình từ 5 người trở lên có AOV cao hơn **+39.4%** so với hộ độc thân.*
>
> *Đặc biệt, sự xuất hiện của trẻ nhỏ kéo theo nhu cầu về các dòng sản phẩm giá trị cao như sữa bột, tã bỉm và đồ ăn dặm. Mặc dù 68% hộ bị thiếu dữ liệu này, việc nhóm chúng vào danh mục `UNKNOWN` vẫn cho phép mô hình khai thác triệt để tín hiệu từ 32% hộ có thông tin mà không làm méo mó phân phối."*

---

### SLIDE 13: CÂU CHUYỆN 10 - ĐỘ ỔN ĐỊNH NHÃN MỤC TIÊU THEO THỜI GIAN
* **Tiêu đề:** 12. Độ Ổn Định Nhãn Mục Tiêu Theo Dòng Thời Gian
* **Biểu đồ:** Tỷ lệ nhãn mục tiêu ($Y = 1$) qua từng tuần trong suốt 711 ngày.
* **Thời lượng:** 50 giây
* **Điểm nhấn trực quan:** Đường ngang phẳng lì dao động quanh mốc 68.25% (dải biên độ chỉ $\pm 2.2\%$).

**Lời thoại trình bày:**
> *"Slide 13 là một trong những slide quan trọng nhất về mặt toán học và kiểm định: **Kiểm tra hiện tượng trôi dạt dữ liệu (Data Drift / Concept Drift)** của nhãn mục tiêu.*
>
> *Khi chúng tôi tính tỷ lệ hộ gia đình có đi chợ trong 14 ngày tới trên toàn bộ trục thời gian 1.5 năm, kết quả cho thấy đường tỷ lệ duy trì ổn định tuyệt đối quanh mức **68.25%**, với độ lệch chuẩn rất hẹp chỉ $\pm 2.2\%$.*
>
> *Sự bất biến theo thời gian này chứng minh tính chất tiêu dùng thiết yếu của ngành bán lẻ, và là bảo chứng khoa học khẳng định chúng ta hoàn toàn có thể áp dụng chiến lược **cắt mẫu trượt thời gian (Multi-cutoff temporal split)** mà không sợ mô hình bị sốc phân phối nhãn."*

---

### SLIDE 14: CÂU CHUYỆN 11 - PHÂN HÓA DOANH THU & KIỂM ĐỊNH PARETO
* **Tiêu đề:** 13. Phân Hóa Giá Trị Khách Hàng (CLV) & Kiểm Định Pareto
* **Biểu đồ:** Đường cong Lorenz tích lũy doanh thu của 2,500 hộ gia đình đối sánh với mốc Pareto 80/20 lý thuyết.
* **Thời lượng:** 50 giây
* **Điểm nhấn trực quan:** Chỉ vào điểm dấu X màu xanh lá (Mốc Pareto 80/20 lý thuyết) và điểm thực tế màu đỏ (Top 20% chỉ đạt 53.0%, cần 44.0% hộ mới đạt 80% doanh thu).

**Lời thoại trình bày:**
> *"Khi phân tích giá trị trọn đời (CLV) qua đường cong Lorenz, chúng tôi thu được một phát hiện thực nghiệm rất đắt giá: **Dữ liệu bán lẻ FMCG không tuân theo quy luật Pareto 80/20 kinh điển**.*
>
> *Khác với mô hình phần mềm SaaS hay hàng hiệu xa xỉ – nơi 20% khách hàng có thể mang lại 80% doanh thu, trong ngành siêu thị bán lẻ, hàng hóa là nhu yếu phẩm thiết yếu nên mọi gia đình đều phải chi tiêu hàng tuần. Kết quả thực nghiệm cho thấy: Top 20% hộ gia đình chỉ đóng góp **53.0% tổng doanh thu** (\$4.27 triệu USD), và chúng ta phải cần tới **44.0% số hộ (khoảng 1,100 hộ)** mới đạt được 80% doanh số.*
>
> *Hệ số Gini thực tế dừng ở mức **0.503** – thể hiện mức độ bất bình đẳng vừa phải. Dù không cực đoan như lý thuyết 80/20, nhóm 500 hộ dẫn đầu vẫn mang lại doanh số gấp 3.4 lần nửa dưới. Vì vậy, thay vì áp đặt tỷ lệ 80/20 cứng nhắc, mô hình của chúng tôi phân khúc khách hàng theo phân vị chi tiêu thực tế `spend_percentile_rank` và cảnh báo CRM khi khách VIP dãn chu kỳ mua (`urgency_ratio > 1.5`)."*

---

### SLIDE 15: CÂU CHUYỆN 12 - CƠ CHẾ CHIẾT KHẤU HAI TẦNG
* **Tiêu đề:** 14. Cơ Chế Chiết Khấu Hai Tầng: Quầy Kệ & Phiếu Giảm Giá
* **Biểu đồ:** Đối sánh tổng ngân sách giảm giá tại quầy (Markdown) vs. giảm giá qua Coupon.
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** Cột Markdown \$1.4M cao vượt trội gấp 32.8 lần cột Coupon \$42.6k.

**Lời thoại trình bày:**
> *"Dữ liệu ghi nhận hai cơ chế chiết khấu hoàn toàn khác nhau về bản chất: Giảm giá niêm yết tại quầy kệ (`RETAIL_DISC`) đạt tới **\$1.4 triệu USD**, lớn gấp **32.8 lần** so với giá trị giảm qua phiếu coupon (`COUPON_DISC` đạt \$42.6k).*
>
> *Giảm giá quầy kệ là cơ chế đại trà tác động lên toàn bộ người mua sắm tại điểm bán, trong khi coupon là hành vi chủ động đòi hỏi nỗ lực sưu tầm. Vì phản ánh hai tâm lý đối lập, chúng tôi bắt buộc phải tách riêng thành hai biến: `retail_discount_ratio` và `coupon_discount_ratio` thay vì gộp chung."*

---

### SLIDE 16: CÂU CHUYỆN 13 - SỨC THÂM NHẬP CỦA NHÃN HÀNG RIÊNG (PRIVATE LABEL)
* **Tiêu đề:** 15. Sức Thâm Nhập Doanh Thu Của Nhãn Hàng Riêng
* **Biểu đồ:** Tỷ trọng doanh thu & số lượng mặt hàng của Private Label so với Thương hiệu Quốc gia.
* **Thời lượng:** 40 giây
* **Điểm nhấn trực quan:** Hiệu suất doanh thu của Private Label gấp 1.9 lần tỷ trọng số lượng mặt hàng.

**Lời thoại trình bày:**
> *"Nhãn hàng riêng (Private Label của Kroger) thể hiện hiệu quả kinh tế đáng kinh ngạc: Dù chỉ chiếm danh mục SKU gọn nhẹ, nhưng nhãn riêng đem lại doanh số và sản lượng gấp **1.9 lần** mức bình quân.*
>
> *Khách hàng tin dùng nhãn riêng cho các nhu cầu thiết yếu hàng ngày vì giá thành hợp lý. Mua sắm nhãn riêng chính là một chỉ dấu quan trọng phản ánh sự gắn bó chặt chẽ với chuỗi siêu thị, được đo lường qua biến `private_label_ratio_90d`."*

---

### SLIDE 17: CÂU CHUYỆN 14 - PHỄU CHUYỂN ĐỔI THEO NHÓM CHIẾN DỊCH
* **Tiêu đề:** 16. Phễu Chuyển Đổi Tiếp Thị Theo Nhóm Chiến Dịch
* **Biểu đồ:** Tỷ lệ đổi phiếu thành công của Chiến dịch Loại A, B và C.
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** Cột Chiến dịch Loại A dẫn đầu với tỷ lệ đổi phiếu vượt trội ~45%.

**Lời thoại trình bày:**
> *"Khi phân tích hiệu quả của 30 chiến dịch tiếp thị, ta thấy rõ sự phân hóa chất lượng: **Chiến dịch Loại A đạt tỷ lệ đổi phiếu thành công cao nhất (~45%)**, trong khi Loại B và C có tỷ lệ chuyển đổi khiêm tốn hơn nhiều.*
>
> *Lý do là Loại A có độ phủ sản phẩm đa ngành rất rộng, giúp mọi hộ gia đình dễ dàng tìm thấy mặt hàng phù hợp với nhu cầu. Việc mô hình hóa bắt buộc phải phân rã chi tiết thành `is_targeted_type_A`, `type_B` và `type_C` thay vì đánh đồng mọi chiến dịch như nhau."*

---

### SLIDE 18: CHUYỂN HÓA PHÁT HIỆN EDA SANG HỆ THỐNG ĐẶC TRƯNG HỌC MÁY
* **Tiêu đề:** 17. Chuyển Hóa Phát Hiện EDA Sang Hệ Thống Đặc Trưng ML
* **Bảng:** Ma trận ánh xạ 6 nhóm hành vi sang hệ thống biến đặc trưng tương ứng.
* **Thời lượng:** 60 giây
* **Điểm nhấn trực quan:** Hàng alertbox dưới cùng nhấn mạnh Kỷ luật thời gian $DAY \le t_0$.

**Lời thoại trình bày:**
> *"Thưa quý vị, toàn bộ 14 câu chuyện thực nghiệm vừa nêu đã được chúng tôi tổng hợp và chuyển hóa thành **Ma trận ánh xạ đặc trưng** trên Slide 17:*
>
> 1. *Nhịp sinh học & Đồ tươi $\rightarrow$ Nhóm biến Recency & Urgency (`days_since_last_basket`, `urgency_ratio`).*
> 2. *Sức mua & Nhân khẩu $\rightarrow$ Nhóm biến Volume & Household Size.*
> 3. *Tập trung doanh thu & Phân vị $\rightarrow$ Nhóm biến Phân vị khách hàng VIP (`spend_percentile_rank`).*
> 4. *Chiết khấu 2 tầng $\rightarrow$ Tách riêng tỷ lệ giảm quầy kệ và giảm coupon.*
> 5. *Hiệu ứng mồi câu & Phễu $\rightarrow$ Lịch sử đổi phiếu và phân loại chiến dịch A/B/C.*
> 6. *Địa bàn & Trung thành $\rightarrow$ Chỉ số trung thành cửa hàng ruột (`store_loyalty_index`).*
>
> *Đặc biệt, **100% các đặc trưng này đều được tính toán nghiêm ngặt tại thời điểm quan sát $DAY \le t_0$**, tuyệt đối không nhìn trước dữ liệu tương lai, bảo đảm mô hình học máy khi triển khai thực tế sẽ đạt độ tin cậy cao nhất."*

---

### SLIDE 19: TỔNG KẾT GIAI ĐOẠN EDA & KẾ HOẠCH TIẾP THEO
* **Tiêu đề:** 18. Tổng Kết Giá Trị Nền Tảng Của Giai Đoạn EDA
* **Thời lượng:** 60 giây
* **Điểm nhấn trực quan:** 4 đóng góp nền tảng ở cột trái và lời cảm ơn / chuyển sang Q&A ở cột phải.

**Lời thoại trình bày:**
> *"Để khép lại phần báo cáo, giai đoạn EDA và Kiểm toán Chất lượng đã mang lại **4 đóng góp nền tảng** cho toàn bộ dự án:*
>
> *Một là, xác lập cửa sổ dự báo tối ưu **$\Delta t = 14$ ngày** trên cơ sở 92.4% chu kỳ tự nhiên;*  
> *Hai là, làm sạch triệt để 942 giỏ hàng $\le \$0$ và khử trùng 5,164 bản ghi coupon, bảo toàn dữ liệu thương mại sạch;*  
> *Ba là, chuyển hóa 14 quy luật hành vi thành bộ đặc trưng máy học có tính giải thích cao;*  
> *Bốn là, chứng minh nhãn mục tiêu ổn định ở mức 68.25%, cho phép triển khai chiến lược huấn luyện trượt thời gian.*
>
> *Đây chính là bệ phóng vững chắc nhất để chúng tôi tự tin bước vào giai đoạn tiếp theo: Huấn luyện các mô hình phân loại LightGBM, XGBoost và CatBoost.*
>
> *Xin chân thành cảm ơn quý thầy cô và các anh chị đã chú ý lắng nghe. Rất mong nhận được các câu hỏi và ý kiến đóng góp ạ!"*
>
> *Đây chính là bệ phóng vững chắc nhất để chúng tôi tự tin bước vào giai đoạn tiếp theo: Huấn luyện các mô hình phân loại LightGBM, XGBoost và CatBoost.*
>
> *Xin chân thành cảm ơn quý thầy cô và các anh chị đã chú ý lắng nghe. Rất mong nhận được các câu hỏi và ý kiến đóng góp ạ!"*

---

## BỘ CÂU HỎI & TRẢ LỜI DỰ PHÒNG CHO PHẦN Q&A (ANTICIPATED Q&A)

### Câu hỏi 1: Tại sao nhóm lại chọn cửa sổ nhãn là 14 ngày mà không phải là 7 ngày hay 30 ngày?
* **Trả lời:**
  > *"Dữ liệu thực nghiệm ở Slide 4 cho thấy: Mốc 7 ngày bao phủ được 82.3% hành vi nhưng vẫn để sót gần 18% khách hàng có chu kỳ đi chợ 10–14 ngày (chu kỳ bán nguyệt theo kỳ lương). Trong khi đó, nếu nới rộng ra 30 ngày thì tỷ lệ dương tính sẽ vượt quá 98%, làm mất đi tính phân hóa của mô hình và khiến cửa sổ hành động của đội ngũ marketing trở nên quá trễ. Cửa sổ 14 ngày bao phủ trọn vẹn 92.4% chu kỳ tự nhiên, vừa đủ để mô hình nắm bắt nhịp mua sắm định kỳ, vừa tạo ra biên độ thời gian lý tưởng 2 tuần để bộ phận CRM gửi ưu đãi kịp thời."*

### Câu hỏi 2: Có những loại sản phẩm nào trong 942 giỏ hàng $\le \$0$ và việc loại bỏ chúng có làm mất dữ liệu quan trọng không?
* **Trả lời:**
  > *"Chúng tôi đã kiểm tra chi tiết từng dòng hàng: 100% trong 942 giỏ này có giá trị đúng bằng $\$0.00$ (không có giỏ âm). Trong đó, hơn 62% dòng hàng thực chất là mã thao tác POS nội bộ (quét thẻ hội viên, mở ngăn kéo) hoặc quét mã coupon đơn lẻ; gần 38% còn lại là các món quà tặng dùng thử 0đ (nước ngọt mẫu, kẹo que quầy thu ngân, cà phê refill). Đây không phải là hành vi mua sắm thương mại tạo doanh thu. Nếu giữ lại, mô hình sẽ bị **nhiễu nhãn (Label Noise)** vì lầm tưởng đó là một lần đi chợ có nhu cầu thực tế. Do đó, loại bỏ chúng là quyết định kỹ thuật chuẩn mực để bảo toàn 275,542 giỏ hàng sạch."*

### Câu hỏi 3: Tỷ lệ khuyết thiếu dữ liệu nhân khẩu học lên tới 68%, tại sao nhóm không dùng kỹ thuật Imputation (như KNN hay MICE) để điền khuyết?
* **Trả lời:**
  > *"Trong lĩnh vực bán lẻ, việc khách hàng từ chối cung cấp thu nhập hay quy mô gia đình thường không phải là khuyết thiếu ngẫu nhiên (Missing Completely at Random - MCAR), mà mang tính chất hành vi (Missing Not at Random - MNAR). Việc dùng thuật toán để dự đoán thu nhập hay số con của 68% hộ sẽ tạo ra giả định áp đặt và đưa thêm nhiễu vào mô hình. Bằng cách gán nhãn `UNKNOWN` như một nhóm độc lập, các thuật toán Tree-based như LightGBM/CatBoost có thể tự động khai thác chính xác tín hiệu: 'nhóm hộ gia đình không khai báo thông tin' có xu hướng hành vi khác biệt thế nào so với nhóm có khai báo."*

### Câu hỏi 4: Nhóm làm thế nào để đảm bảo không xảy ra hiện tượng rò rỉ dữ liệu (Data Leakage) khi tạo đặc trưng?
* **Trả lời:**
  > *"Chúng tôi thiết lập một 'Bức tường thời gian' nghiêm ngặt tại thời điểm mốc $t_0$. Mọi phép tính toán tổng chi tiêu, tần suất, hay số ngày kể từ lần mua gần nhất chỉ được phép quét các dòng hóa đơn có $DAY \le t_0$. Phần dữ liệu trong tương lai từ $t_0 + 1$ đến $t_0 + 14$ chỉ được dùng duy nhất cho một mục đích là kiểm tra xem có phát sinh giỏ hàng nào không để gán nhãn $Y \in \{0, 1\}$. Không có bất kỳ thông tin nào của giai đoạn sau $t_0$ được rò rỉ vào ma trận đặc trưng."*

---
*Tài liệu được chuẩn hóa và lưu trữ tại `docs/presentation/eda_presentation_script.md`.*
