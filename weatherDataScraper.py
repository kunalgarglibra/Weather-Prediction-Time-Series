import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests 
import urllib,time
from urllib.request import urlopen,Request
import csv,datetime,re,time
from requests_html import HTMLSession






start = time.time()

flag = 0
leap_year =[2012,2016,2020]
month_30 = [4,6,9,11]
for year in range(2010,2021): 
	date =[]
	times = []
	temp = []
	dew = []
	hum =[]
	wind=[]
	wind_s =[]
	wind_g =[]
	press = []
	precip = []
	cond = []
	for month in range(1,13): 
		for day in range(1,32): 
			if(year in leap_year):
				if(month == 2 and day >29):
					break
			else:
				if (month == 2 and day >28):
					break
			if(month in month_30 and day >30):
				break
			d = "{}-{}-{}".format(year,month,day)
			start2 = time.time()
			session = HTMLSession()
			url = "https://www.wunderground.com/history/daily/ca/toronto/CYTZ/date/{}".format(d)
			try:
				r = session.get(url)
				r.html.render(timeout = 60)
				soup = BeautifulSoup(r.html.html,'html.parser')
				table = soup.find("tbody",{'role':'rowgroup'})
				row = table.find_all('tr')
				for r in row :
					n = 0
					date.append(d)
					for cell in r.find_all('td'):
						if(n == 0):
							times.append(cell.text)
						elif(n == 1):
							temp.append(cell.text)
						elif(n == 2):
							dew.append(cell.text)
						elif(n == 3):
							hum.append(cell.text)
						elif(n == 4):
							wind.append(cell.text)
						elif(n == 5):
							wind_s.append(cell.text)
						elif(n == 6):
							wind_g.append(cell.text)
						elif(n == 7):
							press.append(cell.text)
						elif(n == 8):
							precip.append(cell.text)
						elif(n == 9):
							cond.append(cell.text)
						n+=1
				end2 = time.time()
				print(d)
				
				print("it took : {} seconds".format(end2-start2))
			

				if( month == 12 and day ==31):
					print("Writing into csv is in progress!\n")
					df = pd.DataFrame({"Date":date,"Time":times,"Temperature":temp,"Dew Point":dew,"Humidity":hum,"Wind" : wind,"Wind Speed":wind_s,"Wind Gust":wind_g, "Pressure":press,"Precipitation":precip,"Condition":cond})
					df.to_csv("C:/kunal/AllProjects/ML Projects/ML Projects//weather{}.csv".format(year))
					print("Done Writing {} Year Data Into CSV!\n".format(year))
			except:
				print("Nothing has been added")

r.close()
session.close()
end = time.time()
print(end-start)
