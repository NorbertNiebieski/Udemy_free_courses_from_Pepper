import os
import random
import subprocess
import sys
from math import trunc
from time import sleep

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import log


def log_to_udemy(web_bot, udemy_login, udemy_password, printing=True, sleep_time=5):
    # go to udemy main page
    web_bot.driver.get("https://www.udemy.com/")
    sleep(sleep_time)

    # check present of bot blockade and if there is try to bypass it
    _check_cloudflare_blockade_and_try_bypass(web_bot)
    _check_is_perimeterx_blockade_and_try_bypass(web_bot)

    # check if you already logged to udemy account
    if _is_logged_to_udemy_account(web_bot, sleep_time):
        if printing:
            print("You was already logged to your udemy account")
        log.root.info("You was already logged to your udemy account")
        return True

    # go to udemy login page
    web_bot.driver.find_element_by_xpath("//a[@data-purpose='header-login']").click()
    sleep(sleep_time / 2)

    # check present of bot blockade and if there is try to bypass it
    _check_is_perimeterx_blockade_and_try_bypass(web_bot)
    _check_cloudflare_blockade_and_try_bypass(web_bot)

    # try to pass udemy login, it can by remembered by page
    try:
        web_bot.driver.find_element_by_xpath("//input[@name=\"email\"]").send_keys(udemy_login)
    except Exception as error:
        log.root.debug("I can not pass udemy login to page - %s", error, exc_info=1)

    # pass udemy password
    web_bot.driver.find_element_by_xpath("//input[@name=\"password\"]") \
        .send_keys(udemy_password + Keys.ENTER)

    # check if logging was successful
    sleep(sleep_time / 2)
    if _is_logged_to_udemy_account(web_bot, sleep_time):
        if printing:
            print("I have successfully logged into your udemy account")
        log.root.info("I have successfully logged into your udemy account")
        return True
    else:
        if printing:
            print("I was unable to login to your udemy account")
        log.root.info("I was unable to login to your udemy account")
        return False


def _check_is_perimeterx_blockade_and_try_bypass(web_bot, solve_captcha=True, how_many_trials=10):
    if _is_perimeterx_blockade(web_bot):
        print("Detected PerimeterX blockade")
        log.root.info("Detected PerimeterX blockade")
        sleep(web_bot.sleep_time / 2)

        # try to solve captcha how_many_trails times
        while solve_captcha and how_many_trials >= 0:
            print("I am trying to solve captcha")
            log.root.info("I am trying to solve captcha")

            if _try_solve_perimeterx_captcha(web_bot):
                print("Successfully bypass PerimeterX blockade")
                log.root.info("Successfully bypass PerimeterX blockade")
                return False

            print("I was not able to solve PerimeterX captcha")
            log.root.info("I was not able to solve PerimeterX captcha")
            how_many_trials -= 1

        print("I was not able to bypass PerimeterX blockade")
        log.root.info("I was not able to bypass PerimeterX blockade")
        return True
    else:
        return False


def _try_solve_perimeterx_captcha(web_bot):
    # Click and hold captcha
    _try_solve_perimeterx_captcha_mouse_movement(web_bot)

    sleep(2 * web_bot.sleep_time)

    # check if successfully bypassed blockade
    if not _is_perimeterx_blockade(web_bot):
        return True

    # refresh page
    web_bot.driver.refresh()

    # check if successfully bypassed blockade
    if not _is_perimeterx_blockade(web_bot):
        return True

    return False


def _is_perimeterx_blockade(web_bot) -> bool:
    return web_bot.driver.find_elements_by_xpath("//*[contains (text(), \"PerimeterX\")]")


def _try_solve_perimeterx_captcha_mouse_movement(web_bot):
    # find captcha bar
    mouse_tracker = web_bot.driver.find_element(By.ID, "px-captcha")

    # click and hold captcha
    ActionChains(web_bot.driver) \
        .move_to_element(mouse_tracker) \
        .move_by_offset(-450 + random.randint(-25, 25), 0 + random.randint(-25, 25)) \
        .click_and_hold() \
        .perform()
    sleep(6 + random.randint(-2, 2))

    # release mouse button
    ActionChains(web_bot.driver).release().perform()


