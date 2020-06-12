from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pprint import pprint
from time import sleep

list_exception = [" ", "NA", "None"]

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-gpu")
driver = webdriver.Chrome('/root/chromedriver', chrome_options=options)

with open('/root/info/ip.txt', 'r') as f:
    Lines = len(f.readlines())
    n = 0
    f.seek(0, 0)
    while True:
        with open('/root/info/ipresult.txt', 'ab+') as fr:
            line = f.readline().rstrip()
            if not line:
                break
            n = n + 1

            driver.get('https://xn--c79as89aj0e29b77z.xn--3e0b707e/kor/whois/whois.jsp')
            driver.find_element_by_xpath('//*[@id="sWord"]').send_keys(line)
            driver.find_element_by_xpath('//*[@id="whois_form"]/table/thead/tr/td[2]/a').click()

            driver.switch_to.frame('frm')
            html = driver.page_source

            list_ = [html]
            for i in range(len(list_)):
                dict_ = {}
                for s in list_[i].split('\n'):
                    x = s.strip()
                    if x == "" or x[0] == '#':
                        continue
                    if x.find(':') == -1:
                        continue
                    key = x[:x.find(':')]
                    key = key.strip()
                    if x.find(':') == len(x) - 1:
                        continue
                    value = x[x.find(':') + 1:]
                    value = value.strip()
                    dict_[key] = value
                    list_[i] = dict_

            try:
                result = str(dict_.get("Organization Name"))
                if result in list_exception:
                    raise ValueError
                else:
                    result = str(dict_.get("Organization Name"))
            except:
                try:
                    result = str(dict_.get("Organization"))
                    if result in list_exception:
                        raise ValueError
                    else:
                        result = str(dict_.get("Organization"))
                except:
                    try:
                        result = str(dict_.get("OrgName"))
                        if result in list_exception:
                            raise ValueError
                        else:
                            result = str(dict_.get("OrgName"))
                    except:
                        try:
                            result = str(dict_.get("descr"))
                            if result in list_exception:
                                raise ValueError
                            else:
                                result = str(dict_.get("descr"))
                        except:
                            try:
                                result = str(dict_.get('owner'))
                                if result in list_exception:
                                    raise ValueError
                                else:
                                    result = str(dict_.get('owner'))
                            except:
                                result = "UnKnow"

            try:
                Nationality = str(dict_.get("country"))
                if Nationality in list_exception:
                    raise ValueError
                else:
                    Nationality = str(dict_.get("country"))
            except:
                try:
                    Nationality = str(dict_.get("Country"))
                    if Nationality in list_exception:
                        raise ValueError
                    else:
                        Nationality = str(dict_.get("Country"))
                except:
                    try:
                        Nationality = str(dict_.get("Address"))
                        if Nationality in list_exception:
                            raise ValueError
                        else:
                            Nationality = str(dict_.get("Address"))
                    except:
                        Nationality = "UnKnow"

            Filter = line.rstrip() + "\t" + Nationality + "\t" + result + "\n"
            fr.write(Filter.encode())
            print(str(n) + " Completed In " + str(Lines) + '\n')

driver.close()