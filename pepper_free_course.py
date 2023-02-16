from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from math import trunc


class PepperBot:
    def __init__(self, sleep_time=5):

        self.udemy_login = ""
        self.udemy_password = ""
        self.pepper_promotion_url = ""

        self.pepper_login = ""
        self.pepper_password = ""

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
        #option.add_argument("--disable-extensions")
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument("--window-size=1920,1080")
        option.add_argument("--enable-javascript")
        option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

        # Path to your chrome profile
        option.add_argument("user-data-dir=C:\\Users\\Norbert\\AppData\\Local\\Google\\Chrome\\User Data\\Default")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })

        self.driver = uc.Chrome(options=option)

    def log_to_pepper_account(self, pepper_login, pepper_password, sleep_time=5):

        self.pepper_login = pepper_login
        self.pepper_password = pepper_password

        # go to pepper login page
        self.driver.get("https://www.pepper.pl")
        sleep(1)

        # uncomment below code if you want check i am not a robot box
        # input("Press Enter to continue...")

        # check if you not log already
        if self.driver.find_elements_by_xpath("//button/img[@alt=\"Avatar\"]"):
            print("You was already log to your pepper account")
            return True

        # click log in button
        self.driver.find_element_by_xpath("//button[@rel=\"nofollow\"]").click()
        sleep(sleep_time)

        # fill necessary data and click another log in button
        self.driver.find_element_by_xpath("//input[@name=\"identity\"]").send_keys(pepper_login)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(pepper_password)
        self.driver.find_element_by_xpath("//button[@name=\"form_submit\"]").click()

        # check if you are successfully log to pepper account and print correct message
        sleep(sleep_time)
        if self.driver.find_elements_by_xpath("//button/img[@alt=\"Avatar\"]"):
            print("I successfully log you into your pepper account")
            return True
        else:
            print("Error! I was unable log to your pepper account")
            return False

    def find_udemy_promotions_on_pepper(self, how_old_in_days=30):

        self.driver.get("https://www.pepper.pl/kupony/udemy.com")

        # div with whole promotion with image, link...
        promotions = self.driver.find_elements_by_xpath("//div[contains(@class, \"threadGrid thread-clickRoot\")]")
        times_since_post = self.driver.find_elements_by_xpath("//span[@class=\"hide--toW3\"]")
        counter = 0
        promotions_links = []
        print("I find this active promotions:")

        # while(self.driver.find_elements_by_xpath("//span[@class=\"hide--toW3\"]")[9 + counter].text):

        for promotion in promotions:

            try:
                # check if promotion is active
                if promotion.find_elements_by_xpath(
                        ".//a[@class=\"cept-thread-image-link imgFrame imgFrame--noBorder thread-listImgCell img--mute\"]"):
                    break
                # find link with promotion title
                links = promotion.find_element_by_xpath(".//strong[@class=\"thread-title \"]/a")
                promotions_links.append(links.get_attribute("href"))
                promotion_title = links.text

                counter += 1
                print(str(counter) + ". " + promotion_title)
            except:
                print("I have problem with this " + promotion + " promotion!")

        return promotions_links

    def give_plus_pepper_promotion(self, pepper_promotion_url="", sleep_time=5):

        # check if you have to go to the pepper promotion url and go if yuo have to
        if pepper_promotion_url != "":
            self.driver.get(pepper_promotion_url)

        # check if you already gave plus this pepper promotion
        if self.driver.find_elements_by_xpath("//span[@class=\"bubbleWrap bubbleWrap--s text--color-white bg--color-grey\"]"):
            print("You already gave plus this pepper promotion")
            return True

        # give plus pepper promotion
        self.driver.find_element_by_xpath("//button[@class=\"cept-up-vote space--h-2\"]").click()

        # check if plus was gave correctly
        sleep(1)
        if self.driver.find_elements_by_xpath("//span[@class=\"bubbleWrap bubbleWrap--s text--color-white bg--color-grey\"]"):
            print("You successfully gave plus this pepper promotion")
            return True
        else:
            print("Error! I was unable to gave plus pepper promotion")
            return False

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

    def taking_links_to_udemy_from_pepper_promotion(self, pepper_promotion_url, printing=True):

        self.driver.get(pepper_promotion_url)
        sub_links = self.driver.find_elements_by_xpath("//a[contains(@title, 'www.udemy.com')]")
        udemy_links = [udemy_link.get_attribute("title") for udemy_link in sub_links if udemy_link.get_attribute("title") != '']
        if printing:
            print("I find " + str(udemy_links.__len__()) + " links")
        return udemy_links

    def buy_free_course(self, udemy_link, sleep_time=5, course_number=0, number_of_course=0):

        if sleep_time == 5:
            sleep_time = self.sleep_time
        self.driver.get(udemy_link)
        self.number_of_link_looked += 1
        sleep(sleep_time)
        course_name = self.driver.find_element_by_xpath("//h1[@data-purpose=\"lead-title\"]").text
        prize = self.driver.find_element_by_xpath('//button[@data-purpose="buy-this-course-button"]')
        if prize.text == "Kup teraz" or prize.text == "Buy now":
            self.number_of_not_free_course += 1
            if course_number:
                print("This course \"" + course_name + "\" is not for free! (" + str(course_number) + "/" + str(number_of_course)+ ")")
            else:
                print("This course \"" + course_name + "\" is not for free!")
            return 0
        elif prize.text == "Zapisz się teraz" or prize.text == "Enroll now":
            saving = 0
            # Transition to checkout
            prize.click()
            sleep(sleep_time)
            # Checking if you are in checkout
            if self.driver.current_url[:50] == "https://www.udemy.com/cart/checkout/express/course":
                sleep(2*sleep_time)
                # Collection how much you're saving
                try:
                    saving = self.driver.find_element_by_xpath('//td[@data-purpose="list-price"]/div/span').get_attribute("innerHTML")
                    saving = saving[:-3]
                    saving = float(saving.replace(',', '.'))
                    saving = trunc(saving*100)/100
                except:
                    pass
                # buying
                button = self.driver.find_elements_by_xpath("//button[@type=\"button\"]")[2]\
                    .click()
            elif self.driver.current_url[:43] != "https://www.udemy.com/cart/subscribe/course":
                self.number_of_checkout_problem += 1
                if course_number:
                    print("I have a problem with this course \"" + course_name + "\" chechout! (" + str(course_number) + "/" + str(
                        number_of_course) + ")")
                else:
                    print("I have a problem with this course \"" + course_name + "\" chechout!")
                return 0
            print("YAY! You have new free course \"" + course_name + "\'!")
            sleep(sleep_time)
            self.number_of_new_course += 1
            return saving
        elif prize.text == "Przejdź do kursu" or prize.text == "Go to course":
            self.number_of_had_course += 1
            if course_number:
                print("You already had course \"" + course_name + "\"! (" + str(course_number) + "/" + str(number_of_course) + ")")
            else:
                print("You already had course \"" + course_name + "\"!")
            return 0
        else:
            self.number_of_unrecognized_course += 1
            print("I don\'t recognize this course \"" + course_name + "\"")
            if course_number:
                print("I don\'t recognize this course \"" + course_name + "\"! (" + str(course_number) + "/" + str(number_of_course) + ")")
            else:
                print("I don\'t recognize this course \"" + course_name + "\"!")
            return 0

    def log_to_udemy(self, udemy_login, udemy_password, printing=True, sleep_time=5):

        self.udemy_login = udemy_login
        self.udemy_password = udemy_password

        self.driver.get("https://www.udemy.com/")
        sleep(1)
        # go to udemy login page
        self.driver.get("https://www.udemy.com/join/login-popup/?locale=pl_PL&response_type=html&next=https%3A%2F%2Fwww.udemy.com%2F")

        # uncomment below code if you want check i am not a robot box
        # input("Press Enter to continue...")

        sleep(sleep_time)

        if self.driver.current_url == "https://www.udemy.com/":
            if printing:
                print("I have successfully logged into your udemy account")
            return True

        sleep(1)
        try:
            self.driver.find_element_by_xpath("//input[@name=\"email\"]") \
                .send_keys(udemy_login)
        except:
            pass

        self.driver.find_element_by_xpath("//input[@name=\"password\"]") \
            .send_keys(udemy_password + Keys.ENTER)


        sleep(1)
        if self.driver.current_url == "https://www.udemy.com/":
            if printing:
                print("I have successfully logged into your udemy account")
            return True
        else:
            if printing:
                print("Error! I was unable to login to your udemy account")
            return False


