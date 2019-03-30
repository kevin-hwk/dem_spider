# -*- coding: utf-8 -*-
import scrapy
from car.items import CarItem

class SuvSpider(scrapy.Spider):
    name = 'suv'
    # allowed_domains = ['price.pcauto.com.cn']         #此处最好注释掉，否者可能无法爬取翻页后的数据
    offset=1                #为页面偏移量 用于拼接新url
    url='https://price.pcauto.com.cn/top/k75-p{0}.html'.format(str(offset))
    start_urls = [url]      #爬虫起始站点，仅执行一次

    def parse(self, response):
        item=CarItem()      #实例化的一个数据字典对象用于存储数据
        car=response.xpath('//div[@class="tbA"]/ul/li')    #当前页20个节点对象

        for each in car:    #遍历并取其对应节点数据值

            item['ranking']=each.xpath('./span/text()').extract()[0]
            item['car_name']=each.xpath('./div[@class="info"]/p[@class="sname"]/a/text()').extract()[0]
            item['price']=each.xpath('./div[@class="info"]/p[@class="col col1 price"]/em/text()').extract()[0]
            item['hot']=each.xpath('./div[@class="info"]/p[@class="col rank"]/span[@class="fl red rd-mark"]/text()').extract()[0]
            item['brand']=each.xpath('./div[@class="info"]/p[@class="col col1"][1]/text()').extract()[0]
            item['style']=each.xpath('./div[@class="info"]/p[@class="col"][1]/text()').extract()[0]
            item['dispt']=each.xpath('./div[@class="info"]/p[@class="col col1"]/em')
            item['gear'] = each.xpath('./div[@class="info"]/p[@class="col"]/em')

            # dispt排量、gear变速箱的值可能为空，直接赋值可能抛异常，必须对其判断后在赋值
            if len(item['dispt'])!=0:
                item['dispt'] =each.xpath('./div[@class="info"]/p[@class="col col1"]/em')[0].xpath('string(.)').extract()[0]
            else:
                item['dispt']='暂无信息'

            if len(item['gear']) != 0:
                item['gear'] = each.xpath('./div[@class="info"]/p[@class="col"]/em')[0].xpath('string(.)').extract()[0]
            else:
                item['gear'] = '暂无信息'

            yield item          #返回字典携带的数据

        if self.offset<30:      #获取后续页面数据
            self.offset+=1
            url = 'https://price.pcauto.com.cn/top/k75-p{0}.html'.format(str(self.offset))
            self.url=url
            yield scrapy.Request(self.url,callback=self.parse)      #递归调用，发送请求

