import os
import timeit
from time import sleep
import calendar
from selenium import webdriver


def login_window(driver, email, password):
    """ if login window exist, then log in """

    # click disclaimer, if exist
    try:
        disclaimer_accept_button = driver.find_element_by_css_selector("button[name='accept']")
        disclaimer_accept_button.click()
        sleep(1)
    except:
        pass

    email_box = driver.find_element_by_css_selector("input[class='d-e-Xg'][placeholder='Nickname or email']")
    email_box.send_keys(email)
    sleep(0.5)
    password_box = driver.find_element_by_css_selector("input[class='d-e-Xg'][type='password']")
    password_box.send_keys(password)
    sleep(0.5)
    sign_in_button = driver.find_element_by_css_selector("div[class='a-b-c d-e-v']")
    sign_in_button.click()


def save_csv(driver, timeout):
    """ try to save data to csv file, up to given timeout. return True/False if successfully/failed save """

    saved_status = False
    for _ in range(timeout):
        sleep(1)
        try:
            save_button = driver.find_element_by_xpath("//*[contains(text(), 'Save as .csv')]")
            save_button.click()
            saved_status = True
            sleep(1)
            break
        except:
            pass

    return saved_status


def set_start_date(driver, year, month, day):
    """ setup starting date to be the given year, month and day
        sample call: set_start_date(driver, 2019, 7, 27) """

    # open date box
    from_date_box = driver.find_element_by_css_selector('div[class="d-wh-vg-xh d-wh-vg-Ch-Dh-p"]')
    from_date_box.click()
    sleep(1)

    set_date(driver, year, month, day, 0)


def set_end_date(driver, year, month, day):
    """ setup starting date to be the given year, month and day
        sample call: set_end_date(driver, 2019, 7, 27) """

    # open date box
    to_date = driver.find_element_by_css_selector('div[class="d-wh-vg-xh d-wh-vg-Ch-wf-p"]')
    to_date.click()
    sleep(1)

    set_date(driver, year, month, day, 1)


def set_date(driver, year, month, day, box_i):
    """ setup date box based on given parameter.
        box_i = 0 if date box is the starting date, or 1 if date box is the end date """

    # set year
    year_box = driver.find_elements_by_css_selector('button[class="d-Ch-fi-btn d-Ch-fi-ni"]')[box_i]
    year_box.click()
    sleep(.5)
    driver.find_element_by_xpath(f"//li[contains(text(), '{year}')]").click()
    sleep(.5)

    # set month
    month_box = driver.find_elements_by_css_selector('button[class="d-Ch-fi-btn d-Ch-fi-mi"]')[box_i]
    month_box.click()
    sleep(.5)
    driver.find_element_by_xpath(f"//li[contains(text(), '{calendar.month_name[month]}')]").click()
    sleep(.5)

    # set day
    days_list = driver.find_elements_by_css_selector('td[class="d-Ch-fi-Ch"') + \
                driver.find_elements_by_css_selector('td[class="d-Ch-fi-Ch d-Ch-fi-U"')
    days_list = [e for e in days_list if e.text == str(day)]
    days_list[0].click()


def handle_date_box(driver, data_type):
    """ setup date using dukascopy GUI.
        if type="old" then setup dates to 2017-2019, if type="new" setup dates to 2017-2020. """

    if data_type == "old":
        # setup dates
        set_start_date(driver, 2018, 1, 1)
        set_end_date(driver, 2019, 1, 1)
        set_start_date(driver, 2017, 1, 2)
    if data_type == "new":
        set_start_date(driver, 2019, 1, 1)


