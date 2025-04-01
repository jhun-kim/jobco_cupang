import time

from main import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def cu_main(keyword):
    url = 'https://www.coupang.com'


    driver = set_chrome_debug(True)
    # driver = set_chrome(True)
    # driver = set_chrome_secret(True)

    # print(driver.window_handles)
    # driver.switch_to(driver.window_handles[0])
    # pyautogui.hotkey('ctrl', 'h')
    # ActionChains(driver).key_down(Keys.CONTROL).click('h').perform()
    #
    # driver.implicitly_wait(5)
    driver.get(url)

    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + "h")



    # keyword = "수입 부채살"
    # keyword = "한돈 오겹살"
    # keyword = "이불 압축 파우치"
    # keyword = "수입 삼겹살"
    # keyword = "싱크대 수전 헤드"
    # keyword = "닭다리살"
    # keyword = "아이폰8 사생활 보호 필름"
    # keyword = "한돈 삼겹살"

    keyword_input = driver.find_element(By.CSS_SELECTOR, '#headerSearchKeyword')
    keyword_input.send_keys(keyword)
    search_click = driver.find_element(By.CSS_SELECTOR, '#headerSearchBtn')
    search_click.click()
    time.sleep(1)

    #로켓배송 콤보박스 클릭
    time.sleep(1)
    com_click = driver.find_element(By.CSS_SELECTOR, '#searchServiceFilter > ul > li:nth-child(1) > label')
    com_click.click()

    time.sleep(1)
    product_list = driver.find_element(By.CSS_SELECTOR, '#productList')
    product_list = product_list.find_elements(By.TAG_NAME, "li")
    print(len(product_list))
    main_list = []
    for i in range(len(product_list)):
        # print(f"{i}  {product_list[i].text}")
        # print(" ")

        product = str(product_list[i].text).split("\n")
        if len(product) < 2:
            continue
        elif "한정 시간" in product or "무료배송" in product or "한정 시간 특가 상품" in product:
            if "0" in product[1]:
                name = product[0]
            else:
                name = product[1]
        else:
            name = product[0]

        link = product_list[i].find_element(By.TAG_NAME, "a")
        url = link.get_attribute("href")

        pd_dict = {}
        pd_dict['name'] = name
        pd_dict['url'] = url
        main_list.append(pd_dict)

    new_main_list = []
    main_df = pd.DataFrame(main_list).reset_index(drop=True)
    print(f'총 상품갯수 {len(main_df)}')

    for j in tqdm(range(len(main_df))):
        name = main_df['name'][j]
        url = main_df['url'][j]
        driver.get(url)
        time.sleep(0.1)

        # 쿠팡할인가
        cupang_price = cupang_price_func(driver)


        # 와우할인가
        wow_price, wow_price_gram, wow_price_gram_won = wow_price_func(driver)
        if "0원" in wow_price:
            try:
                wow_price, wow_price_gram, wow_price_gram_won = wow_fresh(driver)
            except:
                continue



        # 평점 확인
        total_est_num, bad_est_rate = est_check(driver)
        bad_est_num = bad_est_rate / 100
        bad_est_num = total_est_num * bad_est_num

        print(f'제품이름: {name}')
        pd_dict = {}
        pd_dict['name'] = name
        pd_dict['url'] = url
        try:
            # 문자열 전처리
            test = cupang_price
            cleaned_price = cupang_price[0].split("원")[0].replace(",", "").strip()

            # 빈 문자열 여부 확인 후 처리
            if cleaned_price:
                pd_dict['cupang_price'] = int(cleaned_price)
                print('빈 문자열 여부 확인 후 처리 ' , int(cleaned_price))
            else:
                pd_dict['cupang_price'] = 0  # 혹은 기본값 설정
                print('혹은 기본값 ', cupang_price[0])
        except (IndexError, ValueError) as e:
            pd_dict['cupang_price'] = 0  # 기본값 처리
            print(f"가격 정보 처리 중 에러 발생: {e}")
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
    new_main_df.to_csv(f'{today}_{keyword}.csv', encoding='cp949')
    path = os.path.realpath("./")
    os.startfile(path)

def wow_fresh(driver):
    #contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.dawn-only-product.without-subscribe-buy-type.DISPLAY_0.only-one-delivery > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.major-price-coupon
    #contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.dawn-only-product.without-subscribe-buy-type.DISPLAY_0.only-one-delivery > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.major-price-coupon
    # contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.major-price-coupon
    try:
        wow_price = driver.find_element(By.CSS_SELECTOR,
                                        '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0.has-loyalty-exclusive-price > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.major-price-coupon')
        wow_price = wow_price.text.split("\n")
        if len(wow_price) > 1:
            wow_price_gram = wow_price[1]
            wow_price_gram_won = int(wow_price_gram.split(' ')[1].split("원")[0].replace(",", ""))
        else:
            wow_price_gram = 0
            wow_price_gram_won = 0
        return wow_price, wow_price_gram, wow_price_gram_won

    except:
        try:
            wow_price = driver.find_element(By.CSS_SELECTOR,
                                            '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.dawn-only-product.without-subscribe-buy-type.DISPLAY_0.only-one-delivery > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.major-price-coupon')
            wow_price = wow_price.text.split("\n")
        except:
            try:
                wow_price = driver.find_element(By.CSS_SELECTOR,
                                                '#contents > div.prod-atf > div.prod-atf-main > div.prod-buy.new-oos-style.not-loyalty-member.eligible-address.without-subscribe-buy-type.DISPLAY_0 > div.prod-price-container > div.prod-price > div > div.prod-coupon-price.price-align.major-price-coupon')
                wow_price = wow_price.text.split("\n")
            except:
                wow_price = ["0원"]
                wow_price_gram = 0
                wow_price_gram_won = 0
                return wow_price, wow_price_gram, wow_price_gram_won, wow_price_gram, wow_price_gram_won


        if len(wow_price) > 1:
            wow_price_gram = wow_price[1]
            try:
                wow_price_gram_won = int(wow_price_gram.split(' ')[1].split("원")[0].replace(",", ""))
            except:
                wow_price_gram = 0
                wow_price_gram_won = 0
        else:
            wow_price_gram = 0
            wow_price_gram_won = 0
        return wow_price, wow_price_gram, wow_price_gram_won
# cu_main("")
