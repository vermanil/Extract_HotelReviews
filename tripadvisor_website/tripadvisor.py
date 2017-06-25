import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementNotVisibleException
import re
from pyvirtualdisplay import Display
display = Display(visible=0, size=(1024, 768))
display.start()


def init_driver():
	driver = webdriver.Firefox()
	driver.wait = WebDriverWait(driver, 30)
	return driver


def lookup(driver, query):
	driver.get(query)
	FINAL_RESULT=[[]]
	HOTEL_DETAIL=[]
	try:
		# box = driver.wait.until(EC.presence_of_element_located(
		# 	(By.CLASS_NAME, "typeahead_input")))
		# box.click()
		# box.clear()
		# box.send_keys(query)
        #
        #
		# try:
		# 	button = driver.wait.until(EC.presence_of_element_located(
		# 		(By.CLASS_NAME, "form_submit")))
		# 	button.click()
		# except:
		# 	print "form submit does not have element"
        #
		# try:
		# 	button1 = driver.wait.until(EC.element_to_be_clickable(
		# 		(By.CLASS_NAME, "ui_tagcloud_group ")))
		# except:
		# 	print "No such element"
        #
		# try:
		# 	all_spans = driver.find_elements_by_xpath("//span[@class='taLnk ulBlueLinks']")
		# 	for span in all_spans:
		# 		span.click()
		# except:
		# 	print "More cannot be click"
        #
		# time.sleep(1)

		pageSource = driver.page_source
		soup = BeautifulSoup(pageSource, 'html.parser')
		#hotelName = soup.find("h1", { "class" : "heading_title" }).text
		#street_address = soup.find("span", { "class" : "street-address" }).text
		#extended_address = soup.find("span", { "class" : "extended-address" }).text
		#locality=soup.find("span", { "class" : "locality"}).text
		#country_name= soup.find("span", { "class" : "country-name" }).text

		#allReviews = soup.findAll("p", { "class" : "partial_entry" })
		#allReviews_resp = soup.find("div", { "class" : "mgrRspnInline" }).findAll("p")

		pg_detail = soup.findAll("p", { "class" : "pagination-details" })
		#print(allReviews)
		#print(allReviews_resp)
		#allReviews=set(allReviews)-set(allReviews_resp)
		#print(allReviews)

		pg_detail=str(pg_detail[0])

		r=pg_detail.rfind('</b>')
		l=pg_detail.rfind('<b>')+3
		ans=pg_detail[l:r]
		ans=ans.replace(',','')
	   # stars= soup.find("div", { "class" : "starRating detailListItem" }).text
		#HOTEL_DETAIL = [hotelName,street_address,extended_address,locality,country_name,stars,ans]

		#print(hotelName," ",street_address," ",extended_address," ",locality," ",country_name," ",stars," ",ans)
		#for review in allReviews:
		#    print review.text

		my_url=str(driver.current_url)
		insert_index=my_url.rfind('Reviews-')+8
		my_url1=my_url[:insert_index]
		my_url2=my_url[insert_index:]

		for i in range(0,int(ans),5):
			dates_store=[]
			new_url=my_url1+"or"+str(i)+"-"+my_url2
			print(new_url)
			driver.get(new_url)
			try:
				all_spans = driver.find_elements_by_xpath("//span[@class='taLnk ulBlueLinks']")
				for span in all_spans:
					span.click()
			except:
				print "No such elementq11"

			time.sleep(1)
			pageSource = driver.page_source
			ratings = re.findall('<div class="rating reviewItemInline"><span class="ui_bubble_rating bubble_(.*?)">',
								 pageSource, re.DOTALL)

			soup = BeautifulSoup(pageSource, 'html.parser')
			allReviews = soup.findAll("p", { "class" : "partial_entry" })
			dates = soup.findAll("span", { "class" : "ratingDate relativeDate" })
			for date in dates:
				#soup_temp = BeautifulSoup(pageSource, 'html.parser')
				dates_store.append(date["title"])


			response=[]
			try:
				allReviews_resp = soup.findAll("div", { "class" : "mgrRspnInline" })
				for aa in allReviews_resp:
					response.append(aa.find("p", { "class" : "partial_entry" }))
			except:
				print(allReviews_resp)
			main_order={}
			count=0
			for rv in allReviews:
				main_order[count]=rv.text
				count+=1
			allReviews=set(allReviews)-set(response)
			count=0
			temp_review=[]
			for review in allReviews:
				temp_review.append(review.text)
				print()

			for i in range(0,len(main_order)):
				if(main_order[i] in temp_review):
					FINAL_RESULT.append([convert_month_number(dates_store[count]),main_order[i],int(ratings[count])/10])
					count+=1

		return FINAL_RESULT,HOTEL_DETAIL

	except TimeoutException:
		print("Box or Button not found in tripadviser")
		return [],[]


