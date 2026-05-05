import pandas as pd
df = pd.read_excel('hospital_insights_dataset.xlsx')
with open('dataset_analysis_output.txt', 'w') as f:
    f.write('---dtypes---\n')
    f.write(str(df.dtypes) + '\n')
    f.write('---nulls---\n')
    f.write(str(df.isnull().sum()) + '\n')
    f.write('---head---\n')
    f.write(str(df.head(2).to_dict(orient='records')) + '\n')
