# Kịch bản trình bày báo cáo khám phá dữ liệu & kiểm toán chất lượng (EDA & Data Quality)
## Bài toán Dự đoán Xác suất Mua hàng Bán lẻ (14 ngày) & Chiến lược Kinh doanh Chuỗi Siêu thị
### Bộ dữ liệu: Dunnhumby — The Complete Journey (2,500 Hộ gia đình panel, 2.59M Giao dịch, 8 Bảng, 711 Ngày)

---

## Cấu trúc tổng thể bài trình bày (Deck Structure & Narrative Arc)

Bài thuyết trình gồm **23 slide** (1 slide tiêu đề + 21 slide nội dung chuẩn hóa đánh số liên tục 1 đến 21 + 1 slide phụ lục), được tổ chức thành **2 Phần rõ rệt**:

1. **Phần 1: Khám phá dữ liệu cho Bài toán Học máy (Slides 1 – 10 | 7.0 phút):**
   - **Slide 1:** Tiêu đề báo cáo & Định hướng tiếp cận 2 phân hệ (ML Track & Business Track).
   - **Slide 2 (Mục 1):** 1. Kiểm toán chất lượng dữ liệu: Quy trình làm sạch & Khóa liên kết 8 bảng.
   - **Slide 3 (Mục 2):** 2. Kiểm toán chuỗi thời gian: Phân biệt tiến trình mở rộng mẫu và tăng trưởng thực tế.
   - **Slide 4 (Mục 3):** 3. Căn cứ thực nghiệm chọn cửa sổ dự đoán 14 ngày: Cân bằng phân hóa và vận hành.
   - **Slide 5 (Mục 4):** 4. Tương tác độ trễ và tần suất: Phân tách thói quen mua sắm của khách hàng.
   - **Slide 6 (Mục 5):** 5. Nhịp mua đều đặn: Tín hiệu bổ trợ quan trọng trong dự đoán khách quay lại.
   - **Slide 7 (Mục 6):** 6. Mức chi tiêu và độ rộng ngành hàng: Tín hiệu bổ trợ trong từng tầng tần suất.
   - **Slide 8 (Mục 7):** 7. Hàng tươi sống: Chỉ báo chu kỳ tiêu dùng ngắn hạn của hộ gia đình.
   - **Slide 9 (Mục 8):** 8. Tác động của chiến dịch tiếp thị và phiếu giảm giá tại thời điểm dự đoán.
   - **Slide 10 (Mục 9):** 9. Cấu trúc mạng lưới cửa hàng và tính đại diện của nhóm thông tin khuyết thiếu.

2. **Phần 2: Khám phá dữ liệu chuyên sâu cho Chiến lược Bán lẻ (Slides 11 – 22 | 8.0 phút):**
   - **Slide 11 (Mục 10):** 10. Phân khúc khách hàng theo giá trị RFM và ma trận chiến lược giữ chân.
   - **Slide 12 (Mục 11):** 11. Mức độ tập trung doanh thu khách hàng: Đường cong Lorenz và hệ số Gini.
   - **Slide 13 (Mục 12):** 12. Quy mô hộ gia đình và số lượng con nhỏ tác động đến sức mua.
   - **Slide 14 (Mục 13):** 13. Ma trận vai trò ngành hàng: Nhóm thu hút khách hàng và nhóm gia tăng giá trị giỏ.
   - **Slide 15 (Mục 14):** 14. Sức mạnh giỏ hàng đa ngành hàng và tiềm năng tăng trưởng từ bán chéo.
   - **Slide 16 (Mục 15):** 15. Phân tích giỏ mua nhiên liệu: Tách biệt giao dịch đổ xăng khỏi giỏ hàng siêu thị.
   - **Slide 17 (Mục 16):** 16. Cơ hội bán chéo sản phẩm vi mô: Những cặp mặt hàng thường xuyên được mua cùng nhau.
   - **Slide 18 (Mục 17):** 17. Tỷ trọng thâm nhập của nhãn hàng riêng theo từng ngành hàng chủ lực.
   - **Slide 19 (Mục 18):** 18. Phân bổ ngân sách chiết khấu: Giảm giá niêm yết tại quầy và phiếu giảm giá gửi riêng.
   - **Slide 20 (Mục 19):** 19. Cấu trúc chiết khấu niêm yết: Tỷ lệ giảm giá tập trung sâu ở các ngành thịt và thủy sản.
   - **Slide 21 (Mục 20):** 20. Tác động của phiếu giảm giá trong cùng hộ gia đình: Xu hướng kích thích giỏ hàng lớn.
   - **Slide 22 (Mục 21):** 21. Nhịp điệu mua sắm theo thời gian và giải pháp tối ưu hóa vận hành thu ngân.

3. **Phụ lục & Q&A Defense (Slide 23 + 5 Câu hỏi phản biện):**
   - **Slide 23 (Phụ lục):** Phụ lục: Phân phối giá trị giỏ hàng thực tế và kỹ thuật biến đổi dữ liệu.
   - **Phần Q&A:** 5 câu hỏi tình huống chuyên sâu về rò rỉ dữ liệu, xử lý `UNKNOWN`, phân tầng Spend/Breadth, giải cứu khách hàng At-Risk, và quy luật Pareto bán lẻ FMCG.

---

## Kịch bản chi tiết từng slide (Slide-by-Slide Script)

### Slide 1: Tiêu đề báo cáo
* **Tiêu đề:** Khám phá dữ liệu (EDA) & kiểm toán chất lượng dữ liệu
* **Phụ đề:** Phân tích thực nghiệm đa chiều cho Bài toán Dự đoán Mua hàng & Chiến lược Bán lẻ
* **Thời lượng:** 30 giây

**Lời thoại trình bày:**
> *"Kính chào quý thầy cô và hội đồng. Hôm nay, nhóm chúng em xin báo cáo kết quả: **Khám phá dữ liệu (EDA) và Kiểm toán chất lượng dữ liệu**, đóng vai trò là nền tảng thực nghiệm khoa học kép: vừa phục vụ trực tiếp cho việc xây dựng **Mô hình học máy dự đoán xác suất mua hàng 14 ngày**, vừa mở rộng thành **Khung phân tích chiến lược bán lẻ chuyên sâu** cho ban điều hành chuỗi siêu thị.
>
> Toàn bộ nghiên cứu được thực hiện trên bộ dữ liệu thực tế Dunnhumby — The Complete Journey gồm 2.500 hộ panel, 2,59 triệu dòng giao dịch trải dài trên 711 ngày quan sát liên tục. Cấu trúc bài báo cáo gồm 2 phần rõ rệt: **Phần 1: Khám phá dữ liệu cho Bài toán Học máy** và **Phần 2: Khám phá dữ liệu chuyên sâu cho Chiến lược Bán lẻ**."*