def add_latest(driver,query,constraint_date):
	driver.get(query)
	FINAL_RESULT=[[]]
	try:
		# box = driver.wait.until(EC.presence_of_element_located(
		# 	(By.CLASS_NAME, "typeahead_input")))
		# box.click()
		# box.clear()
		# box.send_keys(query)
        #
        #
		# try:
		# 	button = driver.wait.until(EC.presence_of_element_located(
		# 		(By.CLASS_NAME, "form_submit")))
		# 	button.click()
		# except:
		# 	print "form submit does not have element"
        #
		# try:
		# 	button1 = driver.wait.until(EC.element_to_be_clickable(
		# 		(By.CLASS_NAME, "ui_tagcloud_group ")))
		# except:
		# 	print "No such element"
        #
		# try:
		# 	all_spans = driver.find_elements_by_xpath("//span[@class='taLnk ulBlueLinks']")
		# 	for span in all_spans:
		# 		span.click()
		# except:
		# 	print "No such elementq11"
        #
		# time.sleep(1)
		pageSource = driver.page_source
		soup = BeautifulSoup(pageSource, 'html.parser')

		allReviews = soup.findAll("p", { "class" : "partial_entry" })
		allReviews_resp = soup.find("div", { "class" : "mgrRspnInline" }).findAll("p")

		pg_detail = soup.findAll("p", { "class" : "pagination-details" })
		allReviews=set(allReviews)-set(allReviews_resp)

		pg_detail=str(pg_detail[0])

		r=pg_detail.rfind('</b>')
		l=pg_detail.rfind('<b>')+3
		ans=pg_detail[l:r]
		ans=ans.replace(',','')

		for review in allReviews:
			print review.text

		my_url=str(driver.current_url)
		insert_index=my_url.rfind('Reviews-')+8
		my_url1=my_url[:insert_index]
		my_url2=my_url[insert_index:]
		finish=0
		for i in range(0,(int(ans)),5):
			dates_store=[]
			new_url=my_url1+"or"+str(i)+"-"+my_url2
			print(new_url)
			driver.get(new_url)
			try:
				all_spans = driver.find_elements_by_xpath("//span[@class='taLnk ulBlueLinks']")
				for span in all_spans:
					span.click()
			except:
				print "No such elementq11"

			time.sleep(1)
			pageSource = driver.page_source
			ratings = re.findall('<div class="rating reviewItemInline"><span class="ui_bubble_rating bubble_(.*?)">', pageSource, re.DOTALL)
			soup = BeautifulSoup(pageSource, 'html.parser')
			allReviews = soup.findAll("p", { "class" : "partial_entry" })
			dates = soup.findAll("span", { "class" : "ratingDate relativeDate" })
			for date in dates:
				dates_store.append(date["title"])

			response=[]
			try:
				allReviews_resp = soup.findAll("div", { "class" : "mgrRspnInline" })
				for aa in allReviews_resp:
					response.append(aa.find("p", { "class" : "partial_entry" }))
			except:
				print(allReviews_resp)
			main_order={}
			count=0
			for rv in allReviews:
				main_order[count]=rv.text
				count+=1
			allReviews=set(allReviews)-set(response)
			count=0
			temp_review=[]
			for review in allReviews:
				temp_review.append(review.text)
				print()

			for i in range(0,len(main_order)):
				if(main_order[i] in temp_review):
					date=convert_month_number(dates_store[count])
					print(date,constraint_date)
					if(date > constraint_date):
						FINAL_RESULT.append([date,main_order[i],int(ratings[count])/10])
						count+=1
					else:
						finish=1
						break

			if finish==1:
				break
		return FINAL_RESULT

	except TimeoutException:
		print("Box or Button not found in tripadviser")
		return []

def convert_month_number(date):

	month={
	'January' : 1,
	'February' : 2,
	'March' : 3,
	'April' : 4,
	'May' : 5,
	'June' : 6,
	'July' : 7,
	'August' : 8,
	'September' : 9,
	'October' : 10,
	'November' : 11,
	'December' : 12
	}


	date=date.strip()

	string_to_replace=date[date.find(' ')+1:date.rfind(' ')].strip()
	print(string_to_replace)
	date=date.replace(string_to_replace,str(month[string_to_replace]))
	print(date)
	temp_list=date.split(' ')
	if(len(temp_list[1])==1):
		temp_list[1]='0'+temp_list[1]
	if(len(temp_list[0])==1):
		temp_list[0]='0'+temp_list[0]

	date=temp_list[2]+' '+temp_list[1]+' '+temp_list[0]
	print(date)
	return date