# inputs
email = 'your@email.com'
password = 'your_password'
retrieve_num = 5
id_list = [':6q', ':6r', ':6s', ':6t', ':6u', ':6v', ':6w', ':6x', ':6y', ':6z', ':70', ':71', ':72', ':73', ':74', ':75', ':76', ':77', ':78', ':79', ':7a', ':7b', ':7c', ':7d', ':7e', ':7f', ':7g', ':7h', ':7i', ':7j', ':7k', ':7l', ':7m', ':7n', ':7o', ':7p', ':7q', ':7r', ':7s', ':7t', ':7u', ':7v', ':7w', ':7x', ':7y', ':7z', ':80', ':81', ':82', ':83', ':84', ':85', ':86', ':87', ':88', ':89', ':8a', ':8b', ':8c', ':8d', ':8e', ':8f', ':8g', ':8h', ':8i', ':8j', ':8k', ':8l', ':8m', ':8n', ':8o', ':8p', ':8q', ':8r', ':8s', ':8t', ':8u', ':8v', ':8w', ':8x', ':8y', ':8z', ':90', ':91', ':92', ':93', ':94', ':95', ':96', ':97', ':98', ':99', ':9a', ':9b', ':9c', ':9d', ':9e', ':9f', ':9g', ':9h', ':9i', ':9j', ':9k', ':9l', ':9m', ':9n', ':9o', ':9p', ':9q', ':9r', ':9s', ':9t', ':9u', ':9v', ':9w', ':9x', ':9y', ':9z', ':a0', ':a1', ':a2', ':a3', ':a4', ':a5', ':a6', ':a7', ':a8', ':a9', ':aa', ':ab', ':ac', ':ad', ':ae', ':af', ':ag', ':ah', ':ai', ':aj', ':ak', ':al', ':am', ':an', ':ao', ':ap', ':aq', ':ar', ':as', ':at', ':au', ':av', ':aw', ':ax', ':ay', ':az', ':b0', ':b1', ':b2', ':b3', ':b4', ':b5', ':b6', ':b7', ':b8', ':b9', ':ba', ':bb', ':bc', ':bd', ':be', ':bf', ':bg', ':bh', ':bi', ':bj', ':bk', ':bl', ':bm', ':bn', ':bo', ':bp', ':bq', ':br', ':bs', ':bt', ':bu', ':bv', ':bw', ':bx', ':by', ':bz', ':c0', ':c1', ':c2', ':c3', ':c4', ':c5', ':c6', ':c7', ':c8', ':c9', ':ca', ':cb', ':cc', ':cd', ':ce', ':cf', ':cg', ':ch', ':ci', ':cj', ':ck', ':cl', ':cm', ':cn', ':co', ':cp', ':cq', ':cr', ':cs', ':ct', ':cu', ':cv', ':cw', ':cx', ':cy', ':cz', ':d0', ':d1', ':d2', ':d3', ':d4', ':d5', ':d6', ':d7', ':d8', ':d9', ':da', ':db', ':dc', ':dd', ':de', ':df', ':dg', ':dh', ':di', ':dj', ':dk', ':dl', ':dm', ':dn', ':do', ':dp', ':dq', ':dr', ':ds', ':dt', ':du', ':dv', ':dw', ':dx', ':dy', ':dz', ':e0', ':e1', ':e2', ':e3', ':e4', ':e5', ':e6', ':e7', ':e8', ':e9', ':ea', ':eb', ':ec', ':ed', ':ee', ':ef', ':eg', ':eh', ':ei', ':ej', ':ek', ':el', ':em', ':en', ':eo', ':ep', ':eq', ':er', ':es', ':et', ':eu', ':ev', ':ew', ':ex', ':ey', ':ez', ':f0', ':f1', ':f2', ':f3', ':f4', ':f5', ':f6', ':f7', ':f8', ':f9', ':fa', ':fb', ':fc', ':fd', ':fe', ':ff', ':fg', ':fh', ':fi', ':fj', ':fk', ':fl', ':fm', ':fn', ':fo', ':fp', ':fq', ':fr', ':fs', ':ft', ':fu', ':fv', ':fw', ':fx', ':fy', ':fz', ':g0', ':g1', ':g2', ':g3', ':g4', ':g5', ':g6', ':g7', ':g8', ':g9', ':ga', ':gb', ':gc', ':gd', ':ge', ':gf', ':gg', ':gh', ':gi', ':gj', ':gk', ':gl', ':gm', ':gn', ':go', ':gp', ':gq', ':gr', ':gs', ':gt', ':gu', ':gv', ':gw', ':gx', ':gy', ':gz', ':h0', ':h1', ':h2', ':h3', ':h4', ':h5', ':h6', ':h7', ':h8', ':h9', ':ha', ':hb', ':hc', ':hd', ':he', ':hf', ':hg', ':hh', ':hi', ':hj', ':hk', ':hl', ':hm', ':hn', ':ho', ':hp', ':hq', ':hr', ':hs', ':ht', ':hu', ':hv', ':hw', ':hx', ':hy', ':hz', ':i0', ':i1', ':i2', ':i3', ':i4', ':i5', ':i6', ':i7', ':i8', ':i9', ':ia', ':ib', ':ic', ':id', ':ie', ':if', ':ig', ':ih', ':ii', ':ij', ':ik', ':il', ':im', ':in', ':io', ':ip', ':iq', ':ir', ':is', ':it', ':iu', ':iv', ':iw', ':ix', ':iy', ':iz', ':j0', ':j1', ':j2', ':j3', ':j4', ':j5', ':j6', ':j7', ':j8', ':j9', ':ja', ':jb', ':jc', ':jd', ':je', ':jf', ':jg', ':jh', ':ji', ':jj', ':jk', ':jl', ':jm', ':jn', ':jo', ':jp', ':jq', ':jr', ':js', ':jt', ':ju', ':jv', ':jw', ':jx', ':jy', ':jz', ':k0', ':k1', ':k2', ':k3', ':k4', ':k5', ':k6', ':k7', ':k8', ':k9', ':ka', ':kb', ':kc', ':kd', ':ke', ':kf', ':kg', ':kh', ':ki', ':kj', ':kk', ':kl', ':km', ':kn', ':ko', ':kp', ':kq', ':kr', ':ks', ':kt', ':ku', ':kv', ':kw', ':kx', ':ky', ':kz', ':l0', ':l1', ':l2', ':l3', ':l4', ':l5', ':l6', ':l7', ':l8', ':l9', ':la', ':lb', ':lc', ':ld', ':le', ':lf', ':lg', ':lh', ':li', ':lj', ':lk', ':ll', ':lm', ':ln', ':lo', ':lp', ':lq', ':lr', ':ls', ':lt', ':lu', ':lv', ':lw', ':lx', ':ly', ':lz', ':m0', ':m1', ':m2', ':m3', ':m4', ':m5', ':m6', ':m7', ':m8', ':m9', ':ma', ':mb', ':mc', ':md', ':me', ':mf', ':mg', ':mh', ':mi', ':mj', ':mk', ':ml', ':mm', ':mn', ':mo', ':mp', ':mq', ':mr', ':ms', ':mt', ':mu', ':mv', ':mw', ':mx', ':my', ':mz', ':n0', ':n1', ':n2', ':n3', ':n4', ':n5', ':n6', ':n7', ':n8', ':n9', ':na', ':nb', ':nc', ':nd', ':ne', ':nf', ':ng', ':nh', ':ni', ':nj', ':nk', ':nl', ':nm', ':nn', ':no', ':np', ':nq', ':nr', ':ns', ':nt', ':nu', ':nv', ':nw', ':nx', ':ny', ':nz', ':o0', ':o1', ':o2', ':o3', ':o4', ':o5', ':o6', ':o7', ':o8', ':o9', ':oa', ':ob', ':oc', ':od', ':oe', ':of', ':og', ':oh', ':oi', ':oj', ':ok', ':ol', ':om', ':on', ':oo', ':op', ':oq', ':or', ':os', ':ot', ':ou', ':ov']

