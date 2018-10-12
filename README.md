# Albumart-Buster
**NOTE: The DE script is deprecated because reCaptcha was added. The US script is still functional as of 2018-10-09.**
## Description
script to write custom messages to the leaderboard of Red Bull's [German](http://albumartiq.redbull.com/) and [US](https://daily.redbullmusicacademy.com/specials/2016-album-art-iq/#) Album Art IQ.
## Usage
Show overall top ten:
```bash
python bust_en.py topten 
```
Show genre topten
```bash
python bust_en.py topten --genre <genre>
```
Post a specific name and score to a genre:
```bash
python bust_en.py post <name> <score> <genre>
```
Write a text to a genre leaderbord (text is splitted automatically):
```bash
python bust_en.py write <genre> "<text>"
```
Write a twitter feed to a category (updates every 30 seconds):
```bash
python bust_en.py tweet \ 
    --consumer-key <consumer-key> \
    --consumer-secret <consumer-secret> \
    --access-token-key <access-token-key> \
    --access-token-secret <access-token-secret> \
    --screen-name <screen-name>
```

