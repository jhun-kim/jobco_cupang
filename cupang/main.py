import datetime
import subprocess
import time
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
from selenium_stealth import stealth
import undetected_chromedriver as uc
# from seleniumwire import webdriver


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def set_chrome_secret(visualize):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    # Create ChromeOptions instance
    webdriver_options = webdriver.ChromeOptions()

    if not visualize:
        webdriver_options.add_argument('headless')

    try:
        # To disable images and improve performance:
        webdriver_options.add_argument('--incognito')
        webdriver_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        webdriver_options.add_argument("referer=https://www.coupang.com/")
        webdriver_options.add_argument("accept-language=ko-KR,ko;q=0.9")
        driver = webdriver.Chrome(options=webdriver_options)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(options=webdriver_options)

    return driver


def set_chrome(visualize):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    # Create ChromeOptions instance
    webdriver_options = webdriver.ChromeOptions()

    if not visualize:
        webdriver_options.add_argument('headless')

    try:
        webdriver_options.add_argument("--remote-debugging-port=9222")  # 필요 시 포트 변경 가능
        webdriver_options.add_argument("--user-data-dir=C:\\chromeCookie")  # 크롬 프로필 유지
        webdriver_options.add_argument("--disable-infobars")
        webdriver_options.add_argument("--disable-popup-blocking")
        webdriver_options.add_argument("--disable-gpu")
        webdriver_options.add_argument("--no-sandbox")
        webdriver_options.add_argument("--disable-dev-shm-usage")

        # prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
        #                                                     'geolocation': 2, 'notifications': 2,
        #                                                     'auto_select_certificate': 2, 'fullscreen': 2,
        #                                                     'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
        #                                                     'media_stream_mic': 2, 'media_stream_camera': 2,
        #                                                     'protocol_handlers': 2, 'ppapi_broker': 2,
        #                                                     'automatic_downloads': 2, 'midi_sysex': 2,
        #                                                     'push_messaging': 2, 'ssl_cert_decisions': 2,
        #                                                     'metro_switch_to_desktop': 2,
        #                                                     'protected_media_identifier': 2, 'app_banner': 2,
        #                                                     'site_engagement': 2, 'durable_storage': 2}}
        # webdriver_options.add_experimental_option('prefs', prefs)
        # To disable images and improve performance:
        webdriver_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=webdriver_options)

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(options=webdriver_options)

    return driver

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
        # webdriver_options.add_argument('headless')
        webdriver_options.add_argument('--headless=new')

    try:
        options = webdriver.ChromeOptions()
        options.binary_location = "/usr/bin/chromium-browser"  # Streamlit Cloud에서 Chromium 실행 경로
        options.add_argument("--headless")  # Streamlit Cloud에서는 반드시 headless 모드 사용
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = uc.Chrome(options=options)

    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(options=webdriver_options)

    return driver

def set_chrome_mobile(visualize):
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    # Create ChromeOptions instance
    # subprocess.Popen(
    #     r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')
    webdriver_options = webdriver.ChromeOptions()

    if not visualize:
        webdriver_options.add_argument('headless')



    try:
        user_agt = 'Mozilla/5.0 (Linux; Android 9; INE-LX1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36'
        webdriver_options.add_argument(f'user-agent={user_agt}')
        webdriver_options.add_argument("window-size=412,950")
        webdriver_options.add_experimental_option("mobileEmulation",
                                                   {"deviceMetrics": {"width": 360, "height": 760, "pixelRatio": 3.0}})
        driver = webdriver.Chrome(options=webdriver_options)

    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(options=webdriver_options)

    return driver

