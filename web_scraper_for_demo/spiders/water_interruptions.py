import scrapy
from datetime import datetime
import logging
import re
from scrapy.utils.project import get_project_settings

# configure a specific logger
logger = logging.getLogger("WaterInterruptionsSpider")
interruptions_log_file = get_project_settings().get("WATER_INTERRUPTIONS_LOG_FILE")
filehandler = logging.FileHandler(interruptions_log_file)
filehandler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(filehandler)

class WaterInterruptionsSpider(scrapy.Spider):
    name = "water_interruptions"
    allowed_domains = ["www.casomes.ro"]
    start_urls = ["http://www.casomes.ro/"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

    def parse(self, response):
        interruption_page_urls = response.css("a.cat_bg_intreruperi-apa::attr('href')").getall()

        for url in interruption_page_urls:
            logger.info(f"scraping site {url}")
            yield scrapy.Request(url, callback=self.parseArticle)


    def parseArticle(self, response):
        date_string = response.css(".post-date::text").get()

        article_date: datetime = datetime.strptime(date_string, "%B %d, %Y")
        print(article_date)

        if (article_date.date() != datetime.now().date()):
            logger.info(f'article on {response.request.url} is older, skipping scraping')
            return

        logger.info(f'scraping article {response.request.url}, posted on {article_date}')

        text = response.css(".content-column-content > article:nth-child(1) ::text").getall()
        text = "".join(text).strip().lower()

        search_pattern = r'buna ziua|bună ziua|fagului|becas|becaș|craiova'

        if (re.match(search_pattern, text)):
            logger.info(f"found matches in text for pattern '{search_pattern}', better be careful:\n{text}")
        else:
            logger.info(f"no worries, no matches found for pattern \'{search_pattern}\'")
        return

