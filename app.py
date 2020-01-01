from flask import Flask, render_template, request, redirect, url_for,\
send_from_directory, jsonify
import numpy as np
import os
import pandas as pd
import json

# for City1, return 5 simlar cities in each region + all regions
Similar_City_List={}
def Find_N_Similar_City(City, Num, Data_Type, Region, Ex_Same_Region, plot, SimScore):
    # City to compare with
    # Num of similar cities
    # Data_Type: Temp, Precip, or Temp_Precip
    # Region to compare to
    # Ex_Same_Region: exclude region the city is in
    # Plot or not

    #if Data_Type == 'Precip':
    #    SimScore = SimScore_Precip
    #elif Data_Type == 'Temp':
    #    SimScore = SimScore_Temp
    #elif Data_Type == 'Temp_Precip':
    #    SimScore = SimScore_Temp_Precip
    #elif Data_Type == 'Temp_Precip_Ratio':
    #SimScore = SimScore_Temp_Precip_Ratio

    # exclude region the city is in
    if Ex_Same_Region == True:
        Region1 = SimScore['Region'][City]
        if Region1 in Region:
            Region.remove(Region1)

    SimScore2 = SimScore[SimScore['Region'].isin(Region)]
    Similar_City = SimScore2.nsmallest(Num, City).index

    # if similar City include the City, exclude it and add one city
    if Similar_City[0] == City:
        Similar_City = SimScore2.nsmallest(Num + 1, City).index[1:Num + 1]

    Similarity_Score = SimScore2.loc[Similar_City, City]

    if plot == True:
        for i in range(Num):
            Plot_Temp_Precip(City, Similar_City[i])
            plt.show()
            print('Similarity Score = {0:.3f}'.format(Similarity_Score[i]))

    return Similar_City, Similarity_Score

app = Flask(__name__)

try:
    Weather_Data = pd.read_csv(
        'Weather_Data.csv', index_col=0)
    SimScore_Temp = pd.read_csv(
        'Weather_Data_SimScore_Temp.csv', index_col=0)
    SimScore_AveTemp = pd.read_csv(
            'Weather_Data_SimScore_AveTemp.csv', index_col=0)
    SimScore_Precip = pd.read_csv(
            'Weather_Data_SimScore_Precip.csv', index_col=0)

except:
    Weather_Data = pd.read_csv('/home/nyhoustl/mysite/Weather_Data.csv', index_col=0)
    SimScore_Temp = pd.read_csv(
        '/home/nyhoustl/mysite/Weather_Data_SimScore_Temp.csv', index_col=0)
    SimScore_AveTemp = pd.read_csv(
            '/home/nyhoustl/mysite/Weather_Data_SimScore_AveTemp.csv', index_col=0)
    SimScore_Precip = pd.read_csv(
                '/home/nyhoustl/mysite/Weather_Data_SimScore_Precip.csv', index_col=0)

data0 = {
    'City1': [], 'Temp1': [], 'Precip1': [],
    'City2': [], 'Temp2': [], 'Precip2': [],
    'Cities_Japan': list(Weather_Data[Weather_Data
                    ['Region']=='Japan']['City']),
    'Cities_NAmerica': list(Weather_Data[Weather_Data[
                    'Region']=='North America']['City']),
    'Cities_SAmerica': list(Weather_Data[Weather_Data
                    ['Region']=='South America']['City']),
    'Cities_Europe': list(Weather_Data[Weather_Data
                    ['Region']=='Europe']['City']),
    'Cities_Asia': list(Weather_Data[Weather_Data
                    ['Region']=='Asia']['City']),
    'Cities_Oceania': list(Weather_Data[Weather_Data
                    ['Region']=='Oceania']['City']),
    'Cities_Africa': list(Weather_Data[Weather_Data
                    ['Region']=='Africa']['City'])}

@app.route('/')
def index():
	return render_template('index.html', data=data0, title = '気候の比較')

@app.route('/index_en')
def index_en():
	return render_template('index_en.html', data=data0, title = 'Climate Comparison')

@app.route('/instruction')
def instruction():
	return render_template('instruction.html', title = '使い方')

@app.route('/instruction_en')
def instruction_en():
	return render_template('instruction_en.html', title = 'Instruction')

@app.route('/script')
def script():
	return render_template('script.html', title = 'スクリプト')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

