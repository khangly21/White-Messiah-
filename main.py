# 📊 Điểm chính
    # st.text_area: cho phép paste văn bản dài, nhiều dòng.
    # Chunking: chia nhỏ text để tránh vượt giới hạn token.
    # Upload PDF: file được lưu vào thư mục uploads/, sau đó đọc bằng PyPDF2.
    # Summary of summaries: tóm tắt từng chunk, rồi ghép lại để có bản tóm tắt cuối cùng.


import streamlit as st
from utilities import summarize_long_text, summarize_text, summarize_pdf
from pathlib import Path

#Đúng rồi Khang 👍 — phần xử lý đặt tên file duy nhất và check file tồn tại trước khi đọc nên nằm trong main.py, vì đó là nơi bạn nhận file upload từ người dùng và quyết định đường dẫn lưu. Các hàm trong utilities chỉ nên tập trung vào logic xử lý (tóm tắt, chunk, extract text), còn việc quản lý file (tên, lưu, kiểm tra) thì để ở tầng ứng dụng (main.py).
import os
import uuid
def save_uploaded_file(uploaded_file):
    #tạo thư mục uploads trước khi lưu
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    # Tạo tên file duy nhất bằng uuid
    filename = f"{uuid.uuid4()}_{uploaded_file.name}"
    #file_path = os.path.join("uploads", filename) # nếu bạn muốn dùng Path (từ pathlib) thay cho os.path, thì bạn chỉ cần thay đổi cách tạo và lưu file. Path giúp code gọn gàng, dễ đọc hơn.
    file_path= upload_dir / filename
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# ---- giao diện Streamlit -----

st.title("Whitepaper Summarizer")
choice = st.radio("Kindly Choose Your Input Method:", ["Paste Text", "Upload PDF"])

#Người dùng chọn độ dài summary
summary_length= st.slider("Choose the length of the summary (number of tokens): ", 100, 600, 200, step=50)

# Người dùng chọn phong cách summary
style = st.selectbox("Choose summary style:", ["Brief", "Detailed", "Bullet points"])

if choice == "Paste Text":
    user_text = st.text_area("Enter or paste long text:")
    st.info("Tip: the Bee Network Whitepaper")
    if st.button("Summarize Text"):
        if user_text.strip():
            summary = summarize_long_text(user_text, summarize_text, max_len=summary_length, min_len=50)
            st.subheader("Summary:")
            st.balloons()
            if style == "Bullet points":
                st.write("- " + summary.replace(". ", "\n- "))
            else:
                st.write(summary)

elif choice == "Upload PDF":
    # upload_dir = Path("uploads")
    # upload_dir.mkdir(exist_ok=True)

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    st.info("Tip: The Bitcoin Whitepaper")
    st.link_button("🔗 You can find Bitcoin Whitepaper here: https://www.bee.com/sites/71190.html#/", "https://www.bee.com/sites/71190.html#/")

    if uploaded_file is not None:
        #pdf_path = upload_dir / uploaded_file.name
        # with open(pdf_path, "wb") as f:
        #     f.write(uploaded_file.getbuffer())
        # st.success(f"File đã lưu vào: {pdf_path}")
        pdf_path = save_uploaded_file(uploaded_file)
        st.success(f"The file has been saved into: {pdf_path}")

        if st.button("Summarize PDF"):
            if os.path.exists(pdf_path):
                with st.spinner("⏳ The PDF is being summarized ... It takes some minutes "):
                    summary = summarize_pdf(pdf_path, max_len=summary_length, min_len=50) #summary = summarize_pdf(pdf_path, max_len=200, min_len=50)
                st.success("✅ Completed the summary successfully!")
                st.balloons()
                st.subheader("Summary of PDF:")
                if style == "Bullet points":
                    st.write("- " + summary.replace(". ", "\n- "))
                else:
                    st.write(summary)
                # Xóa file sau khi hiển thị summary
                try:
                    os.remove(pdf_path)
                    st.info("📂 The PDF file has been deleted to save space.")
                except Exception as e:
                    st.warning(f"Cannot delete the file: {e}")
            else:
                st.error("The file does not exist or has not been saved.")
            
            
