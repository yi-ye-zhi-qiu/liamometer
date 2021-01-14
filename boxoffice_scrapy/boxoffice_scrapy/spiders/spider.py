import scrapy
from ..items import BoxItem

class mojo_spider(scrapy.Spider):
    name = "mojo_spider"
    allowed_domains = ["boxofficemojo.com"]
    start_urls = [
        "https://www.boxofficemojo.com/year/2019/"
    ]

    for year in [2018, 2019]:
        start_urls.append("https://www.boxofficemojo.com/year/"+str(year)+"/")

    def parse(self, response):
        for tr in response.xpath('//*[@id="table"]/div/table/tr')[1:2]:
            href = tr.xpath('./td[2]/a/@href')
            url = response.urljoin(href[0].extract())
            yield scrapy.Request(url, callback=self.parse_page_contents)


    def parse_page_contents(self, response):
        item = BoxItem()
        elements = []
        for div in response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div')[0:]:
            elements.append(' '.join(div.xpath('./span[1]/text()')[0].extract().split()))
            if 'MPAA' in elements:
                m = elements.index('MPAA') + 1
                loc_MPAA = '//*[@id="a-page"]/main/div/div[3]/div[4]/div[{}]/span[2]/text()'.format(m)
                item["MPAA"] = response.xpath(loc_MPAA)[0].extract()
            else:
                item["MPAA"] = "N/A"

        item['title'] = response.xpath('//*[@id="a-page"]/main/div/div[1]/div[1]/div/div/div[2]/h1/text()')[0].extract()
        item['domestic_revenue'] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[1]/div/div[1]/span[2]/span/text()')[0].extract()
        item['world_revenue'] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[1]/div/div[3]/span[2]/a/span/text()')[0].extract()
        item['distributor'] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div[1]/span[2]/text()')[0].extract()
        item['opening_revenue'] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div[2]/span[2]/span/text()')[0].extract()
        item['opening_theaters'] = ' '.join(response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div[2]/span[2]/text()')[0].extract().split())
        item['budget'] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div[3]/span[2]/span/text()')[0].extract()
        item['genres'] = ','.join(response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div[7]/span[2]/text()')[0].extract().split())
        item['release_days'] = response.xpath('//*[@id="a-page"]/main/div/div[3]/div[4]/div[4]/span[2]/a/text()')[0].extract()
        yield item



# # ------------ TESTING OUR SCRAPY: ------------
#
# #urls follow pattern of https://www.boxofficemojo.com/release/rl2708702721/?ref_=bo_yld_table_1
# #use scrapy shell to debug w/out having to run the entire spider
# #EXAMPLE:
# scrapy shell "https://www.boxofficemojo.com/year/2017/"
# #find xpath of each href
# response.xpath('//*[@id="table"]/div/table/tr[2]/td[2]/a/@href')[0].extract()
# #returns: '/release/rl1182631425/?ref_=bo_yld_table_1'
# response.urljoin('/release/rl1182631425/?ref_=bo_yld_table_1')
# #returns: 'https://www.boxofficemojo.com/release/rl2708702721/? ref_=bo_yld_table_1'
#scrapy shell 'https://www.boxofficemojo.com/release/rl2708702721/? ref_=bo_yld_table_1'
#response.xpath('') this is how you test if your xpath works without having to run the spider each time