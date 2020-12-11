import os

from flask import Flask, render_template, request
from google.cloud import bigquery

app = Flask(__name__)
bigquery_client = bigquery.Client()

# リクエストを受け付ける関数
@app.route('/', methods=['GET'])
def diplay():

    #BigQueryにクエリを投げる
    query_job = bigquery_client.query(
        """
        SELECT
            *
        FROM 
            `COVID19.MHLW_JAPAN`
        ORDER BY 
            DATE
        """
    )

    # クエリの実行結果をデータフレームに取得する
    df = query_job.to_dataframe()

    labels = df["date"]
    datas = [df["pcr_positive_daily"], df["pcr_tested_daily"], df["cases_total"], df["death_total"]]
    
    return render_template('chart.html', datas=datas, labels=labels)


if __name__ == '__main__':
    #ローカル実行時はCloud Shell推奨の8080ポートを使用する
    app.run(host='0.0.0.0', port=8080)