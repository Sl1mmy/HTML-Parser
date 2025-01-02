from bs4 import BeautifulSoup

def parse_file(file_path):
    parsed_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        td_elements = soup.find_all('td', class_='LRUc2')
        for td in td_elements:
            a_element = td.find('a', class_='LRUc2')
            if a_element and 'title' in a_element.attrs:
                title_soup = BeautifulSoup(a_element['title'], 'html.parser')
                for tag in title_soup.find_all(style=True):
                    styles = tag['style'].split(';')
                    styles = [style for style in styles if not style.strip().startswith('color')]
                    tag['style'] = ';'.join(styles)
                parsed_data.append(str(title_soup).replace('<br/>', '\n'))
    return parsed_data