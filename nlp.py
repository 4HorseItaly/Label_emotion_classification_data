import pandas as pd
import re
from pyvi import ViTokenizer
import os

VIETNAMESE_STOPWORDS = [
    'ạ', 'à', 'á', 'ả', 'ã', 'an', 'anh', 'ba', 'bà', 'bác', 'bạn', 'bé',
    'bị', 'bởi', 'cho', 'chú', 'cô', 'có', 'của', 'cùng', 'cũng', 'chỉ',
    'chứ', 'các', 'con', 'do', 'dạ', 'em', 'gì', 'hay', 'khi', 'không',
    'là', 'mà', 'mình', 'mọi', 'một', 'này', 'nên', 'nếu', 'như', 'nhưng',
    'những', 'nào', 'ơi', 'phải', 'ra', 'rằng', 'rồi', 'sao', 'sẽ', 'thì',
    'tại', 'tôi', 'trên', 'trước', 'từ', 'vào', 'vẫn', 'với', 'vì', 'và',
    'vậy', 'việc', 'ý', 'đã', 'đây', 'đó', 'được', 'để', 'ấy'
]

def preprocess_text(text):
    """
    Hàm tiền xử lý văn bản tiếng Việt.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+|\#\w+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = ViTokenizer.tokenize(text)
    words = text.split()
    filtered_words = [word for word in words if word not in VIETNAMESE_STOPWORDS]
    
    return " ".join(filtered_words)

input_file = 'ictu_post_comments.csv'
output_file = 'data_for_labeling.tsv'

try:
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Không tìm thấy file {input_file}")
        
    df = pd.read_csv(input_file, 
                     encoding='utf-8-sig',
                     on_bad_lines='skip', 
                     escapechar='\\',      
                     quoting=3)         
    print(f"Đọc thành công {len(df)} dòng từ file gốc")
    print("\nThông tin DataFrame:")
    print(df.info())
    print("\nMẫu dữ liệu đầu tiên:")
    print(df.head())
    
    df_for_labeling = pd.DataFrame()
    df_for_labeling['text'] = df['raw_text'].apply(
        lambda x: re.sub(r"http\S+|www\S+|https\S+", '', str(x))
    )
    
    print("Đang xử lý dữ liệu...")
    df_for_labeling = df_for_labeling[df_for_labeling['text'].str.len() > 10]
    df_for_labeling = df_for_labeling.drop_duplicates()
    
    df_for_labeling.to_csv(output_file, sep='\t', index=False, encoding='utf-8-sig')
    print(f"Đã xử lý và lưu {len(df_for_labeling)} mẫu vào {output_file}")

except FileNotFoundError as e:
    print(f"Lỗi: {str(e)}")
except Exception as e:
    print(f"Lỗi không xác định: {str(e)}")
    print("Traceback đầy đủ:")
    import traceback
    print(traceback.format_exc())