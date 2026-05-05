import pandas as pd

# Load dataset
df = pd.read_excel('hospital_insights_dataset.xlsx')

original_shape = df.shape

# 1. Remove duplicates
df = df.drop_duplicates()

# 2. Standardize column names
df.columns = df.columns.str.lower().str.replace(' ', '_').str.strip()

# 3. Handle missing values
if 'insurance_type' in df.columns:
    df['insurance_type'] = df['insurance_type'].fillna('Unknown')

# For any other text columns, we might fill with 'Unknown' if there are nulls, 
# and for numeric we might fill with median, but from previous analysis only insurance_type had nulls.

# 4. Convert date columns properly
if 'admission_date' in df.columns:
    df['admission_date'] = pd.to_datetime(df['admission_date'], errors='coerce')
if 'discharge_date' in df.columns:
    df['discharge_date'] = pd.to_datetime(df['discharge_date'], errors='coerce')

# 5. Fix inconsistent values
if 'patient_gender' in df.columns:
    df['patient_gender'] = df['patient_gender'].astype(str).str.title().str.strip()
    gender_map = {'M': 'Male', 'F': 'Female', 'O': 'Other'}
    df['patient_gender'] = df['patient_gender'].replace(gender_map)

if 'department' in df.columns:
    df['department'] = df['department'].astype(str).str.title().str.strip()

# Save cleaned dataset
cleaned_filename = 'cleaned_hospital_insights_dataset.xlsx'
df.to_excel(cleaned_filename, index=False)

with open('cleaned_dataset_structure.txt', 'w') as f:
    f.write(f"Original shape: {original_shape}\n")
    f.write(f"Cleaned shape: {df.shape}\n")
    f.write("---dtypes---\n")
    f.write(str(df.dtypes) + '\n')
    f.write("---nulls---\n")
    f.write(str(df.isnull().sum()) + '\n')
    f.write("---unique_genders---\n")
    f.write(str(df['patient_gender'].unique()) + '\n')
    f.write("---unique_departments---\n")
    f.write(str(df['department'].unique()) + '\n')
