import urllib2
import re
import xml.dom.minidom
import xpath
from db import *
import logging
def fetchUrl(url):
	request = urllib2.Request(url)
	request.add_header('Cache-Control', 'no-cache')
	# request.add_header('User-Agent', 'iTunes/9.2.1 (Macintosh; Intel Mac OS X 10.5.8) AppleWebKit/533.16')
	# request.add_header('Host', 'itunes.apple.com')
	# request.add_header('X-Apple-Store-Front', '143465-2,12')
	# request.add_header('X-Apple-Tz', '3600')
	response = urllib2.urlopen(request)
	return str(response.read())
def fetchCategoryTop(id):
	pre = "https://itunes.apple.com/us/genre/id60"
	url = ""
	for i in range(19,1):
		if i <= 9:
			url = pre + "0" + str(i)
		else:
			url = pre + str(i)
		html = fetchUrl(url)
		print url
		print html
		p = re.compile(r'https://itunes.apple.com/us/app/.+?/id(\d+)')
		m = p.findall(html)
		print m
		writeCategoryIdListToFile(i, m)

def nodeValue(node):
	return node.firstChild.nodeValue.encode('utf-8')
def writeCategoryIdListToFile(id, li):
	f = open(str(id)+'.txt','w')
	for it in li:
		f.write(str(it) + '\n')
	f.close()

def fetchAppReviews(id):
	def urlGene(id, page):
		u = "http://itunes.apple.com/rss/customerreviews/id=#id#/sortby=mosthelpful/page=#page#/xml"
		u = re.sub('#id#', str(id), u)
		u = re.sub('#page#', str(page), u)
		return u

	def parseAppInfo(node):
		app = {'id':0, 'name':'0', 'category':0, 'artist':0, 'price':0.0, 'release_date':'0'}
		app['id'] = int(xpath.find('id/@im:id',node)[0].firstChild.nodeValue)
		app['name'] = str(xpath.find('im:name',node)[0].firstChild.nodeValue.encode('utf-8'))
		app['category'] = int(xpath.find('category/@im:id',node)[0].firstChild.nodeValue)
		artistUrl = str(xpath.find('im:artist/@href', node)[0].firstChild.nodeValue)
		app['artist'] = int(re.findall(r'id(\d+)', artistUrl)[0])
		#price now!!!!!
		price = str(xpath.find('im:price',node)[0].firstChild.nodeValue)
		if price.find('$') == 0:
			price = float(price[1:])
		else:
			price = 0
		app['price'] = price
		app['release_date'] = str(xpath.find('im:releaseDate',node)[0].firstChild.nodeValue)
		return app
	def parseReviewInfo(node):
		review = {'id':0, 'app_id':0, 'title':'0', 'content':'0', 'vote_sum':0, 'vote_count':0, 'rating':0, 'version':'0.0', 'author':'0', 'uid':0, 'time':'0'}
		review['id'] = str(nodeValue(xpath.find('id',node)[0]))
		review['time'] = str(xpath.find('updated',node)[0].firstChild.nodeValue)
		review['title'] = str( nodeValue( xpath.find('title',node)[0]))
		review['content'] = str(nodeValue(xpath.find('content[@type="text"]',node)[0]))
		review['vote_sum'] = int(xpath.find('im:voteSum',node)[0].firstChild.nodeValue)
		review['vote_count'] = int(xpath.find('im:voteCount',node)[0].firstChild.nodeValue)
		review['rating'] = int(xpath.find('im:rating',node)[0].firstChild.nodeValue)
		review['version'] = str(xpath.find('im:version',node)[0].firstChild.nodeValue)
		review['author'] = str(nodeValue( xpath.find('author/name',node)[0]))
		userUrl = str(nodeValue(xpath.find('author/uri',node)[0]))
		# print userUrl
		review['uid'] = int(re.findall(r'id(\d+)', userUrl)[0])
		# print review
		return review

	def parseMaxPage(doc):
		# print str((xpath.find('/feed/link[@rel="first"]/@href', doc)[0].firstChild.nodeValue))
		lastUrl = str(xpath.find('/feed/link[@rel="last"]/@href', doc)[0].firstChild.nodeValue)
		# print lastUrl
		# print 'abc'
		return int(re.findall(r'page=(\d+)', lastUrl)[0])

	# if getReviewAmount(id) > 100:
	# 	print str(id) + " > 100, PASS`"
	# 	return
	maxPage = 1
	
	curPage = 1
	while curPage <= maxPage:
		#each page has a Unique entry
		entryCnt = 0
		# print "Page " + str(curPage) 
		url = urlGene(id,curPage)
		# print url
		html = fetchUrl(url)
		doc = xml.dom.minidom.parseString(html)
		if curPage == 1:
			maxPage = parseMaxPage(doc)
		# print "Max page: " + str(maxPage)
		for entry in xpath.find('/feed/entry', doc):
			entryCnt = entryCnt + 1
			if entryCnt == 1:
				if curPage == 1:
					appInfo = parseAppInfo(entry)
					print appInfo
					# ret = insertApp(appInfo)
					# if(ret==-1):
					# 	return
			else:
				review =  parseReviewInfo(entry)
				review['app_id'] = appInfo['id']
				insertReview_2(review)
		curPage = curPage + 1
		if(curPage >= 10):
			break

def readApp_Cate():
	for curCate in range(4,5):
		try:
			print "Current File: " + str(curCate) + " Cate:" + str(curCate)
			curFile = open('top_ids/' + str(curCate) + '.txt')
			for curId in curFile:
				s = "60"
				if curCate <= 9:
					s += '0' + str(curCate)
				else:
					s += str(curCate)
				insertAppCate(curId, s)
				

		except Exception, e:
			# print e
			logging.error(str(e))
def main():
	# try:
	# 	fetchAppReviews(581357305)
	# except Exception, e:
	# 	print e

	for curCate in range(15,20):
		try:
			print "Current File: " + str(curCate) + " Cate:" + str(curCate)
			curFile = open('top_ids/' + str(curCate) + '.txt')
			for curId in curFile:
				print "Current App: " + curId
				try:
					fetchAppReviews(int(curId))
				except Exception, e:
					pass
		except Exception, e:
			# print e
			logging.error(str(e))
	# for curCate in range(0,23):
	# 	try:
	# 		print "Current File: " + str(curCate) + " Cate:" + str(curCate)
	# 		curFile = open('top_ids/' + str(curCate) + '.txt')
	# 		for curId in curFile:
	# 			print "Current App: " + curId
	# 			try:
	# 				fetchAppReviews(int(curId))
	# 			except Exception, e:
	# 				print e
	# 	except Exception, e:
	# 		print e
	# 		logging.error(str(e))



if __name__ == '__main__':
	logging.basicConfig(filename='log.txt', level = logging.ERROR)
	# print fetchAppReviews(469337564)
	main()