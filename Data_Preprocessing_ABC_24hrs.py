#Dial Plan data preprocessing
#24 hours execution
import pandas as pd
import numpy as np

#Import mapping file - mapping between Test_Case_ID and its details about 'Call of Service' and 'Call type'
mapping_data = pd.read_csv("Test_Case_ID_mapping.csv")

#Import 24 Hours working executions data
data = pd.read_csv("INTLENH_premium_try2_CT_3.csv")
data.rename(columns={'Calling Party': 'Calling_Party', 'Called Party': 'Called_Party'}, inplace=True)
data = data[['Status', 'Calling_Party', 'Called_Party', 'Duration']]

#New dataframe to store combined results - data + mapping_data
data3 = pd.DataFrame(columns=['Status', 'Calling_Party', 'Called_Party', 'Duration', 'Test_Case_ID'])

#Focus on only Failed and Completed executions
status_array = ['Failed', 'Completed']       
data = data.loc[data['Status'].isin(status_array)]


calling_party_series = pd.Series(data['Calling_Party'])
called_party_series = pd.Series(data['Called_Party']) 

#Truncate the text to extract only calling party information
data['Calling_Party']= data.Calling_Party.str.split().str.get(0)

#Call of service codes for 24 hours execution
Call_of_Service = ['InternalOnly', 'Nat24STD', 'Nat24RES'
                   ,'Nat24ENH', 'INTL24STD', 'INTL24ENH'
                   ,'CLIRNat24STD', 'CLIRNat24RES', 'CLIRNat24ENH'
                   , 'CLIRINTL24STD', 'CLIRINTL24ENH']

#Codes available for call type common for all 3 types of executions				   
Call_Type = ['National', 'Service', 'Freephone', 'Emergency'
             , 'International', 'Mobile', 'Premium']

#Define type of execution			 
execution_cycle = '24 Hours Execution'

#Current execution cycle ID
cycle_id = 3

#Mapping logic
for i in range(len(Call_of_Service)):
    data1 = data[data['Calling_Party'] == Call_of_Service[i]]
    #data1 = data[calling_party_series.str.match(Call_of_Service[i])]   
    for j in range(len(Call_Type)):
        data2 = data1[called_party_series.str.contains(Call_Type[j])]
        data2.insert(len(data2.columns), 'Test_Case_ID', pd.Series(np.random.randn(len(data2['Status'])),  index=data2.index))
        for index, row in mapping_data.iterrows():
            if row["Execution_Cycle"] == execution_cycle and row["COS_Code"] == Call_of_Service[i] and row["Call_Type_code"] == Call_Type[j]:
                test_case_id = row["Test_Case_ID"]
                #print(test_case_id)
                data2['Test_Case_ID'] = test_case_id
        data3 = data3.append(data2)

data3.loc[data3['Test_Case_ID'] == 'DP_GERMANY_TC42']

data3.loc[data3['Calling_Party'] == 'INTL24ENH']

data4 = data3.sort_index()
data4['Execution_ID'] = range(1, len(data4) + 1)
data4 = data4.drop(['Calling_Party', 'Called_Party'], axis=1)
data4['Cycle_ID'] = cycle_id
data4 = data4[['Execution_ID', 'Cycle_ID', 'Duration', 'Status', 'Test_Case_ID']]   

#Writing into CSV file 
data4.to_csv('PP_INTLENH_premium_24hrs_try2_CT_3.csv')



