from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

print("Iniciando navegador...")

opciones = Options()
opciones.add_argument("--headless=new") 
opciones.add_argument("--no-sandbox") 
opciones.add_argument("--disable-dev-shm-usage") 
opciones.add_argument("--window-size=1920,1080") 

driver = webdriver.Chrome(options=opciones) 
url = "https://www.sofascore.com/es-la/football/tournament/england/premier-league/17#id:61627,tab:stats"
driver.get(url)

# 1. Aceptar Cookies
try:
    print("Esperando banner de cookies...")
    boton_cookies = WebDriverWait(driver, 12).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Consent') or contains(., 'Aceptar')]"))
    )
    boton_cookies.click()
    print("¡Cookies aceptadas!")
    time.sleep(2)
except:
    print("No se detectó banner de cookies.")

todos_los_jugadores = []
total_paginas = 29

for pagina in range(1, total_paginas + 1):
    print(f"\n--- [PROCESANDO PÁGINA {pagina} / {total_paginas}] ---")
    
    # 2. Esperar tabla
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table tbody tr')))
        time.sleep(2)
    except:
        print("Error: La tabla no apareció.")
        break
    
    # 3. Extraer Datos
    filas = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
    nombre_primer_jugador = ""
    
    for i, fila in enumerate(filas):
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", fila)
        time.sleep(0.05)
        cols = fila.find_elements(By.TAG_NAME, 'td')
        if len(cols) >= 10:
            nombre = cols[2].get_attribute('textContent').strip()
            if i == 0: nombre_primer_jugador = nombre
            
            try: equipo = cols[1].find_element(By.TAG_NAME, 'img').get_attribute('alt')
            except: equipo = "N/A"

            todos_los_jugadores.append({
                'equipo': equipo,
                'nombre': nombre,
                'goles': cols[3].get_attribute('textContent').strip(),
                'goles_esperados': cols[4].get_attribute('textContent').strip(),
                'regates_completados': cols[5].get_attribute('textContent').strip(),
                'entradas': cols[6].get_attribute('textContent').strip(),
                'asistencias': cols[7].get_attribute('textContent').strip(),
                'pases_precisos': cols[8].get_attribute('textContent').strip(),
                'puntuacion': cols[-1].get_attribute('textContent').strip(),
            })
    
    print(f"OK: {len(filas)} jugadores capturados.")

    # 4. Navegación
    if pagina < total_paginas:
        n_objetivo = str(pagina + 1)
        print(f"Buscando botón de página {n_objetivo}...")
        
        try:
            # Buscamos CUALQUIER botón que tenga el número exacto
            # Usamos normalize-space para limpiar espacios invisibles
            xpath_numero = f"//button[normalize-space(text())='{n_objetivo}']"
            
            # Esperamos a que el botón del número aparezca
            boton_siguiente = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_numero))
            )
            
            # Scroll y clic forzado con JavaScript
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", boton_siguiente)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", boton_siguiente)
            print(f"¡Clic enviado a la página {n_objetivo}!")

            # Espera: No seguimos hasta que el primer jugador de la tabla sea distinto
            # Esto evita que extraigamos la misma página 29 veces
            WebDriverWait(driver, 15).until(
                lambda d: d.find_elements(By.CSS_SELECTOR, 'table tbody tr td:nth-child(3)')[0].get_attribute('textContent').strip() != nombre_primer_jugador
            )
            print("Confirmado: Los datos han cambiado.")
            
        except Exception as e:
            print(f"No se pudo ir a la página {n_objetivo}. Intentando con la flecha '>'...")
            try:
                # Si el número no está (por los puntos '...'), buscamos la flecha por su dibujo SVG
                flecha = driver.find_element(By.CSS_SELECTOR, 'button:has(path[d^="M18"])')
                driver.execute_script("arguments[0].click();", flecha)
                time.sleep(3)
            except:
                print("Error fatal: No se encontró ni número ni flecha.")
                break

# 5. Guardar CSV
driver.quit()
print(f"\nFinalizado. Guardando {len(todos_los_jugadores)} jugadores...")
with open('estadisticas_premier.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['equipo', 'nombre', 'goles', 'goles_esperados', 'regates_completados', 'entradas', 'asistencias', 'pases_precisos', 'puntuacion'])
    writer.writeheader()
    writer.writerows(todos_los_jugadores)