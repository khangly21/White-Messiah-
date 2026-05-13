# chứa các hàm có chức năng xử lý text

def chunk_text(text,max_chars=1500):
    return [text[i:i+max_chars] for i in range(0,len(text),max_chars)]

def summarize_long_text(text,summarize_func,max_len=200,min_len=50):
    chunks = chunk_text(text)
    summaries = [summarize_func(chunk, max_len, min_len) for chunk in chunks]
    return summarize_func(" ".join(summaries), max_len, min_len)

