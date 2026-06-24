# Exit Ticket

## Câu 1: Case nào nên dùng multi-agent? Vì sao?

**Nên dùng multi-agent khi task có thể tách thành các bước độc lập với nhau, mỗi bước cần trách nhiệm riêng và cần được kiểm tra độc lập.**

Các case cụ thể:

- **Research pipeline phức tạp**: Tìm kiếm nguồn → phân tích → viết → review là 4 bước có thể tách rõ. Nếu một bước fail, ta biết ngay chỗ nào sai mà không cần debug toàn bộ.
- **Task cần peer review hoặc fact-checking**: Có một agent viết, một agent kiểm tra citation coverage. Nếu để một agent tự làm và tự review, nó dễ bỏ qua lỗi của chính nó.
- **Task cần traceability để audit**: Trong bài lab này, mỗi agent để lại artifact riêng (`research_notes`, `analysis_notes`, `final_answer`, `critic_notes`). Reviewer biết ai làm gì ở bước nào.
- **Task dài có nhiều failure mode khác nhau**: Tách agent giúp retry đúng bước bị lỗi thay vì chạy lại từ đầu.

**Tóm lại**: Multi-agent có giá trị khi **inspectability**, **role separation**, và **failure isolation** quan trọng hơn chi phí phối hợp.

---

## Câu 2: Case nào không nên dùng multi-agent? Vì sao?

**Không nên dùng multi-agent khi task đủ đơn giản để một agent xử lý trong một lượt, hoặc khi overhead phối hợp lớn hơn lợi ích.**

Các case cụ thể:

- **Câu hỏi đơn giản, câu trả lời ngắn**: "Thủ đô của Pháp là gì?" — thêm Supervisor + Researcher + Analyst chỉ tốn thêm latency và token mà không cải thiện gì.
- **Task không có bước tách biệt tự nhiên**: Nếu toàn bộ logic phải chạy tuần tự và không thể tách ra, thêm agent chỉ thêm state trung gian vô nghĩa.
- **Prototype nhanh hoặc MVP**: Khi chưa rõ requirements, multi-agent làm kiến trúc phức tạp sớm hơn cần thiết. Single-agent baseline chạy được trước, rồi mới tách nếu cần.
- **Latency quan trọng hơn chất lượng**: Mỗi agent handoff thêm một lần serialize/deserialize state và xử lý. Nếu cần response dưới 1 giây, single-agent gọn hơn nhiều.
- **Chi phí token / API call là ràng buộc cứng**: Multi-agent chạy nhiều lượt LLM hơn. Với production ở scale lớn, cost tăng tuyến tính theo số agent.

**Tóm lại**: Không cần multi-agent khi task **đơn giản, không cần traceability, và latency/cost là ưu tiên hàng đầu**. Luôn bắt đầu bằng single-agent baseline và chỉ tách khi có lý do cụ thể.
