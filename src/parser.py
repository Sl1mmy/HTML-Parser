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

# title="&lt;div&gt;151 01 03 A&lt;/div&gt;&lt;em&gt;
# (Niveau 2, 10 000 km)&lt;/em&gt;&lt;div 
# style='text-align: left'&gt;Inspection Moteur de traction bogie&lt;/div&gt;&lt;div 
# style='border-top: lightgreen 1pt dotted'&gt;&lt;/div&gt;&lt;div style='text-align: left'&gt;
# ►Inspection visuelle générale du moteur de traction bogie côté entrée d’air&lt;/div&gt;&lt;div style='text-align: left'&gt;►Inspection du moteur de traction bogie côté sortie d’air&lt;/div&gt;&lt;div style='text-align: left'&gt;►Remise en condition&lt;/div&gt;&lt;div style='border-top: lightgreen 1pt dotted'&gt;&lt;/div&gt;&lt;em style='text-align: left'&gt;tâche(s) associée(s)&lt;/em&gt;&lt;div align='left'&gt;&lt;a href='../pdf/task/ALS00745_TASK_H.pdf' 
# style='text-align: left; color: white; border-bottom: steelblue 2pt solid' target='visionneuse'&gt;151 01 02 H &#xA;Capteur de vitesse&lt;/a&gt;&lt;/div&gt;&lt;div align='left'&gt;&lt;a href='../pdf/task/ALS01460_TASK_H.pdf' style='text-align: left; color: white; border-bottom: steelblue 2pt solid' target='visionneuse'&gt;151 01 03 H &#xA;Moteur de traction bogie&lt;/a&gt;&lt;/div&gt;&lt;div align='left'&gt;&lt;a href='../pdf/task/ALS00110_TASK_A2.pdf' style='text-align: left; color: white; border-bottom: steelblue 2pt solid' target='visionneuse'&gt;151 99 01 A2 &#xA;Coffre ETF&lt;/a&gt;&lt;/div&gt;">