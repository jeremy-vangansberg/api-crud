import scrapy
from simplon_formation.items import SimplonFormationItem

class FormationsSpider(scrapy.Spider):
    name = "sessions"
    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html#nos-formations0"]

    def parse(self, response):
        # Parcours de tous les liens découvrez la formation
        formation_urls = response.xpath("//div[@class='card-group-button']/a[contains(text(), 'Découvrez')]/@href").getall()

        for formation_url in formation_urls:
            yield scrapy.Request(formation_url, callback=self.parse_formation)

    def parse_formation(self, response):
        item = SimplonFormationItem()
        item['name'] = response.xpath("//h1/text()").get()
        item['url'] = response.url
        all_sessions_url = response.xpath("(//a[@class='btn btn-pricipale btn-formation'])[1]/@href").get()

        if  all_sessions_url:
            meta = {"item": item}
            yield scrapy.Request(url=all_sessions_url, meta=meta, callback=self.parse_session)
            

    def parse_session(self, response):
        item = response.meta['item']
        sessions = response.xpath("//div[@class='smp-card']")
        for session in sessions : 
            item['session_name'] = session.xpath(".//h2/text()").get()
            day = session.xpath(".//span[@class='day']/text()").get().strip()
            month = session.xpath(".//span[@class='month']/text()").get().strip()
            year = session.xpath(".//div[@class='year']/text()").get().strip()
            item['date_limite_candidature'] = f"{day}/{month}/{year}"
            item['alternance'] = True if session.xpath(".//a[contains(text(),'lternance')]/text()") else False
            item['date_debut'] = session.xpath(".//div[@class='card-session-info calendar']/text()").getall()
            item['duree'] = session.xpath(".//i[contains(text(),'hourglass_empty')]/parent::div/text()").getall()
            item['location'] = session.xpath(".//i[contains(text(),'location')]/parent::div/text()").getall()
            item['niveau'] = session.xpath(".//i[contains(text(),'school')]/parent::div/text()").getall()

            yield item
                
