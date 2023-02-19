import web_bot
import private_date


def main():
    # in the another python file you can write your login and password to udemy account
    try:
        udemy_login = private_date.udemy_login
        udemy_password = private_date.udemy_password
    except:
        print("You can create file private_date.py and write there your login an password to udemy account")
        udemy_login = input("Please, write your udemy account login")
        udemy_password = input("Please, write your udemy account password")

    # in the another python file you can write your login and password to pepper account
    try:
        pepper_login = private_date.pepper_login
        pepper_password = private_date.pepper_password
    except:
        print("You can create file private_date.py and write there your login an password to pepper account")
        pepper_login = input("Please, write your pepper account login")
        pepper_password = input("Please, write your pepper account password")

    # in the another python file you can write path to your chrome profile
    try:
        path_to_chrome_profile = private_date.path_to_chrome_profile
    except:
        print("You can create file private_date.py and write there path to your chrome profile")
        path_to_chrome_profile = input("Please, write path to your chrome profile or leave blank")

    # depends on your internet connection
    sleep_time = 2
    printing = True

    # starting bot
    try:
        my_bot = web_bot.WebBot(udemy_login, udemy_password, pepper_login, pepper_password, path_to_chrome_profile,
                                sleep_time, printing)
        print("Bot lunch correctly!")
    except:
        print("Something went wrong with lunch bot")
        return -1

    # logging to pepper account
    try:
        my_bot.log_to_pepper_account()
    except Exception as error:
        print("I was unable to log your pepper account")

    # finding promotions with udemy courses
    promotion_links = my_bot.find_udemy_promotions_on_pepper()
    links = []

    # extracting links to udemy courses and adding plus to pepper promotion
    for promotion_link in promotion_links:

        links += my_bot.taking_links_to_udemy_from_pepper_promotion(promotion_link)
        try:
            my_bot.give_plus_pepper_promotion()
        except:
            print("There was an error adding the plus!")

    if not links:
        return 0

    # logging to udemy account
    try:
        if my_bot.log_to_udemy():
            return -1
    except Exception as e:
        print("I can't log to your udemy account!")
        print(e)
        return -1

    # checking every link
    saving = 0
    course_number = 0
    number_of_course = len(links)
    for link in links:
        course_number += 1
        try:
            saving += my_bot.buy_free_course(link, course_number, number_of_course)
        except:
            print("Something went wrong with this link: " + link)

    # printing stats and ending
    my_bot.printing_stats_udemy_courses()
    print("You are save: " + str(round(saving, 2)))
    my_bot.driver.quit()

if __name__ == '__main__':
    main()
