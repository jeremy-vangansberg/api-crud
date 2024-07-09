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
        all_sessions_url = response.xpath("(//a[@class='btn btn-pricipale btn-formation'])[1]/@href")

        if not (url_rcnp and all_sessions_url):
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

        item['formacodes_name'] = response.xpath("//button[contains(normalize-space(),'Formacode(s)')]/following-sibling::div//span/text()").getall() 
        item['formacodes_code'] = response.xpath("//button[contains(normalize-space(),'Formacode(s)')]/following-sibling::div//p/text()").getall()
        
        if remaining == 0:
            all_sessions_url = response.xpath("(//a[@class='btn btn-pricipale btn-formation'])[1]/@href")
            if all_sessions_url :
                meta = {"item": item}
                yield scrapy.Request(url=all_sessions_url, meta=meta, callback=self.parse_rncp)
            else :
                yield item
        else:
            response.meta['remaining'] = remaining

    def parse_session(self, response):
        item = response.meta['item']
        item['session_name'] = response.xpath("(//a[@class='btn btn-pricipale btn-formation'])[1]")
