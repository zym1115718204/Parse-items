#!/user/bin/python
# -*- coding: utf-8 -*-

__author__='Mr Ming'
#codetime:2016-4-6

import urllib
import urllib2
import re
import thread
import time

#糗事百科段子爬虫
class QSBK:

    #初始化方法
    def __init__(self):
        self.pageIndex = 1
        self.user_agent='Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
        #初始化headers
        self.headers={'User-Agent':self.user_agent}
        #存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        #存放程序是否继续运行的变量
        self.enable = False

    #传入某一页的索引获得页面代码
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            #构建请求的request
            request = urllib2.Request(url,headers=self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"连接糗事百科失败，错误原因",e.reason
                return None

    #传入某一页面代码，返回本页不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败......"
            return None
        pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>.*?<h2>(.*?)</h2>.*?</a>.*?<div class'+
             '="content".*?>(.*?)<!--.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
        items=re.findall(pattern,pageCode)
        #用来储存每页的段子
        pageStories = []
        #遍历正则表达式匹配的信息
        for item in items:
            #判断是否存在图片
            haveImg = re.search("img",item[2])
            #如果不含有图片，把它加入到list中
            if not haveImg:
                #item[0]是发布者，item[1]是内容，item[3]是点赞的数量
                #print item[0],item[1],item[3]
                pageStories.append([item[0].strip(),item[1].strip(),item[3].strip()])
        return pageStories

    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        #如果当前来看的页数少于2页，则加载新的一页
        if self.enable == True:
            if len(self.stories)<2:
                #获取新的一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1
                    print 'page:',self.pageIndex-1,u'读取完毕'

    #调用该方法，每次回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页的段子
        for story in pageStories:
            #等待用户输入
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            #print u"第%s页\t发布人:%s\t点赞数:%s\n" %(page,story[0],story[1],story[2])
            print u"第%d页\t发布人:%s\n%s\n赞:%s\n" %(page,story[0],story[1],story[2])

    #开始方法
    def start(self):
        print u"正在读取糗事百科，按回车查看新段子，Q退出"
        #使变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前读到的页数加一
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)

spider = QSBK()
spider.start()


