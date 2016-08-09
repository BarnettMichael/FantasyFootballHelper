from scrapy.spiders import Spider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from FFHelper.items import PlayerItem


    
class FFToday(Spider):
    """Spider to get player data from FFtoday.com"""
    name = 'fftoday'
    current_year = '2015'
    allowed_domains = ['fftoday.com/']
    def fftoday_url_generator(playerstart, playerend, teamstart, teamend):
        assert type(playerstart) == type(playerend) == type(teamstart) == type(teamend) == int
        urllist = []
        for x in xrange(playerstart, playerend):
            url = 'http://fftoday.com/stats/players/%d' % x
            urllist.append(url)
            
        for x in xrange(teamstart, teamend):
            url = 'http://fftoday.com/stats/players?TeamID=%d' % x
            urllist.append(url)
            
        return urllist
    
    #brute_start_urls = fftoday_url_generator(0, 1, 9000, 9032)
    
    #start_urls = brute_start_urls
    
    #start_urls = [
                  # 'http://fftoday.com/stats/players/2645',
                  # 'http://fftoday.com/stats/players/2710',
                  # 'http://fftoday.com/stats/players/2755',
                  # 'http://fftoday.com/stats/players/2945',
                  # 'http://fftoday.com/stats/players/12250',
                  # 'http://fftoday.com/stats/players/12329',
                  # 'http://fftoday.com/stats/players/12342',
                  # 'http://fftoday.com/stats/players/12370',
                  # 'http://fftoday.com/stats/players/12512',
                  # 'http://fftoday.com/stats/players/12842',
                  # 'http://fftoday.com/stats/players/13033',
                  # 'http://fftoday.com/stats/players/13093',
                  # 'http://fftoday.com/stats/players/13128',
                  # 'http://fftoday.com/stats/players/13135',
                  # 'http://fftoday.com/stats/players/13174',
                  # 'http://fftoday.com/stats/players/13213',
                  # 'http://fftoday.com/stats/players/13350',
                  # 'http://fftoday.com/stats/players/14143',
                  # 'http://fftoday.com/stats/players/14393',
                  # 'http://fftoday.com/stats/players/14405',
                  # 'http://fftoday.com/stats/players/14579',
                  # 'http://fftoday.com/stats/players/14580',
                  # 'http://fftoday.com/stats/players/15009',
                  # 'http://fftoday.com/stats/players/15053',
                  # 'http://fftoday.com/stats/players/15136',
                  # 'http://fftoday.com/stats/players/15156',
                  # 'http://fftoday.com/stats/players/15201',
                  # 'http://fftoday.com/stats/players/15346',
                  # ]
    rules = [Rule(LinkExtractor(allow=['/players/\d+']), 'parse', follow=True)]
    
    def parse(self, response):
        
        selector = Selector(response)
        loader = ItemLoader(item=PlayerItem(), selector = selector)
        
        last_year_played = selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last()]/td[1]/text()').extract()
        playername = selector.xpath('//tr/td[@class="pageheader"]//text()').extract()
        
        try:
            position = selector.xpath('//table[4]/tr[2]/td[1]/table[7]/tr[2]/td[2]/table/tr/td/table/tr[2]/td[2]/text()').extract()
            position = position[0].rstrip('0123456789 ').upper()
        except:
            position = selector.xpath('//table[4]/tr[2]/td[1]/table[2]/tr[3]/td/text()').extract()
            position = position[0].lstrip('0123456789 ').upper()[0:7]
        
        if self.current_year in last_year_played[0] and position in ['DEFENSE', 'QB', 'RB', 'WR', 'TE', 'K']:
        
            if position == 'DEFENSE':
                loader.add_value('name', selector.xpath('//tr/td[@class="pageheader"]//text()').extract())
                loader.add_value('player_url', response.url)
                loader.add_value('position', selector.xpath('//table[4]/tr[2]/td[1]/table[2]/tr[3]/td/text()').extract())
                loader.add_value('points_one_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 1]/td[12]/text()').extract())
                loader.add_value('points_two_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 2]/td[12]/text()').extract())
                loader.add_value('points_three_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 3]/td[12]/text()').extract())
                return loader.load_item()        
                    
            else:
                loader.add_value('name', selector.xpath('//tr/td[@class="pageheader"]//text()').extract())
                loader.add_value('player_url', response.url)
                for x in xrange(1, 11):
                    foundname = selector.xpath('//table[4]/tr[2]/td[1]/table[7]/tr[2]/td[2]/table/tr/td/table/tr[%d]/td[3]/text()' % x).extract()
                    try:
                        foundname[0].strip() == playername[0].strip()
                        if foundname[0].strip() == playername[0].strip():
                            loader.add_value('position', selector.xpath('//table[4]/tr[2]/td[1]/table[7]/tr[2]/td[2]/table/tr/td/table/tr[%d]/td[2]/text()' % x).extract())
                    except:
                        pass
                loader.add_value('age', selector.xpath('//table[4]/tr[2]/td[1]/table[4]/tr/td/text()[6]').extract())
            
                loader.add_value('current_team', selector.xpath('//table[4]//tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last()]/td[2]/text()').extract())
                loader.add_value('team_one_year_ago', selector.xpath('///table[4]//tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 1]/td[2]/text()').extract())
                loader.add_value('team_two_year_ago', selector.xpath('//table[4]//tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 2]/td[2]/text()').extract())
                loader.add_value('team_three_year_ago', selector.xpath('//table[4]//tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 3]/td[2]/text()').extract())
        
            if position == 'QB':
                loader.add_value('points_one_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 1]/td[15]/text()').extract())
                loader.add_value('points_two_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 2]/td[15]/text()').extract())
                loader.add_value('points_three_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 3]/td[15]/text()').extract())
                return loader.load_item()
        
            elif position == 'RB' or position == 'WR':
                loader.add_value('points_one_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 1]/td[14]/text()').extract())
                loader.add_value('points_two_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 2]/td[14]/text()').extract())
                loader.add_value('points_three_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 3]/td[14]/text()').extract())
                return loader.load_item()
        
            elif position == 'TE':
                loader.add_value('points_one_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 1]/td[10]/text()').extract())
                loader.add_value('points_two_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 2]/td[10]/text()').extract())
                loader.add_value('points_three_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 3]/td[10]/text()').extract())
                return loader.load_item()
            
            elif position == 'K':
                loader.add_value('points_one_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 1]/td[9]/text()').extract())
                loader.add_value('points_two_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 2]/td[9]/text()').extract())
                loader.add_value('points_three_year_ago', selector.xpath('//table[4]/tr[2]/td[1]/table[6]/tr/td/table/tr[position() = last() - 3]/td[9]/text()').extract())
                return loader.load_item()
                
        else:
            print "2015 not last year played or wrong position"
            print last_year_played[0]
            print position
            print playername, " skipped."