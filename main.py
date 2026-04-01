{\rtf1\ansi\ansicpg950\cocoartf2869
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fmodern\fcharset0 Courier;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;\red255\green255\blue255;\red0\green0\blue0;
\red204\green204\blue202;\red203\green203\blue202;\red213\green213\blue212;\red112\green171\blue88;\red194\green125\blue100;
\red167\green197\blue151;\red189\green136\blue185;\red115\green187\blue255;\red72\green140\blue207;}
{\*\expandedcolortbl;;\cssrgb\c0\c1\c1;\cssrgb\c100000\c100000\c100000;\cssrgb\c0\c0\c0;
\cssrgb\c83681\c83679\c83054;\cssrgb\c83502\c83501\c83084;\cssrgb\c86653\c86652\c86220;\cssrgb\c50811\c71567\c41796;\cssrgb\c80757\c56727\c46519;
\cssrgb\c71087\c80874\c65568;\cssrgb\c79030\c61379\c77536;\cssrgb\c51876\c78698\c100000;\cssrgb\c34566\c62178\c84753;}
\paperw11900\paperh16840\margl1440\margr1440\vieww28620\viewh13640\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs36 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec4 import requests\
import pandas as pd\
import gspread\
from google.oauth2.service_account import Credentials \
from bs4 import BeautifulSoup \
import os\
\
# --- 1. \uc0\u39511 \u35657 \u33287 \u35373 \u23450  --- \
# GitHub Actions \uc0\u26371 \u22312 \u22519 \u34892 \u26178 \u21205 \u39636 \u29986 \u29983 \u36889 \u20491  service_account.json \u27284 \u26696  \
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'] \
\
try: \
	# \uc0\u36889 \u35041 \u35712 \u21462 \u30001  GitHub Actions \u29986 \u29983 \u30340 \u37329 \u38000 \u27284  \
	creds = Credentials.from_service_account_file('service_account.json', scopes=scope) \
	gc = gspread.authorize(creds) \
\
exceptException as e: \
	print(f"\uc0\u39511 \u35657 \u22833 \u25943 \u65292 \u35531 \u27298 \u26597 \u37329 \u38000 \u35373 \u23450 : \{e\}") \
	exit(1)
\fs32 \cf2 \strokec5 \
\pard\pardeftab720\partightenfactor0
\cf2 \strokec6 \
filter_arr = \cf2 \strokec7 [\cf2 \strokec6  \cf2 \strokec7 ]\cf2 \strokec6 \
filter_arr1 = \cf2 \strokec7 [\cf2 \strokec6  \cf2 \strokec7 ]\cf2 \strokec6 \
\pard\pardeftab720\partightenfactor0
\cf2 \strokec8 #request_html = requests.get("https://www.e-valuation.com.hk/evaluation/ERegion.html")\cf2 \strokec6 \
\
url = \cf2 \strokec9 "https://www.e-valuation.com.hk/evaluation/ERegion.html"\cf2 \strokec6 \
headers = \cf2 \strokec7 \{\cf2 \strokec6 \
    \cf2 \strokec9 'User-Agent'\cf2 \strokec7 :\cf2 \strokec6  \cf2 \strokec9 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'\cf2 \strokec6 \
\pard\pardeftab720\partightenfactor0
\cf2 \strokec7 \}\cf2 \strokec6 \
\
try:\
	response = requests.get\cf2 \strokec7 (\cf2 \strokec6 url\cf2 \strokec7 ,\cf2 \strokec6  headers=headers\cf2 \strokec7 ,\cf2 \strokec6  timeout=\cf2 \strokec10 15\cf2 \strokec7 )\cf2 \strokec6 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \strokec11 	from\cf2 \strokec6  bs4 \cf2 \strokec11 import\cf2 \strokec6  BeautifulSoup\
	soup = BeautifulSoup\cf2 \strokec7 (\cf2 \strokec6 response.text\cf2 \strokec7 ,\cf2 \strokec6  \cf2 \strokec9 "html.parser"\cf2 \strokec7 )\cf2 \strokec6  \cf2 \strokec8 ## \uc0\u21360 \u20986 \u25490 \u22909 \u29256 \u30340 HTML\u26550 \u27083 \cf2 \strokec6 \
\pard\pardeftab720\partightenfactor0
\cf2 \strokec8 	#print(soup.prettify())\cf2 \strokec6 \
	region_link = soup.find_all\cf2 \strokec7 (\cf2 \strokec9 'a'\cf2 \strokec7 )\cf2 \strokec6 \