def cu_print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    url = 'https://www.coupang.com/np/goldbox'
    # driver = set_chrome_debug(True)
    driver = set_chrome_debug(True)
    driver.implicitly_wait(2)
    driver.get(url)
    # time.sleep(10)
    # driver.implicitly_wait(10)

    #골든박스 물품리스트 갖고 오기
    # contents > div > div > div:nth-child(3)
    main_list = []
    pd_list = driver.find_elements(By.CSS_SELECTOR, '#widget-group > div > span > div > div > div > div > div > div > div > div > div > div')
    for i in range(len(pd_list)):
        try:
            if '한정수량 마감' in pd_list[i].text:
                print(f'''{i}번째 한정수량 마감 {pd_list[i].text}''')
                continue
            try:
                url = pd_list[i].find_element(By.TAG_NAME, "a")
                url_info = url.get_attribute("href")

            except Exception as e:
                num = 50 * i
                driver.execute_script(f"window.scrollBy(0, {num});")  # Scroll down
                scroll_position = driver.execute_script("return window.scrollY;")  # Get current scroll position
                print(f'Scroll position after error: {scroll_position}')

            # widget-group > div:nth-child(3) > span > div > div:nth-child(2) > div > div > div > div > div > div > div > div:nth-child(1) > div > a > div > div.info_section > div.info-section__title-wrap > span
            name = url.find_element(By.CSS_SELECTOR, "div > div.info_section > div.info-section__title-wrap > span")
            name_info = name.text
            try:
                saled_rate = url.find_element(By.CSS_SELECTOR, 'div > div.info_section > div.sale-progress-bar.sale-progress-bar--inline')
                saled_rate_info = saled_rate.text.split('%')[0]
            except:
                saled_rate_info = "0"

            pd_dict = {}
            pd_dict['name'] = name_info
            pd_dict['url'] = "&".join([url_info, "isAddedCart="])
            pd_dict['saled_rate'] = int(saled_rate_info)
            main_list.append(pd_dict)

            print(f'''{i} {pd_list[i].text}''')
            print(' ')
        except:
            print(f'''{i}번째 아웃 {pd_list[i].text}''')
            print(' ')
            break

    new_main_list = []
    main_df = pd.DataFrame(main_list).reset_index(drop=True)
    main_df = main_df.drop_duplicates(subset=['name']).reset_index(drop=True)
    print(f'총 상품갯수 {len(main_df)}')
    # driver = set_chrome_mobile(True)
    #쿠팡가격과 할인가격 비교해서 격차가 가장 큰 리스트 보기
    for j in tqdm(range(len(main_df))):
        name = main_df['name'][j]
        url = main_df['url'][j]
        saled_rate = main_df['saled_rate'][j]
        driver.get(url)
        time.sleep(0.1)

        # try:
        #     element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, "prod-price"))
        # )
        # except:
        #     pass

        # 쿠팡할인가
        cupang_price = cupang_price_func(driver)

        # 와우할인가
        wow_price, wow_price_gram, wow_price_gram_won = wow_price_func(driver)


        #평점 확인
        total_est_num, bad_est_rate = est_check(driver)
        bad_est_num = bad_est_rate / 100
        bad_est_num = total_est_num * bad_est_num


        pd_dict = {}
        pd_dict['name'] = name
        pd_dict['url'] = url
        pd_dict['saled_rate'] = saled_rate
        pd_dict['cupang_price'] = int(cupang_price[0].split("원")[0].replace(",", ""))
        pd_dict['wow_price'] = int(wow_price[0].split("원")[0].replace(",", ""))
        pd_dict['wow_price_gram'] = wow_price_gram
        pd_dict['wow_price_gram_won'] = wow_price_gram_won
        pd_dict['total_est_num'] = total_est_num
        pd_dict['bad_est_num'] = bad_est_num
        pd_dict['bad_est_rate'] = bad_est_rate

        # print(f'{j+1}_{pd_dict}')
        new_main_list.append(pd_dict)
        # driver.quit()

    new_main_df = pd.DataFrame(new_main_list).reset_index(drop=True)
    new_main_df['discount_rate'] = abs(new_main_df['wow_price'] / new_main_df['cupang_price'] - 1) * 100
    new_main_df['discount_won'] = new_main_df['cupang_price'] - new_main_df['wow_price']
    # new_main_df['est_rate'] = (new_main_df['bad_est_num'] / new_main_df['total_est_num']) * 100
    new_main_df = new_main_df.sort_values(by=['discount_rate'], ascending=False).reset_index(drop=True)


    today = str(datetime.datetime.today()).split(' ')[0]
    total_df_cleaned = new_main_df.applymap(lambda x: x.replace('\u2b50', ' ') if isinstance(x, str) else x)
    total_df_cleaned = total_df_cleaned.applymap(lambda x: x.replace('\ufe0f', ' ') if isinstance(x, str) else x)
    total_df_cleaned.to_csv(f'{today}_골든박스.csv', encoding='cp949')
    path = os.path.realpath("./")
    os.startfile(path)
    # driver.close()


