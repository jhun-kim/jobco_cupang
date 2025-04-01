import datetime
import subprocess
import time
import random

from selenium.webdriver.support import expected_conditions as EC

import chromedriver_autoinstaller
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import os

from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
import json
from openpyxl import load_workbook
def set_chrome_debug(visualize):
    os.environ["PATH"] += os.pathsep + "/usr/bin/chromium-browser"
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    # Create ChromeOptions instance
    subprocess.Popen(
    [
        "/usr/bin/chromium-browser",  # Linux 기반 Streamlit Cloud에서 Chromium 실행
        "--remote-debugging-port=9222",
        "--user-data-dir=/tmp/chromeCookie"  # Linux에서 사용할 쿠키 저장소 경로
    ],
    stdout=subprocess.DEVNULL,  # 로그 출력 방지
    stderr=subprocess.DEVNULL,  # 에러 로그 출력 방지
)
    webdriver_options = webdriver.ChromeOptions()

    if not visualize:
        webdriver_options.add_argument('headless')

    try:
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/chromium-browser"  # Streamlit Cloud에서 Chromium 실행 경로
        options.add_argument("--headless")  # Streamlit Cloud에서는 반드시 headless 모드 사용
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(options=webdriver_options)

    return driver

def job_type_func(job_type, driver):
    job_types = driver.find_elements(By.CSS_SELECTOR, '#akc_0')
    for i in range(len(job_types)):
        job_name = job_types[i]
        if job_type in job_name.text:
            job_name.click()
            time.sleep(1)

def options_func(location_list, location, career, driver, key_word):
    options = ['#dev-local-filter-item', '#dev-career-filter-item']
    for i in range(len(options)):
        option = driver.find_elements(By.CSS_SELECTOR, f'{options[i]}')
        option_name = option[0]
        if location in option_name.text:
            option_name.click()
            location_names = driver.find_elements(By.CSS_SELECTOR,
                                                  '#dev-local-filter-item > dialog > div.scroll-area > ul.step.dev-local-ctgr-step > li')
            for j in range(len(location_names)):
                location_name = location_names[j]
                if '서울' in location_name.text:
                    location_name.click()
                    # local_step2_B000_ly > li:nth-child(1)
                    location_details = driver.find_elements(By.CSS_SELECTOR, '#local_step2_I000_ly > li')
                # else:
                #     location_details = driver.find_elements(By.CSS_SELECTOR, '#local_step2_B000_ly > li')

                    for k in range(len(location_details)):
                        location_detail = location_details[k]
                        if location_detail.text in location_list:
                            location_detail.click()
                    done_btn = driver.find_element(By.CSS_SELECTOR,
                                                   '#dev-local-filter-item > dialog > div.dialog-footer > div.button-wrap > button.button-submit')
                    done_btn.click()

        elif career in option_name.text:
            option_name.click()

            # 신입, 경력, 경력무관
            types = driver.find_elements(By.CSS_SELECTOR,
                                         '#dev-career-filter-item > dialog > div.dialog-content > ul.checkbox-list.vertical-line > li')
            for j in range(len(types)):

                if key_word != "연예":
                    type_name = types[j]
                    #######################
                    # if '경력' in type_name.text:
                    #     continue
                    #######################
                    type_name.click()
                else:
                    if j > 0:
                        continue

                    type_name = types[j]
                    type_name.click()
            #######################
            if key_word != "연예":
                input_year_1 = driver.find_element(By.CSS_SELECTOR, '#CareerYearMin')
                input_year_2 = driver.find_element(By.CSS_SELECTOR, '#CareerYearMax')
                input_year_1.send_keys('1')
                input_year_2.send_keys('3')
            #######################
            done_btn = driver.find_element(By.CSS_SELECTOR,
                                           '#dev-career-filter-item > dialog > div.dialog-footer > div.button-wrap > button.button-submit')
            done_btn.click()

        else:
            continue