@app.route('/receive', methods=['POST', 'GET'])
def receive():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)

        City1 = data['city1']
        KoeppenC1 = Weather_Data.loc[City1, 'KC']
        Country1 = Weather_Data.loc[City1, 'Country']

        try:
            Temp1 = Weather_Data.loc[City1,'AveTemp01':'AveTemp12'].values
            Temp1 = np.append(Temp1, Temp1[0])
            if np.isnan(Temp1[0]) == True:
                Temp1 = []

            Temp1_High = Weather_Data.loc[City1,'AveHighTemp01':'AveHighTemp12'].values
            Temp1_High = np.append(Temp1_High, Temp1_High[0])
            if np.isnan(Temp1_High[0]) == True:
                Temp1_High = []

            Temp1_Low = Weather_Data.loc[City1,'AveLowTemp01':'AveLowTemp12'].values
            Temp1_Low = np.append(Temp1_Low, Temp1_Low[0])
            if np.isnan(Temp1_Low[0]) == True:
                Temp1_Low = []
        except:
            Temp1 = []
            Temp1_High = []
            Temp1_Low = []

        # in case city1 is not provided or city2 Precip data are not avilable
        try:
            Precip1 = Weather_Data.loc[City1,'AvePrecip01':'AvePrecip12'].values
            Precip1 = np.append(Precip1, Precip1[0])
            if np.isnan(Precip1[0]) == True:
                            Precip1 = []
        except:
            Precip1 = []

        # in case city2 is not provided or city2 Temp data are not avilable
        try:
            City2 = data['city2']
            Temp2 = Weather_Data.loc[City2,'AveTemp01':'AveTemp12'].values
            Temp2 = np.append(Temp2, Temp2[0])
            if np.isnan(Temp2[0]) == True:
                Temp2 = []

            Temp2_High = Weather_Data.loc[City2,'AveHighTemp01':'AveHighTemp12'].values
            Temp2_High = np.append(Temp2_High, Temp2_High[0])
            if np.isnan(Temp2_High[0]) == True:
                Temp2_High = []

            Temp2_Low = Weather_Data.loc[City2,'AveLowTemp01':'AveLowTemp12'].values
            Temp2_Low = np.append(Temp2_Low, Temp2_Low[0])
            if np.isnan(Temp2_Low[0]) == True:
                Temp2_Low = []
        except:
            Temp2 = []
            Temp2_High = []
            Temp2_Low = []

        # in case city2 is not provided or city2 Precip data are not avilable
        try:
            City2 = data['city2']
            Precip2 = Weather_Data.loc[City2,'AvePrecip01':'AvePrecip12'].values
            Precip2 = np.append(Precip2, Precip2[0])
            if np.isnan(Precip2[0]) == True:
                            Precip2 = []
        except:
            Precip2 = []

        Temp_Precip_Ratio = float(data['temp_precip_ratio'])

        # SimScore, depending on availabe data
        if Temp1_High == [] and Temp1 == [] and Precip1 != []: # Precip only (no Temp)
            Temp_Precip_Ratio = 0
            SimScore_Temp_Precip_Ratio = SimScore_Precip.iloc[0:SimScore_Temp.shape[0], 0:SimScore_Temp.shape[0]]
        elif Temp1_High == [] and Temp1 != [] and Precip1 != []: # aveTemp and Precip
            SimScore_Temp_Precip_Ratio = (
            SimScore_AveTemp.iloc[0:SimScore_AveTemp.shape[0], 0:SimScore_AveTemp.shape[0]]
            * Temp_Precip_Ratio/100
            + SimScore_Precip.iloc[0:SimScore_Temp.shape[0], 0:SimScore_Temp.shape[0]]
            * (1 - Temp_Precip_Ratio/100))
        elif Temp1_High == [] and Temp1 != [] and Precip1 == []: # aveTemp only (no Precip)
            Temp_Precip_Ratio = 100
            SimScore_Temp_Precip_Ratio = SimScore_AveTemp.iloc[0:SimScore_AveTemp.shape[0], 0:SimScore_AveTemp.shape[0]]
        elif Temp1_High != [] and Precip1 == []: # aveTemp and high/lowTemp only (no Precip)
            Temp_Precip_Ratio = 100
            SimScore_Temp_Precip_Ratio = SimScore_Temp.iloc[0:SimScore_Temp.shape[0], 0:SimScore_Temp.shape[0]]
        else: # aveTemp, high/low Temp, Precip (all available)
            SimScore_Temp_Precip_Ratio = (
            SimScore_Temp.iloc[0:SimScore_Temp.shape[0], 0:SimScore_Temp.shape[0]]
            * Temp_Precip_Ratio/100
            + SimScore_Precip.iloc[0:SimScore_Temp.shape[0], 0:SimScore_Temp.shape[0]]
            * (1 - Temp_Precip_Ratio/100))

        SimScore_Temp_Precip_Ratio = pd.concat([SimScore_Temp_Precip_Ratio,
                                    SimScore_Temp.loc[:,'State':'Region']],
                                    axis=1)

        # SimScore_Temp_Precip_Ratio is based on City1's data availabiity.
        # It my not be availabe for City2
        try:
            SimScore_City1_2 = SimScore_Temp_Precip_Ratio.loc[City1, City2]
            if np.isnan(SimScore_City1_2) == True:
                            SimScore_City1_2 = 'NA'  #not available
        except:
            SimScore_City1_2 = 'NA'  #not available

        Similar_City_List={}
        try:
            #top5 similar cities in each region
            for Region in [['North America'], ['South America'], ['Europe'],
                   ['Japan'], ['Asia'], ['Africa'], ['Oceania']]:
                Similar_City, Similarity_Score = Find_N_Similar_City(City1, 5,
                    Data_Type='Temp_Precip_Ratio', Region=Region,
                    Ex_Same_Region=False, plot=False, SimScore=SimScore_Temp_Precip_Ratio)
                Similar_City_List[Region[0]]= [list(Similar_City),
                                               list(Similarity_Score)]
            #top 5 similar cities in all region (exluding region1)
            Similar_City, Similarity_Score = Find_N_Similar_City(City1, 5,
                Data_Type='Temp_Precip_Ratio',
                Region=['North America', 'South America', 'Europe',
                       'Japan', 'Asia', 'Africa', 'Oceania'],
                Ex_Same_Region=True, plot=False, SimScore=SimScore_Temp_Precip_Ratio)
            Similar_City_List['All'] = [list(Similar_City),
                                           list(Similarity_Score)]
        except:
            Similar_City_List = {'North America': [['','','','',''], [0,0,0,0,0]],
                'South America': [['','','','',''], [0,0,0,0,0]],
                'Europe': [['','','','',''], [0,0,0,0,0]],
                'Japan': [['','','','',''], [0,0,0,0,0]],
                'Asia': [['','','','',''], [0,0,0,0,0]],
                'Africa': [['','','','',''], [0,0,0,0,0]],
                'Oceania': [['','','','',''], [0,0,0,0,0]],
                'All': [['','','','',''], [0,0,0,0,0]]}
        print(type(Precip1))
        print(type(Precip2))
        print(Precip1==Precip2)
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
