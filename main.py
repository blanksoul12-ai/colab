import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

# --- 1. 驗證與設定 ---
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

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
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/91.0.4472.124 Safari/537.36'
    )
}

print("開始執行爬蟲任務...")


def get_soup(page_url):
    """
    統一讀取網頁，避免每次 requests.get 都重複寫。
    """
    response = requests.get(page_url, headers=headers, timeout=15)
    response.raise_for_status()

    # 處理舊式香港網站中文編碼問題
    if not response.encoding or response.encoding.lower() == "iso-8859-1":
        response.encoding = response.apparent_encoding

    return BeautifulSoup(response.text, "html.parser")


def clean_text(text):
    """
    清理文字中的空白、換行。
    """
    if text is None:
        return ""

    return (
        text.replace("\xa0", " ")
            .replace("\n", " ")
            .replace("\r", " ")
            .replace("\t", " ")
            .strip()
    )


def is_property_link(href):
    """
    判斷是否為屋苑 / 大廈資料連結。

    原本只判斷 FindBlock，所以會漏 Parkford Garden。
    現在同時接受：
    - EPgeFindBlock
    - EPgeFindFloor
    """
    href_lower = href.lower()

    return (
        "findblock" in href_lower
        or "findfloor" in href_lower
    )


try:
    soup = get_soup(url)
    region_link = soup.find_all('a')

    for region_tag in region_link:
        region_href = region_tag.get('href', '')

        if "District" in region_href:
            region_url = urljoin(url, region_href)

            try:
                soup_1 = get_soup(region_url)
            except Exception as e:
                print(f"讀取地區頁失敗: {region_url} / {e}")
                continue

            district_link = soup_1.find_all('a')

            for district_tag in district_link:
                dist_href = district_tag.get('href', '')

                if "areas=" in dist_href:
                    dist_url = urljoin(region_url, dist_href)

                    try:
                        soup_2 = get_soup(dist_url)
                    except Exception as e:
                        print(f"讀取分區頁失敗: {dist_url} / {e}")
                        continue

                    area_link = soup_2.find_all('a')

                    for area_tag in area_link:
                        area_href = area_tag.get('href', '')

                        # 重要更新：
                        # 原本只接受 FindBlock
                        # 現在接受 FindBlock + FindFloor
                        if is_property_link(area_href):
                            area_text = clean_text(area_tag.get_text())
                            dist_text = clean_text(district_tag.get_text())
                            area_url = urljoin(dist_url, area_href)

                            # 處理新界區
                            if 'areas=NT' in region_href:
                                filter_arr.append(area_url)
                                filter_arr1.append(
                                    f'New Territories,新界 {dist_text} {area_text}'
                                )

                            # 處理離島區，含愉景灣邏輯
                            elif 'areas=IS' in region_href:
                                if 'Discovery Bay' in area_text or '愉景灣' in area_text:
                                    try:
                                        soup_3 = get_soup(area_url)
                                        discovery_link = soup_3.find_all('a')

                                        found_discovery_detail = False

                                        for discovery_tag in discovery_link:
                                            db_href = discovery_tag.get('href', '')
                                            db_text = clean_text(discovery_tag.get_text())

                                            if (
                                                'Discovery%20Bay' in db_href
                                                or 'Discovery Bay' in db_text
                                                or '愉景灣' in db_text
                                            ):
                                                db_url = urljoin(area_url, db_href)

                                                filter_arr.append(db_url)
                                                filter_arr1.append(
                                                    f'{dist_text} {area_text} {db_text}'
                                                )

                                                found_discovery_detail = True

                                        # 如果愉景灣內頁沒有再找到細分資料，保留原本連結
                                        if not found_discovery_detail:
                                            filter_arr.append(area_url)
                                            filter_arr1.append(
                                                f'{dist_text} {area_text}'
                                            )

                                    except Exception as e:
                                        print(f"讀取愉景灣內頁失敗: {area_url} / {e}")

                                        # 即使內頁失敗，也保留原本連結
                                        filter_arr.append(area_url)
                                        filter_arr1.append(
                                            f'{dist_text} {area_text}'
                                        )

                                else:
                                    filter_arr.append(area_url)
                                    filter_arr1.append(
                                        f'{dist_text} {area_text}'
                                    )

                            # 處理九龍區
                            elif 'areas=KL' in region_href:
                                filter_arr.append(area_url)
                                filter_arr1.append(
                                    f'Kowloon,九龍 {dist_text} {area_text}'
                                )

                            # 處理香港島區
                            elif 'areas=HK' in region_href:
                                filter_arr.append(area_url)
                                filter_arr1.append(
                                    f'Hong Kong,香港 {dist_text} {area_text}'
                                )

    # --- 3. 資料處理與寫入 Google Sheets ---
    if not filter_arr:
        print("未抓取到任何資料，請檢查目標網頁結構。")

    else:
        df = pd.DataFrame({
            'Estate Name': pd.Series(filter_arr1),
            'Hypelink': pd.Series(filter_arr)
        })

        # 去重，避免同一條連結重複寫入
        df = df.drop_duplicates(subset=['Hypelink']).reset_index(drop=True)

        # 檢查 Parkford Garden / 百福花園 是否已抓到
        check_parkford = df[
            df['Estate Name'].str.contains('Parkford', case=False, na=False)
            | df['Estate Name'].str.contains('百福', case=False, na=False)
            | df['Hypelink'].str.contains('Parkford', case=False, na=False)
        ]

        if len(check_parkford) > 0:
            print("已找到 Parkford Garden / 百福花園：")
            print(check_parkford.to_string(index=False))
        else:
            print("警告：仍未找到 Parkford Garden / 百福花園。")

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
