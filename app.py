from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Đọc nội dung file csv
    df = pd.read_csv('./data/check.csv')
    data = df.values
    # Trả về template HTML và truyền nội dung vào để hiển thị
    return render_template('index.html', data = data)

if __name__ == '__main__':
    app.run()