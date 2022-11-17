import scrapy
import json
from urllib.parse import urlencode
from elflorida.items import ElfloridaItem




class ElfSpider(scrapy.Spider):
    name = 'elf'


    def start_requests(self):
        start_url = "https://tienda.elflorido.com.mx:4433/Search/Categories"
        yield scrapy.Request(url=start_url, callback=self.parse)


    def parse(self, response):
        categories_raw_data = response.body
        categories_data = json.loads(categories_raw_data)   
        data = categories_data['data']
        for d in data:
            name_cat = d['name']
            category_id = d['categoryId']
            print(f"categoryId: .........."+str(d['categoryId'])+": "+name_cat)
            sub_categories = d['subcategories']
            for sub in sub_categories:
                name_subcat = sub['name']
                sub_category_id = sub['subcategoryId']
                print(f"subCategoryId: "+str(sub_category_id)+":  "+name_subcat)

                category_url2 = "https://tienda.elflorido.com.mx:4433/Search/Products?search=&siteId=136&pageCount=40"+urlencode({'promos': 'false','categoryId': category_id, 'subcategoryId': sub_category_id})

                yield scrapy.Request(url=category_url2, callback=self.parse_product_list)



    def parse_product_list(self, response):
        item = ElfloridaItem()
        raw_data = response.body
        data = json.loads(raw_data)
        data = data['data']
        product = {}
        for d in data:
            product['categoryName'] = d['categoryName']
            product['subcategoryName'] = d['subcategoryName']
            product['brand'] = ""
            product['upc'] = d['slug']
            product['Item'] = d['productName']
            product['URLSKU'] = "https://tienda.elflorido.com.mx/productos/"+str(d['productId'])
            product['Image'] = d['mediaUrl']
            product['Price'] = d['priceTotal']
            product['SalePrice'] = ""
            product['SaleFlag'] = ""
            product['stock'] = d['stock']
            product['productDescription'] = d['productDescription']

            yield product
            



        


   