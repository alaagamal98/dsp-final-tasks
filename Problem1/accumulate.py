import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

def Accumulate(data):
    countries=list(data['country'])
    countries = list(dict.fromkeys(countries))
    newdata= data
    for i in range(len(countries)):
        j=1
        countryData= data[data.values==countries[i]]
        oldrow=countryData.iloc[0]
        newdata=Insert_row(oldrow.name,newdata,oldrow)
        while(j!=len(countryData)):
            row= countryData.iloc[j]
            row['cases']=row['cases']+oldrow['cases']
            row['deaths']=row['deaths']+oldrow['deaths']
            row['recovered']=row['recovered']+oldrow['recovered']
            newdata=Insert_row(row.name,newdata,row)
            oldrow=row
            j=j+1
            print(j)
        print("---------------------------------------------------------")
        print(i)
        print("---------------------------------------------------------")

    return newdata
    
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

    data = pd.read_excel('Database/PreProcessedCOVID-19.xlsx', sheet_name='Sheet1')
    data['date']=data['date'].dt.strftime('%Y-%m-%d')
    data = Accumulate(data)
    data.to_excel(r'Database/PreProcessedCOVID-19(Accumulated).xlsx', sheet_name='Sheet1', index = False)

if __name__ == "__main__":
    main()