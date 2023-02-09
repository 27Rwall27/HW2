import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/tv/18347-community']
    
    def parse(self,response):
        yield scrapy.Request("https://www.themoviedb.org/tv/18347-community/cast", callback = self.parse_full_credits)
        
    def parse_full_credits(self,response): 
        for actor_link in response.css("ol.people.credits:not(ol.crew) li>a"): 
            yield scrapy.Request(response.urljoin(actor_link.attrib["href"]), callback = self.parse_actor_page)
            
    def parse_actor_page(self, response):
        actor_name = response.css("h2.title a::text").get()
        for movie_or_TV_name in response.css("div.credits_list bdi::text").getall():
            yield {
                "actor": actor_name,
                "movie_or_TV_name": movie_or_TV_name
            }
