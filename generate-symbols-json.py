# generated by Claude 3.5 Sonnet

import json
import os
from collections import OrderedDict

def read_list_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def read_categories_file(file_path):
    categories = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                category, symbol = parts
                categories[symbol] = category
    return categories

def generate_symbols_json(list_file, categories_file, output_file):
    symbols_list = read_list_file(list_file)
    categories = read_categories_file(categories_file)
    
    symbols_dict = {}
    
    for index, symbol in enumerate(symbols_list):
        category = categories.get(symbol, "Unlisted")
        full_category = f"Game-icons.net - {category}"
        
        if full_category not in symbols_dict:
            symbols_dict[full_category] = {}
        
        symbols_dict[full_category][symbol] = [index]
    
    # Sort the categories
    sorted_symbols_dict = OrderedDict(sorted(symbols_dict.items()))
    
    # Sort the symbols within each category
    for category in sorted_symbols_dict:
        sorted_symbols_dict[category] = OrderedDict(sorted(sorted_symbols_dict[category].items()))
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as file:
        json.dump(sorted_symbols_dict, file, indent=2)

if __name__ == "__main__":
    list_file = os.path.expanduser("list.txt")
    categories_file = os.path.expanduser("list-categories.txt")
    output_file = "assets/fonts/symbols.json"
    
    generate_symbols_json(list_file, categories_file, output_file)
    print(f"Generated {output_file} successfully.")