def cupang_price_func(driver):
    try:
        # 쿠팡판매가
        #contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price.fix-verdor-section-display > div.prod-price-container > div.prod-price > div > div.prod-sale-price.price-align.sale-price-coupon
        cupang_price = driver.find_element(By.CSS_SELECTOR,
                                           '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div > div.prod-sale-price.price-align.wow-only-coupon')
        cupang_price = cupang_price.text.split("\n")
        if "쿠팡판매가" not in cupang_price and "즉시할인가" not in cupang_price:
            try:
                # cupang_price = driver.find_element(By.CSS_SELECTOR,'#MWEB_PRODUCT_DETAIL_ATF_PRICE_INFO > div > div.PriceInfo_anchorPriceArea__iXmSu > span.PriceInfo_originalPrice__t8M_9')
                #contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.with-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div.prod-price-onetime > div.prod-origin-price > span.origin-price
                cupang_price = driver.find_element(By.CSS_SELECTOR,
                                                   '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div > div.prod-origin-price > span.origin-price')
                cupang_price = [cupang_price.text]
            except:
                cupang_price = cupang_price_func_2(driver)
            return cupang_price

        return cupang_price

    except:
        # 쿠팡판매가
        cupang_price = cupan_direct_price(driver)
        if "0원" in cupang_price:
            cupang_price = cupang_price_func_2(driver)
            return cupang_price

        return cupang_price

def cupang_price_func_2(driver):
    try:
        try:
            # 쿠팡판매가
            # contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price.fix-verdor-section-display > div.prod-price-container > div.prod-price > div > div.prod-sale-price.price-align.sale-price-coupon
            cupang_price = driver.find_element(By.CSS_SELECTOR,
                                               '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div > div.prod-sale-price.price-align.wow-only-coupon')
            cupang_price = cupang_price.text.split("\n")
        except:

            cupang_price = driver.find_element(By.CSS_SELECTOR, '#contents > div > div > div > div > div > div > div')
            # cupang_price = driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.dawn-only-product.without-subscribe-buy-type.DISPLAY_0.only-one-delivery.fix-verdor-section-display.update-price-section-style-with-rds > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.major-price-coupon')
            # cupang_price = driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div.prod-atf-main > div > div.prod-price-container > div.prod-price > div > div.prod-origin-price > span.origin-price')
            # cupang_price = driver.find_element(By.CSS_SELECTOR, '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price.fix-verdor-section-display > div.prod-price-container > div.prod-price > div > div.prod-sale-price.price-align.sale-price-coupon')

            test = cupang_price.text
            # cupang_price = cupang_price.text.split(" ")[1]
            if "%" in test:
                cupang_price = cupang_price.text.split(" ")[1]
            else:
                cupang_price = cupang_price.text.split("\n")[0]
            # cupang_price = [cupang_price.text]
            cupang_price = [cupang_price]
            print(f'쿠팡가격: {cupang_price}')
            return cupang_price

        if "쿠팡판매가" not in cupang_price and "즉시할인가" not in cupang_price:
            try:
                # cupang_price = driver.find_element(By.CSS_SELECTOR,'#MWEB_PRODUCT_DETAIL_ATF_PRICE_INFO > div > div.PriceInfo_anchorPriceArea__iXmSu > span.PriceInfo_originalPrice__t8M_9')
                # contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.with-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div.prod-price-onetime > div.prod-origin-price > span.origin-price
                #.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price
                cupang_price = driver.find_element(By.CSS_SELECTOR,
                                                   '#contents > div.prod-atf > div.prod-atf-main > div > div.prod-price-container > div.prod-price > div > div.prod-origin-price > span.origin-price')
                cupang_price = [cupang_price.text]
            except:
                cupang_price = ["0원"]

            return cupang_price

        return cupang_price
    except:
        # 쿠팡판매가
        cupang_price = ["0원"]
        return cupang_price

