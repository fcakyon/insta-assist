from flask import Flask, request, jsonify, render_template
from igapi import igapi
from utils import (
    load_json,
    get_liked_media_dict_path,
    get_user_likes_per_account,
    get_follower_likes_list_path,
    get_hd_profile_pic,
)


app = Flask(__name__)


@app.route("/likes/<username>")
def likes(username):
    liked_media_dict_path = get_liked_media_dict_path(username)
    liked_media_dict = load_json(liked_media_dict_path)
    liked_media_list = liked_media_dict["clean"]
    # liked_media_list = liked_media_dict

    def sort_function(e):
        return e["timestamp"]

    liked_media_list.sort(reverse=True, key=sort_function)
    return render_template("likes.html", liked_media_list=liked_media_list)


@app.route("/likes_per_account/<username>")
def likes_per_account(username):
    liked_media_dict_path = get_liked_media_dict_path(username)
    liked_media_dict = load_json(liked_media_dict_path)
    user_likes_per_account_list = get_user_likes_per_account(liked_media_dict)

    def sort_function(e):
        return e["number_of_liked_posts"]

    user_likes_per_account_list.sort(reverse=True, key=sort_function)
    return render_template(
        "likes_per_account.html",
        user_likes_per_account_list=user_likes_per_account_list,
    )


@app.route("/follower_likes/<username>")
def follower_likes(username):
    follower_likes_list_path = get_follower_likes_list_path(username)
    follower_likes_list = load_json(follower_likes_list_path)

    def sort_function(e):
        return e["number_of_liked_posts"]

    follower_likes_list.sort(reverse=True, key=sort_function)
    return render_template(
        "follower_likes.html", follower_likes_list=follower_likes_list,
    )


@app.route("/hd_profile_pic/<username>")
def hd_profil_pic(username):
    hd_profile_pic_dict = get_hd_profile_pic(igapi, username)

    return render_template(
        "hd_profile_pic.html", hd_profile_pic_dict=hd_profile_pic_dict,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
