# chứa các hàm liên quan đến tóm tắt
# Khởi tạo summarizer (ép dùng PyTorch)
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")

def summarize_text(text, max_len=200, min_len=50):
    result = summarizer(
        text,
        max_length=max_len,
        min_length=min_len,
        do_sample=False,
        truncation=True
    )

    return result[0]["summary_text"]