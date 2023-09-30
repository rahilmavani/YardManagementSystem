import streamlit as st
import pandas as pd
import base64
from io import BytesIO
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import datetime as dt

# Functions and classes for Location ALgorithm
################################################################################################
class container:
    def __init__(self, size, status, id = None,in_date=None, in_time=None, out_date_time=None):
        self.size = size
        self.status = status
        self.out_date_time = out_date_time
        self.id = id
        self.in_date = in_date
        self.in_time = in_time
    
    def get_size(self):
        return self.size
    def get_status(self):
        return self.status
    def get_out_date_time(self):
        return self.out_date_time
    def set_out_date_time(self, d):
        self.out_date_time = d
    def set_status(self, s):
        self.status = s

yard = {}
area_bifurcation = {'L':[], 'E':[]}
baycode = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5}
rev_baycode = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F"}


size = []
for j in range(60):
    size.append(6*[0])


def addtoYard(incoming_containers_data):
    file = open(incoming_containers_data, "r")
    i = 0
    result = []
    ids = []
    id_wise_data = {}   # id : [[status, size, date time obj] , [], ...]

    for line in file:
        if i == 0:
            i += 1
            continue
        data = line.strip().split(",")
        id = data[0]
        if id not in ids:
            ids.append(id)
            id_wise_data[id] = []
        
        datetime = (data[-1]).split(" ")
        date = datetime[0]
        time = datetime[1]
        date = date.split("-")
        time = time.split(":")
        id_wise_data[id].append([data[5], data[4], (dt.datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]), hour=int(time[0]), minute=int(time[1]), second=(int)(time[2][:2]) )) ])
        
    not_added = []
    for id in id_wise_data:
        _containers = id_wise_data[id]
        containers = sorted(_containers, key=lambda x: x[2], reverse=True) 
        for container in containers:
            if container[0] == '':
                continue
            added = False
            #Finding optimal loc in yard
            for area in ['A', 'B', 'C', 'F', 'G', 'H', 'J', 'K', 'M', 'D', 'E', 'L']:
                
                if ( (area in area_bifurcation[(container[0])]) or (area not in area_bifurcation['E'] and area not in area_bifurcation['L'])):
                    for i in range(5):
                        for j in range(60):
                            for k in range(9):
                                try:
                                    if (yard[area][i][j][k].get_status() == "Empty"):
                                        if (((i == 0) or (yard[area][i-1][j][k].getstatus() != "Empty")) and 
                                            ((i == 0) or (yard[area][i][j][k].get_out_date_time() == None) or (yard[area][i][j][k].get_out_date_time() >= yard[area][i-1][j][k].get_out_date_time())) and
                                            ((i == 0) or (yard[area][i-1][j][k].getsize() == container[1]))):
                                            if area not in area_bifurcation[container[0]]:
                                                area_bifurcation[container[0]].append(area)
                                            yard[area][i][j][k].set_status("GROUNDED\n")
                                            yard[area][i][j][k].set_out_date_time(container[2])
                                            result.append([id, container[0], container[1], f"{area}{j+1:02}{rev_baycode[k+1]}{i+1}"])
                                            added = True
                                            break
                                except:
                                    pass
                            if added:
                                break
                        if added:
                            break
                if added:
                    break
             
            if not added:
                not_added.append(container)
    

    return result

# Machine LEarning Algorithm
#################################################################################################


data = pd.read_csv("D:\HackOut'23\Streamlit\pages\piocd.csv")

# Preprocessing
data['IN_TIME'] = pd.to_datetime(data['IN_TIME'], format='%d-%m-%y %H.%M.%S', errors='coerce')
data['OUT_TIME'] = pd.to_datetime(data['OUT_TIME'], format='%d-%m-%y %H.%M.%S', errors='coerce')
data['TimeElapsed'] = (data['OUT_TIME'] - data['IN_TIME']).dt.total_seconds()

# Drop rows with missing or invalid target values
data = data.dropna(subset=['TimeElapsed'])

# Extract datetime features
data['Year'] = data['IN_TIME'].dt.year
data['Month'] = data['IN_TIME'].dt.month
data['Day'] = data['IN_TIME'].dt.day
data['Hour'] = data['IN_TIME'].dt.hour
data['Minute'] = data['IN_TIME'].dt.minute

