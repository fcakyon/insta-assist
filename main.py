import config
from utils import (
    get_userid_from_username,
    get_all_followings,
    get_liked_media_list_from_username,
    delay,
    save_json,
)
from InstagramAPI import InstagramAPI
import time

agent_id = config.agent_id
agent_pw = config.agent_pw
igapi = InstagramAPI(agent_id, agent_pw)
delay(30, 40, "will login")
igapi.login()

username = config.target_username
liked_media_dict = get_liked_media_list_from_username(igapi, username)

json_path = config.json_path
save_json(liked_media_dict, json_path)
clean_liked_media_list