def list_ting(driver, key_word):

    num = 1
    job_list = []

    while True:
        try:
            time.sleep(1.5)
            search_lists = driver.find_elements(By.CSS_SELECTOR,
                                                '#dev-content-wrap > article > section.content-recruit.on > article.list > article')
            for j in range(len(search_lists)):
                search_list_name = search_lists[j]
                if '홈페이지 지원' in search_list_name.text:
                    continue
                info = search_list_name.get_attribute('data-gainfo')
                info = json.loads(info)
                url = search_list_name.get_attribute('data-gavirturl')

                co_name = info['dimension48']  # 회사이름
                co_type = info['dimension43']  # 회사업종
                co_job_type = info['dimension45']  # 잡타이틀
                if key_word != '연예':
                    if '취업' in co_job_type:
                        continue
                else:
                # if '매니' in co_job_type:
                    if ('마케' not in co_job_type and '광고' not in co_job_type) or '팬마케' in co_job_type:
                        continue

                job_dict = {}
                job_dict['company_name'] = co_name
                job_dict['company_type'] = co_type
                job_dict['job_title'] = co_job_type
                # https: // www.jobkorea.co.kr / Recruit / GI_Read / 45092993?PageGbn = HH & logpath = 1 & stext = python & listno = 87
                # https: // www.jobkorea.co.kr / Recruit / GI_Read / 45092993?PageGbn = HH & logpath = 1 & stext = python & listno = 87
                job_dict['url'] = url.replace('/virtual', '')
                job_list.append(job_dict)

            next_btn = driver.find_element(By.CSS_SELECTOR,
                                           '#dev-content-wrap > article > section.content-recruit.on > article.tplPagination.pagenation > button.button-next')
            next_btn.click()
            num += 1
        except Exception as e:
            print(e)
            # first_btn = driver.find_element(By.CSS_SELECTOR, '#dev-content-wrap > article > section.content-recruit.on > article.tplPagination.pagenation > button:nth-child(2)')
            # first_btn.click()
            break
    return job_list

def total_info(result, driver, location_list, key_word):
    time.sleep(3)
    df_list = []
    try:
        check_df = pd.read_csv(f'{location_list}_{key_word}_잡코리아.csv', encoding='cp949')
        for c in range(len(result)):
            check_job_company_name = result[c]['company_name']
            check_job_title = result[c]['job_title']
            check = check_df[check_df['company_name'] == check_job_company_name].reset_index(drop=True)
            check = check[check['job_title'] == check_job_title].reset_index(drop=True)

            if len(check) > 0:
                continue
            else:
                df_list.append(result[c])

        if len(df_list) > 0:
            total_df = df_list
        else:
            total_df = None
            return total_df
    except:
        total_df = result



    # total_df['지원자수'] = 0
    # total_df['모집인원'] = 0
    co_location = None
    co_employee = None
    end_time = None
    time_num = random.randint(1, 4)
    for i in tqdm(range(len(total_df))):
        try:
            time_num = random.randint(1,4)

            df_url = total_df[i]['url']
            driver.get(df_url)
            # df_info = total_df[i].to_dict(orient='records')

            co_location = driver.find_element(By.CSS_SELECTOR, '#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div:nth-child(2) > dl > dd:nth-child(6) > a')
            co_location = co_location.text
            co_employee = driver.find_element(By.CSS_SELECTOR, '#container > section > div.readSumWrap.clear > article > div.tbRow.clear > div.tbCol.tbCoInfo > dl > dd:nth-child(4)')
            co_employee = co_employee.text
            if '명' in str(co_employee):
                co_employee = int(str(co_employee).replace("명", ''))
            else:
                co_employee = 0

            end_time = driver.find_element(By.CSS_SELECTOR, '#tab02 > div.divReadBx.clear.devMakeSameHeight > article.artReadPeriod > div > dl.date > dd:nth-child(4) > span')
            end_time = end_time.text.replace(".", "-")

            apply_num = driver.find_element(By.CSS_SELECTOR,
                                            '#detailArea > section.secReadStatistic > article > div.metricsContainer > div.metrics.metricsCount > div.value')
            apply_num = int(apply_num.text.split('명')[0])
            gain_num = driver.find_element(By.CSS_SELECTOR,
                                           '#detailArea > section.secReadStatistic > article > div.metricsContainer > div.metrics.metricsRate > div.value')
            gain_num = gain_num.text.split('명')[0]

            total_df[i]['지원자수'] = apply_num
            total_df[i]['모집인원'] = gain_num
            total_df[i]['지역'] = co_location
            total_df[i]['인원수'] = co_employee
            total_df[i]['마감일'] = end_time
            time.sleep(time_num)
        except:
            total_df[i]['지원자수'] = -1
            total_df[i]['모집인원'] = -1
            total_df[i]['지역'] = co_location
            total_df[i]['인원수'] = co_employee
            total_df[i]['마감일'] = end_time
            print(total_df[i])
            time.sleep(time_num)
        # time.sleep(0.5)
        # df_info['지원자수'] = apply_num
        # df_info['모집인원'] = gain_num
        # df_list.append(df_info)
    # df_list = total_df.to_dict(orient='records')
    return total_df

