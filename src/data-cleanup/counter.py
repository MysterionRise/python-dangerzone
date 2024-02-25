import pandas as pd

# Read the Excel spreadsheet
df = pd.read_excel('data/primes.xlsx')

# Initialize variables
current_name = ''
condition_counts = {}

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    name = row['DATA_FILE']  # Column B (index 1)
    condition1 = row['верность_прайма(1-верный,2-ложный)']  # Column EK (index 136)
    condition2 = row['тип_прайма(1-картинка,2-слово)']  # Column EL (index 137)

    # Check if the name has changed
    if name != current_name:
        current_name = name
        condition_counts = {}

    # Create the condition pair
    condition_pair = (condition1, condition2)

    if condition_pair in condition_counts:
        condition_counts[condition_pair] += 1
    else:
        condition_counts[condition_pair] = 1

        # Assign the occurrence count to column EM (index 138)
    df.at[index, 138] = condition_counts[condition_pair]

# Save the updated DataFrame back to the Excel spreadsheet
print("Processed!")
df.to_excel('data/updated_spreadsheet.xlsx', index=False)