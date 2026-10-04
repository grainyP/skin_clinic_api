import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import warnings
warnings.filterwarnings('ignore')

skin_data = pd.read_csv('skin clinic campaign.csv')
skin_data.head()            
   
skin_data.shape

skin_data.dtypes
skin_data['AgeGroup'].unique()
skin_data['Purchase_Last_Quarter'].unique() # check how many 
skin_data['Unique_Products_Purchased'].unique()

 # we can see above that there are 3 unique age ranges in the object AGE GROUP   
 #We can convert the object 'AGE GROUP' into 'int' datatypes using pandas .map(using dictionary)   
skin_data['AgeGroup']= skin_data['AgeGroup'].map({'<30':1 , '30-50':2 , '>50':3})   
skin_data['Gender']= skin_data['Gender'].map({'Male':1 , 'Female':2})   
skin_data['Purchase_Last_Quarter']=skin_data['Purchase_Last_Quarter'].map({'Yes':1 , 'No':0})   
skin_data['Response_to_Campaign'] = skin_data['Response_to_Campaign'].map({'Yes':1 , 'No':0})   
        
#print(skin_data.dtypes) #check datatypes   
skin_data.head() 

# Now convert integer type variables to categorical for AgeGroup  Gender  Purchase_Last_Quarter and Response_to_Campaign   
skin_data['AgeGroup'] = skin_data['AgeGroup'].astype('category')   
skin_data['Gender'] = skin_data['Gender'].astype('category')   
skin_data['Purchase_Last_Quarter'] = skin_data['Purchase_Last_Quarter'].astype('category')   
skin_data['Response_to_Campaign'] = skin_data['Response_to_Campaign'].astype('int')   
skin_data.dtypes  #check the datatypes have been changed  

 # Overall response rate   
overall_response_rate = skin_data['Response_to_Campaign'].mean() * 100    
print(f" Overall Campaign Response Rate: {overall_response_rate:.2f}%") 
 #Create dummies (for categorical variables)   
categorical_vars = ['AgeGroup' , 'Gender','Purchase_Last_Quarter']   
            
dummies = pd.get_dummies(skin_data[categorical_vars] , drop_first=True)   
        
# Append (concatenate) dummy columns to masterdata   
skin_data = pd.concat([skin_data , dummies],  axis=1) 
skin_data.head() 

# List of segmentation variables   
#Create a table showing the response rate (%) for Male and Female customers. 
segment1 = ['Gender']   
        
response_summary1 = {}   
        
for col in segment1:   
    response_summary1[col] = (   
        skin_data.groupby(col)['Response_to_Campaign']   
        .mean()   
        .mul(100)   # convert to %   
        .round(2)   
        .rename(index={1: 'Male', 2: 'Female'})   
        .reset_index()  # This forces it into a Table structure   
    )
    
    # Rename columns so they look clean   
    response_summary1[col].columns = [col, 'Response Rate (%)']   
            
# Print the results
for key, value in response_summary1.items():   
    print(f"Response Rate by {key}:")   
    print(value) 
segment2 = ['AgeGroup']
        
response_summary2 = {}   
        
for col in segment2:   
    response_summary2[col] = (   
        skin_data.groupby(col)['Response_to_Campaign']   
        .mean()   
        .mul(100)   # convert to %   
        .round(2) 
        .rename(index={1:'<30' , 2: '30-50', 3:'>50'})  
        .reset_index()  # This forces it into a Table structure   
    )
    
    # Rename columns so they look clean   
    response_summary2[col].columns = [col, 'Response Rate (%)']   
            
# Print the results
for key, value in response_summary2.items():   
    print(f"Response Rate by {key}:")   
    print(value)
  #Purchase in Last Quarter vs Campaign Response   
#Construct a table showing response rate (%) for customers based on whether they made a purchase in the last quarter (Yes/No).   
segment3 = ['Purchase_Last_Quarter']   
        
response_summary3 = {}   
        
for col in segment3:   
    response_summary3[col] = (   
        skin_data.groupby(col)['Response_to_Campaign']   
        .mean()   
        .mul(100)   # convert to %   
        .round(2)   
        .rename(index={1: 'Yes',  0: 'No'})    
        .reset_index()  # <--- This forces it into a Table structure   
    )   
            
     # Rename columns so they look clean   
    response_summary3[col].columns = [col , 'Response Rate (%)']   
            
            
        
response_summary3   
        
for key, value in response_summary3.items():   
    print(f" Response Rate by {key}:" )   
    print(value)
