import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials 
from bs4 import BeautifulSoup 
import os

# --- 1. 驗證與設定 --- 
# GitHub Actions 會在執行時動體產生這個 service_account.json 檔案 
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'] 

try: 
	# 這裡讀取由 GitHub Actions 產生的金鑰檔 
	creds = Credentials.from_service_account_file('service_account.json', scopes=scope) 
	gc = gspread.authorize(creds) 

except Exception as e: 
	print(f"驗證失敗，請檢查金鑰設定: {e}") 
	exit(1)

filter_arr = [ ]
filter_arr1 = [ ]
#request_html = requests.get("https://www.e-valuation.com.hk/evaluation/ERegion.html")

url = "https://www.e-valuation.com.hk/evaluation/ERegion.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
	response = requests.get(url, headers=headers, timeout=15)

	from bs4 import BeautifulSoup
	soup = BeautifulSoup(response.text, "html.parser") ## 印出排好版的HTML架構
	#print(soup.prettify())
	region_link = soup.find_all('a')
	for region_tag in region_link:

  	aaa = "District" in region_tag.get('href')
  	if aaa == True:
    	request_html = requests.get(region_tag.get('href'))
    	soup_1 = BeautifulSoup(request_html.text, "html.parser")
    	district_link = soup_1.find_all('a')
    	for district_tag in district_link:
      		bbb = "areas=" in district_tag.get('href')
      		if bbb == True:
        		request_html = requests.get(district_tag.get('href'))
        		soup_2 = BeautifulSoup(request_html.text, "html.parser")
        		area_link = soup_2.find_all('a')
        		for area_tag in area_link:
          			ccc = 'FindBlock' in area_tag.get('href')
          			if ccc == True:

            			region_text = 'areas=NT' in region_tag.get('href')
            			if region_text == True:
              				filter_arr.append(area_tag.get('href'))
              				filter_arr1.append('New Territories,新界' + ' ' + district_tag.get_text() + ' ' + area_tag.get_text())

            			region_text = 'areas=IS' in region_tag.get('href')
            			if region_text == True:
              				discovery_text = 'Discovery Bay' in area_tag.get_text()
              				if discovery_text == True:
                				request_html = requests.get(area_tag.get('href'))
                				soup_3 = BeautifulSoup(request_html.text, "html.parser")
                				discovery_link = soup_3.find_all('a')
                				for discovery_tag in discovery_link:
                  					instr_discovery = 'Discovery%20Bay' in discovery_tag.get('href')
                  					if instr_discovery == True:
                    					filter_arr.append(discovery_tag.get('href'))
                    					filter_arr1.append(district_tag.get_text() + ' ' + area_tag.get_text() + ' ' + discovery_tag.get_text())

              				if discovery_text == False:
                				filter_arr.append(area_tag.get('href'))
                				filter_arr1.append(district_tag.get_text() + ' ' + area_tag.get_text())

            			region_text = 'areas=KL' in region_tag.get('href')
            			if region_text == True:
              				filter_arr.append(area_tag.get('href'))
              				filter_arr1.append('Kowloon,九龍' + ' ' + district_tag.get_text() + ' ' + area_tag.get_text())

            			region_text = 'areas=HK' in region_tag.get('href')
            			if region_text == True:
              				filter_arr.append(area_tag.get('href'))
              				filter_arr1.append('Hong Kong,香港' + ' ' + district_tag.get_text() + ' ' + area_tag.get_text())

	# --- 3. 資料處理與寫入 Google Sheets --- 
	df = pd.DataFrame({'Estate Name': pd.Series(filter_arr1), 'Hypelink': pd.Series(filter_arr)}) 

	# 開啟試算表 (請確保 Vigers 已經共用給服務帳戶 Email) 
	sh = gc.open('Vigers') 
	worksheet = sh.get_worksheet(0) 

	# 準備資料 
	values = [df.columns.values.tolist()] + df.values.tolist() 

	# 清除舊內容並更新
	worksheet.clear() 
	worksheet.update(values=values, range_name='A1') 

	print(f"資料更新成功！共有 {len(df)} 筆資料。")

except Exception as e: 
	print(f"執行過程中發生錯誤: {e}")
