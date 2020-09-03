import re
import time
import json
import os.path
from random import randint
from datetime import datetime

# from InstagramAPI import InstagramAPI

INSTAGRAM_DEFAULT_PROFIL_PIC_URL = "https://scontent-maa2-1.cdninstagram.com/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=scontent-maa2-1.cdninstagram.com&_nc_ohc=OU-5fMy1ffUAX-o-6ty&oh=9438c1dcdb6c5d4150e5f396a64eeadb&oe=5F7A818F&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2"


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


def get_all_followers(igapi, target_userid):
    """
    Returns a list of {"username": "", "userid": 0, "is_private": false, "full_name": ""}
    """
    follower_list = []
    current_followers_list = igapi.getTotalFollowers(target_userid)
    for follower in current_followers_list:
        user = {
            "username": follower["username"],
            "userid": follower["pk"],
            "is_private": follower["is_private"],
            "full_name": follower["full_name"],
        }
        follower_list.append(user)
    return follower_list


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


def get_follower_likes_list_path(username):
    follower_likes_list_path = os.path.join(
        "data", username, "follower_likes_list.json"
    )
    return follower_likes_list_path


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


def get_follower_likes_list(igapi, username):
    user_id = get_userid_from_username(igapi, username)
    follower_list = get_all_followers(igapi, user_id)
    follower_dict = dict()
    for ind in range(len(follower_list)):
        follower_username = follower_list[ind]["username"]
        follower_list[ind]["number_of_liked_posts"] = 0
        follower_list[ind]["profile_pic_url"] = INSTAGRAM_DEFAULT_PROFIL_PIC_URL
        follower_dict[follower_username] = follower_list[ind]

    response = igapi.getUserFeed(user_id)
    user_medias = igapi.LastJson["items"]
    media_id_list = [media["pk"] for media in user_medias]

    for media_id in media_id_list:
        response = igapi.getMediaLikers(media_id)
        media_likers_list = igapi.LastJson["users"]
        for media_liker in media_likers_list:
            media_liker_username = media_liker["username"]
            media_liker_profile_pic_url = media_liker["profile_pic_url"]
            if media_liker_username in follower_dict.keys():
                follower_dict[media_liker_username]["number_of_liked_posts"] += 1
                follower_dict[media_liker_username][
                    "profile_pic_url"
                ] = media_liker_profile_pic_url

    # create list with structure: [{"username": "", "full_name": "", "number_of_liked_posts": 0, "profile_url": "", "profile_pic_url": ""}]
    follower_likes_list = [
        {
            "username": follower_username,
            "full_name": follower_dict[follower_username]["full_name"],
            "number_of_liked_posts": follower_dict[follower_username][
                "number_of_liked_posts"
            ],
            "profile_url": "https://www.instagram.com/" + follower_username,
            "profile_pic_url": follower_dict[follower_username]["profile_pic_url"],
        }
        for follower_username in follower_dict.keys()
    ]
    return follower_likes_list


def get_hd_profile_pic(igapi, username):
    """
    Returns {"user_id": 0, "username": "", full_name": "", "hd_profile_pic_url": "",
            "is_private":": false, "is_business": false, "profile_url": ""}
    """
    user_id = get_userid_from_username(igapi, username)
    response = igapi.getUsernameInfo(user_id)
    hd_profile_pic_url = igapi.LastJson["user"]["hd_profile_pic_url_info"]["url"]
    full_name = igapi.LastJson["user"]["full_name"]
    is_private = igapi.LastJson["user"]["is_private"]
    is_business = igapi.LastJson["user"]["is_business"]
    profile_url = ("https://www.instagram.com/" + username,)
    hd_profile_pic_dict = {
        "user_id": user_id,
        "hd_profile_pic_url": hd_profile_pic_url,
        "full_name": full_name,
        "is_private": is_private,
        "is_business": is_business,
        "profile_url": profile_url,
    }
    return hd_profile_pic_dict


if __name__ == "__main__":
    # from igapi import igapi

    username = "fcakyon"
    # get_hd_profile_pic(igapi, username)

    follower_likes_list_path = get_follower_likes_list_path(username)
    follower_likes_list = load_json(follower_likes_list_path)

    def sort_function(e):
        return e["number_of_liked_posts"]

    follower_likes_list.sort(reverse=True, key=sort_function)
    follower_likes_list
