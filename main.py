import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from bs4 import BeautifulSoup
import os

# --- 1. 驗證與設定 ---
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

try:
    # 這裡讀取由 GitHub Actions 產生的金鑰檔
    creds = Credentials.from_service_account_file('service_account.json', scopes=scope)
    gc = gspread.authorize(creds)
except Exception as e:
    print(f"驗證失敗，請檢查金鑰設定: {e}")
    exit(1)

filter_arr = []
filter_arr1 = []

url = "https://www.e-valuation.com.hk/evaluation/ERegion.html"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("開始執行爬蟲任務...")

try:
    response = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")
    region_link = soup.find_all('a')

    for region_tag in region_link:
        region_href = region_tag.get('href', '')
        if "District" in region_href:
            request_html = requests.get(region_href)
            soup_1 = BeautifulSoup(request_html.text, "html.parser")
            district_link = soup_1.find_all('a')
            
            for district_tag in district_link:
                dist_href = district_tag.get('href', '')
                if "areas=" in dist_href:
                    request_html = requests.get(dist_href)
                    soup_2 = BeautifulSoup(request_html.text, "html.parser")
                    area_link = soup_2.find_all('a')
                    
                    for area_tag in area_link:
                        area_href = area_tag.get('href', '')
                        if 'FindBlock' in area_href:
                            area_text = area_tag.get_text()
                            dist_text = district_tag.get_text()

                            # 處理新界區
                            if 'areas=NT' in region_href:
                                filter_arr.append(area_href)
                                filter_arr1.append(f'New Territories,新界 {dist_text} {area_text}')

                            # 處理離島區 (含愉景灣邏輯)
                            elif 'areas=IS' in region_href:
                                if 'Discovery Bay' in area_text:
                                    req_db = requests.get(area_href)
                                    soup_3 = BeautifulSoup(req_db.text, "html.parser")
                                    discovery_link = soup_3.find_all('a')
                                    for discovery_tag in discovery_link:
                                        db_href = discovery_tag.get('href', '')
                                        if 'Discovery%20Bay' in db_href:
                                            filter_arr.append(db_href)
                                            filter_arr1.append(f'{dist_text} {area_text} {discovery_tag.get_text()}')
                                else:
                                    filter_arr.append(area_href)
                                    filter_arr1.append(f'{dist_text} {area_text}')

                            # 處理九龍區
                            elif 'areas=KL' in region_href:
                                filter_arr.append(area_href)
                                filter_arr1.append(f'Kowloon,九龍 {dist_text} {area_text}')

                            # 處理香港島區
                            elif 'areas=HK' in region_href:
                                filter_arr.append(area_href)
                                filter_arr1.append(f'Hong Kong,香港 {dist_text} {area_text}')

    # --- 3. 資料處理與寫入 Google Sheets ---
    if not filter_arr:
        print("未抓取到任何資料，請檢查目標網頁結構。")
    else:
        df = pd.DataFrame({'Estate Name': pd.Series(filter_arr1), 'Hypelink': pd.Series(filter_arr)})
        
        # 開啟試算表
        sh = gc.open('Vigers')
        worksheet = sh.get_worksheet(0)

        # 準備與寫入資料
        values = [df.columns.values.tolist()] + df.values.tolist()
        worksheet.clear()
        worksheet.update(values=values, range_name='A1')

        print(f"資料更新成功！共有 {len(df)} 筆資料寫入 Google Sheets。")

except Exception as e:
    print(f"執行過程中發生錯誤: {e}")
