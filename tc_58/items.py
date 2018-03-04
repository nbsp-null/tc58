# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Tc58Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
   job_n=scrapy.Field()#name
   job_s=scrapy.Field()#salary
   job_c=scrapy.Field()#company
   job_ar=scrapy.Field()#区域
   job_st=scrapy.Field() #保险#放假#包吃住情况#补助
   job_ty=scrapy.Field()#type
   job_d=scrapy.Field()#time
   job_purl=scrapy.Field()#page_url
   job_ed=scrapy.Field()#学历
   job_we=scrapy.Field()#工作经验
   job_ll=scrapy.Field()#工作经验
   job_rn=scrapy.Field()#需求人数
   job_adr=scrapy.Field()#详细地址
   job_rl_ar=scrapy.Field()#真实区域
   job_jt=scrapy.Field()#加入时间
   job_des=scrapy.Field()#职位描述
   job_cdes=scrapy.Field()#公司介绍
   job_cimdes=scrapy.Field()#图片列表
   job_c_sc=scrapy.Field()#公司规模
   job_c_st=scrapy.Field()#公司营业模式
   job_c_ty=scrapy.Field()#公司分类
   job_c_add=scrapy.Field()#公司地址
   job_c_tel=scrapy.Field()#公司电话
   job_c_eml=scrapy.Field()#公司Email
   
   
