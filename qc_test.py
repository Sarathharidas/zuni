import os
import csv

def count_words_in_csv(path):
    total_word_count = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.csv'):
                with open(os.path.join(root, file), 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    for row in csv_reader:
                        if len(row) > 2:  # Check if there are at least 3 columns
                            #print(row[2].split())
                            total_word_count += len(row[2].split())

    return total_word_count



def check_files(folder1, folder2):
    # Get the list of files in each folder (including subdirectories)
    files1 = get_files_recursive(folder1)
    files2 = get_files_recursive(folder2)

    # Check if any files from folder1 are missing in folder2
    missing_files = set(files1) - set(files2)
    if missing_files:
        with open('/Users/sarathharidas/Desktop/zuni/Unit Test Output/missing_file_2.txt', 
                  'a', newline='' ) as txtfile:
            txtfile.write(f"\n \n mising file in folder{folder2}, file {missing_files}")

        print(f"The following files are missing in {folder2}: {missing_files}")
    else:
        with open('/Users/sarathharidas/Desktop/zuni/Unit Test Output/missing_file_2.txt', 
                  'a', newline='' ) as txtfile:
            txtfile.write(f" \n \n All files are there in {folder2}")
        print("all files are there")

    # Compare the number of lines in each file
    # for file in files1:
    #     file1_path = os.path.join(folder1, file)
    #     file2_path = os.path.join(folder2, file)
    #     if os.path.isfile(file2_path):
    #         with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
    #             lines1 = f1.readlines()
    #             lines2 = f2.readlines()
    #             if len(lines1) != len(lines2):
    #                 print(f"The number of lines in {file1_path} does not match {file2_path}")

    #print("All files in batch01 are present in batch01-swahili with matching line counts.")

def get_files_recursive(folder):
    files = []
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            files.append(os.path.relpath(os.path.join(dirpath, filename), folder))
    return files

# Specify the folder paths

#dir = "/Users/sarathharidas/Desktop/zuni/Translation work/Batch01"
for l in ['swahili', 'zulu', 'afrikaans']:
    for batch in ['Batch01', 'Batch02', 'Batch03', 'Batch04', 'Batch05']:
        folder1 = f"/Users/sarathharidas/Desktop/zuni/Translation work/{batch}"
        folder2 = f"/Users/sarathharidas/Desktop/zuni/Final Output combined/{batch}-{l}"
        # Call the function to check the files
        check_files(folder1, folder2)



#### CHECKING FOR WORD COUNT IN BATCHES
# batch = ['Batch01', 'Batch02', 'Batch03', 'Batch04', 'Batch05']

# for b in batch:
#     path_batch = os.path.join(dir, b)
#     print(b, count_words_in_csv(path_batch))