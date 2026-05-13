# chứa các hàm có chức năng xử lý PDF
# Là nhóm theo chức năng để dễ mở rộng
import PyPDF2;
#from utilities import summarize_long_text , summarize_text , chunk_text
#để tránh circular import.
from .summarizer import summarize_text
from .text_utils import summarize_long_text, chunk_text

# def summarize_pdf(pdf_path, max_len=200, min_len=50):
#     summaries = []
    
#     with open(pdf_path,'rb') as f:
#         reader = PyPDF2.PdfReader(f)
#         for page in reader.pages:
#             try:
#                 page_text = page.extract_text()
#             except Exception as e:
#                 print(f"Lỗi đọc trang: {e}")
#                 continue
#             if page_text and page_text.strip(): #Kiểm tra page_text trước khi chunk
#                 #Chunk từng trang
#                 chunks = chunk_text(page_text, max_chars=1200)
#                 for chunk in chunks:
#                     summaries.append(summarize_text(chunk, max_len, min_len))
#     # Ghép summary của từng trang rồi tóm tắt lại
#     # Chỉ gọi summarize_text nếu có dữ liệu
#     if summaries:
#         return summarize_text(" ".join(summaries), max_len, min_len)
#         #ChatGPT[plus]: Vì " ".join(summaries) có thể vẫn quá dài, vượt giới hạn token của BART/Pegasus → gây: IndexError: index out of range in self
#     else:
#         return "Không có nội dung để tóm tắt."

#chatgptplus


def summarize_pdf(pdf_path, max_len=200, min_len=50):
    summaries = []

    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)

        for page in reader.pages:
            try:
                page_text = page.extract_text()
            except Exception as e:
                print(f"Lỗi đọc trang: {e}")
                continue

            if page_text and page_text.strip():
                chunks = chunk_text(page_text, max_chars=1200)

                for chunk in chunks:
                    if len(chunk.strip()) > 100:
                        summary = summarize_text(
                            chunk,
                            max_len=max_len,
                            min_len=min_len
                        )
                        summaries.append(summary)

    if not summaries:
        return "Không có nội dung để tóm tắt."

    combined_text = " ".join(summaries)

    return summarize_long_text(
        combined_text,
        summarize_text, #trong summarize_text() phải có truncation=True
        max_len=max_len,
        min_len=min_len
    )
    
