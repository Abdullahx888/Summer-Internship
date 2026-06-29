import json

# 1. Load the dataset
file_path = 'train_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Initialize our matrix buckets
matrix = {
    'Believable_Valid': 0,      # (Plausibility: True, Validity: True) -> Easy alignment
    'Believable_Invalid': 0,    # (Plausibility: True, Validity: False) -> The human/LLM trap!
    'Unbelievable_Valid': 0,    # (Plausibility: False, Validity: True) -> Counter-intuitive logic test
    'Unbelievable_Invalid': 0   # (Plausibility: False, Validity: False) -> Easy rejection
}

# 3. Sort every item into its quadrant
for item in data:
    val = item['validity']
    plaus = item['plausibility']
    
    if plaus is True and val is True:
        matrix['Believable_Valid'] += 1
    elif plaus is True and val is False:
        matrix['Believable_Invalid'] += 1
    elif plaus is False and val is True:
        matrix['Unbelievable_Valid'] += 1
    elif plaus is False and val is False:
        matrix['Unbelievable_Invalid'] += 1

total_samples = len(data)

# 4. Print out the structured table data for Deliverable D2 and RQ3
print("="*65)
print("       PHASE 3: BELIEVABILITY & BIAS MATRIX REPORT              ")
print("="*65)
print(f"Total Dataset Samples Evaluated: {total_samples}")
print("-"*65)
print("QUADRANT BREAKDOWN:")
print(f"  1. Believable + Logically Valid:    {matrix['Believable_Valid']} samples ({matrix['Believable_Valid']/total_samples*100:.2f}%)")
print(f"  2. Believable + Logically Invalid:  {matrix['Believable_Invalid']} samples ({matrix['Believable_Invalid']/total_samples*100:.2f}%)")
print(f"  3. Unbelievable + Logically Valid:  {matrix['Unbelievable_Valid']} samples ({matrix['Unbelievable_Valid']/total_samples*100:.2f}%)")
print(f"  4. Unbelievable + Logically Invalid:{matrix['Unbelievable_Invalid']} samples ({matrix['Unbelievable_Invalid']/total_samples*100:.2f}%)")
print("="*65)

# 5. Diagnostic Insights for Research Question 3 (RQ3)
print("\nDIAGNOSTIC INSIGHTS FOR RQ3:")
print("-"*65)
total_valid = matrix['Believable_Valid'] + matrix['Unbelievable_Valid']
total_invalid = matrix['Believable_Invalid'] + matrix['Unbelievable_Invalid']

print(f"Total Valid Structures: {total_valid} | Total Invalid Structures: {total_invalid}")
print(f"Are 'Invalid' statements mostly coded as plausible to trap models?")
print(f"  -> {matrix['Believable_Invalid']/total_invalid*100:.2f}% of all invalid logic problems are masked with believable text!")
print("="*65)