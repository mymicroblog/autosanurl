#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 
import urllib 
import urllib2 
from string import strip
import json
import smtplib  
import email.MIMEMultipart# import MIMEMultipart  
import email.MIMEText# import MIMEText  
import email.MIMEBase# import MIMEBase  
import os.path  
import sys
import mimetypes  

class MailSend(object):

	def __init__(self, content):
		#self.config = Config()
		#self.file_name = file_name
		self.From = "hehu@eswine.com"
		self.To = ['1580xxxxxxx@139.com','188xxxxxx@139.com']		
		self.Cc = ['']
		//smtp server
		self.smtp = "smtp.163.com"
		self.username = "xx@xx.com"
		self.password = "pass"
		self.content=content

	def generateHtml(self):
		content=self.content
		msg=''
		for warn in content:
			try:
				url=warn['url']
			except:
				continue			
			params=warn['param']
			method=warn['method']
			res=warn['return']
			code=warn['code']
			msg=msg+'url:'+url+"</br>"+'params:'+params+"</br>"+'method:'+method+"</br>"+'result:'+res+"</br>"+'code:'+str(code)+"</br>"+'##########'+"</br>"
		return msg
	
	def send(self):
		server = smtplib.SMTP(self.smtp)  
		
		#仅smtp服务器需要验证时  
		server.login(self.username, self.password)

		# 构造MIMEMultipart对象做为根容器  
		main_msg = email.MIMEMultipart.MIMEMultipart()  
		# 构造MIMEText对象做为邮件显示内容并附加到根容器  
		
		content = self.generateHtml()
		text_msg = email.MIMEText.MIMEText(content,"html",_charset="utf-8")
		main_msg.attach(text_msg)  
		  
		# 设置根容器属性  
		main_msg['From'] = self.From  
		main_msg['To'] = ','.join(self.To)
		main_msg['Cc'] = ','.join(self.Cc)
		main_msg['Subject'] = 'subject'
		main_msg['Date'] = email.Utils.formatdate( )  
		  
		# 得到格式化后的完整文本  
		fullText = main_msg.as_string( )  
		  
		# 用smtp发送邮件  
		to = self.To + self.Cc
		try:  
			server.sendmail(self.From, to, fullText)  
		finally:  
			server.quit()

i=0
content=range(100)
warn={}
for line in open('urllist.txt').readlines():
	line=line.strip()
	if len(line)==0:
		continue
	lines=line.split("\t")
	method=lines[1]
	method=strip(method)
	if len(lines)==3:
		params=lines[2]
		params=strip(params)
	else:
		params=''
	api_name=lines[0]
	api_name=strip(api_name)
	//url prefix
	prefix='http://api.weibo.com/xx/xx'
	//prameter
	token_params='a=b&c=d'
	url=prefix+'m='+api_name
	if len(method)==0:
		print ('method is null')
		continue
	if len(api_name)==0:
		print ('api_name is null')
		continue
	method=method.lower()
	if  method=='get':
		if len(params)==0:
			params='&'
		else:
			params='&'+params+'&'
		params=params+token_params
		f=urllib.urlopen(url+params)
		code=f.getcode()
	elif method=='post':
		params=params+'&'+token_params
		f=urllib.urlopen(url,params)
		code=f.getcode()	
	else:
		continue

	try:
		text=f.read()
		res=json.loads(text)
	except:
			warn={'url':url,'param':params,'method':method,'return':text,'code':code}
                	content[i]=warn
                	i=i+1	
			continue
#	try:
#		errno=res['errno']
#	except AttributeError:
#		errno=0
#	if errno>0:
#		warn={'url':url,'param':params,'method':method,'return':text,'code':code}
#		content[i]=warn
#		i=i+1

is_null=1
for v in content:
	if v:
		try:
			if v.has_key('url'):
				is_null=0
				break
		except:
			continue
if not is_null:		
	obj=MailSend(content)
	obj.send()




