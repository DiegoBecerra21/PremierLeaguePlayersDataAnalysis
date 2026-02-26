import scrapy
from PlayerStats.items import PlayerstatsItem

class SofascoreStatsSpider(scrapy.Spider):
    name = "sofascore_stats"
    allowed_domains = ["sofascore.com"]
    start_urls = [
        "https://www.sofascore.com/es-la/football/tournament/england/premier-league/17#id:61627,tab:stats"
    ]

    def parse(self, response):
        players = response.css('table thead tr th')

        # Hay 10 columnas en total en las páginas de la San Silvestre:
            # Col 1: Vacía (Invisible)
            # Col 2: Equipo
            # Col 3: Nombre
            # Col 4: Goles
            # Col 5: Goles Esperados
            # Col 6: Regates Completados
            # Col 7: Entradas
            # Col 8: Asistencias
            # Col 9: Pases Precisos
            # Col 10: Puntuación
        
        for player in players:
            item = PlayerstatsItem()
            item['equipo'] = player.css('th:nth-child(2):text').get()
            item['nombre'] = player.css('th:nth-child(3)::text').get()
            item['goles'] = player.css('th:nth-child(4)::text').get()
            item['goles_esperados'] = player.css('th:nth-child(5)::text').get()
            item['regates_completados'] = player.css('th:nth-child(6)::text').get()
            item['entradas'] = player.css('th:nth-child(7)::text').get()
            item['asistencias'] = player.css('th:nth-child(8)::text').get()
            item['pases_precisos'] = player.css('th:nth-child(9)::text').get()
            item['puntuacion'] = player.css('th:nth-child(10)::text').get()
            
            yield item

        # Selector de paginación
        # Usamos XPath para buscar un boton hasta que el botón de avanzar página esté desactivado"
        # Para saber si existe este botón hacemos lo siguiente:
               
        
        
        if next_page:
            # response.follow fusiona automáticamente la URL actual con "?page=x"
            yield response.follow(next_page, callback=self.parse, meta={'anio_carrera': anio})