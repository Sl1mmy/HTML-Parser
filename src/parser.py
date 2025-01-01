from bs4 import BeautifulSoup

def parse_file(file_path):

    parsed_data = []
    
    with open(file_path, 'r') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        parsed_data.append(soup)

    return parsed_data