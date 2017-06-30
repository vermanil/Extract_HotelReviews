from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import time
import requests
from datetime import datetime
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1024, 768))
display.start()


month_map = {"January":'01' , "February": '02' , "March":'03',"April":'04',"May":'05',"June":'06',"July":'07',"August":'08',"September":'09',"October":'10',"November":11,
    "December":'12'}
def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 30)
    return driver


def get_reviews(url,requested_date=None):
	review_tab = "tab-reviews"
	if(len(url)>0):
		main_page = str(url.split('&#')[1])
		url = url.split(main_page)[0]
	else:
		return []
	driver = init_driver()
	driver.get(url+main_page)
	#Collecting Basic Information
	pageSource = driver.page_source
	soup = BeautifulSoup(pageSource, 'html.parser')
	hoteltitle = soup.find("div", { "class" : "hp__hotel-title" })
	hotelName = hoteltitle.find("h2",{"class":"hp__hotel-name"})
	#hotelstar = hoteltitle.find("span",{"class":"nowrap hp__hotel_ratings"}).find("span",{"class":"hp__hotel__ratings__stars"}).find("i",{"class":"bk-icon-wrapper bk-icon-stars star_track"})
	hotelAdd = soup.find("span",{"class":"hp_address_subtitle"}).text
	try:
		num_reviews = int(soup.find("a",{"class":"hp_nav_reviews_link toggle_review track_review_link_zh"}).text.split('(')[1].split(')')[0])
	except Exception as e:
		return list()

	#Collecting Reviews
	driver.get(url+review_tab)
	time.sleep(5)
	pageSource = driver.page_source
	#print(pageSource.encode('utf-8'))
	Reviews_list = list()
	soup = BeautifulSoup(pageSource,"html.parser")
	time.sleep(5)
	review_data = list()
	if(requested_date):
		requested_date = requested_date.split(' ')
		requested_date = datetime(int(requested_date[0]),int(requested_date[1]),int(requested_date[2]))

	try:
		hotelReviews_url = "https://www.booking.com"+str(soup.find("a",{"id":"review_next_page_link"}).get('href'))
		hotelReviews_url = hotelReviews_url.split('roomtype=-1')
		new_older = ";sort=f_recent_desc;type=total;upsort_photo=0&;offset=0;rows=10"
		hotelReviews_url = hotelReviews_url[0]+"roomtype=-1"+new_older
		hotelReviews_url = str(hotelReviews_url.split('offset')[0])
		offset = 0

		while(len(review_data) < num_reviews):
			pre_num_reviews = len(review_data)
			url = hotelReviews_url+"offset="+str(offset)+";rows=10"
			offset += 10
			driver.get(url)
			time.sleep(5)
			pageSource = driver.page_source
			soup = BeautifulSoup(pageSource,"html.parser")
			reviews = soup.findAll("div",{"class":"review_item_review_content"})
			dates = soup.findAll("p",{"class":"review_item_date"})
			for review,date in zip(reviews,dates):
				date = date.get_text().replace('\n','').replace(',',' ').split(' ')
				try:
					temp = int(date[1])
					date_to_send = ' '.join([str(date[2]),str(month_map[date[0]]),str(date[1])])
					date = datetime(int(date[2]),int(month_map[date[0]]),int(date[1]))
				except:
					date_to_send = ' '.join([str(date[2]),str(month_map[date[1]]),str(date[0])])
					date = datetime(int(date[2]),int(month_map[date[1]]),int(date[0]))

				if(requested_date):
					if(requested_date >= date):
						return review_data

				review_string=(review.get_text().replace('\n','')).encode('ascii','ignore')
				#review_string=review_string.replace('b209','')
				#review_string=review_string.replace('b207','')
				review_data.append((date_to_send,review_string))

			if(len(review_data) == pre_num_reviews):
				break
	except Exception as e:
		reviews = soup.findAll("div",{"class":"review_item_review_content"})
		dates = soup.findAll("p",{"class":"review_item_date"})
		for review,date in zip(reviews,dates):
			date = date.get_text().replace('\n','').replace(',','').split(' ')
			try:
				temp = int(date[1])
				date_to_send = ' '.join([str(date[2]),str(month_map[date[0]]),str(date[1])])
				date = datetime(int(date[2]),int(month_map[date[0]]),int(date[1]))
			except:
				date_to_send = ' '.join([str(date[2]),str(month_map[date[1]]),str(date[0])])
				date = datetime(int(date[2]),int(month_map[date[1]]),int(date[0]))
			if(requested_date):
				if(requested_date >= date):
					return review_data
			review_string=review.get_text().replace('\n','').encode('ascii','ignore')
			#review_string=review_string.replace('b209','')
			#review_string=review_string.replace('b207','')

			review_data.append((date_to_send,review_string))
	driver.quit()
	return review_data

# if __name__ == "__main__":
# 	url = "https://www.booking.com/hotel/in/oyo-rooms-mdi-gurgaon.en-gb.html?label=gen173nr-1DCAEoggJCAlhYSDNiBW5vcmVmaGyIAQGYAS7CAQN4MTHIAQzYAQPoAQGSAgF5qAID;sid=a754ebfbf9f0fd9261e4b35cb80d87ca;dest_id=-2096897;dest_type=city;dist=0;group_adults=2;hpos=3;room1=A%2CA;sb_price_type=total;srfid=470514ac9e16934f19b8790c82a96b6d176bcff8X3;type=total;ucfs=1&#hotelTmpl"
# 	print(get_reviews(url))
