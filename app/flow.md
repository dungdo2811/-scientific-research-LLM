flowchart TD
    Start([Bắt đầu]) --> Logging["Thiết lập logging"]
    Logging --> LoadSettings["Đọc và kiểm tra cấu hình"]
    LoadSettings --> CreateClient["Khởi tạo GeminiLLMClient"]
    CreateClient --> NewSession["Tạo SessionState"]
    NewSession --> Input["Nhập lệnh hoặc câu hỏi"]

    Input --> Empty{"Nội dung rỗng?"}
    Empty -->|Có| Warn["Thông báo cần nhập câu hỏi"]
    Warn --> Input

    Empty -->|Không| Command{"Loại nội dung?"}
    Command -->|exit / quit / thoát| End["Kết thúc vòng lặp"]
    Command -->|clear| Clear["Xóa lịch sử và thống kê phiên"]
    Clear --> Input
    Command -->|history| ShowHistory["Hiển thị lịch sử phiên"]
    ShowHistory --> Input
    Command -->|stats| ShowStats["Hiển thị số request và tổng token"]
    ShowStats --> Input

    Command -->|Câu hỏi thông thường| Generate["Gọi llm.generate"]
    Generate --> ValidPrompt{"Prompt hợp lệ và API thành công?"}
    ValidPrompt -->|Không| ShowError["Hiển thị lỗi"]
    ShowError --> Input
    ValidPrompt -->|Có| UpdateSession["Thêm câu hỏi và câu trả lời vào history<br/>Cập nhật request và token"]
    UpdateSession --> PrintAnswer["Hiển thị câu trả lời,<br/>mô hình, thời gian và token"]
    PrintAnswer --> Input

    End --> CloseClient["Đóng Gemini client trong finally"]
    CloseClient --> Stop([Kết thúc])

flowchart LR
    User["Người dùng"] --> CLI["CLI<br/>llm_app/app.py"]

    CLI --> Config["Cấu hình<br/>llm_app/config.py"]
    Env[".env / biến môi trường<br/>GEMINI_API_KEY, GEMINI_MODEL"] --> Config
    Config --> Settings["Settings"]

    CLI --> Session["Trạng thái phiên<br/>SessionState"]
    Session --> History["Lịch sử hiển thị trong phiên"]
    Session --> Stats["Số request và tổng token"]

    CLI --> Client["GeminiLLMClient<br/>llm_app/llm_client.py"]
    Settings --> Client
    Client --> Gemini["Gemini API"]
    Gemini --> Client
    Client --> Response["LLMResponse<br/>text, model, latency, usage, request_id"]
    Response --> CLI
    CLI --> User

sequenceDiagram
    actor User as Người dùng
    participant CLI as CLI app.py
    participant State as SessionState
    participant Client as GeminiLLMClient
    participant API as Gemini API

    User->>CLI: Nhập câu hỏi
    CLI->>Client: generate(prompt)
    Client->>Client: Loại bỏ khoảng trắng
    Client->>Client: Tạo request_id và bắt đầu đo thời gian
    Client->>API: generate_content(prompt, model, system_instruction)
    API-->>Client: Nội dung trả lời và usage metadata

    alt API lỗi
        Client-->>CLI: Ném LLMError kèm request_id
        CLI-->>User: Hiển thị thông báo lỗi
    else Không có nội dung text
        Client-->>CLI: Ném LLMError kèm request_id
        CLI-->>User: Hiển thị thông báo lỗi
    else Có câu trả lời
        Client-->>CLI: LLMResponse
        CLI->>State: Thêm lượt hỏi và đáp, cập nhật thống kê
        CLI-->>User: Câu trả lời, thời gian và token
    end
flowchart TD
    Start([Bắt đầu notebook thử nghiệm]) --> Locate["Tìm các file PDF trong thư mục papers"]
    Locate --> Load["Đọc PDF thành tài liệu"]
    Load --> Split["Chia văn bản thành các đoạn<br/>chunk_size 1200, overlap 200"]
    Split --> Inspect["In và kiểm tra các đoạn văn bản"]
    Inspect --> End([Kết thúc thử nghiệm])

    Inspect -. "Chưa có trong luồng này" .-> Embedding["Tạo embedding"]
    Embedding -. "Chưa có trong luồng này" .-> VectorDB["Lưu vector"]
    VectorDB -. "Chưa có trong luồng này" .-> Retrieval["Truy xuất tài liệu theo câu hỏi"]
    Retrieval -. "Chưa tích hợp với chatbot" .-> Answer["Sinh câu trả lời dựa trên tài liệu"]