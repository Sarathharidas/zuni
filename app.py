
### Language code
#language_dict = {'afrikaans' : 'af', 'zulu' : 'zu', 'swahili': 'sw'}

from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from google.cloud import translate
#from googletrans import Translator
#translator = Translator()
import csv
#from werkzeug import secure_filename
#from removing_substring_logic import process_string

import os
import shutil



### These are Hard coded
# l = 'afrikaans'
# folder = '/Users/sarathharidas/Desktop/zuni test/Batch01/Stories'
# translated_folder = '/Users/sarathharidas/Desktop/zuni test/Batch01-Afrikaans/Stories'
# directory = os.fsencode(folder)
#print(directory)


### Defining a class that reads csv files, and then 
## 1. Reads all the csv file
## 2. Translates the files
## 3. Write the files back to same folder structure and also to a new database
## 4. While translating use the conditions provided

class csv_file_translate:
    
    def __init__(self, batch_source_folder_location, language):
       self.source_folder = batch_source_folder_location
       language_dict = {'afrikaans' : 'af', 'zulu' : 'zu', 'swahili': 'sw'}
       self.language = language
       self.language_code = language_dict[language]
    
    ### Used for reading the file
    def read_first_row(csv_file):
      with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file)
        first_row = next(csv_reader)
        return first_row
    
    #### This function is used for creating the same folder structure
    def create_destination_folder_structure(self):
      new_folder_path = self.source_folder + '-' + self.language
    # Copy the directory tree
      shutil.copytree(self.source_folder, new_folder_path)
    # Now, empty the newly copied directories
      for dirpath, dirnames, filenames in os.walk(new_folder_path):
        for filename in filenames:
          file_path = os.path.join(dirpath, filename)
          os.remove(file_path)
    



c = csv_file_translate('/Users/sarathharidas/Desktop/zuni/Batch01', 'swahili')  
c.create_destination_folder_structure() 
 



# def read_first_row(csv_file):
#     with open(csv_file, 'r') as file:
#         csv_reader = csv.reader(file)
#         first_row = next(csv_reader)
#         return first_row

# def translate_text(text, project_id, language):
#     """Translating Text."""
#     client = translate.TranslationServiceClient()

#     location = "global"

#     parent = f"projects/{project_id}/locations/{location}"
    
#     ## Defining the language code 
#     language_dict = {'afrikaans' : 'af', 'zulu' : 'zu', 'swahili': 'sw'}
#     language_code = language_dict[language]
#     # Translate text from English to French
#     # Detail on supported types can be found here:
#     # https://cloud.google.com/translate/docs/supported-formats
#     response = client.translate_text(
#         request={
#             "parent": parent,
#             "contents": [text],
#             "mime_type": "text/plain",  # mime types: text/plain, text/html
#             "source_language_code": "en-US",
#             "target_language_code": language_code,
#         }
#         ### af, sw, zu for afrikaans, swahili and zulu respectively
#     )

#     # Display the translation for each input text provided
#     for translation in response.translations:
#         #print(f"Translated text: {translation.translated_text}")
#         return translation.translated_text



# def back_translation_function(text, project_id, language):
#     """Translating Text."""

#     client = translate.TranslationServiceClient()

#     location = "global"

#     parent = f"projects/{project_id}/locations/{location}"
    
#     ## Defining the language code 
#     language_dict = {'afrikaans' : 'af', 'zulu' : 'zu', 'swahili': 'sw'}

#     language_code = language_dict[language]
#     # Translate text from English to French
#     # Detail on supported types can be found here:
#     # https://cloud.google.com/translate/docs/supported-formats
#     response = client.translate_text(
#         request={
#             "parent": parent,
#             "contents": [text],
#             "mime_type": "text/plain",  # mime types: text/plain, text/html
#             "source_language_code": language_code, 
#             "target_language_code": "en-US",
#         }
#         ### af, sw, zu for afrikaans, swahili and zulu respectively
#     )

#     # Display the translation for each input text provided
#     for translation in response.translations:
#         #print(f"Translated text: {translation.translated_text}")
#         return translation.translated_text

# def extract_array(df_input):
#   new_text_array = []
#   translated_text_array = []
#   total_cols = df_input.shape[0]
#   for i in range(0,total_cols):
#     text_raw = df_input.iloc[i, 2]
#     #new_text = translator.translate(str(text_raw), dest='afrikaans')
#     new_text_array.append(text_raw)
#     #translated_text_array.append(new_text)
#   return new_text_array

# def array_translation(array, language):
#   translated_array = []
#   back_translation_array =[]
#   for i in range(len(array)):
#     print(i)
#     if isinstance(array[i], str):
#       translation = translate_text(array[i], 'quicktranslates', language)
#       back_translation = back_translation_function(translation, 'quicktranslates', language)
#     else:
#        translation = ''
#     translated_array.append(translation)
#     back_translation_array.append(back_translation)
#     print(translation)
#   return translated_array, back_translation_array


# def write_to_csv(csv_file, header, data1, data2, data3, data4, data5):
#     with open(csv_file, 'w', newline='') as f:
#         csv_writer = csv.writer(f, delimiter=';')
#         #csv_writer.writerow()
#         csv_writer.writerow([header[0].replace('"', ''), '', ''])
#         csv_writer.writerows(zip(data1, data2, data3, data4, data5))

# for file in os.listdir(directory):
#   filename = os.fsdecode(file)
#   file_full_path = os.path.join(folder, filename)
#   _, file_extension = os.path.splitext(file_full_path)
#   if file_extension.lower() == ".csv":
#     df = pd.read_csv(file_full_path, sep=';', skiprows=[0], header=None)
#     header = read_first_row(file_full_path)
#     list_extracted = extract_array(df)
#     translated_array, back_translation_array = array_translation(list_extracted, l) 
#     col1 = [value if isinstance(value, str) else '' for value in df.iloc[:, 0].values]
#     col2 = [value if isinstance(value, str) else '' for value in df.iloc[:, 1].values]
#     col3 = [value if isinstance(value, str) else '' for value in df.iloc[:, 2].values]
#     translated_file_path = os.path.join(translated_folder, filename)
#     array_exact_match = []
#     for x, y in zip(list_extracted, back_translation_array):
#       if x==y:
#           array_exact_match.append("Accurate")
#       else:
#           array_exact_match.append("Needs_Review")
          
#     write_to_csv(translated_file_path, header, col1, col2 ,col3 ,translated_array, 
#                 array_exact_match)