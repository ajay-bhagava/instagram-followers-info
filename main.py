import numpy as np
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC


username = "ajay_bhagava"
password = "Pumpkinpatch1!"

def waitOnElement(waiter, id, name):
    return waiter.until(EC.element_to_be_clickable((id, name)))
    


def main():
    #initialize drivers and load instagram
    driver = webdriver.Firefox()
    waiter = WebDriverWait(driver, 20)
    actions = AC(driver)
    driver.get("https://www.instagram.com/")
    

    #login
    waitOnElement(waiter, "name", "username").send_keys(username)
    waitOnElement(waiter, "name", "password").send_keys(password)
    actions.move_to_element(waitOnElement(waiter, "css selector", "._acap")).click().perform()


    #navigate to profile
    pfp_xpath = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]"
    profile_xpath = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div/div[2]/div[1]"
    actions.move_to_element(waitOnElement(waiter, "xpath", pfp_xpath)).click().perform()
    actions.move_to_element(waitOnElement(waiter, "xpath", profile_xpath)).click().perform()


    #pull up followers
    followers_xpath = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div"
    actions.move_to_element(waitOnElement(waiter, "xpath", followers_xpath)).click().perform()
    

    # get followers page html
    followers_window = "$x(\"//*[@id=\"mount_0_0_xM\"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]\")[0]"
    last_height = driver.execute_script(f"return {followers_window}.scrollHeight;")

    while True:
        # Scroll down to bottom
        driver.execute_script(script=f"{following_window}.scrollTo(0, {followers_window}.scrollHeight);")

        # Wait to load page
        sleep(1)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script(f"return {followers_window}.scrollHeight;")
        if new_height == last_height:
            break
        last_height = new_height
    
    followers_soup = BeautifulSoup(driver.page_source)


    # back out of followers page
    exit_button_xpath = "//*[@id=\"mount_0_0_Ug\"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div[3]/div/button"
    actions.move_to_element(waitOnElement(waiter, "xpath", exit_button_xpath)).click().perform()


    # pull up following
    following_xpath = "//*[@id=\"mount_0_0_Ug\"]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[3]/a"
    actions.move_to_element(waitOnElement(waiter, "xpath", following_xpath)).click().perform()


    # get following html
    following_window = "$x(//*[@id=\"mount_0_0_Ug\"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3])[0]"
    last_height = driver.execute_script(f"return {following_window}.scrollHeight;")

    while True:
        # Scroll down to bottom
        driver.execute_script(f"{following_window}.scrollTo(0, {following_window}.scrollHeight);")

        # Wait to load page
        sleep(1)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script(f"return {following_window}.scrollHeight;")
        if new_height == last_height:
            break
        last_height = new_height

    following_soup = BeautifulSoup(driver.page_source)


    # get the lists of followers and following
    followers = []
    following = []

    for follower_element in followers_soup.find_all("div", class_=" _ab8y  _ab94 _ab97 _ab9f _ab9k _ab9p _abcm"):
        followers.append(follower_element.get_text())

    for following_element in following_soup.find_all("div", class_=" _ab8y  _ab94 _ab97 _ab9f _ab9k _ab9p _abcm"):
        following.append(following_element.get_text())

    
main()
