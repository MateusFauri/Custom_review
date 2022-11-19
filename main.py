import time
import text_classifier
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.amazon.com.br/Labirinto-Cubo-Gatomoderno-para-Gatos/product-reviews/B07YVM3SK1/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
SLEEP_TIME = 2
DRIVER_TIME = 10

def checking_next(driver):
    Xpath = "//ul[@class='a-pagination']/li"
    wait = WebDriverWait(driver,DRIVER_TIME)
    try:
        wait.until(driver.find_elements(By.XPATH, Xpath ))
    except:
        time.sleep(SLEEP_TIME)
        try:
            wait.until(driver.find_elements(By.XPATH, Xpath ))
        except:
            return False
    finally:
        next = driver.find_elements(By.XPATH, Xpath)
        if next[1].get_attribute('class').find("a-disabled") == -1:
            return True
        return False

driver = webdriver.Chrome()
driver.get(URL)

with open('comments.txt', 'w', encoding="utf-8") as f:
    f.write("Phrase\n")
    try:
        next_xpath = "//li[@class='a-last']/a[contains(text(), 'Próximo')]"
        comment_xpath = "//div[@class='a-row a-spacing-small review-data']/span"
        
        wait = WebDriverWait(driver, DRIVER_TIME)

        while True:
            time.sleep(SLEEP_TIME)
            
            try:
                list_comment =  wait.until(lambda d: d.find_elements(By.XPATH, comment_xpath))
            except StaleElementReferenceException:
                time.sleep(SLEEP_TIME)
                list_comment =  wait.until(lambda d: d.find_elements(By.XPATH, comment_xpath))

            for comment in list_comment:
                f.write(comment.text + "\n")

            if checking_next(driver):
                succeed = False
                while not succeed:
                    try:
                        wait.until(EC.presence_of_element_located((By.XPATH, next_xpath))).click()
                        succeed = True
                    except:
                        pass
            else:
                break
    finally:
        driver.quit()

DIR = "E:\Python\API\Customers_review"
file_name = "comments.txt"

text_classifier.get_file(DIR, file_name)