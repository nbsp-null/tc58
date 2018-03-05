# -*- coding: utf-8 -*-
import scrapy
import re
import time
import pdb
from tc_58.items import  Tc58Item
class getst():
	dic={'五险一金':1,'包吃':2,'包住':5,'年底双薪':10,'加班补助':20,'周末双休':40,'话补':80,'交通补助':160,'饭补':320,'房补':640}
	re=0
	def __init__(self,char):
		for s in char:	
			nm=self.dic.get(s,0)
			if nm>0:
				self.re=self.re+nm
				
class gettime():
	times=""
	def __init__(self,date):
		dates=""
		for s in date:
			dates=dates+s
		if '天' in dates and not '今' in dates:
			a=re.sub("\D","",dates)
			if a=="":
				a=0
			#print(a)
			d= time.localtime(time.time())
			ye=d.tm_year
			mon=d.tm_mon
			day=d.tm_mday
			if d.tm_mday-int(a)<=0:
				day=30-int(a)+int(d.tm_mday)
				mon=int(d.tm_mon)-1
				if mon<=0:
					ye=int(d.tm_year)-1
			self.times=str(ye)+"-"+str(mon)+"-"+str(day)
		elif '时' in dates or '分' in dates or '今' in dates :
			d= time.localtime(time.time())
			ye=d.tm_year
			mon=d.tm_mon
			day=d.tm_mday
			self.times=str(ye)+"-"+str(mon)+"-"+str(day)
		else:
			self.times=dates
		

