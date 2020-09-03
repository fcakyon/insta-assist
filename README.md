# insta-assist: My Personal Instagram Tools

## Usage
- install required packages:
```bash
pip install requirements.txt
```

- create a config.py file containing agent login info and target username to be scraped:
```python
agent_id = "ig_username"
agent_pw = "ig_password"
target_username = "target_ig_username"
```

- scrape required data:
```bash
python scrape.py
```

- run web app:
```bash
python app.py
```

- view endponints on browser:
```
localhost:5000/likes/ig_username
```

## Endpoints
- **/likes/target_ig_username:** shows the posts that target instagram user has liked
- **/likes_per_account/target_ig_username:** shows the number of posts that target instagram user has liked from specific accounts
- **/follower_likes/target_ig_username:** shows the number of posts that each follower of the target instagram user has liked
- **/hd_profile_pic/target_ig_username:** returns the hd version of the profile picture of the target instagram user