# Features and target variable
X = data[['Year', 'Month', 'Day', 'Hour', 'Minute']]
y = data['TimeElapsed']

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating the XGBoost model
model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)

# Training the model
model.fit(X_train, y_train)


# Streamlit UI and File Handling
#####################################################################################################

# Define your data processing function here
def process_csv(input_data):
    # Replace this with your actual data processing logic
    incoming_data = pd.read_csv(input_data)
    incoming_data['IN_TIME'] = pd.to_datetime(incoming_data['IN_TIME'], format='%d-%m-%y %H.%M.%S', errors='coerce')
    incoming_data['Year'] = incoming_data['IN_TIME'].dt.year
    incoming_data['Month'] = incoming_data['IN_TIME'].dt.month
    incoming_data['Day'] = incoming_data['IN_TIME'].dt.day
    incoming_data['Hour'] = incoming_data['IN_TIME'].dt.hour
    incoming_data['Minute'] = incoming_data['IN_TIME'].dt.minute
    X_incoming = incoming_data[['Year', 'Month', 'Day', 'Hour', 'Minute']]
    return X_incoming, incoming_data
    # Perform operations on df
    

# Streamlit UI
st.set_page_config(page_title="CSV Processing App", layout="wide")
st.title("Process CSV Data to get Results!")



# File Upload
st.subheader("Upload the file of Incoming Containers")
uploaded_file = st.file_uploader("", type=["csv"])
st.subheader("Upload the file of Yard Locations")
uploaded_file2 = st.file_uploader("\t", type=["csv",])

if uploaded_file:
    # Process the uploaded CSV data
    processed_data, incoming_data = process_csv(uploaded_file)

    predicted_elapsed_times = model.predict(processed_data)
    predicted_out_times = incoming_data['IN_TIME'] + pd.to_timedelta(predicted_elapsed_times, unit='s')
    incoming_data['PredictedOutTime'] = predicted_out_times
    incoming_data.to_csv("incoming_containers_with_predictions2.csv", index=False)

    # Display processed data
    st.subheader("Predicted Out Times")
    st.dataframe(incoming_data)

    # Download link for processed CSV
    output_buffer = BytesIO()
    processed_data.to_csv(output_buffer, index=False)
    b64 = base64.b64encode(output_buffer.getvalue()).decode()
    st.markdown(
        f'<a href="data:file/csv;base64,{b64}" download="processed_data.csv">Download Processed CSV</a>',
        unsafe_allow_html=True,
    )


if uploaded_file2:
    
    temp_file_path = "D:\HackOut'23\Streamlit\pages\\temp_uploaded_file.csv"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file2.read())
    
    def popYard(yard_data):
        f = open(yard_data, "r")
        Area = ['A', 'B', 'C', 'F', 'G', 'H', 'J', 'K', 'M', 'D', 'E', 'L']
        empty = []
        for i in range(5):
            tier = []
            for j in range(60):
                row = []
                for k in range(6):
                    row.append(0)
                tier.append(row)
            empty.append(tier)

        for area in Area:
            yard[area] = empty

        
        i = 0
        for line in f:
            if i == 0:
                i+=1
                continue

            data = line.split(",")
            size = int(data[0])
            area = data[2]
            row = int(data[3])-1
            bay = baycode[data[4]]-1
            level = int(data[5])-1
            status = data[6]
            if data[6] == '\n':
                status = "Empty"
            yard[area][level][row][bay] = container(size, status)
    
    
    popYard(temp_file_path)
    

    result = addtoYard("D:\HackOut'23\Streamlit\incoming_containers_with_predictions2.csv")
    #print(len(result))
    st.subheader("Allocated Locations")
    st.dataframe(result)

    result_file = open("result.csv","w")

    result_file.writelines("ID,IMPORT_EXPORT,CON_SIZE,Assigned_Locations\n")
    for r in result:
        result_file.writelines(f"{r[0]},{r[1]},{r[2]},{r[3]}\n")

    result_file_path = "D:\HackOut'23\Streamlit\incoming_containers_with_predictions2.csv"


###############################################################

    st.markdown(
        f'<a href="data:file/csv;base64,{result_file_path}" download="Allocated_Locations.csv">Download Allocated Locations CSV</a>',
        unsafe_allow_html=True,
    )