import os
import pandas as pd

# root directory
root_dir = '/Users/sarathharidas/Desktop/zuni/Translation work/'
new_file_path = '/Users/sarathharidas/Desktop/zuni/Translation work/Database_afrikaans.csv'

# function to add unique identifier to a DataFrame
def add_unique_id(df, file_path):
    relative_path = os.path.relpath(file_path, root_dir)
    relative_path = relative_path.replace('/', '_').replace('\\', '_')
    print(relative_path)
    df['unique_id'] = [f"{relative_path}_line{i}" for i in range(len(df))]
    return df

# walk through the directory structure
for dirpath, dirs, files in os.walk(root_dir):
    for filename in files:
        file_path = os.path.join(dirpath, filename)
        
        # Check if the file is an Excel file or CSV file
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            #print(f'Processing Excel file {file_path}...')
            
            # read the excel file
            df = pd.read_excel(file_path)
            
            # add a unique identifier to each row
            df = add_unique_id(df, file_path)
            
            # save the DataFrame back to the excel file
            df.to_excel(file_path, index=False)
            #print(f'Updated {file_path} with unique identifiers.')
            
        elif filename.endswith('.csv'):
            #print(f'Processing CSV file {file_path}...')
            #print(2)
            # read the CSV file
            df = pd.read_csv(file_path, on_bad_lines='skip', skiprows=1, sep=";", header=None)
            #print(df.head())
            # add a unique identifier to each row
            df = add_unique_id(df, file_path)
            #print(df['unique_id'])
            # save the DataFrame back to the CSV file
            print(df.columns)


            # Check if the file exists
            if os.path.isfile(new_file_path):
                # If the file exists, append without writing the header
                df.iloc[:, [df.columns.get_loc('unique_id'), 0,1,2 ]].to_csv(new_file_path, mode='a', header=False, index=False)
            
            else:
                # If the file does not exist, write the DataFrame with a header
                df.iloc[:, [df.columns.get_loc('unique_id'), 0,1,2 ]].to_csv(new_file_path, mode='w', index=False)

            #print(f'Updated {file_path} with unique identifiers.')
            
        else:
            print(f'Skipped {filename} (not an Excel or CSV file).')