---

### Slide 2: 1. Kiểm toán chất lượng dữ liệu: Quy trình làm sạch & Khóa liên kết 8 bảng
* **Thời lượng:** 50 giây
* **Trực quan:** Sơ đồ kiến trúc ERD thực tế và bảng phân tích bóc tách làm sạch 8 bảng dữ liệu Dunnhumby.
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Đã loại bỏ 942 hóa đơn lỗi, giữ trọn vẹn 275.542 giỏ hàng và 2.500 hộ gia đình. Dữ liệu chuẩn sạch 100\%, đủ tin cậy để huấn luyện mô hình.

**Lời thoại trình bày:**
> *"Mở đầu ở Mục 1 về Kiểm toán chất lượng dữ liệu, nhìn vào sơ đồ kiến trúc 8 bảng dữ liệu:
> - Nhóm đã thực hiện kiểm toán nghiêm ngặt trên toàn bộ 2,59 triệu dòng giao dịch. Chúng em phát hiện và loại bỏ 942 hóa đơn lỗi (chi tiêu $\le 0$ do khách trả hàng hoặc đổi điểm thưởng). Việc làm sạch này chỉ ảnh hưởng đến đúng 2 nhãn trên 12.500 lượt đánh giá (chỉ chiếm 0,016%), hoàn toàn không gây nhiễu cho mô hình.
> - Sau khi lọc, 275.542 giỏ hàng thương mại hợp lệ và toàn bộ 2.500 hộ gia đình đều được bảo toàn trọn vẹn, không một hộ nào bị loại trừ. Bảng phiếu giảm giá cũng được xử lý sạch hơn 5.000 dòng trùng lặp, đảm bảo độ tin cậy tuyệt đối cho dữ liệu huấn luyện."*

---

