from math import trunc
from time import sleep

from selenium.webdriver.common.keys import Keys


def log_to_udemy(web_bot, udemy_login, udemy_password, printing=True, sleep_time=5):
    # go to udemy main page
    web_bot.driver.get("https://www.udemy.com/")
    sleep(sleep_time / 5)
    # go to udemy login page
    web_bot.driver.get(
        "https://www.udemy.com/join/login-popup/?locale=pl_PL&response_type=html&next=https%3A%2F%2Fwww.udemy.com%2F")

    sleep(sleep_time)

    # check if you already logged to udemy account
    if _is_logged_to_udemy_account(web_bot):
        if printing:
            print("I have successfully logged into your udemy account")
        return True

    sleep(sleep_time / 5)
    try:
        web_bot.driver.find_element_by_xpath("//input[@name=\"email\"]").send_keys(udemy_login)
    except:
        pass

    web_bot.driver.find_element_by_xpath("//input[@name=\"password\"]") \
        .send_keys(udemy_password + Keys.ENTER)

    sleep(sleep_time / 5)
    if _is_logged_to_udemy_account(web_bot):
        if printing:
            print("I have successfully logged into your udemy account")
        return True
    else:
        if printing:
            print("Error! I was unable to login to your udemy account")
        return False


def _is_logged_to_udemy_account(web_bot):
    if web_bot.driver.current_url == "https://www.udemy.com/":
        return True


def buy_free_course(web_bot, udemy_link, sleep_time=5, course_number=0, number_of_course=0):
    if course_number:
        how_many_course_left_text = " (" + str(course_number) + "/" + str(number_of_course) + ")"
    else:
        how_many_course_left_text = ""

    # go to udemy course page
    web_bot.driver.get(udemy_link)
    web_bot.number_of_link_looked += 1
    sleep(sleep_time)

    try:
        course_name = web_bot.driver.find_element_by_xpath("//h1[@data-purpose=\"lead-title\"]").text
    except:
        course_name = "Error"

    prize = web_bot.driver.find_element_by_xpath('//button[@data-purpose="buy-this-course-button"]')
    if prize.text == "Kup teraz" or prize.text == "Buy now":

        web_bot.number_of_not_free_course += 1
        print("This course \"" + course_name + "\" is not for free!" + how_many_course_left_text)
        return 0

    elif prize.text == "Zapisz się teraz" or prize.text == "Enroll now":

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
            except:
                pass

            # buying
            web_bot.driver.find_elements_by_xpath("//button[@type=\"button\"]")[2].click()
            web_bot.number_of_new_course += 1
            print("YAY! You have new free course \"" + course_name + "\'!" + how_many_course_left_text)
            sleep(sleep_time/2)
            return saving

        elif web_bot.driver.current_url[:43] != "https://www.udemy.com/cart/subscribe/course":
            web_bot.number_of_checkout_problem += 1
            print("I have a problem with this course \"" + course_name + "\" chechout!" + how_many_course_left_text)
            return 0

    elif prize.text == "Przejdź do kursu" or prize.text == "Go to course":
        web_bot.number_of_had_course += 1
        print("You already had course \"" + course_name + "\"!" + how_many_course_left_text)
        return 0

    else:
        web_bot.number_of_unrecognized_course += 1
        print("I don\'t recognize this course \"" + course_name + "\"" + how_many_course_left_text)
        return 0