class Demo1Spider(scrapy.Spider):
	name = 'demo1'
	area='jl'
	j_n=0
	#allowed_domains = ['http://jl.58.com/']
	start_urls = ['http://'+area+'.58.com/job.shtml']

	def parse(self, response):
		p_link=response.xpath('.//div[@class="wb-content"]//div[@class="posCont clearfix"]//div[@class="sidebar-right fl"]//ul')
		for c_link in p_link:
			c1_link=c_link.xpath('.//li//a/@href').extract()
			break_l=0
			for link in c1_link :
				if break_l==0:
					break_l=break_l+1
					continue 
				t_link='http://'+self.area+".58.com/"+link
				yield scrapy.Request(t_link,callback=self.parse_date)
			#yield scrapy.Request('http://'+self.area+".58.com/zpkafei",callback=self.parse_date)
		
	def parse_date_url(self,response):
		item=response.meta['item']
		item['job_purl']=response.url
		item['job_rn']=re.sub("\D","","".join(response.xpath('.//div[@class="con"]//div[@class="leftCon"]//div[@class="item_con pos_info"]//div[@class="pos_base_condition"]//span[@class="item_condition pad_left_none"]/text()').extract()))
		job_adr=response.xpath('.//div[@class="con"]//div[@class="leftCon"]//div[@class="item_con pos_info"]//div[@class="pos-area"]//span[2]/text()').extract()
		item['job_adr']= "NULL" if len(job_adr)<2  else job_adr[1]
		job_rl_ar=response.xpath('.//div[@class="con"]//div[@class="leftCon"]//div[@class="item_con pos_info"]//div[@class="pos-area"]//span[@class="pos_area_item"]//text()').extract()
		item['job_rl_ar']="NULL" if  len(job_rl_ar)<2 else job_rl_ar[1]
		
		item['job_jt']=response.xpath('.//div[@class="con"]//div[@class="rightCon"]//div[@class="item_con"]//div[@class="subitem_con company_baseInfo"]//div[@class="com_statistics"]//p[3]//span[1]/text()').extract_first()
		item['job_cdes']=response.xpath('.//div[@class="con"]//div[@class="leftCon"]//div[@class="item_con"]//div[@class="subitem_con comp_intro"]//div[@class="txt"]//div[@class="comIntro"]//div[@class="intro"]//div[@class="shiji"]//p/text()').extract()
		job_ci=response.xpath('.//div[@class="con"]//div[@class="leftCon"]//div[@class="item_con"]//div[@class="subitem_con comp_intro"]//div[@class="photos"]//script/text()')
		job_cii= not job_ci
		if not job_ci :
			item['job_cimdes']= "NULL"
		else:
			item['job_cimdes']= re.sub("tiny","big",re.sub("\/enterprise","http://pic1.58cdn.com.cn/enterprise",re.sub("var picList=|'|-","",job_ci.extract_first())))
		
		item['job_des']="".join(response.xpath('.//div[@class="con"]//div[@class="leftCon"]//div[@class="item_con"]//div[@class="subitem_con pos_description"]//div[@class="posDes"]//div[@class="des"]/text()').extract())
		url_c="".join(response.xpath('.//div[@class="con"]//div[@class="rightCon"]//div[@class="item_con"]//div[@class="subitem_con company_baseInfo"]//div[@class="comp_baseInfo_title"]//div[@class="baseInfo_link"]//a/@href').extract())
		#pdb.set_trace()
		url="http://jst1.58.com/counter?infoid="+re.search("\d+(?=x\.shtml)",response.url).group() +"&userid=&uname=&sid=0&lid=0&px=0&cfpath="
		request=scrapy.Request(url,callback=self.parse_couter)
		request.meta['item']=item
		request.meta['url_c']="http://qy.m.58.com/m_detail/"+re.search("(?<=com\/)\d+",url_c).group()
		#http://qy.58.com/33676822599948/?entinfo=32971740330806_3&PGTID=0d40297b-0603-22ad-69b5-4ad91171f0c4&ClickID=7
		yield request
		
	def parse_company(self,response):
		item=response.meta['item']
		job_c_sc=response.xpath('.//div[@class="compCont"]//div[@class="addB compWrap"]//div[@class="compSum"]//div[@class="detArea"]//dl//dd/text()').extract()
		item['job_c_sc']="NULL" if len(job_c_sc)<2  else re.sub("[\u4e00-\u9fa5]+","",job_c_sc[1])
		job_c_st=response.xpath('.//div[@class="compCont"]//div[@class="addB compWrap"]//div[@class="compSum"]//div[@class="detArea"]//dl//dd/text()').extract()
		item['job_c_st']=re.sub("\\r|\\t|\\n| ","",job_c_st[0])if len(job_c_st)>=1 else "null"
		item['job_c_ty']=response.xpath('.//div[@class="compCont"]//div[@class="addB compWrap"]//div[@class="compSum"]//div[@class="detArea"]//dl//dd/a/text()').extract()
		job_c_add=response.xpath('.//div[@class="compCont"]//div[@class="addB compWrap"]//div[@class="compSum"]//div[@class="detArea"]//dl//dd/text()').extract()
		item['job_c_add']="null" if  len(job_c_add)<2 else job_c_add[len(job_c_add)-1]
		item['job_c_tel']=" ".join(response.xpath('.//div[@class="compCont"]//div[@class="addB compTouch"]//dl//dd[@class="mobMsg"]//p[@class="marB"]//span/text()').extract())
		item['job_c_eml']=response.xpath('.//div[@class="compCont"]//div[@class="addB compTouch"]//dl//dd[2]/text()').extract()
		yield item
		
	def parse_couter(self,response):
		item=response.meta['item']
		item['job_ll']=re.search("(?<=total=)\d+",str(response.body)).group()
		#pdb.set_trace()
		url=response.meta['url_c']
		request=scrapy.Request(url,callback=self.parse_company)
		request.meta['item']=item
		yield request
	
	def parse_date(self,response):
		#print(response.xpath('.').extract())
		date_o=response.xpath('.//div[@class="con"]//div[@class="main clearfix"]//div[@class="leftCon"]//ul//li[@class="job_item clearfix"]')
		
		#print(date_o.extract())
		for date_oc in date_o:
			self.j_n=self.j_n+1
			items=Tc58Item()
			job_ty=date_oc.xpath('.//p[@class="job_require"]//span[@class="cate"]/text()').extract()
			job_url=date_oc.xpath('.//div[@class="job_name clearfix"]//a/@href').extract()
			job_n=date_oc.xpath('.//div[@class="job_name clearfix"]//a//span[@class="name"]/text()').extract()
			job_ar=date_oc.xpath('.//div[@class="job_name clearfix"]//a//span[@class="address"]/text()').extract()
			job_s=date_oc.xpath('.//p[@class="job_salary"]/text()').extract()
			job_ed=date_oc.xpath('.//p[@class="job_require"]//span[@class="xueli"]/text()').extract()
			job_we=date_oc.xpath('.//p[@class="job_require"]//span[@class="jingyan"]/text()').extract()
			job_c=date_oc.xpath('.//div[@class="comp_name"]//a/@title').extract()
			job_st=date_oc.xpath('.//div[@class="job_wel clearfix"]/span/text()').extract()
			job_d=date_oc.xpath('.//span[@class="sign"]/text()').extract()
			if job_st != None:
				char=getst(job_st)
				job_st=char.re
			else:
				job_st=0
			if job_d != None:
				date=gettime(job_d)
				job_d=date.times
			else:
				job_d="0-0-0"
			items['job_s'] = job_s
			items['job_n'] = job_n
			items['job_ar'] = job_ar
			items['job_c'] = job_c
			items['job_st'] = job_st
			items['job_we'] = job_we
			items['job_ed'] = job_ed
			items['job_d'] = job_d
			items['job_ty'] = job_ty
			#print(job_n,job_ar,job_c,job_we,job_ed,job_ar,job_st,job_d)
			print("爬取数:"+str(self.j_n)+"名称:"+"".join(job_n))
			if len(job_url):
				if job_url[0]!=None:
					request= scrapy.Request(job_url[0],callback=self.parse_date_url)
					request.meta['item'] = items
					yield request
				
		page_out=response.xpath('.//div[@class="con"]//div[@class="main clearfix"]//div[@class="pagesout"]//a[@class="next"]/@href').extract()
		if  len(page_out):
			if page_out[0]!=None:
				yield scrapy.Request(page_out[0],callback=self.parse_date)