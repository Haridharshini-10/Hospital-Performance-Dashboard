import pandas as pd
import numpy as np
from datetime import timedelta, date

np.random.seed(42)

# EXACT counts per department - staircase drop of ~300 each
dept_counts = {
    'Cardiology':      2100,
    'Emergency':       1800,
    'General Surgery': 1500,
    'Orthopedics':     1200,
    'Neurology':        900,
    'Pediatrics':       600,
    'Oncology':         300,
}

# EXACT counts per doctor - staircase drop
doctor_counts = {
    'Dr. Smith':    2100,
    'Dr. Patel':    1800,
    'Dr. Lee':      1500,
    'Dr. Garcia':   1200,
    'Dr. Williams': 900,
    'Dr. Kim':      600,
    'Dr. Martinez': 300,
}

# EXACT counts per location
location_counts = {
    'California':  2100,
    'Texas':       1800,
    'New York':    1500,
    'Florida':     1200,
    'Illinois':     900,
    'Pennsylvania': 600,
    'Ohio':         300,
}

diagnoses = {
    'Cardiology':      [('Heart Attack', 900), ('Heart Failure', 650), ('Arrhythmia', 400), ('Angina', 150)],
    'Emergency':       [('Trauma', 750),        ('Cardiac Arrest', 550), ('Poisoning', 350),  ('Severe Burn', 150)],
    'General Surgery': [('Appendicitis', 600),  ('Hernia', 450),         ('Gallstones', 300),  ('Bowel Obstruction', 150)],
    'Orthopedics':     [('Fracture', 500),       ('Osteoarthritis', 350), ('Torn Ligament', 250),('Spinal Disc', 100)],
    'Neurology':       [('Stroke', 380),         ('Epilepsy', 270),       ('Migraine', 180),    ('Multiple Sclerosis', 70)],
    'Pediatrics':      [('Viral Fever', 250),    ('Pneumonia', 180),      ('Asthma', 120),      ('Appendicitis', 50)],
    'Oncology':        [('Breast Cancer', 120),  ('Lung Cancer', 90),     ('Leukemia', 60),     ('Lymphoma', 30)],
}

outcomes = ['Recovered', 'Discharged', 'Under Treatment', 'Critical']
outcome_counts = [4200, 3100, 1900, 300]  # Clean staircase for outcomes

admission_types = ['OPD', 'Emergency', 'Referral']
adm_counts =     [3800,  3300,        2400]   # Clear difference

genders = ['Male', 'Female']

start_date = date(2023, 1, 1)
end_date   = date(2024, 5, 31)
date_range_days = (end_date - start_date).days

rows = []
patient_counter = 1

# Build rows dept by dept for exact counts
for dept, count in dept_counts.items():
    diag_pool = diagnoses[dept]
    
    # Assign diagnoses with exact counts inside each dept
    diag_labels = []
    for (diag_name, diag_count) in diag_pool:
        diag_labels.extend([diag_name] * diag_count)
    # If total diag count doesn't match dept count, fill remainder with first diag
    while len(diag_labels) < count:
        diag_labels.append(diag_pool[0][0])
    diag_labels = diag_labels[:count]
    np.random.shuffle(diag_labels)
    
    for i in range(count):
        los = np.random.randint(1, 4) if np.random.rand() < 0.4 else (
              np.random.randint(3, 20) if np.random.rand() < 0.5 else np.random.randint(2, 15))
        
        adm_date = start_date + timedelta(days=int(np.random.randint(0, date_range_days)))
        dis_date  = adm_date + timedelta(days=los)
        
        if dept in ['Oncology', 'Cardiology', 'Neurology']:
            cost = np.random.randint(50000, 250000)
        elif dept in ['Emergency', 'General Surgery', 'Orthopedics']:
            cost = np.random.randint(20000, 100000)
        else:
            cost = np.random.randint(5000, 30000)
        
        adm_type = np.random.choice(admission_types, p=[a/sum(adm_counts) for a in adm_counts])
        
        rows.append({
            'Patient_ID':     f"P{str(patient_counter).zfill(5)}",
            'Admission_Date': adm_date,
            'Discharge_Date': dis_date,
            'Length_of_Stay': los,
            'Treatment_Cost': cost,
            'Department':     dept,
            'Doctor_Name':    '',   # fill below
            'Location':       '',   # fill below
            'Diagnosis':      diag_labels[i],
            'Outcome':        '',   # fill below
            'Admission_Type': adm_type,
            'Gender':         np.random.choice(genders),
        })
        patient_counter += 1

df = pd.DataFrame(rows)
total = len(df)

# Assign Doctor_Name with exact staircase counts
doc_labels = []
for doc, cnt in doctor_counts.items():
    doc_labels.extend([doc] * cnt)
while len(doc_labels) < total:
    doc_labels.append('Dr. Smith')
doc_labels = doc_labels[:total]
np.random.shuffle(doc_labels)
df['Doctor_Name'] = doc_labels

# Assign Location with exact staircase counts
loc_labels = []
for loc, cnt in location_counts.items():
    loc_labels.extend([loc] * cnt)
while len(loc_labels) < total:
    loc_labels.append('California')
loc_labels = loc_labels[:total]
np.random.shuffle(loc_labels)
df['Location'] = loc_labels

# Assign Outcome with exact staircase counts
out_labels = []
for out, cnt in zip(outcomes, outcome_counts):
    out_labels.extend([out] * cnt)
while len(out_labels) < total:
    out_labels.append('Recovered')
out_labels = out_labels[:total]
np.random.shuffle(out_labels)
df['Outcome'] = out_labels

# Shuffle the full dataframe so rows aren't grouped
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv('perfect_hospital_dataset.csv', index=False)

print(f"Dataset generated: {len(df)} total rows")
print("\nDepartment Counts:")
print(df['Department'].value_counts())
print("\nDiagnosis Counts (Top 10):")
print(df['Diagnosis'].value_counts().head(10))
print("\nDoctor Counts:")
print(df['Doctor_Name'].value_counts())
print("\nLocation Counts:")
print(df['Location'].value_counts())
print("\nOutcome Counts:")
print(df['Outcome'].value_counts())
