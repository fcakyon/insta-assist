from InstagramAPI import InstagramAPI
from utils import delay
import config

agent_id = config.agent_id
agent_pw = config.agent_pw
igapi = InstagramAPI(agent_id, agent_pw)
delay(30, 40, "will login")
igapi.login()
