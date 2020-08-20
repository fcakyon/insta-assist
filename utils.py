import re
import time
import json
import os.path
from random import randint
#from InstagramAPI import InstagramAPI


def get_future_time_string(seconds_from_now):
    now_in_seconds = time.mktime(time.localtime())
    future_in_seconds = now_in_seconds + seconds_from_now
    future_in_struct = time.localtime(future_in_seconds)
    future_in_string = ('%02d' % future_in_struct[2]) + "." + ('%02d' % future_in_struct[1]) + "." + ('%04d' % future_in_struct[0]) + " | " + ('%02d' % future_in_struct[3]) + ":" + ('%02d' % future_in_struct[4])
    future_in_string_detailed = ('%02d' % future_in_struct[2]) + "." + ('%02d' % future_in_struct[1]) + "." + ('%04d' % future_in_struct[0]) + " | " + ('%02d' % future_in_struct[3]) + ":" + ('%02d' % future_in_struct[4]) + ":" + ('%02d' % future_in_struct[5])
    return future_in_string, future_in_string_detailed


def delay(min_delay, max_delay, display_text):
    bekleme_suresi = randint(min_delay, max_delay)
    futureTimeString, futureTimeStringDetailed = GetFutureTimeString(bekleme_suresi)
    print(futureTimeStringDetailed +"'de " + display_text)

    if bekleme_suresi < 5:
        time.sleep(bekleme_suresi)
    else:
        for ind in range(bekleme_suresi):
            time.sleep(1)

def GetUserIDFromUsername(igapi, targetUserName):
    success = igapi.searchUsername(targetUserName)
    if success:
        userID = igapi.LastJson["user"]["pk"]
        return userID
    else
        print("Böyle bir kullanıcı yokmuş: "+targetUserName)
        return False 