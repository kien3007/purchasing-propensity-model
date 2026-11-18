# KỊCH BẢN TRÌNH BÀY BÁO CÁO KHÁM PHÁ DỮ LIỆU & KIỂM TOÁN CHẤT LƯỢNG (EDA & DATA QUALITY)

**Dự án:** Dự Đoán Xác Suất Mua Hàng Của Hộ Gia Đình (Purchasing Propensity Model)  
**Tập dữ liệu:** Dunnhumby - The Complete Journey (2.6M giao dịch, 2,500 hộ, 711 ngày)  
**Thời lượng dự kiến:** 12 – 14 phút thuyết trình + 5 phút Q&A  

---

## CẤU TRÚC TỔNG THỂ BÀI TRÌNH BÀY (NARRATIVE ARC)

```
[Mở Đầu] Thách thức dữ liệu thực tế & Sứ mệnh của EDA (Slide 1-2)
   │
   ├──> [Nền Tảng Dữ Liệu] Kiến trúc 8 bảng & Tiêu chuẩn làm sạch (Slide 3)
   │
   ├──> [Phần I: 10 Quy Luật Hành Vi Cốt Lõi - Nền Tảng Học Máy] (Slide 4-13)
   │      • Nhịp đi chợ (Chu kỳ 14 ngày) & Phân hóa AOV (Slide 4-5)
   │      • Thực phẩm tươi sống & Mỏ neo đa ngành (Slide 6-7)
   │      • Hiệu ứng mồi câu coupon & Gia tốc tiếp thị (Slide 8-9)
   │      • Mua sắm đa cửa hàng & Nhân khẩu quy mô hộ (Slide 10-11)
   │      • Độ ổn định nhãn mục tiêu & Phễu chuyển đổi chiến dịch (Slide 12-13)
   │
   ├──> [Phần II: Thấu Cảm Chiến Lược Bán Lẻ & Vận Hành Doanh Nghiệp] (Slide 14-17)
   │      • Phân hóa CLV & Bác bỏ quy luật Pareto 80/20 cực đoan (Slide 14)
   │      • Cấu trúc chiết khấu 2 tầng: Giảm giá quầy vs Coupon (Slide 15)
   │      • Sức thâm nhập vượt trội của Nhãn hàng riêng - Private Label (Slide 16)
   │      • Nhịp điệu thời gian vi mô: Ngày trong tuần & Giờ cao điểm (Slide 17)
   │
   └──> [Phần III: Chuyển Giao Sang Học Máy & Vận Hành CRM] (Slide 18)
          • Ma trận chuyển hóa 15 phát hiện EDA sang Đặc trưng ML & Chiến lược CRM
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
> *Trong các dự án máy học thực tế, EDA không đơn thuần chỉ là vẽ các biểu đồ mô tả thống kê, mà chính là **la bàn định hướng toàn bộ bài toán**: từ việc phát hiện và làm sạch nhiễu nghiệp vụ, xác lập cửa sổ dự báo khoa học, cho đến việc thiết kế hệ thống đặc trưng chống rò rỉ dữ liệu và cung cấp góc nhìn chiến lược kinh doanh cho doanh nghiệp bán lẻ."*

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
> *Từ thách thức đó, giai đoạn EDA của chúng tôi tập trung vào 2 mục tiêu cốt lõi: Thứ nhất, kiểm toán và bảo toàn 100% tập mẫu dữ liệu sạch; Thứ hai, bóc tách **15 phát hiện thực nghiệm cốt lõi** – trong đó gồm 10 quy luật hành vi làm nền tảng cho hệ thống đặc trưng Machine Learning, và 5 góc nhìn chiến lược bán lẻ định hình chính sách vận hành và CRM của doanh nghiệp."*

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
> *Sau khi nền tảng dữ liệu đã đạt chuẩn sạch, chúng ta cùng bước vào Phần I: 10 quy luật hành vi tiêu dùng cốt lõi phục vụ xây dựng mô hình học máy."*

---

### SLIDE 4: CÂU CHUYỆN 1 - NHỊP SINH HỌC ĐI CHỢ & CHU KỲ MUA SẮM
* **Tiêu đề:** 3. Nhịp Sinh Học Đi Chợ & Chu Kỳ Mua Sắm Của Hộ Gia Đình
* **Biểu đồ:** Phân phối khoảng cách thời gian giữa các chuyến đi chợ liên tiếp (Inter-trip Days).
* **Thời lượng:** 50 giây
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
* **Điểm nhấn trực quan:** Khoảng cách giữa P50 (\$18.06) và Giá trị trung bình (\$29.24).

**Lời thoại trình bày:**
> *"Khi phân tích giá trị chi tiêu mỗi giỏ hàng, ta nhận thấy hiện tượng phân hóa mạnh mẽ: Trung vị một giỏ hàng là **\$18.06**, nhưng giá trị trung bình (AOV) lại lên tới **\$29.24** – chênh lệch hơn 60%, trong khi nhóm P90 đạt \$63.38.*
>
> *Điều này phản ánh đúng thực tế bán lẻ: Phần lớn các chuyến đi chợ là mua lẻ bổ sung hàng ngày, nhưng dòng tiền thực sự lại được gánh vác bởi các giỏ hàng lớn cuối tuần hoặc mua sắm tiệc tùng.*
>
> *Hàm ý máy học ở đây là: **Khách hàng chi nhiều tiền chưa chắc đã đi chợ thường xuyên**. Do đó, mô hình bắt buộc phải tách bạch giữa nhóm đặc trưng về **Tần suất** (`frequency`) và nhóm đặc trưng về **Quy mô dòng tiền** (`spend_30d`, `aov_90d`)."*

---

### SLIDE 6: CÂU CHUYỆN 3 - ĐỒ TƯƠI SỐNG: ĐỘNG LỰC THÚC ĐẨY MUA SẮM
* **Tiêu đề:** 5. Thực Phẩm Tươi Sống & Động Lực Thúc Đẩy Mua Sắm
* **Biểu đồ:** So sánh chu kỳ quay lại giữa giỏ có đồ tươi (Perishable) và giỏ chỉ có đồ khô.
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** Đường phân phối của giỏ có đồ tươi lệch hẳn về bên trái (chu kỳ ngắn hơn 1.8 ngày).

**Lời thoại trình bày:**
> *"Một trong những phát hiện thực tế nhất về mặt tâm lý tiêu dùng là **hiệu ứng chiếc đồng hồ đếm ngược của thực phẩm tươi sống** (thịt, rau củ, sữa tươi).*
>
> *Do hạn sử dụng ngắn (chỉ 2 đến 5 ngày), hộ gia đình mua đồ tươi có khoảng cách quay lại siêu thị ngắn hơn gần **1.8 ngày** so với các giỏ hàng chỉ mua đồ khô hoặc hóa mỹ phẩm. Chiếc tủ lạnh hết thức ăn tươi chính là động lực tự nhiên mạnh nhất thúc đẩy chuyến đi kế tiếp.*
>
> *Vì vậy, các đặc trưng như `days_since_last_perishable` và `perishable_basket_ratio_90d` trở thành nhóm tín hiệu dự báo có trọng số cực cao trong mô hình."*

---

### SLIDE 7: CÂU CHUYỆN 4 - ĐỘ PHỦ NGÀNH HÀNG & MỎ NEO GIỮ CHÂN KHÁCH HÀNG
* **Tiêu đề:** 6. Độ Phủ Ngành Hàng & Hiệu Ứng Mỏ Neo Giữ Chân Khách Hàng
* **Biểu đồ:** Tương quan giữa Số lượng ngành hàng đã mua trong 90 ngày (Category Breadth) và Xác suất mua hàng 14 ngày tới $P(Y=1)$.
* **Thời lượng:** 50 giây
* **Điểm nhấn trực quan:** Cột xác suất tăng vọt từ 31.8% (Đơn ngành) lên tới 96.5% (Toàn diện $\ge 12$ ngành), chênh lệch gấp 3.03 lần (+64.7%).

**Lời thoại trình bày:**
> *"Slide 7 giới thiệu một phát hiện thực nghiệm mang tính bước ngoặt: **Quy luật Mỏ neo Đa ngành (Category Breadth & Basket Stickiness)**.*
>
> *Khi chúng tôi phân tích xác suất mua hàng 14 ngày tới theo số lượng ngành hàng mà hộ gia đình đã mua trong 90 ngày qua, dữ liệu bộc lộ một khoảng cách phân hóa cực độ:*
> * *Hộ mua sắm toàn diện từ **12 ngành hàng trở lên**: Xác suất mua sắm trong 2 tuần tới đạt tới **96.5%** – gần như chắc chắn sẽ quay lại.*
> * *Ngược lại, hộ chỉ mua **1 đến 2 ngành hàng**: Xác suất mua rơi tự do xuống chỉ còn **31.8%**.*
>
> *Bản chất nghiệp vụ ở đây rất rõ ràng: Khách hàng mua trải rộng nhiều danh mục xem siêu thị là **'Điểm đến sinh hoạt toàn diện' (One-Stop Destination)** cho cả gia đình, gắn chặt với cuộc sống thường nhật. Trong khi đó, khách mua đơn ngành chỉ là khách vãng lai tiện đường ghé mua món đồ lẻ (Convenience Shopper).*
>
> *Quy luật này chứng minh tại sao đặc trưng `department_breadth_90d` và `avg_items_per_basket_90d` là một trong những tín hiệu dự báo mạnh nhất của mô hình."*

---

### SLIDE 8: CÂU CHUYỆN 5 - HIỆU ỨNG MỒI CÂU & ĐỘ LAN TỎA COUPON
* **Tiêu đề:** 7. Hiệu Ứng Mồi Câu & Độ Lan Tỏa Của Phiếu Giảm Giá
* **Biểu đồ:** Cấu trúc chi tiêu của giỏ hàng có dùng Coupon (Spend with vs. without Coupon).
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** Cột giá trị giỏ hàng có coupon cao gấp 2.53 lần (\$67.60 vs \$26.76).

**Lời thoại trình bày:**
> *"Slide 8 minh họa **Hiệu ứng Mồi câu (Halo Effect)** của các phiếu giảm giá. Khách hàng sử dụng coupon có giá trị giỏ hàng trung bình lên tới **\$67.60**, cao gấp **2.53 lần** so với giỏ hàng thông thường (\$26.76).*
>
> *Mặc dù phiếu ưu đãi chỉ giảm cho một vài món cụ thể, nhưng khi đã cầm coupon đến siêu thị, khách hàng dạo qua các quầy hàng khác và mua sắm chéo rất nhiều. Hơn **80%** giá trị giỏ hàng có coupon đến từ các sản phẩm nguyên giá đi kèm.*
>
> *Điều này khẳng định: Nhóm khách hàng chủ động dùng coupon là nhóm khách hàng có giá trị cao nhất (VIP), và tần suất dùng phiếu `coupon_redempt_count_180d` là tín hiệu vàng của lòng trung thành."*

---

### SLIDE 9: CÂU CHUYỆN 6 - SỨC BẬT CHU KỲ TỪ CHIẾN DỊCH TIẾP THỊ
* **Tiêu đề:** 8. Sức Bật Chu Kỳ Từ Các Chiến Dịch Tiếp Thị
* **Biểu đồ:** So sánh chu kỳ tái mua trong đợt chiến dịch (Active Campaign) vs. ngoài chiến dịch.
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** Chu kỳ tái mua bị rút ngắn từ 6.49 ngày xuống 3.55 ngày (rút ngắn gần 45%) khi chiến dịch được kích hoạt.

**Lời thoại trình bày:**
> *"Bên cạnh động lực tự nhiên, các chiến dịch gửi thư tiếp thị trực tiếp (Direct Mail) đóng vai trò là **chất xúc tác ngoại sinh phá vỡ độ ì mua sắm**.*
>
> *Trong các giai đoạn chiến dịch hoạt động, thời gian chờ mua hàng của hộ gia đình được rút ngắn từ **6.49 ngày xuống chỉ còn 3.55 ngày**, đồng thời tần suất mua sắm tăng gần gấp đôi.*
>
> *Do đó, biến cờ `is_targeted_by_active_campaign` tại thời điểm quan sát là một đặc trưng ngoại sinh quan trọng giúp mô hình bắt được sự gia tốc hành vi."*

---

### SLIDE 10: CÂU CHUYỆN 7 - HÀNH VI MUA SẮM ĐA CỬA HÀNG & LÒNG TRUNG THÀNH
* **Tiêu đề:** 9. Hành Vi Mua Sắm Đa Cửa Hàng & Lòng Trung Thành
* **Biểu đồ:** Hiện tượng mua sắm đa cửa hàng (Store Hopping) và tỷ lệ chi tiêu cho cửa hàng ruột.
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** 66.4% hộ đi từ 4 cửa hàng trở lên, nhưng gần 3/4 ngân sách (73.4%) tập trung vào đúng 1 cửa hàng ruột.

**Lời thoại trình bày:**
> *"Khám phá về mặt địa lý cho thấy hơn **66.4%** hộ gia đình có ghé mua sắm ở từ 4 chi nhánh khác nhau trở lên (tiện đường đi làm, đón con hoặc du lịch).*
>
> *Tuy nhiên, họ không phân bổ tiền đồng đều: Gần **3/4 ngân sách (73.35%)** vẫn dồn trọn vẹn vào một 'cửa hàng ruột' duy nhất. Các chi nhánh còn lại chỉ đóng vai trò mua sắm phát sinh lẻ.*
>
> *Từ phát hiện này, mô hình được bổ sung chỉ số trung thành `store_loyalty_index` và `primary_store_id`, giúp phân biệt rõ đâu là địa bàn tiêu dùng cốt lõi của khách hàng."*

---

### SLIDE 11: CÂU CHUYỆN 8 - QUY MÔ HỘ GIA ĐÌNH & GIÁ TRỊ GIỎ HÀNG
* **Tiêu đề:** 10. Quy Mô Hộ Gia Đình & Tác Động Lên Giá Trị Giỏ Hàng
* **Biểu đồ:** Tương quan giữa Quy mô hộ gia đình và AOV.
* **Thời lượng:** 40 giây
* **Điểm nhấn trực quan:** AOV tăng từ \$31.49 (độc thân) lên \$43.91 (hộ đông người), chênh lệch +39.4%.

**Lời thoại trình bày:**
> *"Mối liên hệ giữa nhân khẩu học và quy mô giỏ hàng diễn ra theo quan hệ tuyến tính: Số miệng ăn trong gia đình quy định trực tiếp giá trị hóa đơn. Các hộ gia đình đông người có AOV đạt **\$43.91**, cao hơn **+39.4%** so với hộ độc thân (\$31.49).*
>
> *Đặc biệt, sự xuất hiện của trẻ nhỏ kéo theo nhu cầu về các dòng sản phẩm giá trị cao như sữa bột, tã bỉm và đồ ăn dặm. Mặc dù 68% hộ bị thiếu dữ liệu này, việc nhóm chúng vào danh mục `UNKNOWN` vẫn cho phép mô hình khai thác triệt để tín hiệu từ 32% hộ có thông tin mà không làm méo mó phân phối."*

---

### SLIDE 12: CÂU CHUYỆN 9 - ĐỘ ỔN ĐỊNH NHÃN MỤC TIÊU THEO THỜI GIAN
* **Tiêu đề:** 11. Độ Ổn Định Nhãn Mục Tiêu Theo Dòng Thời Gian
* **Biểu đồ:** Tỷ lệ nhãn mục tiêu ($Y = 1$) qua 16 mốc chốt sổ quan sát $t_0$ từ Ngày 200 đến Ngày 680.
* **Thời lượng:** 50 giây
* **Điểm nhấn trực quan:** Đường ngang phẳng lì dao động quanh mốc 68.25% (dải biên độ chỉ $\pm 2.2\%$).

**Lời thoại trình bày:**
> *"Slide 12 là một trong những slide quan trọng nhất về mặt toán học và kiểm định: **Kiểm tra hiện tượng trôi dạt dữ liệu (Data Drift / Concept Drift)** của nhãn mục tiêu.*
>
> *Khi chúng tôi tính tỷ lệ hộ gia đình có đi chợ trong 14 ngày tới trên 16 mốc chốt sổ trải dài gần 2 năm, kết quả cho thấy đường tỷ lệ duy trì ổn định tuyệt đối quanh mức **68.25%**, với độ lệch chuẩn rất hẹp chỉ $\pm 2.2\%$.*
>
> *Sự bất biến theo thời gian này chứng minh tính chất tiêu dùng thiết yếu của ngành bán lẻ, và là bảo chứng khoa học khẳng định chúng ta hoàn toàn có thể áp dụng chiến lược **cắt mẫu trượt thời gian (Multi-cutoff temporal split)** mà không sợ mô hình bị sốc phân phối nhãn."*

---

### SLIDE 13: CÂU CHUYỆN 10 - PHỄU CHUYỂN ĐỔI THEO NHÓM CHIẾN DỊCH
* **Tiêu đề:** 12. Phễu Chuyển Đổi Tiếp Thị Theo Nhóm Chiến Dịch
* **Biểu đồ:** Tỷ lệ đổi phiếu thành công và quy mô phễu của Chiến dịch Loại A, B và C.
* **Thời lượng:** 45 giây
* **Điểm nhấn trực quan:** Cột Chiến dịch Loại A dẫn đầu với tỷ lệ đổi phiếu vượt trội 45.01% (gấp 3.5 lần Loại C).

**Lời thoại trình bày:**
> *"Khi phân tích phễu chuyển đổi của các chiến dịch tiếp thị, ta thấy rõ sự phân hóa chất lượng: **Chiến dịch Loại A đạt tỷ lệ đổi phiếu thành công lên tới 45.01%**, trong khi Loại B chỉ đạt 17.1% và Loại C chỉ đạt 12.7%.*
>
> *Chiến dịch Loại A có hiệu quả kích hoạt hành vi **gấp 3.5 lần** so với Loại C nhờ độ phủ sản phẩm đa ngành rất rộng, giúp mọi hộ gia đình dễ dàng tìm thấy mặt hàng phù hợp với nhu cầu. Vì vậy, đặc trưng ngoại sinh `is_targeted_by_active_campaign` là một biến phân loại mang tính quyết định trong mô hình.*
>
> *Bây giờ, chúng ta bước sang Phần II: Những góc nhìn chiến lược bán lẻ và vận hành sâu sắc được khai phá từ dữ liệu."*

---

### SLIDE 14: CÂU CHUYỆN 11 - PHÂN HÓA CLV & KIỂM ĐỊNH PARETO 80/20
* **Tiêu đề:** 13. Phân Hóa Giá Trị Trọn Đời (CLV) & Kiểm Định Pareto 80/20
* **Biểu đồ:** Đường cong Lorenz thực tế so với đường phân bổ bình đẳng ($45^\circ$) cho 2,500 hộ gia đình.
* **Thời lượng:** 55 giây
* **Điểm nhấn trực quan:** Vùng bất bình đẳng màu xanh; mốc Top 20% đạt 53.05% doanh số ($4.27M); mốc 44% hộ để đạt 80% doanh thu.

**Lời thoại trình bày:**
> *"Trên Slide 14, chúng tôi thực hiện kiểm định giả thuyết kinh điển trong quản trị khách hàng: **Quy luật Pareto 80/20** về giá trị trọn đời (CLV).*
>
> *Đường cong Lorenz thực tế từ 2 năm chi tiêu của 2,500 hộ gia đình (tổng doanh thu \$8.06 Triệu USD) cho thấy:*
> * *Top 10% hộ gia đình tạo ra **34.29% tổng doanh thu** (\$2.76 Triệu USD).*
> * *Top 20% hộ gia đình tạo ra **53.05% tổng doanh thu** (\$4.27 Triệu USD).*
> * *Ngược lại, 50% số hộ ở nửa dưới chỉ đóng góp vỏn vẹn **15.66% tổng doanh thu**.*
>
> *Tuy nhiên, kiểm định thực nghiệm đã **bác bỏ quy luật Pareto 80/20 cực đoan**: Thực tế cần tới **44% số hộ gia đình** mới đạt được 80% doanh số (chỉ số Gini = 0.50). Trong ngành bán lẻ nhu yếu phẩm, mức độ phân hóa nhẹ nhàng hơn so với các mặt hàng xa xỉ hay phần mềm B2B.*
>
> *Góc nhìn này đem lại 2 giá trị: Đối với bộ phận CRM, đây là cơ sở phân khúc khách hàng VIP để có chính sách chăm sóc riêng biệt. Đối với Machine Learning, để tuyệt đối chống rò rỉ dữ liệu tương lai, mô hình chỉ sử dụng biến `spend_180d` quá khứ làm proxy an toàn mà không nhét trực tiếp CLV 2 năm vào đặc trưng."*

---

### SLIDE 15: CÂU CHUYỆN 12 - CẤU TRÚC CHIẾT KHẤU 2 TẦNG
* **Tiêu đề:** 14. Cấu Trúc Khuyến Mãi 2 Tầng: Giảm Giá Niêm Yết Siêu Thị vs Phiếu Giảm Giá
* **Biểu đồ:** Đối sánh tổng ngân sách chiết khấu (Triệu USD) và tỷ lệ bao phủ giỏ hàng giữa Giảm giá tại quầy (`RETAIL_DISC`) và Coupon (`COUPON_DISC`).
* **Thời lượng:** 50 giây
* **Điểm nhấn trực quan:** Cột màu cam \$1.40M gấp 32.8 lần cột xanh \$42.6k; tỷ lệ phủ 48.7% vs 6.2%.

**Lời thoại trình bày:**
> *"Slide 15 bóc tách một bí mật thú vị về cấu trúc tài chính trong bán lẻ: **Sự bất cân xứng giữa Giảm giá niêm yết tại quầy và Phiếu giảm giá Coupon**.*
>
> *Nhiều người nghĩ rằng coupon là nguồn chiết khấu chủ yếu. Nhưng số liệu thực nghiệm chứng minh điều ngược lại:*
> * *Giảm giá niêm yết tại quầy của siêu thị (`RETAIL_DISC`) đạt tới **\$1.40 Triệu USD** (chiếm gần 15% tổng doanh thu gộp) và xuất hiện ở **48.74% số giỏ hàng**.*
> * *Trong khi đó, giảm giá bằng phiếu coupon (`COUPON_DISC`) chỉ đạt **\$42.6k USD** (chiếm 0.53% doanh thu gộp) và chỉ bao phủ **6.22% số giỏ hàng**.*
>
> *Giảm giá niêm yết trên kệ lớn **gấp 32.8 LẦN** so với coupon! Điều này cho thấy: Siêu thị là bên chủ động hy sinh biên lợi nhuận đại trà trên kệ hàng để cạnh tranh giá; còn coupon chỉ là vũ khí nhắm trúng đích cho nhóm khách hàng chuyên săn ưu đãi.*
>
> *Phát hiện này định hướng cho ban giám đốc cân đối lại ngân sách khuyến mãi đại trà để bảo toàn biên lợi nhuận ròng."*

---

### SLIDE 16: CÂU CHUYỆN 13 - SỨC THÂM NHẬP CỦA NHÃN HÀNG RIÊNG (PRIVATE LABEL)
* **Tiêu đề:** 15. Sức Thâm Nhập Vượt Trội Của Nhãn Hàng Riêng Siêu Thị
* **Biểu đồ:** So sánh tỷ trọng danh mục SKU (15.0%) vs Tỷ trọng Doanh thu (27.8%) và Tỷ trọng Sản lượng (28.8%).
* **Thời lượng:** 50 giây
* **Điểm nhấn trực quan:** Thanh màu xanh chỉ chiếm 15% SKU nhưng vươn lên chiếm gần 28% doanh thu và 29% sản lượng; chỉ số hiệu suất 1.86x.

**Lời thoại trình bày:**
> *"Tiếp tục ở Slide 16 là một phát hiện chiến lược về quản trị danh mục mặt hàng: **Sức thâm nhập phi thường của Nhãn hàng riêng (Private Label / Store Brand)**.*
>
> *Trong tổng số hơn 92,000 mã hàng hóa, nhãn hàng riêng của siêu thị chỉ chiếm khiêm tốn **14.96% số SKU**, nhường 85% kệ hàng cho các thương hiệu quốc gia (National Brand).*
>
> *Thế nhưng, 15% mặt hàng này lại tạo ra tới **27.83% tổng doanh thu** (\$2.24 Triệu USD) và chiếm **28.80% tổng sản lượng hàng hóa bán ra**!*
>
> *Chỉ số hiệu suất doanh thu trên mỗi SKU của nhãn riêng đạt **1.86x**, cao gấp **2.18 lần** so với thương hiệu quốc gia (0.85x). Người tiêu dùng tin tưởng nhãn riêng như một giải pháp 'chất lượng tốt - giá hợp lý' cho nhu yếu phẩm hàng ngày.*
>
> *Đây là khuyến nghị chiến lược đắt giá để chuỗi siêu thị tiếp tục mở rộng các dòng sản phẩm Private Label nhằm tối ưu hóa biên lợi nhuận gộp."*

---

### SLIDE 17: CÂU CHUYỆN 14 - NHỊP ĐIỆU THỜI GIAN VI MÔ
* **Tiêu đề:** 16. Nhịp Điệu Thời Gian Vi Mô: Ngày Trong Tuần & Khung Giờ Vàng
* **Biểu đồ:** Biểu đồ kép: Phân phối lượng giỏ hàng theo Ngày trong tuần (bên trái) và Khung giờ mua sắm trong ngày (bên phải).
* **Thời lượng:** 50 giây
* **Điểm nhấn trực quan:** Hai cột cuối tuần Thứ Bảy & Chủ Nhật đạt đỉnh 32%; dải giờ vàng 11h - 18h chiếm 65% giao dịch.

**Lời thoại trình bày:**
> *"Bên cạnh chu kỳ 14 ngày vĩ mô, dữ liệu còn tiết lộ **nhịp điệu thời gian vi mô cực kỳ rõ nét** trên Slide 17:*
>
> 1. *Theo ngày trong tuần: Thứ Bảy và Chủ Nhật chiếm tới **32% tổng lượng giao dịch** cả tuần. Khách hàng dồn sức đi sắm giỏ hàng lớn vào hai ngày nghỉ.*
> 2. *Theo khung giờ trong ngày: Toàn bộ lưu lượng mua sắm tập trung đậm đặc vào khung **11 giờ trưa đến 18 giờ chiều**, chiếm tới **65% tổng số giao dịch** trong ngày, và đạt đỉnh cao nhất vào khoảng 14h - 17h khi các gia đình mua thực phẩm chuẩn bị bữa tối.*
>
> *Phát hiện này cung cấp giải pháp vận hành thực chiến: Ban quản lý siêu thị cần tối ưu hóa ca trực thu ngân và tiếp tế quầy đồ tươi vào khung giờ vàng; đồng thời, các thông báo kích cầu qua ứng dụng CRM nên được tự động gửi vào sáng Thứ Sáu để đón đầu làn sóng mua sắm cuối tuần."*

---

### SLIDE 18: MA TRẬN CHUYỂN HÓA PHÁT HIỆN EDA SANG HỆ THỐNG ĐẶC TRƯNG & VẬN HÀNH
* **Tiêu đề:** 17. Chuyển Hóa Phát Hiện EDA Sang Đặc Trưng ML & Vận Hành CRM
* **Bảng:** Ma trận ánh xạ 7 trụ cột phát hiện thực nghiệm sang Đặc trưng ML và Giải pháp vận hành CRM.
* **Thời lượng:** 75 giây
* **Điểm nhấn trực quan:** Nhấn mạnh dòng Kỷ luật thời gian màu cam ở cuối: 100% biến ML tuân thủ ranh giới $DAY \le t_0$, cùng lời cảm ơn chuyển sang Q&A.

**Lời thoại trình bày:**
> *"Thưa quý vị, toàn bộ 15 phát hiện thực nghiệm vừa nêu đã được chúng tôi tổng hợp và chuyển hóa thành **Ma trận chuyển giao 2 tầng** trên Slide 17:*
>
> *Ở tầng **Machine Learning**, 10 quy luật hành vi tiêu dùng đã được mã hóa thành **28 đặc trưng point-in-time chất lượng cao**:*
> * *Nhịp sinh học & Đồ tươi $\rightarrow$ `days_since_last_basket`, `urgency_ratio`, `days_since_perishable`.*
> * *Sức mua & Độ phủ ngành hàng $\rightarrow$ `spend_30d/90d`, `aov_90d`, `department_breadth_90d`.*
> * *Tiếp thị & Trung thành $\rightarrow$ `coupon_redempt_count_180d`, `store_loyalty_index`, `is_targeted_by_active_campaign`.*
> * *Nhân khẩu học $\rightarrow$ Các biến danh mục được gán nhãn `UNKNOWN` chuẩn hóa.*
>
> *Ở tầng **Chiến Lược Bán Lẻ & CRM**, 5 phát hiện kinh doanh trở thành kim chỉ nam cho vận hành:*
> * *Phân khúc CLV chăm sóc khách VIP Top 20%.*
> * *Cân đối ngân sách chiết khấu niêm yết trên kệ.*
> * *Mở rộng danh mục sản phẩm Nhãn hàng riêng.*
> * *Tối ưu ca trực thu ngân và lịch gửi thông báo kích cầu cuối tuần.*
>
> *Đặc biệt, **100% đặc trưng học máy đều được tính toán nghiêm ngặt tại thời điểm $DAY \le t_0$**, tuyệt đối không nhìn trước tương lai, triệt tiêu hoàn toàn rủi ro rò rỉ dữ liệu. Đây là bệ phóng vững chắc nhất để chuyển giao sang giai đoạn Huấn luyện mô hình LightGBM Calibrated Classifier.*
>
> *Xin chân thành cảm ơn quý thầy cô và các anh chị đã chú ý lắng nghe. Nhóm chúng tôi rất mong nhận được các câu hỏi và ý kiến đóng góp ạ!"*

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

### Câu hỏi 5: Tại sao kiểm định Pareto ở Slide 14 lại cho thấy Top 20% chỉ chiếm 53% doanh thu thay vì 80%? Điều đó có ý nghĩa gì đối với bài toán ML?
* **Trả lời:**
  > *"Quy luật Pareto 80/20 là một ước lượng kinh nghiệm ban đầu, nhưng trong ngành bán lẻ thực phẩm thiết yếu, mọi hộ gia đình đều phải ăn uống và sinh hoạt hàng ngày. Mức chi tiêu tối thiểu của một hộ gia đình bình thường không thể quá nhỏ so với hộ khá giả, dẫn đến hệ số bất bình đẳng Gini chỉ ở mức 0.50 (thay vì >0.80 ở các ngành xa xỉ). Cần tới 44% số hộ mới đạt được 80% doanh thu. Về mặt ML, điều này chứng minh bài toán dự đoán xác suất mua hàng là bài toán dự đoán hành vi phổ quát của toàn bộ tập khách hàng, không thể chỉ tập trung vào một nhóm thiểu số cực đoan; và chúng ta bắt buộc phải sử dụng các biến lịch sử gần như `spend_30d/90d` để nắm bắt sự biến động chu kỳ thay vì một nhãn tĩnh CLV."*

---
*Tài liệu được chuẩn hóa và lưu trữ tại `docs/presentation/eda_presentation_script.md`.*
