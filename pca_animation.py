import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from numpy.testing import assert_almost_equal
from sklearn.decomposition import PCA
import sys
import datetime
import plotly.express as px



#--input setting------------------------------------------------------------------------------------------------
file_name=input('file_name: ')
w=int(input('Window_Size: '))
stime=[0, 0, 0]
stime[0]=int(input('start_time_hour: '))
stime[1]=int(input('start_time_min: '))
stime[2]=int(input('start_time_sec: '))
print("Starting...")

#--reading data from csv----------------------------------------------------------------------------------------
raw_data = pd.read_csv(file_name)
data_en=data_all.drop(columns=['Attack'])
data_en.dropna(inplace=True)

#-caculate PCA--------------------------------------------------------------------------------------------------
# w=20
# stime=[20, 18, 31]
row=data_en.shape[0]

for i in range(row):
    if(i<=row-w):
        
        scaler = StandardScaler()
        z = scaler.fit_transform(data_en[i:i+w])
        
        pca = PCA(n_components=2, random_state=9527)
        L = pca.fit_transform(z)

        pcs = np.array(pca.components_)

        l = pd.DataFrame(L)
        l.columns=['pc1','pc2']
        
        st=datetime.datetime(2000,1,1,stime[0], stime[1], stime[2])+datetime.timedelta(seconds=(i+1)*15)
        et=st+ datetime.timedelta(seconds=15*w)
        
        l['windows']=str(i+1)+"("+str(st.time())+"-"+str(et.time())+")"
    
        if(i==0):
            pc=l
        if(i!=0):
            pc=pc.append(l)

#--drawing animation----------------------------------------------------------------------------------------------
fig=px.scatter(pc, x='pc1', y='pc2', animation_frame='windows', range_x=[-15,15], range_y=[-10,10])

#--output to html file----------------------------------------------------------------------------------------------
fig.write_html(file_name)