
from operator import index
from traceback import print_tb
from unittest import result
from winreg import REG_DWORD
from flask import Flask, render_template, request, url_for, flash, redirect
from matplotlib.style import use
from colorsys import ONE_SIXTH
from os import link
from re import X
from statistics import mean
import instaloader
from instaloader import  Profile
from datetime import datetime
from itertools import dropwhile, takewhile
import statistics 
from os import listdir
import os
from os.path import isfile, join
from re import L
from PIL import Image
import instaloader
from instaloader import Profile 
import time 
import shutil
import datetime
from os import listdir
import os
from os.path import isfile, join
from re import L

from pwnedpasswords import Password
app = Flask(__name__)



@app.route('/',methods = ['POST', 'GET'])
def home():
   if request.method == 'POST':
      return redirect(url_for("login"))
   return render_template("home.html")

percentage=0
users = []


# Create an instance of Instaloader class


@app.route('/login', methods = ['POST', 'GET'] )
def login():
   if request.method== 'POST':
      username=str(request.form["username"])
      password=str(request.form["password"])
      percentage=0
      users = []

      # Create an instance of Instaloader class
      ig = instaloader.Instaloader()

      #req_user = input("Enter your username: ")
      #password= input("Enter your password: ")
      ig.login(username,password)

      # Load a profile from an Instagram handle
      profile  = instaloader.Profile.from_username(ig.context, username)




      # user = profile .username
      # no_of_post =  profile .mediacount 
      # bio = profile .biography
      # links = profile .external_url
      # private = profile.is_private # displays True, if private account 
      #ig.download_profile(username , profile_pic_only=True)
      posts = profile.get_posts()

      no_of_followers = profile .followers 
      no_of_following =  profile .followees
      no_of_post =  profile .mediacount 
      

      followers_public_fake = []
      followers_public_real = []

      following_fake = []
      following_real = []

      ratios = []

      likes1=[1]
      for i in posts:
         x = i.likes
         if x == 0:
            x = 1
            likes1.append(x)
         else: 
            likes1.append(x)

      average_likes = statistics.mean(likes1)

      followers_following_ratio = no_of_followers / no_of_following
      post_followers_ratio = no_of_post / no_of_followers
      likes_followers_ratio = average_likes / no_of_followers


      ratios.append(followers_following_ratio)
      ratios.append(post_followers_ratio)
      ratios.append(likes_followers_ratio)

      #followers
      for followers in profile.get_followers():  

         profile  = instaloader.Profile.from_username(ig.context, followers.username)
         percentage = 0 
         
         user = profile .username
         bio = profile .biography
         links = profile .external_url
         no_of_post =  profile .mediacount 
         no_of_followers = profile.followers 
         no_of_following =  profile.followees

         
         
         #PROFILE COMPARISON 

         ig.download_profile(user,profile_pic_only=True)
         
         file_names=[]

         x = listdir(user)
         for i in x:
            file_names.append(i)
         # #print(len(file_names))

         unique_name=[]
         for i in file_names:
            if(i not in unique_name):
                  unique_name.append(i)
         # #print(len(unique_name))

         c=0

         for i in unique_name:
            # #print(i[-15:])    
            if(i[-15:]=="profile_pic.jpg"):
                  os.rename("./{}/".format(user)+i,"./{}/profile_pic.jpg".format(user))
            

         img1 = Image.open("D:\\Hackathon 2022\\{}\\profile_pic.jpg".format(user)).convert('RGB')
         img2 = Image.open("D:\\Hackathon 2022\\blankpof.jpg").convert('RGB')
         if img1.im.bands != img2.im.bands:
            #print('PROFILE IS NOT EMPTY')
            exit(-1)

         imdata1 = list(img1.getdata())
         imdata2 = list(img2.getdata())


         diff = 0
         if img1.im.bands == 1:
            diff = sum([abs(float(i1) - float(i2)) for i1, i2 in zip(imdata1, imdata2)])
            
         else:
            diff = sum([abs(float(i1) - float(i2)) for i1, i2 in
                        zip([i for p in imdata1 for i in p],
                              [i for p in imdata2 for i in p])])
            
            
         if diff > 0:
            pass
            #print('Profile is not empty')
            
         else:

            if(profile.is_private is False):
                  percentage += 25
            else:
                  percentage += 35  
            
            #print("Profile is empty")

         

         # RATIOS 


         if( no_of_followers == 0):
            no_of_followers=1
         if( no_of_following == 0):
            no_of_following=1
         followers_following_ratio = no_of_followers / no_of_following

         if(no_of_post == 0):
            no_of_post=1
         post_followers_ratio = no_of_post / no_of_followers
         
         


         if profile.is_private is False:
            percentage += 5 


            #LIKES_FOLLOWERS RATIO 


            likes1=[1]
            for i in posts:
                  x = i.likes
                  if x == 0:
                     x = 1
                     likes1.append(x)
                  else: 
                     likes1.append(x)

            average_likes = statistics.mean(likes1)

            if ( average_likes <= 0):
                  average_likes=1
            if( no_of_followers == 0):
                  no_of_followers=1
            likes_followers_ratio = average_likes / no_of_followers




            if likes_followers_ratio < 0.25 and likes_followers_ratio > 0.20:
                  percentage += 5 

            elif likes_followers_ratio < 0.20 and likes_followers_ratio > 0.167:
                  percentage += 7

            elif likes_followers_ratio < 0.167:
                  percentage += 10




            #FOLLOWERS_FOLLOWING RATIO 


            if followers_following_ratio < 0.5 and followers_following_ratio > 0.3:
                  percentage += 10
            elif followers_following_ratio < 0.3 and followers_following_ratio > 0.25:
                  percentage += 12 
            elif followers_following_ratio < 0.25:
                  percentage += 15 




            #BIO LENGTH 


            if len(bio) == 0 or len(bio) >= 125:
                  percentage +=10


      

            #POST_FOLLOWERS RATIO 

            if post_followers_ratio > 2 and post_followers_ratio < 3:
                  percentage += 10 
            elif post_followers_ratio > 3 and post_followers_ratio < 4:
                  percentage += 12
            elif post_followers_ratio > 4:
                  percentage += 15

            if (percentage >= 60):
                  print(user,"fake")
                  followers_public_fake.append(user)
            else:
                  print(user,"real")
                  followers_public_real.append(user)

            #CAPTIONS
      

         else:


            #FOLLOWERS_FOLLOWING RATIO


            if followers_following_ratio < 0.5 and followers_following_ratio > 0.3:
                  percentage += 20
            elif followers_following_ratio < 0.3 and followers_following_ratio > 0.25:
                  percentage += 23
            elif followers_following_ratio < 0.25:
                  percentage += 25 


            
            #BIO LENGTH


            if len(bio) == 0 or len(bio) >= 125:
                  percentage +=20 



         
            #POST_FOLLOWERS RATIO 


            if post_followers_ratio > 2 and post_followers_ratio < 3:
                  percentage += 15 
            elif post_followers_ratio > 3 and post_followers_ratio < 4:
                  percentage += 17
            elif post_followers_ratio > 4:
                  percentage += 20

         
            if (percentage >= 75 ):
                  print(user,"fake")
                  following_fake.append(user)
            else:
                  print(user,"real")
                  following_real.append(user)

         
         shutil.rmtree('./{}'.format(user))

      #following



      for following in profile.get_followees(): 

         profile  = instaloader.Profile.from_username(ig.context, following.username)
         percentage = 0 
         
         user = profile .username
         bio = profile .biography
         links = profile .external_url
         no_of_post =  profile .mediacount 
         no_of_followers = profile.followers 
         no_of_following =  profile.followees
         if(no_of_post == 0):
            no_of_post = 1
         if(no_of_followers == 0):
            no_of_followers = 1
         if ( no_of_following == 0):
            no_of_following = 1

         
         
         #PROFILE COMPARISON 

         ig.download_profile(user,profile_pic_only=True)

         file_names=[]

         x = listdir(user)
         for i in x:
            file_names.append(i)
         # #print(len(file_names))

         unique_name=[]
         for i in file_names:
            if(i not in unique_name):
                  unique_name.append(i)
         # #print(len(unique_name))

         c=0

         for i in unique_name:
            # #print(i[-15:])    
            if(i[-15:]=="profile_pic.jpg"):
                  os.rename("./{}/".format(user)+i,"./{}/profile_pic.jpg".format(user))
            

         img1 = Image.open("C:\\Users\\Dell\\Desktop\\Hackathon\\{}\\profile_pic.jpg".format(user)).convert('RGB')
         img2 = Image.open("C:\\Users\\Dell\\Desktop\\Hackathon\\blankpof.jpg").convert('RGB')
         if img1.im.bands != img2.im.bands:
            print('PROFILE IS NOT EMPTY')
            exit(-1)

         imdata1 = list(img1.getdata())
         imdata2 = list(img2.getdata())


         diff = 0
         if img1.im.bands == 1:
            diff = sum([abs(float(i1) - float(i2)) for i1, i2 in zip(imdata1, imdata2)])
            
         else:
            diff = sum([abs(float(i1) - float(i2)) for i1, i2 in
                        zip([i for p in imdata1 for i in p],
                              [i for p in imdata2 for i in p])])
            
            
         if diff > 0:
            print('Profile is not empty')
            
         else:
            print("Profile is empty")
            percentage += 25


         

         # RATIOS 

         if( no_of_followers == 0):
            no_of_followers=1
         if( no_of_following == 0):
            no_of_following=1
         followers_following_ratio = no_of_followers / no_of_following

         if(no_of_post == 0):
            no_of_post=1
         post_followers_ratio = no_of_post / no_of_followers
         
         #PUBLIC OR PRIVATE

         if profile.is_private is False:
            percentage += 5
         else:
            pass

         

         # LIKES



         likes1=[1]
         for i in posts:
            x = i.likes
            if x == 0:
                  x = 1
                  likes1.append(x)
            else: 
                  likes1.append(x)

         average_likes = statistics.mean(likes1)

         if ( average_likes <= 0):
            average_likes=1
         if( no_of_followers == 0):
            no_of_followers=1
         likes_followers_ratio = average_likes / no_of_followers



         if likes_followers_ratio < 0.25 and likes_followers_ratio > 0.20:
            percentage += 10 

         elif likes_followers_ratio < 0.20 and likes_followers_ratio > 0.167:
            percentage += 15

         elif likes_followers_ratio < 0.167:
            percentage += 20



         #FOLLOWERS_FOLLOWING RATIO 



         if followers_following_ratio < 0.5 and followers_following_ratio > 0.3:
            percentage += 10
         elif followers_following_ratio < 0.3 and followers_following_ratio > 0.25:
            percentage += 15 
         elif followers_following_ratio < 0.25:
            percentage += 20 




         #BIO LENGTH 


         if len(bio) == 0 or len(bio) >= 125:
            percentage +=5 



         #POST_FOLLOWERS RATIO 

         if post_followers_ratio > 2 and post_followers_ratio < 3:
            percentage += 10 
         elif post_followers_ratio > 3 and post_followers_ratio < 4:
            percentage += 15
         elif post_followers_ratio > 4:
            percentage += 20

         
         

         if (percentage >= 60 ):
                  print(user,"fake")
                  following_fake.append(user)
         else:
            print(user,"real")
            following_real.append(user)

         shutil.rmtree('./{}'.format(user))



      # print(ratios)
      
      global followers1
      followers1=[followers_public_fake,followers_public_real]
      global following1
      following1=[following_fake,following_real]

   return render_template("login.html")


@app.route('/feedback',methods = ['POST', 'GET'])
def feedback():
   if request.method=='POST':
      return redirect(url_for("results"))
   return render_template("feedbackform.html")


@app.route('/results',methods=['POST', 'GET'])
def results():
   return render_template("results.html",followers=followers1, following=following1)


      


if __name__ == '__main__':
   app.run(debug = True)