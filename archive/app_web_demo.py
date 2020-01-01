from flask import Flask, render_template, request, redirect, url_for,\
send_from_directory, jsonify
import numpy as np
import pandas as pd
import json

# 処理で使うfuncution
def Find_N_Similar_City(City, Num, Data_Type, Region, Ex_Same_Region, plot, SimScore):
    #省略
    return Similar_City, Similarity_Score

app = Flask(__name__)

# Dataの読み込み
Weather_Data = pd.read_csv('/home/nyhoustl/mysite/Weather_Data.csv', index_col=0)
    # 省略

# 初期データ、都市名リスト
data0 = {
    'City1': [], 'Temp1': [], 'Precip1': [],
    'City2': [], 'Temp2': [], 'Precip2': [],
    'Cities_Japan': list(Weather_Data[Weather_Data
                    ['Region']=='Japan']['City']),
    'Cities_NAmerica': list(Weather_Data[Weather_Data[
                    'Region']=='North America']['City'])}

# インデックスページを読み込む。
@app.route('/')
def index():
	return render_template('index.html', data=data0, title = '気候の比較')

# インストラクションのページを読み込む。
@app.route('/instruction')
def instruction():
	return render_template('instruction.html',
                    title = '使い方')

# データを受信して値を返す。
@app.route('/receive', methods=['POST', 'GET'])
def receive():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)

        City1 = data['city1']
        KoeppenC1 = Weather_Data.loc[City1, 'KC']
        Country1 = Weather_Data.loc[City1, 'Country']
        Temp1 = Weather_Data.loc[City1,'AveTemp01':'AveTemp12'].values
        # 以下データ処理は省略

        return jsonify({'City1': City1,
                        'Temp1': list(Temp1),
                        'Temp1_High': list(Temp1_High),
                        'Temp1_Low': list(Temp1_Low),
                        'Precip1': list(Precip1),
                        'City2': City2,
                        'Temp2': list(Temp2),
                        'Temp2_High': list(Temp2_High),
                        'Temp2_Low': list(Temp2_Low),
                        'Precip2': list(Precip2),
                        'SimScore_City1_2': SimScore_City1_2,
                        'Similar_City_List': Similar_City_List,
                        'Temp_Precip_Ratio': Temp_Precip_Ratio,
                        'KoeppenC1': KoeppenC1,
                        'Country1': Country1})
    else:
        return jsonify({'City1': [], 'Temp1': [], 'Precip1': [],
                        'City2': [], 'Temp2': [], 'Precip2': []})

if __name__ == '__main__':
 app.debug = True
 app.run(host='0.0.0.0', port=8888)
