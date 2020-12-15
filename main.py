import pepper_free_course
import private_date

if __name__ == '__main__':

    # in the another python file you could do your on file with this string or write your login and password below
    udemy_login = private_date.udemy_login
    udemy_password = private_date.udemy_password

    # Write pepper promotion url below
    # url = ""

    url = input("Pepper's promotion url: ")

    # depends of your internet connection
    sleep_time = 5

    my_bot = pepper_free_course.PepperBot()

    # taking links from pepper
    links = my_bot.taking_links_to_udemy_from_pepper_promotion(url)

    # logging to udemy
    my_bot.log_to_udemy(udemy_login, udemy_password)

    # checking every link
    saving = 0.0
    for link in links:
        saving += my_bot.buy_free_course(link, sleep_time)

    # printing stats and ending
    my_bot.printing_stats_udemy_courses()
    print("You are save: " + str(saving))
    my_bot.driver.close()