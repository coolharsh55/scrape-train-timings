import scrapy

from learn.items import Train


class LearnSpider(scrapy.Spider):

    """spider to crawl DOWN locals at punediary
    """

    name = 'down_spider'
    allowed_domains = ['punediary.com', ]
    start_urls = [
        "http://www.punediary.com/html/downside_local.html",
    ]

    def parse(self, response):
        """parse html to retrieve data in a table

        The DOM tree is weird, it contains WAY too many
        tables than is reasonable
        What works is:
            div->table->tr->td->table->tr
                gives each train timing row for a station
            td->b->font OR td->font->b
                gives the station name
            td->font
                gives the train timing at that station
        """
        for sel in response.xpath('//div/table/tr/td/table/tr'):
            train = Train()
            train['station'] = None
            train['stops'] = []

            for x in sel.xpath('td'):
                if x.xpath('b/font'):
                    train['station'] = x.xpath('b/font/text()').extract()[0]
                elif x.xpath('font/b'):
                    train['station'] = x.xpath('font/b/text()').extract()[0]
                elif x.xpath('font'):
                    train['stops'].append(x.xpath('font/text()').extract()[0])
                else:
                    train['stops'].append('DOES_NOT_STOP')

            if train['station']:
                """return only if we have a valid train timing row
                other matching rows can also exist
                but they will not have a station name param
                """
                yield train