### Slide 3: 2. Kiểm toán chuỗi thời gian: Phân biệt tiến trình mở rộng mẫu và tăng trưởng thực tế
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ kết hợp cột và đường thể hiện Số hộ tham gia Panel và Doanh thu qua 102 tuần (`27_panel_onboarding_vs_revenue.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Doanh thu 20 tuần đầu tăng vọt do số hộ tuyển vào tăng từ 390 lên 1.336, không phải siêu thị lớn mạnh. Cần phân tích theo nhóm gia nhập để đánh giá đúng.

**Lời thoại trình bày:**
> *"Bước sang Mục 2 về Kiểm toán chuỗi thời gian 102 tuần:
> - Doanh thu ở 10 tuần đầu chỉ đạt 22 nghìn USD/tuần với 390 hộ mua hàng, nhưng sau đó tăng mạnh lên 69 nghìn USD ở tuần 11–20 và chạm mốc 89 nghìn USD từ tuần 53 trở đi với 1.336 hộ hoạt động.
> - Đây là phát hiện kiểm toán rất quan trọng: sự tăng vọt này là do dự án Dunnhumby liên tục tuyển thêm hộ gia đình vào mẫu khảo sát, chứ không phải do siêu thị kinh doanh tăng trưởng gấp 4 lần.
> - Nếu không kiểm soát số hộ hoạt động, các phân tích xu hướng sẽ bị bẫy ngộ nhận. Do đó, việc đánh giá bắt buộc phải chia theo từng nhóm hộ cùng thời điểm gia nhập (cohort analysis)."*

---

### Slide 4: 3. Căn cứ thực nghiệm chọn cửa sổ dự đoán 14 ngày: Cân bằng phân hóa và vận hành
* **Thời lượng:** 45 giây
* **Trực quan:** Đồ thị tỷ lệ mẫu dương và độ lệch chuẩn của 3 cửa sổ: 7 ngày, 14 ngày và 30 ngày (`01_horizon_selection_curve.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Nhìn 14 ngày đạt tỷ lệ quay lại ổn định 68,3\%, khớp đúng nhịp nhận lương đi chợ 2 tuần/lần. Đây là khoảng thời gian lý tưởng để gửi khuyến mại giữ chân.

**Lời thoại trình bày:**
> *"Tại Mục 3, để lựa chọn cửa sổ dự đoán tối ưu cho bài toán học máy, nhóm đã thử nghiệm thực nghiệm 3 khung thời gian:
> - Cửa sổ 7 ngày có tỷ lệ mua 51%, quá nhạy cảm với các yếu tố ngẫu nhiên như thời tiết hay ngày nghỉ, đồng thời siêu thị không thể in ấn và phát tờ rơi hàng tuần.
> - Cửa sổ 30 ngày có tỷ lệ mua vọt lên 84%, khiến phần lớn khách hàng đều có nhãn dương, làm mất đi tính phân loại của mô hình.
> - Khung thời gian 14 ngày đạt tỷ lệ quay lại 68,3% với độ lệch chuẩn cực thấp (chỉ $\pm 1,04\%$). Khoảng thời gian 2 tuần này vừa khớp đúng chu kỳ nhận lương và đi chợ định kỳ của các hộ gia đình, vừa là nhịp vận hành chuẩn để phòng Marketing thiết kế và gửi chương trình khuyến mãi tiếp theo."*

---

### Slide 5: 4. Tương tác độ trễ và tần suất: Phân tách thói quen mua sắm của khách hàng
* **Thời lượng:** 45 giây
* **Trực quan:** Heatmap 2D phân tách xác suất mua theo tương tác giữa Recency và Frequency (`10_recency_frequency_heatmap.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Khách đi chợ $\ge 16$ lần dù nghỉ cả tháng vẫn có 77,4\% quay lại; khách ít đi thì vừa ghé hôm qua tỷ lệ cũng dưới 50\%. Cần ưu tiên gọi khách quen về trước.

**Lời thoại trình bày:**
> *"Tại Mục 4, biểu đồ nhiệt 2D thể hiện sự tương tác phi tuyến tính giữa Độ trễ (Recency) và Tần suất (Frequency):
> - Với nhóm khách hàng thân thiết đi chợ từ 16 lần trở lên trong 90 ngày: nếu họ vừa ghé 2–3 ngày trước thì xác suất quay lại lên tới 97%. Thậm chí khi họ trễ nhịp cả tháng (15–30 ngày), họ vẫn có tới 77% khả năng quay lại vì thói quen mua sắm đã hình thành vững chắc.
> - Trái lại, với nhóm khách vãng lai chỉ ghé 1–5 lần: dù vừa bước chân khỏi siêu thị 2 ngày trước, tỷ lệ quay lại cũng chưa tới 47%, và nếu trễ 1 tháng thì tụt dốc còn 31%.
> - Điều này chứng minh quán tính thói quen quan trọng hơn nhiều so với việc khách vừa mới ghé hay không, và siêu thị cần can thiệp chăm sóc khách quen ngay khi họ trễ nhịp quá 1 tuần."*

---

### Slide 6: 5. Nhịp mua đều đặn: Tín hiệu bổ trợ quan trọng trong dự đoán khách quay lại
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ so sánh xác suất quay lại P(Y=1) theo 3 nhóm độ đều đặn nhịp mua (`28_interpurchase_regularity_predictive.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Khách đi chợ đều đặn theo tuần có tỷ lệ quay lại 86,1\%, cao hơn nhóm thất thường 5,6\%. Cần đưa nhịp mua đều đặn vào mô hình để tăng độ chính xác.

**Lời thoại trình bày:**
> *"Mục 5 khám phá một khía cạnh hành vi mới: **Nhịp mua đều đặn (Regularity)**:
> - Tại cùng mốc thời gian kiểm định, khi nhóm cố định những hộ có cùng tần suất lịch sử (40–100 ngày đi chợ) và cùng độ trễ gần nhất trong 14 ngày:
> - Nhóm có nhịp mua đều đặn theo tuần (hệ số biến thiên $CV \le 0,65$) đạt xác suất quay lại lên tới **86,1%**, cao hơn rõ rệt so với mức 80,5% ở nhóm mua sắm ngẫu hứng, thất thường (chênh lệch +5,6%). Cả 3 nhóm đều vượt xa mức Base rate toàn mẫu 68,3%.
> - Hai hộ gia đình có thể cùng đi chợ 50 lần trong năm, nhưng người đi đều đặn mỗi sáng thứ Bảy hàng tuần sẽ có tính cam kết và độ tin cậy dự báo cao hơn nhiều. Đây là một đặc trưng hành vi giàu giá trị để chuyển giao cho mô hình học máy."*

---

### Slide 7: 6. Mức chi tiêu và độ rộng ngành hàng: Tín hiệu bổ trợ trong từng tầng tần suất
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ phân tầng kiểm soát tần suất, phân tích hiệu ứng của Spend và Breadth (`11_stratified_spend_breadth.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Mua rộng nhiều ngành giúp tăng tỷ lệ quay lại từ 64,0\% lên 83,7\%, hiệu quả hơn chỉ tiêu nhiều tiền. Nên khuyến khích khách mua thêm rau củ, đồ gia dụng.

**Lời thoại trình bày:**
> *"Tại Mục 6, nhóm áp dụng phương pháp phân tầng kiểm soát để tách bạch giá trị của Mức chi tiêu (Spend) và Độ rộng ngành hàng (Breadth):
> - Khi giữ cố định số lần đi chợ ở mức trung bình (3–6 chuyến trong 90 ngày): những hộ mua sắm trải rộng trên nhiều quầy (từ thực phẩm tươi, đồ khô đến gia dụng) đạt tỷ lệ quay lại 83,7%, vượt trội so với mức 64,0% ở hộ chỉ mua 1 ngành hàng duy nhất — chênh lệch tới gần 20%.
> - Trong khi đó, việc chi tiêu nhiều tiền chỉ giúp tăng thêm 8,5% tỷ lệ quay lại.
> - Kết quả chứng minh: độ gắn kết đa ngành hàng phản ánh sự tin tưởng và mức độ phụ thuộc vào siêu thị, là chỉ báo giữ chân khách hàng mạnh mẽ hơn nhiều so với chỉ nhìn vào giá trị hóa đơn."*

---

### Slide 8: 7. Hàng tươi sống: Chỉ báo chu kỳ tiêu dùng ngắn hạn của hộ gia đình
* **Thời lượng:** 40 giây
* **Trực quan:** Biểu đồ phân rã xác suất mua theo số ngày kể từ lần cuối mua rau củ hoặc thịt tươi (`05_p_y1_perishable_recency.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Rau thịt chỉ tươi vài ngày: vừa mua 3 hôm trước thì 90,0\% quay lại, nhưng quá 2 tuần giảm còn 37,7\%. Phải dùng đồ tươi làm chuông báo động để gửi ưu đãi ngay.

**Lời thoại trình bày:**
> *"Mục 7 làm rõ vai trò của ngành hàng tươi sống (rau củ quả và thịt cá tươi):
> - Do đặc tính nhanh hỏng chỉ bảo quản được 3–5 ngày, thực phẩm tươi sống đóng vai trò như một 'chiếc đồng hồ sinh học' đo nhịp đi chợ của gia đình.
> - Hộ gia đình vừa mua đồ tươi trong vòng 3 ngày gần nhất có tới 89,7% xác suất sẽ tiếp tục đi chợ trong 14 ngày tới. Nhưng nếu đã quá 2 tuần căn bếp không có đồ tươi từ siêu thị, tỷ lệ quay lại sụt giảm chỉ còn 42,4%.
> - Quá 14 ngày không mua đồ tươi là tín hiệu báo động đỏ cho thấy hộ gia đình đã chuyển sang mua tại chợ truyền thống hoặc siêu thị đối thủ, cần được kích hoạt ưu đãi giữ chân ngay lập tức."*

---

### Slide 9: 8. Tác động của chiến dịch tiếp thị và phiếu giảm giá tại thời điểm dự đoán
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ xác suất mua theo trạng thái chiến dịch active và tỷ lệ chuyển đổi đổi coupon (`12_campaign_coupon_combined.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Được nhận chiến dịch tiếp thị thì 86,8\% khách quay lại, không nhận chỉ còn 59,9\%. Nên ưu tiên phiếu giảm giá toàn giỏ vì hiệu quả gấp đôi giảm một món.

**Lời thoại trình bày:**
> *"Tại Mục 8, chúng em phân tích tác động kích hoạt từ các chương trình khuyến mại tại mốc thời điểm dự đoán $t_0$:
> - Những khách hàng đang có chiến dịch gửi đến nhà có tỷ lệ quay lại đạt 86,8%, cao hơn gần 27% so với nhóm không nhận được tiếp thị (59,9%).
> - Đồng thời, tỷ lệ đổi phiếu giảm giá phụ thuộc rất lớn vào cơ chế: phiếu áp dụng chung cho toàn bộ giỏ hàng (Type A) đạt tỷ lệ chuyển đổi 16,3%, cao gấp đôi so với các phiếu chỉ giảm giá cho một sản phẩm đơn lẻ (Type B và C chỉ đạt 7–8%).
> - Đây là cơ sở thực nghiệm khẳng định biến tiếp thị mang tín hiệu dự báo mạnh mẽ tại mốc $t_0$ mà không hề bị rò rỉ thông tin tương lai."*

---

### Slide 10: 9. Cấu trúc mạng lưới cửa hàng và tính đại diện của nhóm thông tin khuyết thiếu
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ tương quan số cửa hàng ghé thăm và tỷ lệ mua hàng của nhóm `UNKNOWN` (`13_loyalty_demographics_combined.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** 1.699 hộ giấu nhân khẩu học vẫn đi chợ y hệt nhóm khai báo (68,4\% so với 68,2\%). Cứ giữ trọn vẹn họ lại trong mô hình dự đoán mà không sợ sai lệch.

**Lời thoại trình bày:**
> *"Khép lại Phần 1 ở Mục 9 với hai phát hiện cấu trúc nền tảng:
> - Thứ nhất, khách hàng linh hoạt ghé 2–3 cửa hàng khác nhau trong chuỗi đạt tỷ lệ quay lại 79,0%, cao hơn nhóm chỉ trung thành tuyệt đối với 1 cửa hàng duy nhất (63,0%). Họ là những người có phong cách sống năng động và gắn bó với thương hiệu siêu thị trên các cung đường di chuyển hàng ngày.
> - Thứ hai, nhóm 1.699 hộ không khai báo nhân khẩu học (chiếm 68% panel) có tỷ lệ mua hàng thực tế đạt 68,4%, tương đương gần như tuyệt đối với mức 68,2% của nhóm có khai báo đầy đủ. Điều này chứng minh dữ liệu khuyết hoàn toàn ngẫu nhiên về mặt hành vi, việc giữ nguyên 2.500 hộ và gắn nhãn `UNKNOWN` giúp bảo toàn 100% dung lượng mẫu mà không gây sai lệch chọn mẫu."*

---

### Slide 11: 10. Phân khúc khách hàng theo giá trị RFM và ma trận chiến lược giữ chân
* **Thời lượng:** 50 giây
* **Trực quan:** Biểu đồ cột kép so sánh quy mô số hộ và mức đóng góp doanh thu trên 6 phân khúc RFM (`22_rfm_customer_segmentation.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** 541 hộ VIP gánh hơn nửa doanh thu (54,3\%). Riêng 52 hộ sắm lớn đã vắng mặt gần 3 tháng cần được gọi về khẩn cấp kẻo mất 244 nghìn USD.

**Lời thoại trình bày:**
> *"Mở đầu Phần 2 về Chiến lược Bán lẻ ở Mục 10, nhóm phân khúc 2.500 hộ gia đình theo giá trị RFM:
> - **Trụ cột doanh thu — Nhóm VIP (541 hộ, chiếm 21,6% khách hàng):** Đóng góp tới **54,3% tổng doanh thu** toàn chuỗi (4,38 triệu USD), trung bình cứ 2,4 ngày ghé một lần với giỏ hàng gần 40 USD. Đây là tài sản quý giá nhất cần được chăm sóc đặc quyền qua chương trình khách hàng thân thiết.
> - **Cảnh báo khẩn cấp — Nhóm Nguy cơ rời bỏ (At-Risk, 52 hộ):** Từng đóng góp 244 nghìn USD với giỏ hàng rất cao (43,8 USD), nhưng đã vắng mặt trung bình 83 ngày (gần 3 tháng). Với chỉ 52 hộ, chi phí gọi điện hoặc gửi bưu thiếp ưu đãi riêng là rất nhỏ nhưng giúp cứu vãn gần một phần tư triệu USD doanh thu."*

---

### Slide 12: 11. Mức độ tập trung doanh thu khách hàng: Đường cong Lorenz và hệ số Gini
* **Thời lượng:** 45 giây
* **Trực quan:** Đường cong Lorenz thực tế (Gini = 0.5028) so sánh với đường bình đẳng tuyệt đối 45° (`19_clv_pareto_distribution.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Bán đồ ăn không có chuyện 20\% khách nuôi cả chợ, mà cần tới 44\% hộ để gom đủ 80\% doanh thu. Chính sách chăm sóc phải phủ rộng thay vì chỉ nhắm số ít.

**Lời thoại trình bày:**
> *"Tại Mục 11, đường cong Lorenz và hệ số Gini mang lại cái nhìn chân thực về đặc thù ngành hàng tiêu dùng nhanh (FMCG):
> - Khác với ngành hàng xa xỉ hay phần mềm B2B nơi 20% khách tạo ra 80% doanh thu, trong siêu thị thực phẩm, Top 20% khách hàng chỉ tạo ra 53,0% doanh thu.
> - Muốn đạt được 80% doanh thu, siêu thị phải giữ chân được tới 44,0% lượng khách hàng (tương đương 1.100 hộ). Hệ số Gini ở mức 0,5028 phản ánh tính phân hóa vừa phải, bởi nhu cầu ăn uống hàng ngày của con người có giới hạn sinh học tự nhiên.
> - Do đó, ban giám đốc không thể chỉ dồn lực cho nhóm trên cùng, mà bắt buộc phải triển khai chính sách giữ chân và kích cầu trên diện rộng."*

---

### Slide 13: 12. Quy mô hộ gia đình và số lượng con nhỏ tác động đến sức mua
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ so sánh AOV và mức chi tiêu hàng năm theo Quy mô hộ gia đình và Số lượng trẻ em (`26_demographics_family_basket_spend.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Nhà đông người ($\ge 5$ người hoặc $\ge 2$ con) giỏ hàng đạt 42 USD, chi tiêu gấp rưỡi người độc thân. Nên phát triển gói sản phẩm cỡ lớn và combo gia đình.

**Lời thoại trình bày:**
> *"Tại Mục 12, cấu trúc nhân khẩu học cho thấy mối tương quan rõ rệt với sức mua:
> - Hộ gia đình đông người ($\ge 5$ thành viên) chi tiêu trung bình gần 6.700 USD/năm, giá trị giỏ hàng đạt 42 USD, cao hơn 50% so với hộ độc thân (chỉ 28 USD/giỏ).
> - Tương tự, những gia đình có từ 2–3 con nhỏ có nhu cầu tiêu dùng rất lớn về sữa tã, bánh kẹo và thực phẩm đóng gói lớn.
> - Đây là phân khúc khách hàng lý tưởng để siêu thị phát triển các gói sản phẩm cỡ đại (family-size packaging), combo tiết kiệm gia đình và dịch vụ giao hàng tận nhà định kỳ."*

---

### Slide 14: 13. Ma trận vai trò ngành hàng: Nhóm thu hút khách hàng và nhóm gia tăng giá trị giỏ
* **Thời lượng:** 45 giây
* **Trực quan:** Ma trận định vị 2 chiều giữa Doanh thu, Độ phủ giỏ hàng và Giá trị chi tiêu mỗi chuyến (`23_department_performance_matrix.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Tạp hóa khô thu hút khách lớn nhất, chiếm 50,8\% doanh thu và 78,1\% giỏ hàng. Cần bố trí lối đi dẫn khách từ quầy đồ khô sang quầy rau thịt và mỹ phẩm lời cao.

**Lời thoại trình bày:**
> *"Mục 13 định vị vai trò chiến lược của từng ngành hàng trong siêu thị:
> - **Quầy Tạp hóa khô (Grocery):** Đóng vai trò 'nam châm' hút khách hàng chính, xuất hiện ở 78,1% tổng số giỏ hàng và mang lại 50,8% doanh thu (hơn 4,1 triệu USD). Khách đến siêu thị trước hết là để mua gạo, gia vị, dầu ăn và đồ tiêu dùng thiết yếu.
> - **Quầy Hóa mỹ phẩm, Dược phẩm và Đồ tươi:** Đóng vai trò gia tăng giá trị giỏ hàng với giá trị chi tiêu mỗi chuyến rất cao và biên lợi nhuận tốt.
> - Siêu thị cần thiết kế luồng di chuyển thông minh: bố trí hàng tạp hóa khô ở phía trong để khách hàng trên đường đi sẽ tiếp cận quầy thực phẩm tươi sống và mỹ phẩm."*

---

### Slide 15: 14. Sức mạnh giỏ hàng đa ngành hàng và tiềm năng tăng trưởng từ bán chéo
* **Thời lượng:** 45 giây
* **Trực quan:** Đồ thị cột AOV giỏ hàng theo số lượng ngành hàng kèm đường tỷ trọng doanh thu tích lũy (`24_basket_category_breadth_aov.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Giỏ mua $\ge 5$ ngành đạt 84 USD, gấp 7 lần giỏ 1 ngành (12 USD) và đem lại 38,0\% doanh thu. Thúc đẩy bán chéo đa ngành là đòn bẩy tăng trưởng mạnh nhất.

**Lời thoại trình bày:**
> *"Tại Mục 14, đòn bẩy tài chính từ việc mở rộng giỏ hàng đa ngành thể hiện rất ấn tượng:
> - Khách hàng ghé siêu thị chỉ mua 1 ngành hàng thì giá trị giỏ bình quân chỉ đạt 12,22 USD. Nhưng khi khách chọn mua hàng từ 5 ngành hàng trở lên, giá trị giỏ vọt lên 84,12 USD — gấp gần 7 lần.
> - Dù các giỏ hàng từ 5 ngành trở lên chỉ chiếm 12,7% tổng số lượt đi chợ, nhưng lại đóng góp tới 38,0% tổng doanh thu toàn chuỗi.
> - Khuyến khích khách hàng bỏ thêm hàng từ các quầy khác vào giỏ chính là con đường ngắn nhất và hiệu quả nhất để gia tăng doanh số mà không cần tốn chi phí tìm kiếm khách hàng mới."*

---

### Slide 16: 15. Phân tích giỏ mua nhiên liệu: Tách biệt giao dịch đổ xăng khỏi giỏ hàng siêu thị
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ cơ cấu 22.056 giỏ xăng và phân tích so sánh giá trị giỏ hàng khi tách xăng (`29_gas_fuel_basket_distortion.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Gần 96\% giao dịch đổ xăng chỉ mua xăng đơn thuần (24,83 USD), trong khi giỏ thực phẩm 1 ngành chỉ có 8,83 USD. Phải tách riêng xăng để không bóp méo giỏ đi chợ.

**Lời thoại trình bày:**
> *"Sang Mục 15, nhóm đưa ra phát hiện then chốt về trạm xăng KIOSK-GAS:
> - Cần làm rõ: 'Một ngành hàng' hoàn toàn không đồng nghĩa với 'một món đồ'. Trong 22.056 giao dịch có xuất hiện xăng, có tới **95,7% (21.108 giao dịch) là khách chỉ ghé đổ xăng** rồi rời đi ngay.
> - Giá trị trung bình của giỏ chỉ mua xăng là **24,83 USD**. Nếu không tách xăng ra, giá trị thực tế của các giỏ chỉ mua 1 ngành thực phẩm thông thường (vốn chỉ có giá trị **8,83 USD**) sẽ bị thổi phồng lên mức 12,22 USD và làm sai lệch nghiêm trọng đánh giá về tiềm năng bán chéo.
> - Đổ xăng xe và đi chợ thực phẩm là hai mục đích chuyến đi hoàn toàn khác biệt, cần được phân tích thành hai luồng riêng biệt."*

---

### Slide 17: 16. Cơ hội bán chéo sản phẩm vi mô: Những cặp mặt hàng thường xuyên được mua cùng nhau
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ tỷ lệ đính kèm sản phẩm mua kèm và hệ số Lift của các cặp sản phẩm tương hỗ tự nhiên (`30_cross_sell_product_affinity_pairs.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Gần một nửa giỏ có mì khô cũng mua sốt mì (45,8\%, gấp 10,7 lần bình thường); phô mai đi kèm thịt nguội đạt 63,0\%. Nên làm combo và xếp các cặp này cạnh nhau.

**Lời thoại trình bày:**
> *"Tại Mục 16, nhóm đào sâu vào cấp độ vi mô để tìm ra chính xác những cặp mặt hàng thường xuyên được mua cùng nhau:
> - **Mì khô/Pasta $\to$ Sốt mì:** Bình thường sốt mì chỉ có mặt trong 4,3% tổng số giỏ hàng. Nhưng trong những giỏ đã có mì khô, tỷ lệ có thêm sốt mì tăng vọt lên **45,8% (6.423 giỏ)** — tức hệ số gắn kết tự nhiên (Lift) tăng gấp **10,7 lần**.
> - **Phô mai $\to$ Thịt nguội:** Đạt tỷ lệ mua kèm lên tới **63,0% (7.132 giỏ)**, tăng gấp 4,4 lần so với tỷ lệ nền.
> - **Giấy vệ sinh $\to$ Khăn giấy cuộn:** Đạt tỷ lệ mua kèm **27,5% (3.743 giỏ)**, tăng gấp 3,2 lần.
> - Đây là bằng chứng thực nghiệm rõ ràng nhất để đội ngũ bán lẻ trưng bày sản phẩm cạnh nhau hoặc tạo các combo giảm giá mua kèm có căn cứ khoa học."*

---

### Slide 18: 17. Tỷ trọng thâm nhập của nhãn hàng riêng theo từng ngành hàng chủ lực
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ tỷ trọng Doanh thu và Sản lượng tiêu thụ của Nhãn hàng riêng (Private Label) trên 7 ngành hàng (`25_private_label_by_department.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Hàng nhãn riêng chiếm 51,6\% doanh số bánh nhưng quầy thịt mới đạt 5,0\% và mỹ phẩm 9,5\%. Cần mở rộng nhãn riêng sang hai ngành này để tăng lãi thêm 5--12\%.

**Lời thoại trình bày:**
> *"Tại Mục 17, phân tích sản phẩm nhãn hàng riêng (Private Label) mở ra cơ hội tối ưu hóa biên lợi nhuận ròng:
> - Hàng nhãn riêng do chuỗi siêu thị tự đặt hàng sản xuất mang lại biên lợi nhuận cao hơn hàng thương hiệu từ 5% đến 12%.
> - Siêu thị đang làm rất tốt ở quầy bánh mì nướng (chiếm 51,6% doanh thu) và quầy tạp hóa khô (chiếm 27,0% doanh thu và 36,1% sản lượng).
> - Tuy nhiên, tỷ trọng nhãn riêng tại quầy thịt tươi mới chỉ đạt 5,0% và quầy hóa mỹ phẩm chỉ có 9,5%. Đây chính là dư địa tăng trưởng lợi nhuận rất lớn nếu chuỗi siêu thị chủ động mở rộng danh mục nhãn riêng sang các quầy này."*

---

### Slide 19: 18. Phân bổ ngân sách chiết khấu: Giảm giá niêm yết tại quầy và phiếu giảm giá gửi riêng
* **Thời lượng:** 40 giây
* **Trực quan:** Biểu đồ so sánh Quy mô dòng tiền chiết khấu và Tỷ lệ giỏ hàng được áp dụng giữa Markdown và Coupon (`20_markdown_vs_coupon_spend.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Giảm giá dán trên kệ tốn 1,4 triệu USD mà ai cũng hưởng; coupon gửi riêng chỉ tốn 43 nghìn USD nhưng trúng đích. Nên chuyển bớt ngân sách sang tặng coupon đích danh.

**Lời thoại trình bày:**
> *"Mục 18 phân tích bài toán phân bổ ngân sách chiết khấu giữa hai hình thức:
> - Giảm giá niêm yết tại quầy (Markdown) ngốn tới **1,40 triệu USD** và xuất hiện ở 83,7% giỏ hàng. Đây là hình thức cào bằng ai mua cũng được giảm, khiến siêu thị thất thoát biên lợi nhuận trên những khách hàng vốn sẵn sàng trả giá gốc.
> - Ngược lại, phiếu giảm giá (Coupon) gửi riêng từng nhà chỉ tốn **42,6 nghìn USD** (chỉ bằng 1/33 chi phí niêm yết) nhưng kích hoạt đúng nhóm khách hàng nhạy cảm về giá.
> - Ban quản lý siêu thị cần tái cấu trúc lại ngân sách, cắt giảm các khoản giảm giá thụ động tại kệ để chuyển sang phiếu giảm giá gửi đích danh theo từng phân khúc."*

---

### Slide 20: 19. Cấu trúc chiết khấu niêm yết: Tỷ lệ giảm giá tập trung sâu ở các ngành thịt và thủy sản
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ quy mô tiền giảm giá và mức giảm sâu (%) theo từng ngành hàng (`31_markdown_depth_by_department.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Dù tạp hóa tốn nhiều tiền nhất (817K USD), riêng các ngành thịt và hải sản bị giảm sâu nhất (22--25\%, tốn 296K USD). Cần rà soát lại định giá và bảo quản thịt cá.

**Lời thoại trình bày:**
> *"Tại Mục 19, khi mổ xẻ chi tiết khoản ngân sách 1,40 triệu USD giảm giá tại quầy:
> - Quầy Tạp hóa khô chiếm khoản tiền giảm giá lớn nhất với **817 nghìn USD** (58,4%), nhưng tỷ lệ giảm giá trên doanh thu chỉ ở mức 16,6%.
> - Đáng chú ý, điểm nóng về mức giảm giá sâu lại tập trung ở các ngành hàng thịt và thủy sản: Thịt tươi giảm trung bình **24,4%** (177 nghìn USD), Thịt đóng gói giảm **22,5%** (119 nghìn USD), và Hải sản đóng gói giảm sâu nhất tới **25,3%** (21 nghìn USD).
> - Riêng hai ngành thịt đã chiếm tới **21,2% toàn bộ ngân sách giảm giá**. Điều này cảnh báo ban quản lý cần rà soát lại quy trình quản lý hạn sử dụng và chiến lược định giá để tránh phải giảm giá thanh lý quá sâu gây tổn thất biên lợi nhuận."*

---

### Slide 21: 20. Tác động của phiếu giảm giá trong cùng hộ gia đình: Xu hướng kích thích giỏ hàng lớn
* **Thời lượng:** 45 giây
* **Trực quan:** Biểu đồ so sánh giá trị giỏ hàng ghép cặp trong cùng hộ gia đình và tỷ lệ hộ có giỏ coupon lớn hơn (`32_within_household_coupon_basket_lift.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Cùng một hộ, chuyến có coupon đạt 63 USD, gấp đôi chuyến không dùng (31 USD) ở 87,2\% số hộ. Nên đặt điều kiện đơn tối thiểu 50 USD để kích thích mua nhiều.

**Lời thoại trình bày:**
> *"Tại Mục 20, để kiểm chứng tác động thực chất của phiếu giảm giá, nhóm thực hiện phân tích ghép cặp nội bộ trên **1.856 hộ gia đình có cả hai loại chuyến đi**:
> - Kết quả cho thấy: Khi sử dụng coupon, giá trị giỏ hàng trung bình đạt **63,43 USD**, cao hơn gấp đôi so với khi không dùng coupon (**31,09 USD**) — chênh lệch tới +32,34 USD mỗi giỏ.
> - Có tới **87,2% số hộ gia đình (1.618 hộ)** có mức chi tiêu giỏ coupon lớn hơn giỏ thông thường.
> - Điều này phản ánh tâm lý người tiêu dùng: họ chủ động gom hàng và để dành phiếu giảm giá cho các chuyến mua sắm tích trữ lớn cuối tuần. Siêu thị nên tận dụng đặc tính này để thiết kế điều kiện coupon kèm ngưỡng hóa đơn tối thiểu nhằm tối đa hóa quy mô giỏ hàng."*

---

### Slide 22: 21. Nhịp điệu mua sắm theo thời gian và giải pháp tối ưu hóa vận hành thu ngân
* **Thời lượng:** 40 giây
* **Trực quan:** Biểu đồ phân phối ngày trong tuần và biểu đồ phân bổ khung giờ mua sắm trong ngày (`03_temporal_combined_rhythm.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** 63\% khách mua dồn vào 11h--18h và một phần ba rơi vào cuối tuần. Cần tăng nhân viên thu ngân giờ cao điểm và gửi tin nhắn ưu đãi trước 11h trưa đón đầu.

**Lời thoại trình bày:**
> *"Khép lại 21 nội dung ở Mục 21 với phân tích nhịp điệu vận hành theo thời gian:
> - Hai ngày thứ Bảy và Chủ Nhật lượng mua sắm tăng vọt, chiếm tới **33,7% tổng lượt mua** trong cả tuần.
> - Trong ngày, khung giờ từ **11h trưa đến 18h chiều chiếm tới 62,9% tổng giao dịch**, với đỉnh điểm rơi vào 16h–17h chiều.
> - Hai đề xuất vận hành cụ thể cho ban quản lý:
>   1. Tối ưu hóa nhân sự thu ngân và mở tối đa các quầy thanh toán trong khung giờ 11h–18h và hai ngày cuối tuần để giải tỏa ùn tắc.
>   2. Lên lịch tự động gửi tin nhắn thông báo ưu đãi vào khoảng 10h–11h sáng để đón đầu thời điểm các gia đình bắt đầu lên kế hoạch đi chợ."*

---

### Slide 23: Phụ lục: Phân phối giá trị giỏ hàng thực tế và kỹ thuật biến đổi dữ liệu
* **Thời lượng:** 30 giây (Dành cho phần thảo luận kỹ thuật hoặc phản biện)
* **Trực quan:** Biểu đồ phân phối chi tiêu giỏ hàng với đường Median, Mean và phân tích độ lệch (`02_basket_spend_distribution.png`).
* **Câu kết luận chốt trên slide:** $\to$ **Kết luận:** Đa số đi chợ hết 17 USD, nhưng vài giỏ khủng kéo trung bình lên 29 USD. Cần lấy logarit các biến chi tiêu để huấn luyện mô hình chuẩn xác, không bị méo lệch.

**Lời thoại trình bày:**
> *"Tại trang phụ lục kỹ thuật:
> - Giá trị giỏ hàng thực tế có phân phối lệch phải điển hình: giá trị trung vị là 17,18 USD, nhưng giá trị trung bình bị kéo lên tới 29,24 USD bởi các chuyến mua sắm tiệc tùng hoặc gia đình lớn trên 100 USD.
> - Vì vậy trong khâu tiền xử lý dữ liệu cho mô hình học máy, các biến liên quan đến chi tiêu tài chính đều cần được chuyển đổi qua hàm logarit hoặc chuẩn hóa phân vị nhằm kiểm soát các giá trị ngoại lai và tối ưu hóa hàm mất mát của mô hình."*

**Lời thoại trình bày:**
> *"Tại trang phụ lục kỹ thuật:
> - Giá trị giỏ hàng thực tế có phân phối lệch phải điển hình: giá trị trung vị là 17,18 USD, nhưng giá trị trung bình bị kéo lên tới 29,24 USD bởi các chuyến mua sắm tiệc tùng hoặc gia đình lớn trên 100 USD.
> - Vì vậy trong khâu tiền xử lý dữ liệu cho mô hình học máy, các biến liên quan đến chi tiêu tài chính đều cần được chuyển đổi qua hàm logarit hoặc chuẩn hóa phân vị nhằm kiểm soát các giá trị ngoại lai và tối ưu hóa hàm mất mát của mô hình."*

---

## Bộ câu hỏi & trả lời dự phòng cho phần Q&A (Defense Strategy)

### Câu hỏi 1: Tại sao nhóm không loại bỏ 68% số hộ gia đình bị khuyết thông tin nhân khẩu học trong bảng `hh_demographic` để dữ liệu được sạch hoàn toàn?
**Câu trả lời:**
> *"Dạ thưa quý thầy cô, trong khai phá dữ liệu bán lẻ, việc loại bỏ các mẫu khuyết chỉ phù hợp khi dữ liệu khuyết ngẫu nhiên hoàn toàn (MCAR) và tỷ lệ khuyết nhỏ. Ở đây, có tới 1.699 trên 2.500 hộ (68%) không có thông tin nhân khẩu học.
> Nếu loại bỏ 68% số hộ này, chúng ta sẽ phạm phải sai lầm nghiêm trọng về **sai lệch chọn mẫu (Selection Bias)**: mô hình sẽ chỉ học được hành vi của nhóm khách hàng chịu cung cấp thông tin cá nhân.
> Thực nghiệm kiểm tra nhãn của nhóm đã chứng minh: Nhóm không khai báo (`UNKNOWN`) có tỷ lệ phát sinh mua hàng trong 14 ngày là **68,4%**, gần như tương đồng hoàn hảo với mức **68,2%** của nhóm có khai báo. Do đó, giải pháp khoa học chuẩn mực nhất là giữ nguyên toàn bộ 2.500 hộ và mã hóa nhóm khuyết thành một danh mục riêng mang tên `UNKNOWN`. Cách làm này vừa bảo toàn 100% dung lượng mẫu nghiên cứu, vừa cho phép mô hình khai thác giá trị từ chính hành vi không khai báo thông tin."*

### Câu hỏi 2: Có hiện tượng rò rỉ dữ liệu (Data Leakage) khi tính toán các đặc trưng Recency, Frequency và Campaign tại mốc chốt sổ $t_0$ hay không?
**Câu trả lời:**
> *"Dạ hoàn toàn không có rò rỉ dữ liệu. Nhóm chúng em tuân thủ nghiêm ngặt nguyên lý **Point-in-Time Discipline**:
> - Toàn bộ các đặc trưng đầu vào chỉ được phép truy vấn dữ liệu giao dịch và chiến dịch thỏa mãn điều kiện $DAY \le t_0$.
> - Cụ thể: Với đặc trưng chiến dịch tiếp thị, nhóm kiểm tra điều kiện $START\_DAY \le t_0 \le END\_DAY$, nghĩa là tại đúng ngày $t_0$, siêu thị đã biết rõ hộ đó đang có chiến dịch gửi đến nhà hay chưa.
> - Cửa sổ tính toán nhãn mục tiêu là khoảng thời gian tương lai độc lập hoàn toàn: $DAY \in (t_0, t_0 + 14]$.
> - Nhóm đã xây dựng bộ kiểm thử tự động (`test_data_quality.py`) để khẳng định không có bất kỳ bản ghi nào sau $t_0$ bị rò rỉ vào ma trận đặc trưng."*

### Câu hỏi 3: Tại sao nhóm lại khẳng định Spend và Breadth cung cấp tín hiệu bổ trợ độc lập cho Frequency? Nhóm đã chứng minh như thế nào?
**Câu trả lời:**
> *"Dạ thưa quý thầy cô, trong toàn bộ tập dữ liệu, Frequency, Spend và Breadth đều có tương quan dương với nhau. Tuy nhiên, nếu chỉ nhìn tương quan đơn biến thì không thể biết liệu Spend và Breadth có giá trị gia tăng (incremental value) hay chỉ là bản sao của Frequency.
> Để bóc tách, nhóm đã sử dụng phương pháp **phân tầng kiểm soát (Stratified Control)**:
> Cố định nhóm hộ gia đình có cùng mức tần suất đi chợ trung bình (3–6 chuyến trong 90 ngày). Khi số chuyến đi đã được cố định, nhóm phân hóa tiếp theo độ rộng ngành hàng (Breadth). Kết quả cho thấy: Những hộ mua $\ge 11$ ngành hàng đạt xác suất mua **83,7%**, cao hơn rất nhiều so với mức **64,0%** ở hộ chỉ mua 1–4 ngành hàng ($\Delta = +19,7\%$).
> Tương tự, tầng chi tiêu cao đạt **76,8%** so với **68,3%** ở tầng chi tiêu thấp. Điều này chứng minh thực nghiệm rằng: Ngay cả khi hai khách hàng có số lần đi chợ như nhau, người mua sắm đa ngành và chi tiêu lớn vẫn có xác suất quay lại cao hơn hẳn, mang lại tín hiệu dự báo độc lập cho mô hình."*

### Câu hỏi 4: Nhóm At-Risk trong ma trận RFM chỉ có 52 hộ (2.1%), tại sao lại xem đây là trọng tâm cứu vãn kinh doanh khẩn cấp?
**Câu trả lời:**
> *"Dạ thưa thầy cô, tuy về số lượng chỉ có 52 hộ (chiếm 2,1% panel), nhưng về mặt tài chính, nhóm này đóng góp tới **244.000 USD** — chiếm **3,0% tổng doanh thu** của chuỗi siêu thị.
> Đặc điểm của 52 hộ này là: Giá trị giỏ hàng trung bình AOV của họ rất cao (**43,8 USD** — cao hơn cả nhóm VIP thông thường), chứng tỏ đây là những khách hàng gia đình lớn từng chi tiêu rất đậm tại siêu thị. Tuy nhiên, độ trễ hiện tại của họ đã lên tới **83,2 ngày** (gần 3 tháng chưa quay lại).
> Theo lý thuyết giá trị trọn đời (CLV) và giữ chân khách hàng bán lẻ, chi phí để thu hút một khách hàng mới có giá trị tương đương cao gấp 5 đến 7 lần chi phí gửi một voucher giải cứu cá nhân hóa (Win-back campaign). Do quy mô chỉ 52 hộ, chi phí gửi thư hay gọi điện chăm sóc trực tiếp là vô cùng nhỏ, nhưng doanh thu bảo vệ được lên tới gần một phần tư triệu USD."*

### Câu hỏi 5: Tại sao đường cong Lorenz của siêu thị lại cho thấy Top 20% hộ chỉ đóng góp 53.0% doanh thu, trong khi quy luật Pareto kinh điển thường là 80/20?
**Câu trả lời:**
> *"Dạ thưa hội đồng, đây là một phát hiện thực nghiệm rất đặc trưng của ngành bán lẻ hàng tiêu dùng nhanh (FMCG) và siêu thị thực phẩm:
> - Quy luật Pareto kinh điển 80/20 (20% khách tạo 80% doanh thu) thường xuất hiện phổ biến trong ngành thời trang xa xỉ, thương mại điện tử, hoặc dịch vụ B2B, nơi có những khách hàng cá biệt chi tiêu gấp hàng trăm lần người bình thường.
> - Ngược lại, trong siêu thị bán lẻ thực phẩm, hàng hóa chủ yếu là nhu yếu phẩm thiết yếu (gạo, sữa, thịt, rau củ). Một gia đình dù giàu có đến đâu thì nhu cầu ăn uống hàng ngày cũng có giới hạn sinh học tự nhiên, không thể ăn gấp 100 lần hộ khác được.
> - Do đó, mức phân hóa doanh thu trong bán lẻ thực phẩm có xu hướng thoái triển về mức trung bình cao: Top 20% hộ đóng góp **53,0% doanh thu**, và cần **44,0% số hộ** để tích lũy 80% doanh thu. Hệ số Gini đạt **0,5028** phản ánh chính xác cấu trúc kinh tế phân hóa tự nhiên của ngành FMCG."*