def cupan_direct_price(driver):
    try:
        cupang_price = driver.find_element(By.CSS_SELECTOR,
                                           '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.only-one-delivery.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div > div.prod-origin-price > span')
        cupang_price = cupang_price.text.split("\n")
        if "쿠팡판매가" not in cupang_price and "즉시할인가" not in cupang_price:
            try:
                # cupang_price = driver.find_element(By.CSS_SELECTOR,'#MWEB_PRODUCT_DETAIL_ATF_PRICE_INFO > div > div.PriceInfo_anchorPriceArea__iXmSu > span.PriceInfo_originalPrice__t8M_9')
                cupang_price = driver.find_element(By.CSS_SELECTOR,
                                                   '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div > div.prod-origin-price > span.origin-price')
                cupang_price = [cupang_price.text]
            except:
                cupang_price = ["0원"]

            return cupang_price

        return cupang_price

    except:
        # 쿠팡판매가
        cupang_price = ["0원"]
        return cupang_price
def wow_price_func(driver):
    try:
        # contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.with-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div.prod-price-onetime > div.prod-coupon-price.price-align.major-price-coupon
        wow_price = driver.find_element(By.CSS_SELECTOR,
                                        '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.major-price-coupon')
        wow_price = wow_price.text.split("\n")
        if len(wow_price) > 1:
            wow_price_gram = wow_price[1]
            if "원" not in wow_price_gram:
                wow_price_gram = 0
                wow_price_gram_won = 0
            else:
                wow_price_gram_won = int(wow_price_gram.split(' ')[1].split("원")[0].replace(",", ""))

            return wow_price, wow_price_gram, wow_price_gram_won
        else:
            wow_price_gram = 0
            wow_price_gram_won = 0
            return wow_price, wow_price_gram, wow_price_gram_won
    except:
        try:
            wow_price = driver.find_element(By.CSS_SELECTOR,
                                            '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.with-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div.prod-price-onetime > div.prod-coupon-price.price-align.major-price-coupon')
            wow_price = wow_price.text.split("\n")
            if len(wow_price) > 1:
                wow_price_gram = wow_price[1]
                if "원" not in wow_price_gram:
                    wow_price_gram = 0
                    wow_price_gram_won = 0
                else:
                    wow_price_gram_won = int(wow_price_gram.split(' ')[1].split("원")[0].replace(",", ""))

                return wow_price, wow_price_gram, wow_price_gram_won
            else:
                wow_price_gram = 0
                wow_price_gram_won = 0
                return wow_price, wow_price_gram, wow_price_gram_won
        except:
            wow_price, wow_price_gram, wow_price_gram_won = wow_direct_price(driver)
            return wow_price, wow_price_gram, wow_price_gram_won
def wow_direct_price(driver):
    try:
        wow_price = driver.find_element(By.CSS_SELECTOR,
                                        '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.wow-only-coupon')

        wow_price = wow_price.text.split("\n")
        if len(wow_price) > 1:
            wow_price_gram = wow_price[1]
            if "원" not in wow_price_gram:
                wow_price_gram = 0
                wow_price_gram_won = 0
            else:
                wow_price_gram_won = int(wow_price_gram.split(' ')[1].split("원")[0].replace(",", ""))

        else:
            wow_price_gram = 0
            wow_price_gram_won = 0

        return wow_price, wow_price_gram, wow_price_gram_won
    except:
        wow_price = ["0원"]
        wow_price_gram = 0
        wow_price_gram_won = 0
        return wow_price, wow_price_gram, wow_price_gram_won




