import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider' #Names the spider
    
    start_urls = ['https://www.themoviedb.org/tv/18347-community'] #Sets the starting page for the spider
    
    def parse(self,response):
        "Parses the cast page of the Community TV show and recursively calls the parse_full_credits function"
        "args: css response varaible"
        "returns: none"
        yield scrapy.Request("https://www.themoviedb.org/tv/18347-community/cast", callback = self.parse_full_credits)
        
    def parse_full_credits(self,response): 
        "Loops through each actor in the cast page and recursively calls the parse_full_credits"
        "args: css response varaible"
        "returns: none"
        #Gets all the links to the actor's profile page
        for actor_link in response.css("ol.people.credits:not(ol.crew) li>a"): 
            #sends a request to the actor's profile page link and recersively calls the parse_actor_page function
            yield scrapy.Request(response.urljoin(actor_link.attrib["href"]), callback = self.parse_actor_page)
            
    def parse_actor_page(self, response):
        "Loops through each movie in the actors page and yields a dictonary with the actors name and each movie he/she stars in"
        "args: css response varaible"
        "returns: none"
        #Gets the name of the actor
        actor_name = response.css("h2.title a::text").get()
        #Loops through each movie/tv show the actor stars in and yields a dictonary
        for movie_or_TV_name in response.css("div.credits_list bdi::text").getall():
            yield {
                "actor": actor_name,
                "movie_or_TV_name": movie_or_TV_name
            }