def merge_df(today, location_list, key_word):
    # yesterday = str(datetime.datetime.now()-datetime.timedelta(days=1)).split(" ")[0]
    try:
        or_df = pd.read_csv(f'{location_list}_{key_word}_잡코리아.csv', encoding='cp949')
    except:
        return
    new_df = pd.read_csv(f'{today}_{location_list}_{key_word}_잡코리아.csv', encoding='cp949')
    or_df = or_df[['company_name',	'company_type',	'job_title',	'url',	'지원자수',	'모집인원',	'지역',	'인원수',	'마감일']]
    new_df = new_df[['company_name',	'company_type',	'job_title',	'url',	'지원자수',	'모집인원',	'지역',	'인원수',	'마감일']]
    # new_df_2 = pd.read_csv(f'{yesterday}_{location_list}_{key_word}_잡코리아.csv', encoding='cp949')
    merge_total_df = pd.concat([or_df, new_df]).reset_index(drop=True)
    # merge_total_df = pd.concat([merge_total_df, new_df_2]).reset_index(drop=True)
    merge_total_df = merge_total_df.sort_values(['지원자수', '모집인원', '인원수'], ascending=[True, True, False]).reset_index(drop=True)
    # print(merge_total_df)
    merge_total_df.to_csv(f'{location_list}_{key_word}_잡코리아.csv', encoding='cp949')

def login_func(driver):
    try:
        url = 'https://www.jobkorea.co.kr/Login/Logout.asp'
        driver.get(url)
        # devMemTab > li.on
        time.sleep(2)
        taps = driver.find_elements(By.CSS_SELECTOR, '#devMemTab > li')
        for t in range(len(taps)):
            tap = taps[t]
            tap_name = tap.text
            if "개인회원" in tap_name:
                tap.click()
            else:
                continue

        time.sleep(3)
        login = driver.find_element(By.CSS_SELECTOR, '#M_ID')
        login.send_keys('gyjh486')
        pw = driver.find_element(By.CSS_SELECTOR, '#M_PWD')
        pw.send_keys('dkrkwk18!')
        login_click = driver.find_element(By.CSS_SELECTOR,
                                          '#login-form > fieldset > section.login-input > button')
        login_click.click()

        return True
    except:
        return False

