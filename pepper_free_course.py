from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


class PepperBot:
    def __init__(self, sleep_time=5):

        self.udemy_login = ""
        self.udemy_password = ""
        self.pepper_promotion_url = ""

        # set depends of speed of your internet connection
        self.sleep_time = sleep_time

        # stats
        self.number_of_link_looked = 0
        self.number_of_new_course = 0
        self.number_of_had_course = 0
        self.number_of_not_free_course = 0
        self.number_of_unrecognized_course = 0
        self.number_of_checkout_problem = 0

        # web browser settings
        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })

        self.driver = webdriver.Chrome(options=option)

    def printing_stats_udemy_courses(self):

        print("I looked at " + str(self.number_of_link_looked) + " course and I find:")
        if self.number_of_new_course > 0:
            print(" - " + str(self.number_of_new_course) + " new course, wchich i added to your account")
        if self.number_of_not_free_course > 0:
            print(" - " + str(self.number_of_not_free_course) + " paid course")
        if self.number_of_had_course > 0:
            print(" - " + str(self.number_of_had_course) + " course, wchich you had allready")
        if self.number_of_unrecognized_course > 0:
            print(" - " + str(self.number_of_unrecognized_course) + " course i dont recognize")
        if self.number_of_checkout_problem > 0:
            print(" - " + str(self.number_of_checkout_problem) + " course i had a problem with checkout")

    def talking_links_to_udemy_from_pepper_promotion(self, pepper_promotion_url, printing=True):

        self.driver.get(pepper_promotion_url)
        sub_links = self.driver.find_elements_by_xpath("//a[contains(@title, 'www.udemy.com')]")
        udemy_links = [udemy_link.get_attribute("title") for udemy_link in sub_links if udemy_link.get_attribute("title") != '']
        if printing:
            print("I find " + str(udemy_links.__len__()) + " links")
        return udemy_links

    def buy_free_course(self, udemy_link, sleep_time=5):

        if sleep_time == 5:
            sleep_time = self.sleep_time
        self.driver.get(udemy_link)
        self.number_of_link_looked += 1
        sleep(sleep_time)
        course_name = self.driver.find_element_by_xpath("//h1[@data-purpose=\"lead-title\"]").text
        prize = self.driver.find_element_by_xpath('//button[@data-purpose="buy-this-course-button"]')
        if prize.text == "Kup teraz" or prize.text == "Buy now":
            self.number_of_not_free_course += 1
            print("This course \"" + course_name + "\" is not for free")
        elif prize.text == "Zapisz się teraz" or prize.text == "Enroll now":
            prize.click()
            sleep(sleep_time)
            if self.driver.current_url[:50] == "https://www.udemy.com/cart/checkout/express/course":
                sleep(2*sleep_time)
                self.driver.find_element_by_xpath("//*[@id=\"udemy\"]/div[1]/div[2]/div/div/div/div[2]/form/div[2]/div/div[4]/button")\
                    .click()
            elif self.driver.current_url[:43] != "https://www.udemy.com/cart/subscribe/course":
                self.number_of_checkout_problem += 1
                print("I have a problem with this course \"" + course_name + "\" chechout")
                return None
            print("YAY! You have new free course \"" + course_name + "\'!")
            sleep(sleep_time)
            self.number_of_new_course += 1
        elif prize.text == "Przejdź do kursu" or prize.text == "Go to course":
            self.number_of_had_course += 1
            print("You already had course \"" + course_name + "\"")
        else:
            self.number_of_unrecognized_course += 1
            print("I don\'t recognize this course \"" + course_name + "\"")

    def log_to_udemy(self, udemy_login, udemy_password, printing=True):

        self.udemy_login = udemy_login
        self.udemy_password = udemy_password

        # go to udemy login page
        self.driver.get("https://www.udemy.com/join/login-popup/?locale=pl_PL&response_type=html&next=https%3A%2F%2Fwww.udemy.com%2F")
        sleep(1)
        self.driver.find_element_by_xpath("//input[@name=\"email\"]") \
            .send_keys(udemy_login)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]") \
            .send_keys(udemy_password)
        self.driver.find_element_by_xpath("//input[@name=\"submit\"]") \
            .click()
        sleep(1)
        if self.driver.current_url == "https://www.udemy.com/":
            if printing:
                print("I have successfully logged into your udemy account")
            return True
        else:
            if printing:
                print("Error! I was unable to login to your udemy account")
            return False


