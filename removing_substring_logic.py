from googletrans import Translator
import re

def process_translate_string(input_str, glossary):
    # Compile regex pattern for the special cases
    pattern = re.compile(r'(\[.*?\]|\n|%d|%s)')

    # Find all matches
    matches = pattern.findall(input_str)

    # Replace matches with a placeholder
    placeholder = "<>"
    glossary_placeholder = "||"

    temp_str = pattern.sub(placeholder, input_str)
    #print(temp_str)
    # Now handle the glossary terms
    glossary_terms = list(glossary.keys())
    glossary_pattern = re.compile(r'\b(' + '|'.join(re.escape(term) for term in glossary_terms) + r')\b')
   
    # Replace glossary terms with placeholders and keep track of replacements
    glossary_matches = []
    
    def glossary_replace(string, glossary):
        matched_items = []
        for key in dictionary:
            if key in string:
                string = string.replace(key, "||")
                matched_items.append(key)
        return string, matched_items
    
    print(temp_str)
    # Translate string
  

    # Replace placeholders with original matches and glossary replacements
    all_replacements = matches + glossary_matches
   # print(placeholder)
    final_str = re.sub(placeholder, lambda x: all_replacements.pop(0), temp_str)
    print(final_str)
    return final_str




glossary = {"Hello": "Greetings", "world": "earth"}
print(process_translate_string("Hello my name [world]\n how %d are %s?", glossary))
