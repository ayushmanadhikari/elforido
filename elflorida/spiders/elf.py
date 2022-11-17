import scrapy
import json
from urllib.parse import urlencode
from elflorida.items import ElfloridaItem
import datetime



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


        raw_data = response.body
        data = json.loads(raw_data)
        data = data['data']
        product = {}
        for d in data:
            product['Date'] = datetime.datetime.now().strftime('%d/%m/%Y')
            product['Canal'] = ""
            product['Category'] = d['categoryName']
            product['Subcategory'] = d['subcategoryName']


            #gets sub categories
            subs_list = product['Subcategory'].split(",")
            count = 0
            for sub in subs_list:
                count = count + 1
                col1 = f"Subcategory{count}"
                product[col1] = sub           
            del product['Subcategory']


            product['Marca'] = ""
            product['Modelo'] = ""
            product['SKU'] = d['slug']
            product['UPC'] = d['slug']
            product['Item'] = d['productName']
            product['Item Characteristics'] = d['productDescription']
            product['URL SKU'] = "https://tienda.elflorido.com.mx/productos/"+str(d['productId'])
            product['Image'] = d['mediaUrl']
            product['Price'] = d['priceTotal']
            product['Sale Price'] = ""
            product['Shipment Cost'] = ""
            product['SaleFlag'] = ""
            product['Store ID'] = ""
            product['Store Name'] = ""
            product['Store Address'] = ""
            product['Stock'] = d['stock']
            product['UPC WM'] = ""
            product['Final Price'] = d['priceTotal']
            product['productId'] = d['productId']
        

            
            yield product

            # https://tienda.elflorido.com.mx:4433/Search/GetVariants?productId=8171&siteId=136

            # sale_flag_url = "https://tienda.elflorido.com.mx/productos/"+str(d['productId'])
            # yield scrapy.Request(url=sale_flag_url, callback=self.parse_product, meta={'product': product})

    # def parse_product(self, response):
    #     product = response.meta.get('product')
    #     d = product
    #     api_url = "https://tienda.elflorido.com.mx:4433/Search/GetVariants?"+urlencode({'productId': d['productId'], 'siteId': 136})
    #     print(api_url)
    #     yield scrapy.Request(url=api_url, callback=self.parse_sale_flag, meta = {'products': product})
    


    # def parse_sale_flag(self, response):
    #     raw_data = response.body
    #     data = json.loads(raw_data)
    #     print(data)
    #     # sale_flag = f"Lleva {data['stock']} o más por ${data['unitPrice']}/PIEZA"
    #     # product = response.meta.get('product')

    #     # product['SaleFlag'] = sale_flag

    #     # yield product

    #     # api_url = "https://tienda.elflorido.com.mx:4433/Search/GetVariants?"+urlencode({'productId': d['productId'], 'siteId': d['siteId'] })
    #     # api_url = "https://tienda.elflorido.com.mx:4433/Search/GetVariants?productId=13643&siteId=136"

        


   
