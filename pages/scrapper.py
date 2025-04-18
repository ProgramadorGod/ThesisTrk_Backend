from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json
from bs4 import BeautifulSoup
import os

# Configura el navegador Brave
options = Options()
options.binary_location = "/usr/bin/brave-browser"
options.add_argument("--headless")  # opcional si no quieres que se abra el navegador
options.add_argument("--disable-gpu")

service = Service()
driver = webdriver.Chrome(service=service, options=options)

# Función para extraer todas las URLs de hojas de cálculo
def get_spreadsheet_urls(main_url):
    driver.get(main_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all("a", href=True)
    sheet_urls = [a['href'] for a in links if "docs.google.com/spreadsheets" in a['href']]
    return sheet_urls

# Función para procesar una hoja de cálculo individual
def process_sheet(sheet_url):
    driver.get(sheet_url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        time.sleep(3)
    except:
        print("Error cargando iframe en:", sheet_url)
        return

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all('tr')

    data = []
    CarrerCode = ""
    for row in rows:
        row_length = len(row.find_all('td'))
        title = ""
        authors = ""
        year = ""
        link = ""
        final_authors = []

        for i in range(row_length):
            cell = row.find_all('td')[i].text.strip()
            if i == 0:
                CarrerCode = cell
            if i == 2:
                title = cell
            if i == 3:
                authors_raw = row.find_all('td')[i].decode_contents()
                authors_raw_clean = re.sub(r'<br\s*/?>', '|||', authors_raw)
                authors = [author.strip() for author in authors_raw_clean.split('|||') if author.strip()]
                authors_split_by_y = []
                for author in authors:
                    authors_split_by_y.extend([a.strip() for a in author.split(' Y ') if a.strip()])
                authors_final = [re.sub(r' Y$', '', author) for author in authors_split_by_y]
                final_authors = []
                for author in authors_final:
                    split_authors = re.split(r'\s{7,}', author)
                    final_authors.extend([a.strip() for a in split_authors if a.strip()])
            if i == 4:
                year = cell if cell else "Undefined"
            if i == 5:
                a_tag = row.find("a")
                if a_tag and a_tag.has_attr("href"):
                    link = a_tag["href"]

        if title:  # Evita filas vacías
            data.append({
                "title": title,
                "authors": final_authors,
                "year": year,
                "link": link
            })

    # Obtener nombre de la carrera del título de la página (fuera del iframe)
    driver.switch_to.default_content()
    career_title = driver.title.split(" - ")[0].strip()

    if data:
        output = {
            "career": career_title,
            "CarrerCode": CarrerCode,
            "works": data
        }

        safe_filename = re.sub(r'[^\w\-_\. ]', '_', career_title.lower().replace(" ", "_"))
        with open(f"{safe_filename}.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=4)
        print(f"Guardado: {safe_filename}.json")
    else:
        print(f"No se encontraron trabajos para: {career_title}")

# URL principal
main_url = "https://unipaz.edu.co/bibliotesis/"

# Extraer y procesar cada hoja de cálculo
sheet_urls = get_spreadsheet_urls(main_url)
print(f"Encontradas {len(sheet_urls)} hojas de cálculo.")

for sheet_url in sheet_urls:
    print(f"\nProcesando: {sheet_url}")
    process_sheet(sheet_url)

driver.quit()