\pard\pardeftab720\partightenfactor0
\cf2 \strokec11 	for\cf2 \strokec6  region_tag \cf2 \strokec12 in\cf2 \strokec6  region_link\cf2 \strokec7 :\cf2 \strokec6 \
\
  	aaa = \cf2 \strokec9 "District"\cf2 \strokec6  \cf2 \strokec12 in\cf2 \strokec6  region_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 )\cf2 \strokec6 \
  	\cf2 \strokec11 if\cf2 \strokec6  aaa == \cf2 \strokec13 True\cf2 \strokec7 :\cf2 \strokec6 \
    	request_html = requests.get\cf2 \strokec7 (\cf2 \strokec6 region_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 ))\cf2 \strokec6 \
    	soup_1 = BeautifulSoup\cf2 \strokec7 (\cf2 \strokec6 request_html.text\cf2 \strokec7 ,\cf2 \strokec6  \cf2 \strokec9 "html.parser"\cf2 \strokec7 )\cf2 \strokec6 \
    	district_link = soup_1.find_all\cf2 \strokec7 (\cf2 \strokec9 'a'\cf2 \strokec7 )\cf2 \strokec6 \
    	\cf2 \strokec11 for\cf2 \strokec6  district_tag \cf2 \strokec12 in\cf2 \strokec6  district_link\cf2 \strokec7 :\cf2 \strokec6 \
      		bbb = \cf2 \strokec9 "areas="\cf2 \strokec6  \cf2 \strokec12 in\cf2 \strokec6  district_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 )\cf2 \strokec6 \
      		\cf2 \strokec11 if\cf2 \strokec6  bbb == \cf2 \strokec13 True\cf2 \strokec7 :\cf2 \strokec6 \
        		request_html = requests.get\cf2 \strokec7 (\cf2 \strokec6 district_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 ))\cf2 \strokec6 \
        		soup_2 = BeautifulSoup\cf2 \strokec7 (\cf2 \strokec6 request_html.text\cf2 \strokec7 ,\cf2 \strokec6  \cf2 \strokec9 "html.parser"\cf2 \strokec7 )\cf2 \strokec6 \
        		area_link = soup_2.find_all\cf2 \strokec7 (\cf2 \strokec9 'a'\cf2 \strokec7 )\cf2 \strokec6 \
        		\cf2 \strokec11 for\cf2 \strokec6  area_tag \cf2 \strokec12 in\cf2 \strokec6  area_link\cf2 \strokec7 :\cf2 \strokec6 \
          			ccc = \cf2 \strokec9 'FindBlock'\cf2 \strokec6  \cf2 \strokec12 in\cf2 \strokec6  area_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 )\cf2 \strokec6 \
          			\cf2 \strokec11 if\cf2 \strokec6  ccc == \cf2 \strokec13 True\cf2 \strokec7 :\cf2 \strokec6 \
\
            			region_text = \cf2 \strokec9 'areas=NT'\cf2 \strokec6  \cf2 \strokec12 in\cf2 \strokec6  region_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 )\cf2 \strokec6 \
            			\cf2 \strokec11 if\cf2 \strokec6  region_text == \cf2 \strokec13 True\cf2 \strokec7 :\cf2 \strokec6 \
              				filter_arr.append\cf2 \strokec7 (\cf2 \strokec6 area_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 ))\cf2 \strokec6 \
              				filter_arr1.append\cf2 \strokec7 (\cf2 \strokec9 'New Territories,\uc0\u26032 \u30028 '\cf2 \strokec6  + \cf2 \strokec9 ' '\cf2 \strokec6  + district_tag.get_text\cf2 \strokec7 ()\cf2 \strokec6  + \cf2 \strokec9 ' '\cf2 \strokec6  + area_tag.get_text\cf2 \strokec7 ())\cf2 \strokec6 \
\
            			region_text = \cf2 \strokec9 'areas=IS'\cf2 \strokec6  \cf2 \strokec12 in\cf2 \strokec6  region_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 )\cf2 \strokec6 \
            			\cf2 \strokec11 if\cf2 \strokec6  region_text == \cf2 \strokec13 True\cf2 \strokec7 :\cf2 \strokec6 \
              				discovery_text = \cf2 \strokec9 'Discovery Bay'\cf2 \strokec6  \cf2 \strokec12 in\cf2 \strokec6  area_tag.get_text\cf2 \strokec7 ()\cf2 \strokec6 \
              				\cf2 \strokec11 if\cf2 \strokec6  discovery_text == \cf2 \strokec13 True\cf2 \strokec7 :\cf2 \strokec6 \
                				request_html = requests.get\cf2 \strokec7 (\cf2 \strokec6 area_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 ))\cf2 \strokec6 \
                				soup_3 = BeautifulSoup\cf2 \strokec7 (\cf2 \strokec6 request_html.text\cf2 \strokec7 ,\cf2 \strokec6  \cf2 \strokec9 "html.parser"\cf2 \strokec7 )\cf2 \strokec6 \
                				discovery_link = soup_3.find_all\cf2 \strokec7 (\cf2 \strokec9 'a'\cf2 \strokec7 )\cf2 \strokec6 \
                				\cf2 \strokec11 for\cf2 \strokec6  discovery_tag \cf2 \strokec12 in\cf2 \strokec6  discovery_link\cf2 \strokec7 :\cf2 \strokec6 \
                  					instr_discovery = \cf2 \strokec9 'Discovery%20Bay'\cf2 \strokec6  \cf2 \strokec12 in\cf2 \strokec6  discovery_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 )\cf2 \strokec6 \
                  					\cf2 \strokec11 if\cf2 \strokec6  instr_discovery == \cf2 \strokec13 True\cf2 \strokec7 :\cf2 \strokec6 \
                    					filter_arr.append\cf2 \strokec7 (\cf2 \strokec6 discovery_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 ))\cf2 \strokec6 \
                    					filter_arr1.append\cf2 \strokec7 (\cf2 \strokec6 district_tag.get_text\cf2 \strokec7 ()\cf2 \strokec6  + \cf2 \strokec9 ' '\cf2 \strokec6  + area_tag.get_text\cf2 \strokec7 ()\cf2 \strokec6  + \cf2 \strokec9 ' '\cf2 \strokec6  + discovery_tag.get_text\cf2 \strokec7 ())\cf2 \strokec6 \
