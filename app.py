from flask import Flask, request, jsonify, render_template
from utils import load_json, get_liked_media_dict_path, get_user_likes_per_account
import config


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


if __name__ == "__main__":
    app.run(host="0.0.0.0")
