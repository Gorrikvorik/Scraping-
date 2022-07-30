"""
Исрафилов Руслан
Тестовое задание - получения информации о товарах интернет-магазина из списка категорий по заранее заданному шаблону
"""
import scrapy
from datetime import datetime

ts = datetime.timestamp(datetime.now())


class AptekaSpider(scrapy.Spider):
    name = 'apteka_24'
    start_urls = ['https://apteka-ot-sklada.ru/catalog?start=0']

    def parse(self, response, **kwargs):
        for link  in response.css('#__layout > div > div.layout-default__page > main > section > div.goods-catalog-view__goods > div.goods-grid.conainer-ignore-mobile > div a::attr(href)').getall():
            self.name_link = link
            yield response.follow(link,  callback=self.parse_aid)
        #
        for i in range(12, 64, 12):
            next_page = f'https://apteka-ot-sklada.ru/catalog?start={i}'
            yield response.follow(next_page, callback=self.parse)

    def parse_aid(self, response):
        global sale_tag
        stock = False
        price_cur = None
        price_orig = None
        marketing_tags = []
        name =  response.css('h1.text.text_size_display-1.text_weight_bold> span::text').get()
        try:
            marketing_tags.append(response.css(
                '#__layout > div > div.layout-default__page > main > header > div.ui-breadcrumbs.text.text_weight_medium.page-header__breadcrumbs.text.text_size_caption > ul > li:nth-child(1) > a > span > span::text').get())
            marketing_tags.append(response.css(
                '#__layout > div > div.layout-default__page > main > header > div.ui-breadcrumbs.text.text_weight_medium.page-header__breadcrumbs.text.text_size_caption > ul > li:nth-child(2) > a > span > span::text').get())
            marketing_tags.append(response.css(
                '#__layout > div > div.layout-default__page > main > header > div.ui-breadcrumbs.text.text_weight_medium.page-header__breadcrumbs.text.text_size_caption > ul > li:nth-child(3) > a > span > span::text').get())
            marketing_tags.append(response.css(
                '#__layout > div > div.layout-default__page > main > header > div.ui-breadcrumbs.text.text_weight_medium.page-header__breadcrumbs.text.text_size_caption > ul > li:nth-child(4) > a > span > span::text').get())
            marketing_tags.append(response.css(
                '#__layout > div > div.layout-default__page > main > header > div.ui-breadcrumbs.text.text_weight_medium.page-header__breadcrumbs.text.text_size_caption > ul > li:nth-child(5) > a > span > span::text').get())
        except:
            pass
        try:
            if response.css(
                    '#__layout > div > div.layout-default__page > main > section:nth-child(3) > div > aside > div > div.goods-offer-panel > link').get().split()[
                2]:
                stock = True
        except:
            stock = False
        try:
            price_cur = float(response.css(
                '#__layout > div > div.layout-default__page > main > section:nth-child(3) > div > aside > div > div.goods-offer-panel > div:nth-child(1) > div.goods-offer-panel__price > span').get().split()[
                                  7])
        except:
            price_cur = None
        try:
            price_orig = float(response.css(
                '#__layout > div > div.layout-default__page > main > section:nth-child(3) > div > aside > div > div.goods-offer-panel > div:nth-child(1) > div.goods-offer-panel__price > span.goods-offer-panel__cost.goods-offer-panel__cost_old.text.text_size_title.text_weight_medium').get().split()[
                                   8])
        except:
            price_orig = None
        if price_orig and price_cur:
            sale_tag = int(((price_orig - price_cur) / price_orig) * 100)
        else:
            sale_tag = None
        try:
            volume = response.css('h1.text.text_size_display-1.text_weight_bold> span::text').re('\d+\w{1,2}')[0]
        except:
            volume = None
        try:
            main_image = response.css(
                '#__layout > div > div.layout-default__page > main > section:nth-child(3) > div > div.goods-gallery.goods-details-page__gallery.goods-details-page__details-part.content-section-small > div.goods-gallery__view > div.goods-gallery__active-picture-area.goods-gallery__active-picture-area_gallery_trigger > img::attr(src)').get()
        except:
            main_image = None

        set_images = None

        try:
            __description = response.css('#description > div > div.ui-collapsed-content__content > div > p:nth-child(1)::text').extract()
        except:
            __description =None
        result_dict = {
            "timestamp": ts,
            "url": self.name_link,
            "title": {'Название':name,
                      'Объем': volume},
            'marketing_tags': marketing_tags,
            'price_data': {
                'current': price_cur,
                'orignial': price_orig,
                'sale_tag': {'Скидка': f'{sale_tag}%'}
            },
            "stock": {
                "in_stock": stock,
                'count': 'Unknown'
            },
            "assets": {
                "main_image": main_image,
                "set_images": set_images,
            },
            "metadata": {
                "__description":__description
            }
        }
        #JsonStr = json.loads(json.dumps(result_dict))
        yield result_dict
