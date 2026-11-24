import random
import time
from pathlib import Path

from llm_app_copy.config import load_settings
from llm_app_copy.llm_client import GeminiLLMClient, LLMError
from llm_app_copy.logging_config import configure_logging
from llm_app_copy.schemas import BatchSummaryResponse


# Cấu hình đường dẫn gốc và đường dẫn song song
INPUT_ROOT = Path(r"D:\Do_An_1\app\26K1_DA1_Class01_Group06\output\vnexpress")
OUTPUT_ROOT = Path(r"D:\Do_An_1\app\26K1_DA1_Class01_Group06\output\vnexpress_summary")

BATCH_SIZE = 5          # Số bài báo (n) nạp vào mỗi lần gọi API (khuyên dùng 3-5)
SLEEP_SECONDS = 13.0    # Nghỉ giữa các request để tránh lỗi 429 (an toàn cho mức 5 RPM)


def collect_and_sync_articles(input_root: Path, output_root: Path) -> list[dict]:
    """
    Quét thư mục gốc, đồng bộ tạo thư mục con bên thư mục song song
    và trả về danh sách các bài báo chưa được tóm tắt.
    """
    output_root.mkdir(parents=True, exist_ok=True)
    pending_articles = []

    for category_dir in sorted(input_root.iterdir()):
        if not category_dir.is_dir():
            continue

        # Tự động tạo thư mục chuyên mục tương ứng ở thư mục song song
        target_category_dir = output_root / category_dir.name
        target_category_dir.mkdir(parents=True, exist_ok=True)

        for news_file in sorted(category_dir.iterdir()):
            if not news_file.is_file():
                continue

            target_file = target_category_dir / news_file.name

            # Bỏ qua nếu file tóm tắt đã tồn tại (hỗ trợ chạy tiếp khi bị ngắt quãng)
            if target_file.exists() and target_file.stat().st_size > 0:
                continue

            content = news_file.read_text(encoding="utf-8").strip()
            if not content:
                continue

            # Dùng đường dẫn tương đối làm ID duy nhất (VD: "the-thao/bai_01.txt")
            article_id = f"{category_dir.name}/{news_file.name}"
            pending_articles.append({
                "id": article_id,
                "content": content,
                "output_path": target_file,
            })

    return pending_articles


def chunk_list(data: list, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]


def main() -> None:
    configure_logging()
    settings = load_settings()
    llm = GeminiLLMClient(settings)

    articles = collect_and_sync_articles(INPUT_ROOT, OUTPUT_ROOT)
    print(f"Tìm thấy {len(articles)} bài báo mới cần tóm tắt.")

    if not articles:
        print("Toàn bộ thư mục đã được đồng bộ tóm tắt đầy đủ!")
        return

    # Trộn ngẫu nhiên các bài khác chuyên mục trước khi gom nhóm n bài
    # Giúp giảm tối đa rủi ro model trộn lẫn thông tin giữa các bài cùng chủ đề
    random.seed(42)
    random.shuffle(articles)

    batches = list(chunk_list(articles, BATCH_SIZE))
    total_batches = len(batches)

    try:
        for batch_idx, batch in enumerate(batches, start=1):
            print(f"\n--- Đang xử lý lô {batch_idx}/{total_batches} ({len(batch)} bài) ---")
            expected_map = {item["id"]: item["output_path"] for item in batch}

            try:
                llm_response = llm.generate_summary(batch)
                parsed_response = BatchSummaryResponse.model_validate_json(llm_response.text)

                saved_count = 0
                for res_item in parsed_response.results:
                    out_path = expected_map.get(res_item.article_id)
                    if out_path is None:
                        print(f"[Cảnh báo] ID trả về không khớp đầu vào: {res_item.article_id}")
                        continue

                    clean_summary = res_item.summary.strip()
                    if clean_summary:
                        out_path.write_text(clean_summary, encoding="utf-8")
                        saved_count += 1
                        print(f"  [OK] {res_item.article_id} ({len(clean_summary.split())} từ)")

                # Kiểm tra nếu có bài nào trong lô bị thiếu
                if saved_count < len(batch):
                    missing = set(expected_map.keys()) - {r.article_id for r in parsed_response.results}
                    print(f"  [Thiếu {len(batch) - saved_count} bài]: {missing}")

                print(
                    f"Hoàn thành lô {batch_idx} | Mô hình: {llm_response.model} | "
                    f"Thời gian: {llm_response.latency_ms / 1000:.2f}s | "
                    f"Token: {llm_response.usage.total_tokens}"
                )

            except (ValueError, LLMError, Exception) as error:
                print(f"[Lỗi lô {batch_idx}]: {error}")

            # Nghỉ giữa các lô để tuân thủ giới hạn RPM của gói Free
            if batch_idx < total_batches:
                time.sleep(SLEEP_SECONDS)

    finally:
        llm.close()


if __name__ == "__main__":
    main()