# init
failed_list = []
dukas_url = 'https://www.dukascopy.com/swiss/english/marketwatch/historical/'
driver_path = os.path.join(os.path.dirname(__file__), 'drivers', 'opera_win_driver.exe')

# setup driver
driver = webdriver.Opera(executable_path=driver_path)
driver.maximize_window()
driver.get(dukas_url)
driver.implicitly_wait(5)

input("setup VPN manually, and then press enter")

for i, id in enumerate(id_list):
    start_time = timeit.default_timer()

    # download both old (2017-2019) and new (2019-2020) data
    for data_type in ["old", "new"]:

        # try to get data several times until giving up
        for r_num in range(1, retrieve_num+1):
            try:
                driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))

                # set tick size to 1 minute
                driver.find_element_by_id(":k").click()
                sleep(0.5)
                driver.find_element_by_id(":2").click()
                sleep(0.5)

                # click BID (:7) or ASK (:8)
                driver.find_element_by_id(":7").click()
                sleep(1)

                # click current ticker
                ticker = driver.find_element_by_id(id)
                sleep(1)
                ticker.click()
                sleep(1)

                # setup dates
                handle_date_box(driver, data_type)

                # download current instrument
                download_button = driver.find_element_by_css_selector("div[class='a-b-c d-oh-i-ph-v d-wh-vg-Tg']")
                download_button.click()
                sleep(0.5)

                # handle login window
                login_window(driver, email, password)

                # save data to csv
                save_status = save_csv(driver, 200)
                if save_status:
                    print(f"attepmt {r_num} to get data for id={id} - SUCCESS")
                    break
                else:
                    raise TimeoutError("saving took too long")

            except Exception as e:
                print(f"attepmt {r_num} to get data for id={id} - FAILED")
                if r_num == retrieve_num:
                    failed_list.append(id)
                    print(e)
            finally:
                driver.refresh()
                sleep(5)

        print(f"failed_list = {failed_list}")
        print(f"id_list = {id_list}")
        print(f"run: {i}/{len(id_list)}")
        print(f"time: {(timeit.default_timer() - start_time):.2f}")
        print("-" * 30)
