import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile


def PreProcessData(data):
    countries=list(data['country'])
    countries = list(dict.fromkeys(countries))
    for i in range(len(countries)):
        j=1
        countryData= data[data.values==countries[i]]
        lastDay=countryData.iloc[-1,:]['day']
        lastMonth=countryData.iloc[-1,:]['month']
        if (lastDay!=1 and lastMonth!=1): 
            while (lastMonth!=0):
                while (lastDay!=1):
                    lastDay= lastDay-1
                    newRow= countryData.iloc[-1,:]
                    newRow['day']=lastDay
                    newRow['month']=lastMonth
                    newRow['cases']=0
                    newRow['deaths']=0
                    newRow.name = newRow.name+j     
                    j=j+1
                    data=Insert_row(newRow.name,data,newRow)
                lastMonth=lastMonth-1
                lastDay=29
    return data
    
def PreProcessData2(data):
    countries=list(data['country'])
    countries = list(dict.fromkeys(countries))
    for i in range(len(countries)):
        countryData= data[data.values==countries[i]]
        month=4
        day=29
        j=0
        while(month!=0):
            while (day!=0):
                row= countryData.iloc[j]
                if (row['day']!=day or row['month']!=month):
                    row=countryData.iloc[j-1]
                    row['day']=day
                    row['month']=month
                    row.name =row.name+1
                    data=Insert_row(row.name,data,row)
                    countryData= data[data.values==countries[i]]
                day=day-1
                j=j+1
            month=month-1
            day=29
    return data
    

def Insert_row(row_number, df, row_value): 

    start_upper = 0
    end_upper = row_number 
    start_lower = row_number 
    end_lower = df.shape[0] 
    upper_half = [*range(start_upper, end_upper, 1)] 
    lower_half = [*range(start_lower, end_lower, 1)] 
    lower_half = [x.__add__(1) for x in lower_half] 
    index_ = upper_half + lower_half 
    df.index = index_ 
    df.loc[row_number] = row_value     
    df = df.sort_index() 
    return df 


def main():
    data = pd.read_excel('COVID-19.xlsx', sheet_name='Sheet1')
    data=PreProcessData(data)
    data=PreProcessData2(data)
    data.to_excel(r'PreProcessedCOVID-19.xlsx', sheet_name='Sheet1', index = False)

if __name__ == "__main__":
    main()