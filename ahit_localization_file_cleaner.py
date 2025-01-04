import re
import os
import chardet
import argparse

SUPPORTED_LOCALIZATIONS = {
    '.chn': 'Chinese',
    '.deu': 'German',
    '.esn': 'Spanish',
    '.fra': 'French',
    '.int': 'English',
    '.ita': 'Italian',
    '.jpn': 'Japanese',
    '.kor': 'Korean',
    '.ptb': 'Portuguese'
}

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
    return result['encoding']

def clean_text(input_file, output_file=None, print_to_terminal=False):
    try:
        # Detect file encoding
        encoding = detect_encoding(input_file)

        with open(input_file, 'r', encoding=encoding) as file:
            lines = file.readlines()

        cleaned_lines = []
        for line in lines:
            # Remove all '=' characters and everything else on its left side.
            line = re.sub(r'^.*?=', '', line)

            # Remove all characters that start with '[' and end with ']'
            line = re.sub(r'\[.*?\]', ' ', line)

            # Remove a possible whitespace before a punctuation mark.
            line = re.sub(r'\s+([.,!?:;])', r'\1', line)

            # Remove possible double (or more) whitespaces
            line = re.sub(r'\s+', ' ', line)

            cleaned_lines.append(line.strip())

        # Remove unnecessary empty lines except leave only 1 left.
        final_lines = []
        for i, line in enumerate(cleaned_lines):
            if line or (i > 0 and cleaned_lines[i-1]):
                final_lines.append(line)

        if print_to_terminal:
            for line in final_lines:
                print(line)
        else:   
            with open(output_file, 'w', encoding=encoding) as file:
                for line in final_lines:
                    file.write(line + '\n')

    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='A Hat in Time localization file cleaner')
    parser.add_argument('-f', '--file', required=True, help='Path to a localization file')
    parser.add_argument('-p', '--print', action='store_true', help='Print cleaned text to the terminal rather than write it to a file')
    args = parser.parse_args()

    localization_file = args.file
    if os.path.isdir(localization_file):
        print(f"Error: Given localization file is a directory...")
        return
    
    if os.stat(localization_file).st_size == 0:
        print(f"Error: Localization file {localization_file} is empty...")
        return

    localization_ext = os.path.splitext(localization_file)[1]

    if localization_ext not in SUPPORTED_LOCALIZATIONS:
        print(f"Error: Localization Unknown ({localization_ext}) is not supported...")
        print("Supported localizations:")
        print('\n'.join([f' - {v} ({k})' for k, v in SUPPORTED_LOCALIZATIONS.items()]))
        return

    print_to_terminal = args.print
    cleaned_localization_file = localization_file + ".cleaned"

    if not print_to_terminal:
        print("Cleaning...")

    cleaned_text = clean_text(localization_file, cleaned_localization_file, print_to_terminal)

    if not print_to_terminal:
        print("Cleaned and written to a file...")

if __name__ == "__main__":
    main()