# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayerstatsItem(scrapy.Item):
    equipo = scrapy.Field()
    nombre = scrapy.Field()
    goles = scrapy.Field()
    goles_esperados = scrapy.Field()
    regates_completados = scrapy.Field()
    entradas = scrapy.Field()
    asistencias = scrapy.Field()
    pases_precisos = scrapy.Field()
    puntuacion = scrapy.Field()
    