def est_check(driver):
    #상품평 총갯수 확인
    #별점1 갯수 확인 -> 비율 확인

    try:
        total_est = driver.find_element(By.CSS_SELECTOR, '#prod-review-nav-link > span.count')
        total_est_num = int(total_est.text.split('개')[0].replace(",", ""))

        time.sleep(2)
        total_est.click()
    except:
        return 0, 0



    # content = driver.find_element(By.TAG_NAME, "iframe")
    # print(content.text)
    # driver.switch_to.frame(content)
    #
    try:
        element_0 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sdp-review__average__total-star__info-detail"))
        )

        element_1 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "#btfTab > ul.tab-contents > li.product-review.tab-contents__content > div > div.sdp-review__article.js_reviewArticleContainer > section.sdp-review__article__order.js_reviewArticleOrderContainer.sdp-review__article__order--active"))
        )
    except:
        time.sleep(4)

    try:
        # bad_est = driver.find_element(By.CSS_SELECTOR, '#btfTab > ul.tab-contents > li.product-review.tab-contents__content > div > div.sdp-review__article.js_reviewArticleContainer > section.sdp-review__article__order.js_reviewArticleOrderContainer.sdp-review__article__order--active > div.sdp-review__article__order__star.js_reviewArticleSearchStarSelectBtn')
        bad_est = driver.find_element(By.CSS_SELECTOR,
                                      '#btfTab > ul.tab-contents > li.product-review.tab-contents__content > div > div.sdp-review__average.js_reviewAverageContainer > section.sdp-review__average__total-star > div.sdp-review__average__total-star__info > div.sdp-review__average__total-star__info-detail > span')
        bad_est.click()
    except:
        return 0, 0

    try:
        # bad_est = driver.find_element(By.CSS_SELECTOR, '#btfTab > ul.tab-contents > li.product-review.tab-contents__content > div > div.sdp-review__article.js_reviewArticleContainer > section.sdp-review__article__order.js_reviewArticleOrderContainer.sdp-review__article__order--active > div.sdp-review__article__order__star.js_reviewArticleSearchStarSelectBtn > div.sdp-review__article__order__star__option.js_reviewArticleStarSelectOptionContainer > ul > li:nth-child(5)')
        bad_est = driver.find_element(By.CSS_SELECTOR,
                                      '#btfTab > ul.tab-contents > li.product-review.tab-contents__content > div > div.sdp-review__average.js_reviewAverageContainer > section.sdp-review__average__total-star > div.sdp-review__average__total-star__summary.js_reviewAverageSummaryModalContainer.sdp-review__average__total-star__summary--active > div:nth-child(2) > div:nth-child(6) > div.sdp-review__average__total-star__summary__graph__percent')
        bad_est_text = bad_est.text.replace("%", "")
        bad_est_num = int(bad_est_text)
    except:
        bad_est_num = 0



    # bad_est_text = bad_est.text.split(' ')[1]
    # if "," in bad_est_text:
    #     bad_est_num = int(bad_est_text.replace(",", ""))
    # else:
    #     bad_est_num = int(bad_est_text)

    # driver.switch_to.default_content()

    return total_est_num, bad_est_num



def test():
    # today = str(datetime.datetime.today()).split(' ')[0]
    # new_main_df = pd.read_csv(f'{today}_골든박스.csv', encoding='cp949')
    #
    # new_main_df['discount_rate'] = abs((new_main_df['wow_price'] / new_main_df['cupang_price']) - 1) * 100
    # new_main_df['discount_won'] = new_main_df['cupang_price'] - new_main_df['wow_price']
    # new_main_df = new_main_df.sort_values(by=['discount_rate'], ascending=False).reset_index(drop=True)
    # new_main_df.to_csv(f'{today}_골든박스.csv', encoding='cp949')
    # path = os.path.realpath("./")
    # os.startfile(path)

    driver = set_chrome_debug(True)
    driver.get("https://www.coupang.com/")
    # asd = driver.get_log('browser')
    asd = driver.get_cookies()
    for i in range(len(asd)):
        name = asd[i]['domain']
        t = driver.delete_cookie(name)
        print(t)
    # asd = driver.get_log(type)
    print(asd)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cu_print_hi('PyCharm')
    # test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
