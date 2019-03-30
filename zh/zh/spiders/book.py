# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from zh.items import ZhItem

class BookSpider(CrawlSpider):
    name = 'book'
    # allowed_domains = ['book.zongheng.com']
    start_urls = ['http://book.zongheng.com/store/']
    for offset in range(1,1000):
        url = 'http://book.zongheng.com/store/c0/c0/b0/u0/p{0}/v9/s9/t0/u0/i1/ALL.html'.format(str(offset))
        start_urls.append(url)


    rules = (
        #匹配符合条件的所有页面
        Rule(LinkExtractor(allow=(r'http://book.zongheng.com/store/c0/c0/b0/u0/p(\d+)/v9/s9/t0/u0/i1/ALL\.html')),follow=True),      #
        #匹配子页面详情信息
        Rule(LinkExtractor(allow=r'http://book.zongheng.com/book/(\d+)\.html'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        item=ZhItem()

        item['book_name']=self.get_book_name(response)
        item['state'] = self.get_state(response)
        item['type'] = self.get_type(response)
        item['label'] = self.get_label(response)
        item['author'] = self.get_author(response)
        item['number'] = self.get_number(response)
        item['about'] = self.get_about(response)
        item['news'] = self.get_news(response)
        item['photo'] = self.get_photo(response)

        yield item

        #//div[@class="book-name"]/text()
        # //div[@class="book-label"]/a[@class="state"]/text()
        # //div[@class="book-label"]/a[@class="label"]/text()
        # //div[@class="book-label"]/span/a/text()      可能为多个，需要string
        #//div[@class="au-name"]/a/text()               作者
        # //div[@class="au-words"]/span/i/text()        字数需要处理
        # //div[@class="book-info"]/div[@class="book-dec Jbook-dec hide"]/p/text()
        # //div[@class="book-new-chapter"]/div/a/text()
        # //div[@class="book-img fl"]/img/@src





    def get_book_name(self,response):
        book_name=response.xpath('//div[@class="book-name"]/text()').extract()[0]
        if len(book_name)>0:
            book_name=book_name.strip()
        else:
            book_name='NULL'
        return book_name

    def get_state(self,response):
        state=response.xpath('//div[@class="book-label"]/a[@class="state"]/text()').extract()[0]
        if len(state)>0:
            state=state.strip()
        else:
            state='NULL'
        return state

    def get_type(self,response):
        type=response.xpath('//div[@class="book-label"]/a[@class="label"]/text()').extract()[0]
        if len(type)>0:
            type=type.strip()
        else:
            type='NULL'
        return type

    def get_label(self,response):
        label=response.xpath('//div[@class="book-label"]/span/a/text()')
        if len(label)>0:
            label=response.xpath('//div[@class="book-label"]/span/a/text()').extract()
            s=''        #获取列表全部数据，并转化为字符串形式
            for la in label:
                s+=' '+la
            label=s
        else:
            label='NULL'
        return label

    def get_author(self,response):
        author=response.xpath('//div[@class="au-name"]/a/text()').extract()[0]
        if len(author)>0:
            author=author.strip()
        else:
            author='NULL'
        return author

    def get_number(self,response):
        number=response.xpath('//div[@class="au-words"]/span/i/text()').extract()[1]
        if len(number)>0:
            number=number.strip()
        else:
            number='NULL'
        return number

    def get_about(self,response):
        about=response.xpath('//div[@class="book-info"]/div[@class="book-dec Jbook-dec hide"]/p/text()').extract()[0]
        if len(about)>0:
            about=about.strip()
        else:
            about='NULL'
        return about

    def get_news(self,response):
        news=response.xpath('//div[@class="book-new-chapter"]/div/a/text()').extract()[0]
        if len(news)>0:
            news=news.strip()
        else:
            news='NULL'
        return news

    def get_photo(self,response):
        photo=response.xpath('//div[@class="book-img fl"]/img/@src').extract()[0]
        if len(photo)>0:
            photo=photo.strip()
        else:
            photo='NULL'
        return photo

