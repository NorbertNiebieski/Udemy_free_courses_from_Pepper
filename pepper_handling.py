from time import sleep


def log_to_pepper_account(web_bot, pepper_login, pepper_password, sleep_time=5):

    # check if you not log already
    if _is_logged_to_pepper_account(web_bot, sleep_time):
        return True

    # click log in button
    web_bot.driver.find_element_by_xpath("//button[@rel=\"nofollow\"]").click()
    sleep(sleep_time)

    # fill necessary data and click another log in button
    web_bot.driver.find_element_by_xpath("//input[@name=\"identity\"]").send_keys(pepper_login)
    web_bot.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(pepper_password)
    web_bot.driver.find_element_by_xpath("//button[@name=\"form_submit\"]").click()

    # check if you are successfully log to pepper account and print correct message
    if _is_logged_to_pepper_account(web_bot, sleep_time):
        print("I successfully log you into your pepper account")
        return True
    else:
        print("Error! I was unable log to your pepper account")
        return False


def _is_logged_to_pepper_account(web_bot, sleep_time):

    # go to pepper login page
    web_bot.driver.get("https://www.pepper.pl")
    sleep(sleep_time / 5)

    # check if you not log already
    if web_bot.driver.find_elements_by_xpath("//button/img[@alt=\"Avatar\"]"):
        return True
    else:
        return False


def give_plus_pepper_promotion(web_bot, pepper_promotion_url, sleep_time=5):

    # check if you already are in correct page
    if pepper_promotion_url == "":
        pepper_promotion_url = web_bot.driver.current_url

    # check if you already gave plus this pepper promotion
    if _is_plus_already_given(web_bot, pepper_promotion_url, sleep_time):
        print("You already gave plus this pepper promotion")
        return True

    # give plus pepper promotion
    web_bot.driver.find_element_by_xpath("//button[@class=\"cept-up-vote space--h-2\"]").click()

    # check if plus was given correctly
    if _is_plus_already_given(web_bot, pepper_promotion_url, sleep_time):
        print("You successfully gave plus this pepper promotion")
        return True
    else:
        print("Error! I was unable to gave plus pepper promotion")
        return False


def _is_plus_already_given(web_bot, pepper_promotion_url, sleep_time):

    # go to the pepper promotion url
    web_bot.driver.get(pepper_promotion_url)
    sleep(sleep_time/5)

    # check if you already gave plus this pepper promotion
    if web_bot.driver.find_elements_by_xpath(
            "//span[@class=\"bubbleWrap bubbleWrap--s text--color-white bg--color-grey\"]"):
        return True


def find_udemy_promotions_on_pepper(web_bot, how_old_in_days=30):

    # go to the pepper page with udemy coupons and promotions
    web_bot.driver.get("https://www.pepper.pl/kupony/udemy.com")
    
    times_since_post = web_bot.driver.find_elements_by_xpath("//span[@class=\"hide--toW3\"]")
    # while(web_bot.driver.find_elements_by_xpath("//span[@class=\"hide--toW3\"]")[9 + counter].text):

    # div with whole promotion with image, link...
    promotions = web_bot.driver.find_elements_by_xpath("//div[contains(@class, \"threadGrid thread-clickRoot\")]")
    counter = 0
    promotions_links = []
    print("I find this active promotions:")
    
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


def taking_links_to_udemy_from_pepper_promotion(web_bot, pepper_promotion_url, printing=True):

    # go to the pepper promotion page
    web_bot.driver.get(pepper_promotion_url)

    # get all link elements containing udemy page
    sub_links = web_bot.driver.find_elements_by_xpath("//a[contains(@title, 'www.udemy.com')]")

    # get url link form link elements
    udemy_links = [udemy_link.get_attribute("title") for udemy_link in sub_links if
                   udemy_link.get_attribute("title") != '']

    if printing:
        print("I find " + str(udemy_links.__len__()) + " links")
    return udemy_links
