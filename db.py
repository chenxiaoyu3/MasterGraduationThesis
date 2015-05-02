import mysql.connector
from dateutil import parser
import logging

con = mysql.connector.connect(user='root', host = '127.0.0.1', database='app')
cursor = con.cursor()
def insertApp(appInfo):
	ret = 0
	try:
		sql = 'INSERT INTO app_info(id,name,category,artist,price,release_date)VALUES(%s, %s, %s, %s, %s,%s)'
		
		cursor.execute(sql, (appInfo['id'], appInfo['name'], appInfo['category'], 
			appInfo['artist'], appInfo['price'], 
			parser.parse(appInfo['release_date'])))

		con.commit()
	except mysql.connector.errors.IntegrityError, e:
		print e
		ret = -1
	except Exception, e:
		logging.error(str(e))
	return ret

def insertReview(review):
	try:
		sql = 'INSERT INTO review(id,title,content,author,rating,time,version,vote_sum,vote_count,app_id)VALUES(%s, %s, %s, %s, %s,%s,%s,%s,%s,%s)'
		
		cursor.execute(sql, (review['id'], review['title'], review['content'], 
			review['author'], review['rating'], review['time'], review['version'],
			review['vote_sum'], review['vote_count'], review['app_id']))

		con.commit()
	except mysql.connector.errors.IntegrityError, e:
		pass
	except Exception, e:
		logging.error(str(e))


def insertReview_2(review):
	try:
		sql = 'INSERT INTO review_2(id,title,content,author,rating,time,version,vote_sum,vote_count,app_id,uid)VALUES(%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)'
		
		cursor.execute(sql, (review['id'], review['title'], review['content'], 
			review['author'], review['rating'], review['time'], review['version'],
			review['vote_sum'], review['vote_count'], review['app_id'], review['uid']))

		con.commit()
	except mysql.connector.errors.IntegrityError, e:
		pass
	except Exception, e:
		logging.error(str(e))

def getReviewAmount(app_id):
	ret = 0
	try:
		sql = 'SELECT COUNT(id) FROM review WHERE app_id=' + str(app_id)
		cursor.execute(sql)
		result = cursor.fetchone()
		# print result
		ret = int(result[0])
		con.commit()
	except mysql.connector.errors.IntegrityError, e:
		pass
	except Exception, e:
		logging.error(str(e))
		print e
	return ret
	
def insertAppCate(app_id, cate):
	try:
		sql = 'INSERT INTO app_category(app_id,cate)VALUES(%s, %s)'
		
		cursor.execute(sql, (app_id,cate))

		con.commit()
	except mysql.connector.errors.IntegrityError, e:
		pass
	except Exception, e:
		logging.error(str(e))