def ai_recom():
    today = str(datetime.datetime.today()).split(" ")[0]
    location_list = 'AI'
    key_word = '추천'
    # merge_df(today, location_list, key_word)


    driver = set_chrome_debug(True)

    login_func(driver)

    url = "https://www.jobkorea.co.kr/User/AI?SourceType=11"
    driver.get(url)

    job_list = []
    taps = driver.find_elements(By.CSS_SELECTOR, '#container > section.content > div > div.mtuTab > ul > li')
    for i in range(len(taps)):
        if i > 0:
            taps[i].click()

        list_comps = driver.find_elements(By.CSS_SELECTOR, '#container > section.content > div > div.ai-recommendations-list > ul > li')
        for j in range(len(list_comps)):
            # container > section.content > div > div.ai-recommendations-list > ul > li:nth-child(100) > div.recruit-company
            # container > section.content > div > div.ai-recommendations-list > ul > li:nth-child(2)
            if '홈페이지 지원' in list_comps[j].text:
                continue
            try:
                co_name = list_comps[j].find_element(By.CSS_SELECTOR, f'#container > section.content > div > div.ai-recommendations-list > ul > li:nth-child({j+1}) > div.recruit-company > div.headers > div')
            except:
                print(j)
            co_job_type = list_comps[j].find_element(By.CSS_SELECTOR, f'#container > section.content > div > div.ai-recommendations-list > ul > li:nth-child({j+1}) > div.recruit-content > div > a')
            co_type = list_comps[j].find_element(By.CSS_SELECTOR, f'#container > section.content > div > div.ai-recommendations-list > ul > li:nth-child({j+1}) > div.recruit-content > a > div.job')
            co_url = co_job_type.get_attribute("href")

            job_dict = {}
            job_dict['company_name'] = co_name.text
            job_dict['company_type'] = co_type.text
            job_dict['job_title'] = co_job_type.text
            job_dict['url'] = co_url
            job_list.append(job_dict)

    result = job_list
    df = total_info(result, driver, location_list, key_word)
    if df is None:
        driver.quit()
        print('새로운 데이터가 없습니다.')
        return

    total_df = pd.DataFrame(df).reset_index(drop=True)
    # total_df = total_df.sort_values(['지원자수', '모집인원'], ascending=True).reset_index(drop=True)
    total_df = total_df.sort_values(['인원수', '지원자수', '모집인원'], ascending=[False, True, True]).reset_index(drop=True)
    total_df.to_csv(f'{today}_{location_list}_{key_word}_잡코리아.csv', encoding='cp949')
    # total_df.to_csv(f'{today}_{location_list}_{key_word}_잡코리아.xlsx')
    # auto_column_dimension(f'{today}_{location_list}_{key_word}_잡코리아.xlsx')
    # driver.quit()
    merge_df(today, location_list, key_word)
    path = os.path.realpath("./")
    os.startfile(path)

def main_fucntion(driver, key_word, job_type,location_list, location, career, today):
    # 검색어
    search = driver.find_element(By.CSS_SELECTOR, '#stext')
    search.send_keys(key_word)
    time.sleep(1)

    # 잡 타입찾기
    job_type_func(job_type, driver)

    # 지역, 경력설정
    options_func(location_list, location, career, driver, key_word)

    # 리스팅
    result = list_ting(driver, key_word)

    # 지원자, 모집인원정보

    df = total_info(result, driver, location_list, key_word)
    if df is None:
        driver.close()
        print('새로운 데이터가 없습니다.')
        return False
    total_df = pd.DataFrame(df).reset_index(drop=True)
    # total_df = total_df.sort_values(['지원자수', '모집인원'], ascending=True).reset_index(drop=True)
    total_df = total_df.sort_values(['인원수', '지원자수', '모집인원'], ascending=[False, True, True]).reset_index(drop=True)
    total_df.to_csv(f'{today}_{location_list}_{key_word}_잡코리아.csv', encoding='cp949')
    # total_df.to_excel(f'{today}_{location_list}_{key_word}_잡코리아.xlsx')
    # auto_column_dimension(f'{today}_{location_list}_{key_word}_잡코리아.xlsx')
    # driver.quit()
    merge_df(today, location_list, key_word)
    path = os.path.realpath("./")
    os.startfile(path)
    return True