def _check_cloudflare_blockade_and_try_bypass(web_bot, ask_human_for_help=True, restart_if_blockade=True):
    if _is_cloudflare_blockade(web_bot):
        print("Detected Cloudflare blockade")
        log.root.info("Detected Cloudflare blockade")

        # try manually solve captcha
        if ask_human_for_help:
            input("Please confirm that you are human and press any key to continue ")
            if not _is_cloudflare_blockade(web_bot):
                print("Successfully bypass Cloudflare blockade")
                log.root.info("Successfully bypass Cloudflare blockade")
                return False

        # restart whole program and hope some randomization of data help
        if restart_if_blockade:
            print("Randomizing data and restarting")
            log.root.info("Randomizing data and restarting")
            web_bot.driver.quit()
            subprocess.call([sys.executable, os.path.realpath(web_bot.starting_file)] + sys.argv[1:])

        print("I was not able to bypass Cloudflare blockade")
        log.root.info("I was not able to bypass Cloudflare blockade")
        return True
    else:
        return False


def _is_cloudflare_blockade(web_bot) -> bool:
    return web_bot.driver.find_elements_by_xpath("//*[contains (text(), 'Cloudflare')]")


def _is_logged_to_udemy_account(web_bot, sleep_time) -> bool:
    # check if webdriver is on correct page
    if "udemy.com" not in web_bot.driver.current_url:

        # save current url
        current_url = web_bot.driver.current_url

        # get to udemy url
        web_bot.driver.get("https://www.udemy.com/")

        # check if link to user account(avatar) is on page
        is_logged = web_bot.driver.find_elements_by_xpath("//div/a[@data-purpose='user-dropdown']")

        # go back to first url
        web_bot.driver.get(current_url)
        sleep(sleep_time / 5)
        return is_logged
    else:
        # check if link to user account(avatar) is on page
        return web_bot.driver.find_elements_by_xpath("//div/a[@data-purpose='user-dropdown']")


