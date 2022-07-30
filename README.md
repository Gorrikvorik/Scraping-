# Scraping-
Scraping via Scrapy
Для запуска скрипта необходимо:
 pip install -r Requirements.txt для установки библиотек 
 scrapy crawl -o apteka.csv apteka_24  в терминале запуск скрипта
 в файле apteka_spider.py в функции def parese  имеется 2 константы : 
   def parse(self, response, **kwargs):
        start = 1  # начальная страница каталога
        stop = 4  #  последняя страница каталога, 
        которые отвечают за размер количество страниц, для парсинга
        
        
