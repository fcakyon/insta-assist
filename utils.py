import re
import time
import json
import os.path
from random import randint
from datetime import datetime

# from InstagramAPI import InstagramAPI


def get_future_time_string(seconds_from_now):
    now_in_seconds = time.mktime(time.localtime())
    future_in_seconds = now_in_seconds + seconds_from_now
    future_in_struct = time.localtime(future_in_seconds)
    future_in_string = (
        ("%02d" % future_in_struct[2])
        + "."
        + ("%02d" % future_in_struct[1])
        + "."
        + ("%04d" % future_in_struct[0])
        + " | "
        + ("%02d" % future_in_struct[3])
        + ":"
        + ("%02d" % future_in_struct[4])
    )
    future_in_string_detailed = (
        ("%02d" % future_in_struct[2])
        + "."
        + ("%02d" % future_in_struct[1])
        + "."
        + ("%04d" % future_in_struct[0])
        + " | "
        + ("%02d" % future_in_struct[3])
        + ":"
        + ("%02d" % future_in_struct[4])
        + ":"
        + ("%02d" % future_in_struct[5])
    )
    return future_in_string, future_in_string_detailed


def delay(min_delay, max_delay, display_text):
    seconds_from_now = randint(min_delay, max_delay)
    futureTimeString, futureTimeStringDetailed = get_future_time_string(
        seconds_from_now
    )
    print(futureTimeStringDetailed + " : " + display_text)

    if seconds_from_now < 5:
        time.sleep(seconds_from_now)
    else:
        for ind in range(seconds_from_now):
            time.sleep(1)


def get_userid_from_username(igapi, username):
    success = igapi.searchUsername(username)
    if success:
        userid = igapi.LastJson["user"]["pk"]
        return userid
    else:
        print("User doesnt exist: " + username)
        return False


def get_all_followings(igapi, target_userid):
    following_list = []
    current_followings_list = igapi.getTotalFollowings(target_userid)
    for following in current_followings_list:
        user = {
            "username": following["username"],
            "userid": following["pk"],
            "is_private": following["is_private"],
            "full_name": following["full_name"],
        }
        following_list.append(user)
    return following_list


def get_following_liked_medias(igapi, following_list, target_username):
    full_liked_media_list = []
    clean_liked_media_list = []
    for following in following_list:
        if following["is_private"] is False:
            try:
                delay(5, 10, "will scrap user: " + following["username"])
                igapi.getUserFeed(following["userid"])
                items = igapi.LastJson["items"]
                for item in items:
                    if target_username in item["top_likers"]:
                        full_liked_media_list.append(item)
                        media_url_list = []
                        try:
                            carousel_media_list = item["carousel_media"]
                            for carousel_media in carousel_media_list:
                                media_url = carousel_media["image_versions2"][
                                    "candidates"
                                ][0]["url"]
                                media_url_list.append(media_url)
                        except:
                            media_url = item["image_versions2"]["candidates"][1]["url"]
                            media_url_list.append(media_url)

                        clean_media = {
                            "media_id": item["pk"],
                            "username": item["user"]["username"],
                            "full_name": item["user"]["full_name"],
                            "profile_pic_url": item["user"]["profile_pic_url"],
                            "timestamp": item["taken_at"],
                            "date": datetime.fromtimestamp(item["taken_at"]).strftime(
                                "%d/%m/%Y, %H:%M"
                            ),
                            "like_count": item["like_count"],
                            "media_url_list": media_url_list,
                            "media_url": "https://instagram.com/p/" + item["code"],
                        }
                        clean_liked_media_list.append(clean_media)
            except:
                None
    return {"full": full_liked_media_list, "clean": clean_liked_media_list}


def get_liked_media_list_from_username(igapi, username):
    userid = get_userid_from_username(igapi, username)
    following_list = get_all_followings(igapi, userid)
    liked_media_dict = get_following_liked_medias(igapi, following_list, username)
    return liked_media_dict


def load_json(json_path):
    with open(json_path) as json_file:
        json_dict = json.load(json_file)
    return json_dict


def save_json(json_data, json_path):
    json_dir = os.path.dirname(json_path)
    create_dir(json_dir)
    with open(json_path, "w") as outfile:
        json.dump(json_data, outfile)


def create_dir(_dir):
    """
    Creates given directory if it is not present.
    """
    if not os.path.exists(_dir):
        os.makedirs(_dir)