def print_hi(name):
    today = str(datetime.datetime.today()).split(" ")[0]


    key_word = '연예'
    key_word = 'AWS'
    key_word = '데이터라벨링'
    key_word = 'python'
    # key_word = 'java'
    job_type = '산업'
    job_type = '전문분야'
    job_type = '스킬'
    location = '지역'
    career = '경력'

    # key_word = '해외무역'
    # job_type = '전문분야'
    # location = '지역'
    # career = '경력'

    location_list = []
    location_list = ['구로구', '동대문구', '강남구']
    # location_list = ['성남시 분당구']
    # location_list = ['강남구']
    location_list = ['전체']
    location_list = ['강남구']
    location_list = ['강서구', '양천구', '영등포구', '마포구', '용산구']
    location_list = ['동대문구', '중구', '종로구']
    location_list = ['서대문구']
    location_list = ['금천구']
    location_list = ['구로구']

    location_dict = [
        {"0" : ['강서구', '양천구', '영등포구', '마포구', '용산구']},
        {"1" : ['동대문구', '중구', '종로구']},
        {"2" : ['서대문구']},
        {"3" : ['금천구']},
        {"4" : ['구로구']},
        {"5" : ['강남구']},
        {"6" : ['동작구']},
    ]

    for lo in range(len(location_dict)):
        url = 'https://www.jobkorea.co.kr/'
        driver = set_chrome_debug(True)

        # login_func(driver)

        driver.get(url)
        location_list = location_dict[lo][str(lo)]
        print(f"총 {len(location_dict)}개 중 {lo} 번째 검색 시작 : {location_list}.....")
        flage = main_fucntion(driver, key_word, job_type, location_list, location, career, today)
        if flage:
            driver.close()

    # #검색어
    # search = driver.find_element(By.CSS_SELECTOR, '#stext')
    # search.send_keys(key_word)
    # time.sleep(1)
    #
    # #잡 타입찾기
    # job_type_func(job_type, driver)
    #
    # #지역, 경력설정
    # options_func(location_list, location, career, driver, key_word)
    #
    # #리스팅
    # result = list_ting(driver, key_word)
    #
    # #지원자, 모집인원정보
    #
    # df = total_info(result, driver, location_list, key_word)
    # if df is None:
    #     driver.close()
    #     print('새로운 데이터가 없습니다.')
    #     return
    # total_df = pd.DataFrame(df).reset_index(drop=True)
    # # total_df = total_df.sort_values(['지원자수', '모집인원'], ascending=True).reset_index(drop=True)
    # total_df = total_df.sort_values(['인원수', '지원자수', '모집인원'], ascending=[False, True,True]).reset_index(drop=True)
    # total_df.to_csv(f'{today}_{location_list}_{key_word}_잡코리아.csv', encoding='cp949')
    # # driver.quit()
    # merge_df(today, location_list, key_word)
    # path = os.path.realpath("./")
    # os.startfile(path)

def test19():
    file = r"C:\Users\LeadersTrading\Desktop\잡코\2025-03-13_AI_추천_잡코리아.csv"
    new_file = r"C:\Users\LeadersTrading\Desktop\잡코\2025-03-13_AI_추천_잡코리아.xlsx"
    df = pd.read_csv(file, encoding='cp949')
    df.to_excel(new_file)
    print(df)

def auto_column_dimension(new_file=None):
    # new_file = r"C:\Users\LeadersTrading\Desktop\잡코\2025-03-13_AI_추천_잡코리아.xlsx"
    # 엑셀 파일 열기
    wb = load_workbook(new_file)
    ws = wb.active

    # 특정 열의 너비 자동 조절 (A, B 열 조정 예시)
    for col in ["C", "E", "I"]:  # 원하는 열 추가 가능
        ws.column_dimensions[col].auto_size = True  # 자동 너비 설정 (openpyxl은 직접 지정해야 함)

    # 파일 저장
    wb.save(new_file)
    wb.close()

if __name__ == '__main__':
    # test()
    # print_hi('PyCharm')
    ai_recom()
    # auto_column_dimension()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
