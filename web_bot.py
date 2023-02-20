import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import random
import chromedriver_autoinstaller

import pepper_handling
import udemy_handling
import user_agents
import log


class WebBot:
    def __init__(self, udemy_login="", udemy_password="", pepper_login="", pepper_password="",
                 path_to_chrome_profile="", sleep_time=5, printing=True, starting_file="main.py"):

        # Check if the current version of chromedriver exists and if it doesn't exist, download it automatically,
        # then add chromedriver to path
        chromedriver_autoinstaller.install()

        self.udemy_login = udemy_login
        self.udemy_password = udemy_password

        self.pepper_login = pepper_login
        self.pepper_password = pepper_password

        # set depends on speed of your internet connection
        self.sleep_time = sleep_time + random.randint(-1, 3)

        # True if you want detailed info in console
        self.printing = printing

        self.starting_file = starting_file

        # stats
        self.number_of_link_looked = 0
        self.number_of_new_course = 0
        self.number_of_had_course = 0
        self.number_of_not_free_course = 0
        self.number_of_unrecognized_course = 0
        self.number_of_checkout_problem = 0

        # flags for logged accounts
        self.is_logged_to_pepper = False
        self.is_logged_to_udemy = False

        # web browser settings
        options = Options()

        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--enable-javascript")

        # number_of_user_agents = len(user_agents.user_agents)
        # options.add_argument("user-agent=" + user_agents.user_agents[random.randint(0, number_of_user_agents - 1)])
        options.add_argument("user-agent=" + "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                             "like Gecko) Chrome/110.0.0.0 Safari/537.36'")

        # Path to your chrome profile
        if path_to_chrome_profile != "":
            options.add_argument("user-data-dir=" + path_to_chrome_profile)

        # options.add_argument("headless")
        # options.add_argument("--incognito")
        options.add_argument("use_subprocess=True")

        # Pass the argument 1 to allow and 2 to block
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })

        # web browser experimental options
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        self.driver = uc.Chrome(options=options)
        # self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def printing_stats_udemy_courses(self):

        print("I looked at " + str(self.number_of_link_looked) + " course and I find:")
        if self.number_of_new_course > 0:
            print(" - " + str(self.number_of_new_course) + " new course, which i added to your account")
        if self.number_of_not_free_course > 0:
            print(" - " + str(self.number_of_not_free_course) + " paid course")
        if self.number_of_had_course > 0:
            print(" - " + str(self.number_of_had_course) + " course, which you had already")
        if self.number_of_unrecognized_course > 0:
            print(" - " + str(self.number_of_unrecognized_course) + " course i dont recognize")
        if self.number_of_checkout_problem > 0:
            print(" - " + str(self.number_of_checkout_problem) + " course i had a problem with checkout")

    def log_to_pepper_account(self):

        if self.is_logged_to_pepper:
            return True

        self.is_logged_to_pepper = pepper_handling.log_to_pepper_account(self, self.pepper_login, self.pepper_password,
                                                                         self.sleep_time)
        return self.is_logged_to_pepper

    def give_plus_pepper_promotion(self, pepper_promotion_url=""):
        if self.is_logged_to_pepper:
            return pepper_handling.give_plus_pepper_promotion(self, pepper_promotion_url, self.sleep_time)
        else:
            return False

    def find_udemy_promotions_on_pepper(self):
        return pepper_handling.find_udemy_promotions_on_pepper(self)

    def taking_links_to_udemy_from_pepper_promotion(self, promotion_link):
        return pepper_handling.taking_links_to_udemy_from_pepper_promotion(self, promotion_link)

    def log_to_udemy(self):

        if self.is_logged_to_udemy:
            return True
        else:
            self.is_logged_to_udemy = udemy_handling.log_to_udemy(self, self.udemy_login, self.udemy_password,
                                                                  self.printing, self.sleep_time)
            return self.is_logged_to_udemy

    def buy_free_course(self, link, course_number=0, number_of_course=0):
        if self.is_logged_to_udemy:
            return udemy_handling.buy_free_course(self, link, self.sleep_time, course_number, number_of_course)
        else:
            print("You are not logged to udemy account, when trying to handle this link - " + link)
            log.root.warning("You are not logged to udemy account, when trying to handle this link - " + link)
            return 0
