from utils import (
    load_json,
    save_json,
    delay,
    get_liked_media_list_from_username,
    get_follower_likes_list,
    get_liked_media_dict_path,
    get_follower_likes_list_path,
)


def scrape_liked_media_list(igapi, config):
    username = config.target_username
    liked_media_dict = get_liked_media_list_from_username(igapi, username)

    liked_media_dict_path = get_liked_media_dict_path(username)
    save_json(liked_media_dict, liked_media_dict_path)


def scrape_follower_likes_list(igapi, config):
    username = config.target_username
    follower_likes_list = get_follower_likes_list(igapi, username)

    follower_likes_list_path = get_follower_likes_list_path(username)
    save_json(follower_likes_list, follower_likes_list_path)


if __name__ == "__main__":
    import config
    from igapi import igapi

    scrape_liked_media_list(igapi, config)
    scrape_follower_likes_list(igapi, config)
