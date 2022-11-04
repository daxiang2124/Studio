# -*- coding: UTF-8 -*-
import httplib

def codeHttp_1():
	com=httplib.HTTPConnection('www.baidu.com:80',True,10)
	print(com.request('get','/','',{'user-agent':'test'}))
	# com.request('GET','')
	# res=com.getresponse() #获取一个http响应对象，相当于执行最后的2个回车
	# print('read:',res.read()) #获得http响应的内容部分，即网页源码
	# print('getheaders:',res.getheaders()) #获得所有的响应头内容
	# com.close()

def codeHttp_2():
	com=httplib.HTTPConnection('www.baidu.com',80,False,10)
	com.request('get','/','',{'user-agent':'test'})
	res=com.getresponse() #获取一个http响应对象，相当于执行最后的2个回车
	print('res:',res)
	com.close()

def codeHttp_3():
	com=httplib.HTTPConnection('www.google.com',80,False,10)
	com.request('GET','')
	res=com.getresponse() #获取一个http响应对象，相当于执行最后的2个回车
	print('res:',res.read())
	# com.close()

# codeHttp_1()
# codeHttp_2()
codeHttp_3()












