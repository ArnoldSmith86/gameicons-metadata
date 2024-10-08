import json
import os
import sys
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

def read_tags_file(file_path):
    tags = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                symbol, tag_list = parts
                tags[symbol] = tag_list.split(', ')
    return tags

def sort_key(item):
    # Split the string and return the part after the '/'
    return item[0].split('/')[-1]

def generate_symbols_json(list_file, categories_file, tags_file, output_file):
    symbols_list = read_list_file(list_file)
    categories = read_categories_file(categories_file)
    tags = read_tags_file(tags_file)

    symbols_dict = {}

    for index, symbol in enumerate(symbols_list):
        category = categories.get(symbol, "Unlisted")
        full_category = f"Game-icons.net - {category}"

        if full_category not in symbols_dict:
            symbols_dict[full_category] = {}

        symbol_tags = tags.get(symbol, [])
        symbols_dict[full_category][symbol] = [index] + symbol_tags

    # Sort the categories
    sorted_symbols_dict = OrderedDict(sorted(symbols_dict.items()))

    # Sort the symbols within each category
    for category in sorted_symbols_dict:
        sorted_symbols_dict[category] = OrderedDict(
            sorted(sorted_symbols_dict[category].items(), key=sort_key)
        )

    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, 'w') as file:
        json.dump(sorted_symbols_dict, file, indent=2)

if __name__ == "__main__":
    list_file = os.path.expanduser("list.txt")
    categories_file = os.path.expanduser("list-categories.txt")
    tags_file = os.path.expanduser("list-tags.txt")
    output_file = "symbols.json"
    generate_symbols_json(list_file, categories_file, tags_file, output_file)
    print(f"Generated {output_file} successfully.")
