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
    """
    Returns a list of {"username": "", "userid": 0, "is_private": false, "full_name": ""}
    """
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
    """
    each element in following_list should have the form: {"username": "", "userid": 0, "is_private": false, "full_name": ""}

    Returns {"full": full_liked_media_list, "clean": clean_liked_media_list}
    """
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
                            "user_id": item["user"]["pk"],
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
    """
    Returns {"full": full_liked_media_list, "clean": clean_liked_media_list}
    """
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


def get_liked_media_dict_path(username):
    liked_media_dict_path = os.path.join("data", username, "liked_media_dict.json")
    return liked_media_dict_path


def get_user_likes_per_account(liked_media_dict):
    """
    Returns a list of {"username": "", "number_of_liked_posts": 0, "liked_media_list": [], "profile_pic_url": "", "profile_url": ""}
    """
    liked_media_list = liked_media_dict["clean"]
    # create dict with structure: {username: {"liked_media_list": []}}
    user_likes_per_account = dict()
    for liked_media in liked_media_list:
        liked_username = liked_media["username"]
        if liked_username not in user_likes_per_account.keys():
            user_likes_per_account[liked_username] = {"liked_media_list": [liked_media]}
        else:
            user_likes_per_account[liked_username]["liked_media_list"].append(
                liked_media
            )
    # create dict with structure: {username: {"liked_media_list": [], "number_of_liked_posts": 0}}
    for liked_username in user_likes_per_account.keys():
        user_likes_per_account[liked_username]["number_of_liked_posts"] = len(
            user_likes_per_account[liked_username]["liked_media_list"]
        )
    # create list with structure: [{"username": "", "number_of_liked_posts": 0}]
    user_likes_per_account_list = [
        {
            "username": liked_username,
            "number_of_liked_posts": user_likes_per_account[liked_username][
                "number_of_liked_posts"
            ],
            "profile_pic_url": user_likes_per_account[liked_username][
                "liked_media_list"
            ][0]["profile_pic_url"],
            "profile_url": "https://www.instagram.com/" + liked_username,
            "liked_media_list": user_likes_per_account[liked_username][
                "liked_media_list"
            ],
        }
        for liked_username in user_likes_per_account
    ]

    return user_likes_per_account_list
