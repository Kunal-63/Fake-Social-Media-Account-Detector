import instaloader
from datetime import datetime
from instagrapi import Client
L = instaloader.Instaloader()
username1 = input("Username: ")
password1 = input("Password: ")
account_name1 = input("Account Name: ")
L.login(username1, password1)

cl = Client()
cl.login(username1, password1)

percent = 0
dict=cl.user_info_by_username(account_name1).dict()
if (dict["is_verified"] == True):
    print(account_name1,"is real")
else:
    try:
        profile = instaloader.Profile.from_username(L.context, account_name1)
        posts = profile.get_posts()
        post1 = next(posts)
        post2 = next(posts)
        timestamp1 = datetime.fromtimestamp(post1.date_local.timestamp())
        timestamp2 = datetime.fromtimestamp(post2.date_local.timestamp())
        duration = timestamp2 - timestamp1
        if (abs(duration.days) == 1):
            percent +=  0.2


        likes1=[1]
        for i in posts:
            x = i.likes
            if x == 0:
                x = 1
                likes1.append(x)
            else: 
                likes1.append(x)
        avg_likes = sum(likes1) / len(likes1)
        likes_followers_ration = avg_likes / int(dict["follower_count"])
        if (likes_followers_ration >= 0.33):
            percent += 0.05
        elif(likes_followers_ration >= 0.2):
            percent += 0.1
    except :
        pass
    
    try:
        if dict["is_private"] == False:
            percent += 0.1
        else:
            percent += 0.05
    except:
        pass
    try:
        follower_following_ratio = int(dict['follower_count']) / int(dict['following_count'])
        if (follower_following_ratio >= 0.5):
            percent += 0.05
        elif (follower_following_ratio < 0.5 and follower_following_ratio >= 0.33):
            percent += 0.1
        elif (follower_following_ratio < 0.33):
            percent += 0.2
    except:
        pass
        
    try:
        media_follower_ratio = int(dict["media_count"]) / int(dict["follower_count"])
        if (media_follower_ratio >= 0.5):
            percent += 0.05
        elif (media_follower_ratio > 0.8):
            percent += 0.1
        elif (media_follower_ratio > 1):
            percent += 0.2
    except:
        pass
    try:
        if (dict["biography"] == None) or (len(dict["biography"]) >= 125):
                percent += 0.2
    except:
        pass
if (percent >= 0.6):
    print(account_name1, "is fake")
elif (percent >= 0.5 and percent < 0.6):
    print(account_name1, "is probl fake")
elif (percent < 0.5 and percent <= 0.35):
    print(account_name1, "is probl real")
elif (percent < 0.35):
    print(account_name1,"is real")