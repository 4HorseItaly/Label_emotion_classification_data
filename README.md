# ICTU Sentiment Analysis

Dự án phân tích cảm xúc bình luận Facebook của ICTU sử dụng Label Studio và Python.

## Cấu trúc dự án
```
├── crawldata.py          # Thu thập dữ liệu từ Facebook
├── itcu_post_comments.csv      # Danh sách dữ liệu lưu vào file csv
├── nlp.py                # Tiền xử lý dữ liệu và tạo tệp TSV
├── data_for_labeling.py          # Tạo file TSV cho Label Studio
├── json_label_studio.py  # Xử lý dữ liệu sau khi gán nhãn
└── data_for_labeling.tsv # Dữ liệu đã thu thập
```

## Yêu cầu
- Python 3.8+
- Label Studio
- Các thư viện Python
- pip install label-studio
- Cài đặt pandas, Numby, selenium, Visual Studio Development C/C++

## Cài đặt
```bash
pip install -r requirements.txt
label-studio start
```

## Quy trình sử dụng

1. Thu thập dữ liệu:
```bash
python crawldata.py
```

2. Tiền xử lý và tạo TSV:
```bash
python nlp.py
```

3. Gán nhãn với Label Studio:
- python label-studio start
- Truy cập http://localhost:8080
- Tạo project mới
- Upload data_for_labeling.tsv
- Gán nhãn thủ công

4. Xử lý dữ liệu đã gán nhãn:
```bash
python json_label_studio.py
```

## Kết quả
- File JSON và CSV chứa dữ liệu đã gán nhãn
- 3 nhãn: Tích cực, Tiêu cực, Trung tính