def buy_free_course(web_bot, udemy_link, sleep_time=5, course_number=0, number_of_course=0):
    # setting variable depends on if count curses checked
    if course_number:
        how_many_course_left_text = " (" + str(course_number) + "/" + str(number_of_course) + ")"
    else:
        how_many_course_left_text = ""

    # check if the course is already owned form cache
    try:
        if _check_if_course_already_owned(web_bot, udemy_link):
            course_name = web_bot.cache_owned_courses.get(udemy_link)
            return _buying_owned_course(course_name, how_many_course_left_text, web_bot)

    except Exception as error:
        print("Something went wrong when trying check if course is already owned from cache")
        log.root.warning("Something went wrong when trying check if course is already owned from cache - %s",
                         error, exc_info=1)

    # go to udemy course page
    web_bot.driver.get(udemy_link)
    web_bot.number_of_link_looked += 1
    sleep(sleep_time)

    # getting course name
    try:
        course_name = web_bot.driver.find_element_by_xpath("//h1[@data-purpose=\"lead-title\"]").text
    except Exception as error:
        log.root.warning("Something was wrong when trying to obtain course name - %s", error, exc_info=1)
        course_name = "Error"

    # getting buy course button
    prize = web_bot.driver.find_element_by_xpath('//button[@data-purpose="buy-this-course-button"]')

    #  free course
    if prize.text == "Zapisz się teraz" or prize.text == "Enroll now":

        # Transition to check out
        prize.click()
        sleep(sleep_time)
        saving = 0

        # Checking if you are in checkout
        if web_bot.driver.current_url[:50] == "https://www.udemy.com/cart/checkout/express/course":

            sleep(2 * sleep_time)

            # Collection how much you're saving
            try:
                saving = web_bot.driver.find_element_by_xpath(
                    '//td[@data-purpose="list-price"]/div/span').get_attribute("innerHTML")
                saving = saving[:-3]
                saving = float(saving.replace(',', '.'))
                saving = trunc(saving * 100) / 100
            except Exception as error:
                log.root.warning("Something was wrong, when trying calculate savings for - " + course_name +
                                 ", error - %s", error, exc_info=1)

            # buying
            web_bot.driver.find_elements_by_xpath("//button[@type=\"button\"]")[2].click()
            sleep(sleep_time)

            web_bot.number_of_new_course += 1
            print("YAY! You have new free course \"" + course_name + "\'!" + how_many_course_left_text)
            log.root.info("YAY! You have new free course \"" + course_name + "\'!" + how_many_course_left_text)
            return saving

        elif web_bot.driver.current_url[:43] != "https://www.udemy.com/cart/subscribe/course":
            web_bot.number_of_checkout_problem += 1
            print("I have a problem with this course \"" + course_name + "\" checkout!" + how_many_course_left_text)
            log.root.warning("I have a problem with this course \"" + course_name + "\" checkout!" +
                             how_many_course_left_text)
            return 0

    # course not free
    elif prize.text == "Kup teraz" or prize.text == "Buy now":
        web_bot.number_of_not_free_course += 1
        print("This course \"" + course_name + "\" is not for free!" + how_many_course_left_text)
        log.root.info("This course \"" + course_name + "\" is not for free!" + how_many_course_left_text)
        return 0

    # owned course
    elif prize.text == "Przejdź do kursu" or prize.text == "Go to course":
        # cache owned courses, so you do not need check it later
        try:
            _cache_owned_courses(udemy_link, course_name, web_bot.cache_folder_path,
                                 web_bot.cache_owned_courses_file_name)
        except Exception as error:
            log.root.warning("Something went wrong when caching owned course information - %s", error, exc_info=1)
            print("Something went wrong when caching owned course information")

        return _buying_owned_course(course_name, how_many_course_left_text, web_bot)

    # unknown course
    else:
        web_bot.number_of_unrecognized_course += 1
        print("I don\'t recognize this course \"" + course_name + "\"" + how_many_course_left_text)
        log.root.warning("I don\'t recognize this course \"" + course_name + "\"" + how_many_course_left_text)
        return 0


def _buying_owned_course(course_name, how_many_course_left_text, web_bot):
    # update stats and write info
    web_bot.number_of_had_course += 1
    print("You already had course \"" + course_name + "\"!" + how_many_course_left_text)
    log.root.info("You already had course \"" + course_name + "\"!" + how_many_course_left_text)
    return 0


def _check_if_course_already_owned(web_bot, udemy_link):
    # collecting udemy link from file to set
    if not web_bot.cache_owned_courses:
        # creating relative path and opening file in reading mode
        file_path = web_bot.folder_path + web_bot.file_name
        try:
            cached_owned_courses_information = open(file_path, 'r')
        except FileNotFoundError as error:
            print("File with cached owned courses does not exist")
            log.root.warning("File with cached owned courses does not exist - %s", error, exc_info=1)
            return False

        # taking all line to list
        lines = cached_owned_courses_information.readlines()
        for line in lines:
            # extracting udemy link and adding it to dictonary - udemy_link -> course_name
            udemy_link_from_file = line.split(" ")[0]
            course_name = line.split(" ")[1]
            web_bot.cache_owned_courses[udemy_link_from_file] = course_name

        # closing file
        cached_owned_courses_information.close()

    # checking if udemy link is in owned courses
    return udemy_link in web_bot.cache_owned_courses


def _cache_owned_courses(udemy_link, course_name, folder_path, file_name):
    # prepare relative file path and create folder with file if it does not exit
    file_path = folder_path + file_name
    os.makedirs(folder_path, mode=0o777, exist_ok=True)

    # open file in append mode, create if it does not exit
    cached_owned_courses_information = open(file_path, 'a')

    # append line with - "udemy_link course_name hashed_udemy_link and close file
    cached_owned_courses_information.write(udemy_link + " " + course_name + " \n")
    cached_owned_courses_information.close()