#Product Usage vs Campaign Response   
#Categorize customers based on the number of unique products purchased in the last year:   
        
#(1–4)(5–8)(>8)   
#Create a table showing the response rate (%) for each category.   
#Feature Engineering - Recoding Numerical variable to Categorical   
# List of variables to bucketize   
bucket_var = ['Unique_Products_Purchased']   
        
     # Apply qcut in a loop   
for var in bucket_var:   
        skin_data[f'{var}_Bucket'] = pd.cut(   
        skin_data[var],    
        bins=[0 , 4,  8 , float('inf')],    
        labels=['1-4' , '5-8'  ,'>8']   
         )   
        
           
skin_data.head()       
       
segment4 = ['Unique_Products_Purchased_Bucket']   
        
response_summary4 = {}   
        
for col in segment4:   
         response_summary4[col] = (   
             skin_data.groupby(col)['Response_to_Campaign']   
             .mean()   
             .mul(100)   # convert to %   
             .round(2)   
             .reset_index()  # <--- This forces it into a Table structure   
         )   
            
         # Rename columns so they look clean   
         response_summary4[col].columns = [col , 'Response Rate (%)']   
            
        
response_summary4   
        
for key,  value in response_summary4.items():   
         print(f" Response Rate by {key}:" )   
         print(value) 


HTML_FRONTEND = """
<!DOCTYPE html>   
<html>   
<head>   
    <title>Skin Clinic Campaign Response Summary</title>   
    <style>   
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #fafafa; }   
        button { padding: 10px 16px; font-size: 16px; margin-bottom: 20px; cursor: pointer; background-color: #007bff; color: white; border: none; border-radius: 4px; }   
        button:hover { background-color: #0056b3; }   
        table { border-collapse: collapse; width: 100%; margin-bottom: 30px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }   
        th, td { border: 1px solid #e0e0e0; padding: 12px 8px; text-align: center; }   
        th { background-color: #f4f4f4; font-weight: 600; }   
        tr:nth-child(even) { background-color: #f9f9f9; }   
    </style>   
</head>   
<body>   
    <h2>Campaign Summary</h2>   
    <button onclick="loadData()">Load Summary</button>   
    <div id="tablesContainer"></div>   

    <script>   
        function loadData() {   
            fetch('/campaign-analysis-data')   
                .then(response => response.json())   
                .then(data => {   
                    const container = document.querySelector('#tablesContainer');   
                    container.innerHTML = ''; 
               
                    for (const [segmentName, rows] of Object.entries(data)) {
                        if (!rows || rows.length === 0) continue;
                        
                        const sectionHeader = document.createElement('h3');
                        sectionHeader.innerText = segmentName.replace(/_/g, ' ').toUpperCase();
                        container.appendChild(sectionHeader);

                        const table = document.createElement('table');
                        
                        // FIXED: target rows[0] to grab actual table column headers
                        // Extract actual table column headers
                        const headers = Object.keys(rows[0]);

                        let theadHTML = '<tr>';
                        headers.forEach(header => { theadHTML += '<th>' + header + '</th>'; });
                        theadHTML += '</tr>';

                        let tbodyHTML = '';
                        rows.forEach(row => {   
                            tbodyHTML += '<tr>';
                            headers.forEach(header => { tbodyHTML += '<td>' + row[header] + '</td>'; });
                            tbodyHTML += '</tr>';
                        });   

                        table.innerHTML = '<thead>' + theadHTML + '</thead><tbody>' + tbodyHTML + '</tbody>';
                        container.appendChild(table);
                    }
                })   
                .catch(error => {   
                    alert('Error fetching data');   
                    console.error(error);   
                });   
        }   
    </script>   
</body>   
</html>
"""


app = FastAPI(   
    title="Skin Clinic Campaign Analysis API",     
    description="API for evaluating marketing campaign responses across demographics."    
) 

@app.get("/campaign-analysis", response_class=HTMLResponse)   
def home():   
    return HTML_FRONTEND  

@app.get("/campaign-analysis-data")   
def get_campaign_analysis():   
    return {   
        "gender_vs_campaign_response": response_summary1['Gender'].to_dict(orient="records"),
        "age_group_vs_campaign_response": response_summary2['AgeGroup'].to_dict(orient="records"),
        "purchase_last_quarter_vs_campaign_response": response_summary3['Purchase_Last_Quarter'].to_dict(orient="records"),
        "product_usage_vs_campaign_response": response_summary4['Unique_Products_Purchased_Bucket'].to_dict(orient="records")
    }