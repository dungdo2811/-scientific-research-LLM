# Nghiên cứu và thử nghiệm một số kỹ thuật mở rộng khả năng của mô hình ngôn ngữ lớn (LLM)

## 📖 Giới thiệu
Dự án này tập trung nghiên cứu, thử nghiệm và hệ thống hóa các kiến thức về Mô hình Ngôn ngữ Lớn (Large Language Model - LLM). Điểm nhấn của dự án là việc đi sâu vào hai kỹ thuật quan trọng nhất hiện nay giúp khắc phục hạn chế của LLM: **Function Calling** (gọi hàm/tương tác với công cụ bên ngoài) và **RAG - Retrieval-Augmented Generation** (thêm dữ liệu bên ngoài để sinh văn bản). Từ các nghiên cứu lý thuyết, dự án xây dựng một ứng dụng thực tế kết hợp cả hai kỹ thuật này.

## 🎯 Mục tiêu đề tài
- **Nghiên cứu LLM:** Tìm hiểu các khái niệm cơ bản, khả năng và hạn chế của LLM trong xử lý và sinh văn bản.
- **Làm chủ Function Calling:** Tìm hiểu nguyên lý hoạt động và cách sử dụng Function Calling để kết nối LLM với các công cụ, API và chức năng bên ngoài.
- **Làm chủ RAG:** Tìm hiểu nguyên lý hoạt động của RAG, quy trình xử lý dữ liệu (thu thập tài liệu, chia nhỏ - chunking, tạo embedding, lưu trữ và truy xuất vector).
- **Phát triển ứng dụng:** Xây dựng thành công ứng dụng thực tế tích hợp cả Function Calling và RAG.

## 📚 Nội dung nghiên cứu và Sản phẩm đạt được
Đề tài được thực hiện bởi toàn bộ nhóm với các hạng mục công việc và sản phẩm cụ thể như sau:

| STT | Nội dung nghiên cứu | Sản phẩm đạt được |
|:---:|:---|:---|
| 1 | Tìm hiểu tổng quan về LLM, khả năng và hạn chế. | Báo cáo tổng quan về LLM. |
| 2 | Tìm hiểu cơ chế Function Calling và cách LLM tương tác với các hàm/chức năng bên ngoài. | Báo cáo về Function Calling; Chương trình minh họa (Demo). |
| 3 | Tìm hiểu nguyên lý RAG. | Báo cáo về RAG; Ứng dụng Demo RAG. |
| 4 | Tìm hiểu khả năng kết hợp RAG và Function Calling trong một ứng dụng. | Báo cáo về khả năng kết hợp Function Calling & RAG; Ứng dụng Demo. |
| 5 | Phát triển ứng dụng tổng hợp sử dụng RAG và Function calling. | **Báo cáo tổng kết và Ứng dụng hoàn chỉnh.** |

## 🏆 Kết quả của dự án
1. **Về mặt lý thuyết:**
   - Hệ thống hóa thành công các khái niệm cơ bản về LLM và tiềm năng ứng dụng trong các hệ thống thông minh.
   - Làm rõ nguyên lý, quy trình hoạt động của Function Calling khi kết nối LLM với các API bên ngoài.
   - Làm rõ quy trình xây dựng hệ thống RAG tiêu chuẩn từ A-Z (Thu thập tài liệu ➡️ Chia nhỏ văn bản ➡️️ Tạo Embedding ➡️ Lưu trữ Vector Database ➡️ Truy xuất và Sinh văn bản).
2. **Về mặt thực tiễn:** 
   - Triển khai thành công ứng dụng AI thông minh có khả năng tự động tra cứu dữ liệu tri thức nội bộ (thông qua RAG) và thực hiện các tác vụ/lấy dữ liệu thời gian thực (thông qua Function Calling).

## 🚀 Hướng dẫn cài đặt và Sử dụng
*(Lưu ý: Thay đổi phần này cho phù hợp với stack công nghệ bạn đang dùng như Python, LangChain, LlamaIndex, OpenAI, v.v.)*

### 1. Yêu cầu hệ thống
- Python 3.9+
- Các thư viện cần thiết (xem trong `requirements.txt`)
- API Key của nhà cung cấp LLM (OpenAI, Gemini, Anthropic...)

### 2. Cài đặt
Clone kho lưu trữ về máy:
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
