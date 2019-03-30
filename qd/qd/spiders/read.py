# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qd.items import QdItem
import re,requests
from scrapy_redis.spiders import RedisCrawlSpider


class ReadSpider(RedisCrawlSpider):
    name = 'read'
    # allowed_domains = ['qidian.com']
    # start_urls = ['https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=1']
    redis_key = 'readspider:start_urls'     #readis_spider项目启动命令

    #动态域范围获取
    def __init__(self,*args,**kwargs):
        domain=kwargs.pop('domain','')
        self.allowed_domains=filter(None,domain.split(','))
        super(ReadSpider,self).__init__(*args,**kwargs)

    rules = (
        #匹配全部主页面的url规则  深度爬取子页面
        Rule(LinkExtractor(allow=(r'https://www.qidian.com/all\?orderId=\&style=1\&pageSize=20\&siteid=1\&pubflag=0\&hiddenField=0\&page=(\d+)')),follow=True),
        #匹配详情页面 不作深度爬取
        Rule(LinkExtractor(allow=r'https://book.qidian.com/info/(\d+)'), callback='parse_item', follow=False,),
    )

    def parse_item(self, response):
        item=QdItem()

        item['book_name']=self.get_book_name(response)
        item['author']=self.get_author(response)
        item['state']=self.get_state(response)
        item['type']=self.get_type(response)
        item['about']=self.get_about(response)
        # item['number']=self.get_number(response)
        item['score']=self.get_score(response)
        item['story']=self.get_story(response)
        item['news']=self.get_news(response)
        item['photo']=self.get_photo(response)

        yield item

    def get_book_name(self,response):

        book_name=response.xpath('//h1/em/text()').extract()[0]
        if len(book_name)>0:
            book_name=book_name.strip()
        else:
            book_name='NULL'
        return book_name

    def get_author(self,response):
        author=response.xpath('//h1/span/a/text()').extract()[0]
        if len(author)>0:
            author=author.strip()
        else:
            author='NULL'
        return author

    def get_state(self,response):
        state=response.xpath('//p[@class="tag"]/span/text()').extract()[0]
        if len(state)>0:
            state=state.strip()
        else:
            st='NULL'
        return state

    def get_type(self,response):
        type=response.xpath('//p[@class="tag"]/a/text()').extract()
        if len(type)>0:
            t=""
            for i in type:
                t+=' '+i
            type=t
        else:
            type='NULL'
        return type

    def get_about(self,response):
        about=response.xpath('//p[@class="intro"]/text()').extract()[0]
        if len(about)>0:
            about=about.strip()
        else:
            about='NULL'
        return about

    # def get_number(self,response):
    #
    #     def get_font(url):      #获取字体对应的字典编码
    #         time.sleep(2)
    #         resp=requests.get(url)
    #         font=TTFont(BytesIO(resp.content))
    #         cmap=font.getBestCmap()
    #         font.close()
    #         return cmap
    #
    #     def get_encode(cmap,values):
    #         #values的值    '&#100054;&#100056;&#100053;&#100052;&#100046;&#100046;'
    #         #中英数字编码表
    #         WORD_MAP = {'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6',
    #                     'seven': '7','eight': '8', 'nine': '9', 'period': '.'}
    #         list=values.split(';')
    #         list.pop(-1)
    #         new_num=''
    #         #移除最后的分号；
    #         for num in list:
    #             value=num[2:]
    #             key=cmap[int(value)]
    #             new_num+=WORD_MAP[key]
    #         return new_num
    #
    #     # pattern=re.compile('</style><span.*?>(.*?)</span>',re.S)           #数字字符匹配规则
    #     # # &#100054;&#100056;&#100053;&#100052;&#100046;&#100046;
    #     # number_list=re.findall(pattern,response)
    #     # #匹配所有数字字符列表
    #     # reg=re.compile('<style.*?>(.*?)\s*</style>',re.S)                  #包含字体链接的文本
    #     # font_url=re.findall(reg,response)[0]
    #     # url=re.search('woff.*?url.*?\'(.+?)\'.*?truetype',font_url).group(1)        #获取当前数字库的链接地址
    #     # # https://qidian.gtimg.com/qd_anti_spider/xxxxx.ttf
    #     #
    #     # cmap=get_font(url)          #获取字典对应编码
    #     # #   {100046: 'seven', 100048: 'three', 100049: 'five', 100050: 'six', 100051: 'one', 100052: 'period', 100053: 'nine', 100054: 'four', 100055: 'eight', 100056: 'two', 100057: 'zero'}
    #     #
    #     #
    #     # d_num=[]                    #解码后的所有数字追加进去
    #     # for num in number_list:     #遍历列表中的元素
    #     #     d_num.append(get_encode(cmap,num))
    #     # if len(d_num)>0:
    #     #     return d_num[0]+'万字'
    #     # else:
    #     return 'NULL'

    def get_score(self,response):

        def get_sc(id):
            urll = 'https://book.qidian.com/ajax/comment/index?_csrfToken=ziKrBzt4NggZbkfyUMDwZvGH0X0wtrO5RdEGbI9w&bookId=' + id + '&pageSize=15'
            rr = requests.get(urll)
            # print(rr)
            score = rr.text[16:19]
            return score

        bid=response.xpath('//a[@id="bookImg"]/@data-bid').extract()[0]         #获取书的id
        if len(bid)>0:
            score=get_sc(bid)           #调用方法获取评分 若是整数 可能返回 9，"
            if score[1]==',':
                score=score.replace(',"',".0")
            else:
                score=score

        else:
            score='NULL'
        return score

    def get_story(self,response):
        story=response.xpath('//div[@class="book-intro"]/p/text()').extract()[0]
        if len(story)>0:
            story=story.strip()
        else:
            story='NULL'
        return story

    def get_news(self,response):
        news=response.xpath('//div[@class="detail"]/p[@class="cf"]/a/text()').extract()[0]
        if len(news)>0:
            news=news.strip()
        else:
            news='NULL'
        return news

    def get_photo(self,response):
        photo=response.xpath('//div[@class="book-img"]/a[@class="J-getJumpUrl"]/img/@src').extract()[0]
        if len(photo)>0:
            photo=photo.strip()
        else:
            photo='NULL'
        return photo

