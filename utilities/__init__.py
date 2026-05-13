from .summarizer import summarize_text
from .text_utils import summarize_long_text, chunk_text
from .pdf_utils import summarize_pdf

#thì các file summarizer.py, text_utils.py, pdf_utils.py chính là module trong package utilities.
#thì app.py sẽ là from utilities import summarize_text, summarize_long_text, extract_pdf_text