\
              				\cf2 \strokec11 if\cf2 \strokec6  discovery_text == \cf2 \strokec13 False\cf2 \strokec7 :\cf2 \strokec6 \
                				filter_arr.append\cf2 \strokec7 (\cf2 \strokec6 area_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 ))\cf2 \strokec6 \
                				filter_arr1.append\cf2 \strokec7 (\cf2 \strokec6 district_tag.get_text\cf2 \strokec7 ()\cf2 \strokec6  + \cf2 \strokec9 ' '\cf2 \strokec6  + area_tag.get_text\cf2 \strokec7 ())\cf2 \strokec6 \
\
            			region_text = \cf2 \strokec9 'areas=KL'\cf2 \strokec6  \cf2 \strokec12 in\cf2 \strokec6  region_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 )\cf2 \strokec6 \
            			\cf2 \strokec11 if\cf2 \strokec6  region_text == \cf2 \strokec13 True\cf2 \strokec7 :\cf2 \strokec6 \
              				filter_arr.append\cf2 \strokec7 (\cf2 \strokec6 area_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 ))\cf2 \strokec6 \
              				filter_arr1.append\cf2 \strokec7 (\cf2 \strokec9 'Kowloon,\uc0\u20061 \u40845 '\cf2 \strokec6  + \cf2 \strokec9 ' '\cf2 \strokec6  + district_tag.get_text\cf2 \strokec7 ()\cf2 \strokec6  + \cf2 \strokec9 ' '\cf2 \strokec6  + area_tag.get_text\cf2 \strokec7 ())\cf2 \strokec6 \
\
            			region_text = \cf2 \strokec9 'areas=HK'\cf2 \strokec6  \cf2 \strokec12 in\cf2 \strokec6  region_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 )\cf2 \strokec6 \
            			\cf2 \strokec11 if\cf2 \strokec6  region_text == \cf2 \strokec13 True\cf2 \strokec7 :\cf2 \strokec6 \
              				filter_arr.append\cf2 \strokec7 (\cf2 \strokec6 area_tag.get\cf2 \strokec7 (\cf2 \strokec9 'href'\cf2 \strokec7 ))\cf2 \strokec6 \
              				filter_arr1.append\cf2 \strokec7 (\cf2 \strokec9 'Hong Kong,\uc0\u39321 \u28207 '\cf2 \strokec6  + \cf2 \strokec9 ' '\cf2 \strokec6  + district_tag.get_text\cf2 \strokec7 ()\cf2 \strokec6  + \cf2 \strokec9 ' '\cf2 \strokec6  + area_tag.get_text\cf2 \strokec7 ())\
\pard\pardeftab720\partightenfactor0
\cf2 \strokec6 \
\pard\pardeftab720\partightenfactor0

\fs36 \cf0 \cb1 \strokec4 	# --- 3. \uc0\u36039 \u26009 \u34389 \u29702 \u33287 \u23531 \u20837  Google Sheets --- \
	df = pd.DataFrame(\{'Estate Name': pd.Series(filter_arr1), 'Hypelink': pd.Series(filter_arr)\}) \
\
	# \uc0\u38283 \u21855 \u35430 \u31639 \u34920  (\u35531 \u30906 \u20445  Vigers \u24050 \u32147 \u20849 \u29992 \u32102 \u26381 \u21209 \u24115 \u25142  Email) \
	sh = gc.open('Vigers') \
	worksheet = sh.get_worksheet(0) \
\
	# \uc0\u28310 \u20633 \u36039 \u26009  \
	values = [df.columns.values.tolist()] + df.values.tolist() \
\
	# \uc0\u28165 \u38500 \u33290 \u20839 \u23481 \u20006 \u26356 \u26032 \
	worksheet.clear() \
	worksheet.update(values=values, range_name='A1') \
\
	print(f"\uc0\u36039 \u26009 \u26356 \u26032 \u25104 \u21151 \u65281 \u20849 \u26377  \{len(df)\} \u31558 \u36039 \u26009 \u12290 ")\
\
except Exception as e: \
	print(f"\uc0\u22519 \u34892 \u36942 \u31243 \u20013 \u30332 \u29983 \u37679 \u35492 : \{e\}")}