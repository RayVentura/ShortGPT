# from shortGPT.api_utils.pexels_api import getBestVideo
# import json
# from shortGPT.gpt.gpt_editing import getVideoSearchQueriesTimed
# timed_captions = """
# [[[0,0.81],"Are you a coffee lover?"],[[0.81,1.8],"Do you know the difference"],[[1.8,2.64],"between Arabica and Robusta"],[[2.64,3.96],"coffee beans?"],[[3.96,5.1],"At CoffeeMedia, we"],[[5.1,5.85],"are passionate about coffee"],[[5.85,6.57],"and we want to share"],[[6.57,7.26],"our knowledge with you."],[[7.26,8.4],"Arabica beans are known"],[[8.4,9.69],"for their smooth and delicate"],[[9.69,11.01],"flavor,"],[[11.01,12.09],"while Robusta beans"],[[12.09,13.41],"have a stronger and more"],[[13.41,14.4],"bitter taste."],[[14.4,16.11],"Our expert coffee"],[[16.11,17.31],"roasters carefully select"],[[17.31,18.78],"the finest Arabica beans"],[[18.78,20.37],"to create the perfect blend"],[[20.37,23.97],"for your morning cup of joe."],[[23.97,25.47],"We take pride"],[[25.47,26.85],"in sourcing our beans"],[[26.85,28.38],"from sustainable farms"],[[28.38,30.36],"around the world,"],[[30.36,31.74],"ensuring that every sip"],[[31.74,33.84],"you take is ethically produced."],[[33.84,34.95],"Whether you prefer a"],[[34.95,36.15],"bold espresso or a creamy"],[[36.15,37.29],"latte,"],[[37.29,39.03],"CoffeeMedia has the best"],[[39.03,40.32],"coffee in California."],[[40.32,41.61],"Join us on a"],[[41.61,42.54],"journey of flavor and"],[[42.54,43.59],"quality."],[[43.59,45.15],"Start your day right"],[[45.15,46.2],"with CoffeeMedia,"],[[46.2,47.04],"your ultimate coffee experience."]]"""
# timed_captions = json.loads(timed_captions)
# video_queries = getVideoSearchQueriesTimed(timed_captions)
# things = []
# used_links = []
# for (t1, t2), (q1, q2,q3) in video_queries:
#     url = ""
#     for query in [q2, q3, q1]:
#         url = getBestVideo(query,orientation_landscape=True, used_vids=used_links)
#         if url:
#             used_links.append(url.split('.hd')[0])
#             break
#     things.append([[t1,t2], url])
#     print(t1, t2, url)

# from moviepy.editor import VideoFileClip, CompositeVideoClip
# video = []
# for (t1, t2), url in things:
#     target_duration = t2-t1
#     print("processing", t1, t2, url)
#     video.append(VideoFileClip(url).set_start(t1).set_end(t2))
# final_vid = CompositeVideoClip(video)
# final_vid.write_videofile('test.mp4')

# import json
# from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
# timed_captions = """
# [[[0,0.81],"Are you a coffee lover?"],[[0.81,1.8],"Do you know the difference"],[[1.8,2.64],"between Arabica and Robusta"],[[2.64,3.96],"coffee beans?"],[[3.96,5.1],"At CoffeeMedia, we"],[[5.1,5.85],"are passionate about coffee"],[[5.85,6.57],"and we want to share"],[[6.57,7.26],"our knowledge with you."],[[7.26,8.4],"Arabica beans are known"],[[8.4,9.69],"for their smooth and delicate"],[[9.69,11.01],"flavor,"],[[11.01,12.09],"while Robusta beans"],[[12.09,13.41],"have a stronger and more"],[[13.41,14.4],"bitter taste."],[[14.4,16.11],"Our expert coffee"],[[16.11,17.31],"roasters carefully select"],[[17.31,18.78],"the finest Arabica beans"],[[18.78,20.37],"to create the perfect blend"],[[20.37,23.97],"for your morning cup of joe."],[[23.97,25.47],"We take pride"],[[25.47,26.85],"in sourcing our beans"],[[26.85,28.38],"from sustainable farms"],[[28.38,30.36],"around the world,"],[[30.36,31.74],"ensuring that every sip"],[[31.74,33.84],"you take is ethically produced."],[[33.84,34.95],"Whether you prefer a"],[[34.95,36.15],"bold espresso or a creamy"],[[36.15,37.29],"latte,"],[[37.29,39.03],"CoffeeMedia has the best"],[[39.03,40.32],"coffee in California."],[[40.32,41.61],"Join us on a"],[[41.61,42.54],"journey of flavor and"],[[42.54,43.59],"quality."],[[43.59,45.15],"Start your day right"],[[45.15,46.2],"with CoffeeMedia,"],[[46.2,47.04],"your ultimate coffee experience."]]"""
# timed_captions = json.loads(timed_captions)
# #mycaption = TextClip("Hello world world hello man", font="Berlin-Sans-FB-Demi-Bold", color="white", fontsize=100).set_position(('center', 800)).set_end(1)
# video = VideoFileClip('test.mp4')
# total = [video]
# for (t1, t2), text in timed_captions:
#     total.append(TextClip(text, font="Berlin-Sans-FB-Demi-Bold", color="white", fontsize=100, stroke_width=2, stroke_color="black").set_position(('center', 800)).set_start(t1).set_end(t2))
# CompositeVideoClip(total).write_videofile('test2.mp4')


from gui.gui import run_app
run_app() 

# from moviepy.editor import VideoFileClip

# a = VideoFileClip('https://player.vimeo.com/external/473728076.hd.mp4?s=b7e94531f04d373bac03c2d4e7df95b79a9dabd2&profile_id=175&oauth2_token_id=57447761')
# print(a.write_videofile('test.mp4'))
