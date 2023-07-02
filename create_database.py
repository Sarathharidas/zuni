import os
import pandas as pd
import csv

dir = '/Users/sarathharidas/Desktop/zuni/Translation_full_file'
def process_csv_files(folder_rel):
    # define the output file
    output_file = os.path.join("directory_afrikaans.csv")

    # define the header of the output file
    header = ["Folder Name", "Relative Path", "English", "Translation", "Accuracy"]
    folder = os.path.join(dir, folder_rel)
    # open the output file in write mode
    with open(output_file, "w", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(header)

        # walk through the directory structure
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                # only process .csv files
                if filename.endswith(".csv"):
                    file_path = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(file_path, folder)

                    # read the csv file
                    df = pd.read_csv(file_path)
                    df = df.iloc[:,[2,]]

                    # iterate over each row and write to the output file
                    for index, row in df.iterrows():
                        writer.writerow([dirpath, relative_path] + list(row))

# call the function with the root folder as argument
process_csv_files("Batch02-swahili")
