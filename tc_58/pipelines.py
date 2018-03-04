# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class Tc58Pipeline(object):
    def process_item(self, item, spider):
		if item['job_s']!=None:
			if item['job_s']=="面议":
				job_s=0
			else:
				s_1=item['job_s'].split("-")
				if	len(s_1)>1 and int(s_1[0])>0 and int(s_1[1])>0:
					job_s=(int(s_1[0])+int(s_1[1]))/2
				else:
					job_s=99
		if item['job_we']!=None:
			if item['job_we']=="不限":
				job_we=0
			elif item['job_we']=="1年以下":
				job_we=1
			else:
				item['job_we']=re.sub('年',"",item['job_we'])
				s_2=item['job_we'].split("-")
				if	len(s_2)>1 and int(s_2[0])>0 and int(s_2[1])>0:
					job_we=(int(s_2[0])+int(s_2[1]))/2
				else:
					job_we=99
		job_ed={"中专":1,"技校":2,"大专":3,"本科":4,"高中":5,"硕士":6,"博士":7,}.get(item['job_ed'],0)
		db = pymysql.connect("localhost","root","qq123456","tc_58" )
		cursor = db.cursor()
		sql = "Insert into job values (%d ,'%s',%d,'%s','%s','%s',%d,%d,%d,'%s','%s','%s',%d,%d,'%s',%d)" % (
                    0, item['job_n'], job_s, item['job_ar'],item['job_rl_ar'],item["job_adr"],int(item["job_st"]),job_ed,job_we,item["job_ty"],item["job_d"],item["job_purl"],int(item['job_ll']),int(item['job_rn']),item["job_des"],0)
		sql_c="Insert into company values (%d ,'%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s')" % (
                    0, item['job_cdes'], item['job_cimdes'],item['job_c_add'],item["job_c_tel"],item["job_c_eml"],int(item["job_jt"]),item["job_c_ty"],item["job_c_sc"],item['job_c_st'],item['job_c'])
		try:
		   # 执行sql语句
		   print(sql)
		    print(sql_c)
		   cursor.execute(sql)
		   cursor.execute(sql_c)
		   # 提交到数据库执行
		   db.commit()
		except:
		   # 如果发生错误则回滚
		   
		   db.rollback()
		 
		# 关闭数据库连接
		db.close()
		#print(item)
        return item
		
		# SELECT `company`.`index`,
    # `company`.`c_des`,
    # `company`.`c_imdes`,
    # `company`.`c_add`,
    # `company`.`c_tel`,
    # `company`.`c_eml`,
    # `company`.`c_jt`,
    # `company`.`c_ty`,
    # `company`.`c_sc`,
    # `company`.`c_st`,
    # `company`.`c_n`
# FROM `tc_58`.`company`;

		
		 # job_n=scrapy.Field()#name
   # job_s=scrapy.Field()#salary
   # job_c=scrapy.Field()#company
   # job_ar=scrapy.Field()#区域
   # job_st=scrapy.Field() #保险#放假#包吃住情况#补助
   # job_ty=scrapy.Field()#type
   # job_d=scrapy.Field()#time
   # job_purl=scrapy.Field()#page_url
   # job_ed=scrapy.Field()#学历
   # job_we=scrapy.Field()#工作经验
   # job_ll=scrapy.Field()#工作经验
   # job_rn=scrapy.Field()#需求人数
   # job_adr=scrapy.Field()#详细地址
   # job_rl_ar=scrapy.Field()#真实区域
   # job_jt=scrapy.Field()#加入时间
   # job_des=scrapy.Field()#职位描述
   # job_cdes=scrapy.Field()#公司介绍
   # job_cimdes=scrapy.Field()#图片列表
   # job_c_sc=scrapy.Field()#公司规模
   # job_c_st=scrapy.Field()#公司营业模式
   # job_c_ty=scrapy.Field()#公司分类
   # job_c_add=scrapy.Field()#公司地址
   # job_c_tel=scrapy.Field()#公司电话
   # job_c_eml=scrapy.Field()#公司Email
   
   
# SELECT `job`.`id`,
    # `job`.`job_n`,
    # `job`.`job_s_max`,
    # `job`.`job_s_min`,
    # `job`.`job_ar`,
    # `job`.`job_re_ar`,
    # `job`.`job_add`,
    # `job`.`job_st`,
    # `job`.`job_ed`,
    # `job`.`job_we`,
    # `job`.`job_ty`,
    # `job`.`job_d`,
    # `job`.`job_purl`,
    # `job`.`job_ll`,
    # `job`.`job_rn`,
    # `job`.`job_des`,
    # `job`.`comp_index`
# FROM `tc_58`.`job`;
