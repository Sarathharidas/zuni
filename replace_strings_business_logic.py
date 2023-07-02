from google.cloud import translate
import re


def process_translate_string(input_str, glossary):
    # Compile regex pattern for the special cases
    pattern = re.compile(r'(\[.*?\]|\n|%d|%s)')
    # Create a pattern for the glossary terms
    glossary_terms = list(glossary.keys())
    glossary_pattern = re.compile(r'\b(' + '|'.join(re.escape(term) for term in glossary_terms) + r')\b')

    # Initialize an empty list to hold all matches in order
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
        all_replacements.append(glossary[term])
        return glossary_placeholder
    temp_str = glossary_pattern.sub(glossary_replacer, temp_str)

    # Translate string
    print(temp_str)
    print(all_replacements)
    translated_str = translate_function(temp_str, 'quicktranslates', 'sw')
    print(translated_str)
    # Replace placeholders with original matches
    final_str = re.sub(special_cases_placeholder, lambda x: all_replacements.pop(0), translated_str)
    print(final_str)
    print("printing all replacement")
    print(all_replacements)
    final_str = re.sub(glossary_placeholder, lambda x: all_replacements.pop(0), final_str)

    return final_str


def translate_function(text, project_id, language_code):
      """Translating Text."""
      client = translate.TranslationServiceClient()

      location = "global"

      parent = f"projects/{project_id}/locations/{location}"
    
    ## Defining the language code 
      # Translate text from English to French
      # Detail on supported types can be found here:
      # https://cloud.google.com/translate/docs/supported-formats
      response = client.translate_text(
          request={
              "parent": parent,
              "contents": [text],
              "mime_type": "text/plain",  # mime types: text/plain, text/html
              "source_language_code": "en-US",
              "target_language_code": language_code,
          }
          ### af, sw, zu for afrikaans, swahili and zulu respectively
      )
      # Display the translation for each input text provided
      for translation in response.translations:
          #print(f"Translated text: {translation.translated_text}")
          return translation.translated_text



input_str = "[Hello], %s! welcome to ooty my man, nice to meet you. hello how are you bro? %n"
dict_values = {"hello": "Hola", "bro": "sis", "ooty":"kodai"}

temp_str = process_translate_string(input_str, dict_values)
print(temp_str,)
