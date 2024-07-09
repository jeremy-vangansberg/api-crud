import scrapy
from simplon_formation.items import SimplonFormationItem

class FormationsSpider(scrapy.Spider):
    name = "formations"
    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html#nos-formations0"]
    custom_settings = {
        'ITEM_PIPELINES' : {
            "simplon_formation.pipelines.Cleaning": 300,
            "simplon_formation.pipelines.FormationSaving": 400,
        }
    }

    def parse(self, response):
        # Parcours de tous les liens découvrez la formation
        formation_urls = response.xpath("//div[@class='card-group-button']/a[contains(text(), 'Découvrez')]/@href").getall()

        for formation_url in formation_urls:
            yield scrapy.Request(formation_url, callback=self.parse_formation)

    def parse_formation(self, response):
        item = SimplonFormationItem()
        item['name'] = response.xpath("//h1/text()").get()
        item['url'] = response.url
        url_rcnp = response.xpath("//a[contains(@href,'francecompetences.fr')]/@href").getall()

        if not url_rcnp :
            yield item

        elif url_rcnp :
            meta = {"item": item, "remaining": len(url_rcnp)}
            for url in url_rcnp:
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_rncp)
        else:
            pass
            
    def parse_rncp(self, response):
        item = response.meta['item']
        remaining = response.meta['remaining'] - 1

        formacodes_name = response.xpath("//button[contains(normalize-space(),'Formacode(s)')]/following-sibling::div//span/text()").getall() 
        formacodes_code = response.xpath("//button[contains(normalize-space(),'Formacode(s)')]/following-sibling::div//p/text()").getall()

        item.setdefault('formacodes_name', []).extend(formacodes_name)
        item.setdefault('formacodes_code', []).extend(formacodes_code)

        # item['formacodes_name'] = formacodes_name
        # item['formacodes_code'] = formacodes_code


        
        if remaining == 0:
            yield item
        else:
            response.meta['remaining'] = remaining

