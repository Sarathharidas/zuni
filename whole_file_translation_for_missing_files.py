
### Language code
#language_dict = {'afrikaans' : 'af', 'zulu' : 'zu', 'swahili': 'sw'}

from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from google.cloud import translate
import csv
#from werkzeug import secure_filename
#from removing_substring_logic import process_string
import os
import shutil
import re
import pandas as pd
import datetime

### Defining a class that reads csv files, and then 
## 1. Reads all the csv file
## 2. Translates the files
## 3. Write the files back to same folder structure and also to a new database
## 4. While translating use the conditions provided

class csv_file_translate:
    
    def __init__(self, batch_source_folder_location, language, glossary_df, project_id):
       self.source_folder = batch_source_folder_location
       language_dict = {'afrikaans' : 'af', 'zulu' : 'zu', 'swahili': 'sw'}
       self.language = language
       self.language_code = language_dict[language]
       self.glossary_dict = pd.Series(glossary_df.iloc[:, 1].values,index=glossary_df.iloc[:, 0]).to_dict()
       self.project_id = project_id

    ### Used for reading the file
    def read_first_row(self, csv_file):
      with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        first_row = next(csv_reader)
        return first_row

    #### This function is used for creating the same folder structure
    def recreate_folder_with_translation(self):
    # Create a new folder name by appending the suffix string
      new_folder = self.source_folder + '-' + self.language

    # Recreate the new folder in the same place as the original folder
      os.makedirs(new_folder, exist_ok=True)

    # Iterate over all files and subdirectories in the original folder
      for root, dirs, files in os.walk(self.source_folder):
        # Create corresponding subdirectories in the new folder
        for dir_name in dirs:
            new_dir = os.path.join(root.replace(self.source_folder, new_folder), dir_name)
            os.makedirs(new_dir, exist_ok=True)

        # Process each file in the original folder
        for file_name in files:
            time_1 = datetime.datetime.now()
            original_path = os.path.join(root, file_name)
            print(original_path)
            new_path = os.path.join(root.replace(self.source_folder, new_folder), file_name)
            print(new_path)  
            # If it's a CSV file, call the translate function
            if os.path.isfile(new_path):
               print(f'{new_path} file exists')
            else:

              if file_name.lower().endswith('.csv'):
                  try:
                      self.translate(original_path, new_path)
                      time_2 = datetime.datetime.now()
                      print(f"time taken is {time_2-time_1}")
                  except:
                    txt_path = os.path.join(self.source_folder, 'error.txt')
                    with open(txt_path, 'a') as file:
                        file.write(file_name)
                        
              else:
                  # Otherwise, copy the file as it is
                  shutil.copyfile(original_path, new_path)
    
    def translate(self, original_file, new_file):

      df = pd.read_csv(original_file, sep=';', skiprows=[0], header=None)
      header = self.read_first_row(original_file)
      ## hard coding 2 to be removed
      list_extracted = df.iloc[:, 2].values
      translated_array, back_translation_array = self.array_translation(list_extracted, 
                                                                        self.language_code)
      print(translated_array) 
      col1 = [value if isinstance(value, str) else '' for value in df.iloc[:, 0].values]
      col2 = [value if isinstance(value, str) else '' for value in df.iloc[:, 1].values]
      col3 = [value if isinstance(value, str) else '' for value in df.iloc[:, 2].values]
    
      array_exact_match = []
      for x, y in zip(list_extracted, back_translation_array):
        print(f'x is {x}')
        print(f'y is {y}')
        if x==y:
          array_exact_match.append("Accurate")
        else:
          array_exact_match.append("Needs_Review")
      self.write_to_csv(new_file, header, col1, col2 ,col3 ,translated_array, 
                 array_exact_match)
    
    def array_translation(self, array, language_code):

        translated_text_array = self.process_translate_string(array)
        back_translated_text_array = self.back_translate_text(translated_text_array, self.language_code, "en-US")
        print(f'Translation is {translated_text_array}')                                              
        print(f'back translation is {back_translated_text_array}')
        return translated_text_array, back_translated_text_array
    
  
    def process_translate_string(self, input_str_list):
    # Compile regex pattern for the special cases
        
        pattern = re.compile(r'(\[.*?\]|\n|%d|%s)')
    
    # Create a pattern for the glossary terms
        glossary_terms = list(self.glossary_dict.keys())
        glossary_pattern = re.compile(r'\b(' + '|'.join(re.escape(term) for term in glossary_terms) + r')\b')

        def process_string(input_str):
        # Initialize an empty list to hold all matches in order
            input_str = str(input_str)
            all_replacements = []
        
        # Define placeholders
            special_cases_placeholder = "<><>"
            glossary_placeholder = "@@"

        # Replace matches with a placeholder
            def special_cases_replacer(match):
                match_str = match.group(0)
                all_replacements.append(match_str)
                return special_cases_placeholder
            temp_str = pattern.sub(special_cases_replacer, input_str)

        # Replace glossary terms with a placeholder
            def glossary_replacer(match):
                term = match.group(0)
                all_replacements.append(self.glossary_dict[term])
                return glossary_placeholder
            temp_str = glossary_pattern.sub(glossary_replacer, temp_str)

        # Translate string
            translated_str = self.translate_text(temp_str,"en-US", self.language_code)

        # Replace placeholders with original matches
            final_str = re.sub(special_cases_placeholder, lambda x: all_replacements.pop(0), translated_str)
            final_str = re.sub(glossary_placeholder, lambda x: all_replacements.pop(0), final_str)

            return final_str
    
        return [process_string(input_str) for input_str in input_str_list]


    def translate_text(self, text, source_language_code, target_language_code):
      """Translating Text."""
      client = translate.TranslationServiceClient()

      location = "global"

      parent = f"projects/{self.project_id}/locations/{location}"
    
    ## Defining the language code 
      # Translate text from English to French
      # Detail on supported types can be found here:
      # https://cloud.google.com/translate/docs/supported-formats

      try:
        response = client.translate_text(
          request={
              "parent": parent,
              "contents": [text],
              "mime_type": "text/plain",  # mime types: text/plain, text/html
              "source_language_code": source_language_code,
              "target_language_code": target_language_code
          }, timeout=100
          ### af, sw, zu for afrikaans, swahili and zulu respectively
      )
      # Display the translation for each input text provided
        for translation in response.translations:
          #print(f"Translated text: {translation.translated_text}")
            return translation.translated_text
      except:
        try:
          response = client.translate_text(
          request={
              "parent": parent,
              "contents": [text],
              "mime_type": "text/plain",  # mime types: text/plain, text/html
              "source_language_code": source_language_code,
              "target_language_code": target_language_code
          }
          ### af, sw, zu for afrikaans, swahili and zulu respectively
      )
      # Display the translation for each input text provided
          for translation in response.translations:
          #print(f"Translated text: {translation.translated_text}")
            return translation.translated_text
        except:
          return text  
      
    def back_translate_text(self, list_of_strings, source_language_code, target_language_code):
        """Translating Text."""
        client = translate.TranslationServiceClient()

        location = "global"
        parent = f"projects/{self.project_id}/locations/{location}"

    # Convert list of strings to a single string
        text = "||".join(list_of_strings)
    
        try:
            response = client.translate_text(
            
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": source_language_code,
                "target_language_code": target_language_code
            }
        )
    
    # Split the translated string back into a list
            translated_list = response.translations[0].translated_text.split("||")
            return translated_list
        except:
           return list_of_strings

      
    def write_to_csv(self, csv_file, header, data1, data2, data3, data4, data5):
      with open(csv_file, 'w', newline='') as f:
        csv_writer = csv.writer(f, delimiter=';')
        #csv_writer.writerow()
        csv_writer.writerow([header[0].replace('"', ''), '', ''])
        csv_writer.writerows(zip(data1, data2, data3, data4, data5))


### For each language-Batch combination. This will do for all csv files

for l in ['zulu', 'afrikaans', 'swahili']:
  
  base_directory = '/Users/sarathharidas/Desktop/zuni/Translation_full_file'
  folders = ['Batch02']
  
  for folder in folders:
    print("Starting Batch {folder}")
    now_time = datetime.datetime.now()
    print(now_time)
    print(folder, l)
    file_path = os.path.join(base_directory, folder)
    df_glossary = pd.read_excel(os.path.join(base_directory, f'{l}_glossary.xlsx'))
    l_batch_n_class = csv_file_translate(file_path, l, df_glossary, 'quicktranslates')
    l_batch_n_class.recreate_folder_with_translation()
    

### For xls files


### For txt files 

