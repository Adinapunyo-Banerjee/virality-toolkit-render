# Views imports
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PredictionForm1, ReviewForm
from django.http import JsonResponse

# Prediction Imports
import os
import pickle
import numpy as np
import tensorflow as tf
from PIL import Image
from datetime import datetime, timezone, timedelta

# Custom Settings

CUMM_PRED = 5
DAY_CHANGE = 1

# Predictions here

QP_MODEL_DIR = 'MODELS/'
QP_SCALAR_DIR = 'MODELS/Model1/complements/'
QP_IMG_DIR = 'media/prediction_model1/'

model = tf.keras.models.load_model(QP_MODEL_DIR + 'final_model.h5')
stat_scaler = pickle.load(open(QP_SCALAR_DIR + 'stats_scaler.pickle', 'rb'))
like_scaler = pickle.load(open(QP_SCALAR_DIR + 'likes_scaler.pickle', 'rb'))
view_scaler = pickle.load(open(QP_SCALAR_DIR + 'views_scaler.pickle', 'rb'))

def quick_predict_script(stats, img_url):
    try:
        img = Image.open(img_url)
    except:
        return False

    img = img.resize((150, 150))
    thumb = np.array(img, dtype=np.float32)/255
    img_to_predict = np.expand_dims(thumb, axis=0)
    img.close()

    input_stat = np.expand_dims(stats, axis=0)
    input_stat = stat_scaler.transform(input_stat)

    try:
        ans = model.predict([img_to_predict, input_stat])
    except:
        return False
    view = view_scaler.inverse_transform(ans[0])
    like = like_scaler.inverse_transform(ans[1])
    return [view, like]

def quick_multi_predict_script2(input_stat, img_url):
    try:
        img = Image.open(img_url)
    except:
        return False

    img = img.resize((150, 150))
    thumb = np.array(img, dtype=np.float32)/255
    img.close()

    img_to_pred = np.expand_dims(thumb, axis=0)
    app = np.expand_dims(thumb, axis=0)

    print(img_to_pred.shape)
    for i in range(CUMM_PRED-1):
        app = np.append(app, img_to_pred, axis=0)
    print(app.shape)

    # for i in range(CUMM_PRED):
    #     imgs[0].append(thumb)
    # print(len(imgs), len(imgs[0]), len(imgs[0][0]), len(imgs[0][0][0]))
    # img_to_predict = np.expand_dims(thumb, axis=0)
    
    # input_stat = np.expand_dims(input_stat, axis=0)

    input_stat = stat_scaler.transform(input_stat)
    print(input_stat)
    print(app)

    ans = model.predict([app, input_stat])
    
    view = view_scaler.inverse_transform(ans[0])
    like = like_scaler.inverse_transform(ans[1])

    print(view)
    print(like)

    return [view, like]

def quick_multi_predict_script(input_stat, img_url):
    try:
        img = Image.open(img_url)
    except:
        return False

    img = img.resize((150, 150))
    thumb = np.array(img, dtype=np.float32)/255
    img_to_predict = np.expand_dims(thumb, axis=0)
    img.close()

    stat = np.expand_dims(input_stat[0], axis=0)
    stat = stat_scaler.transform(stat)

    ans = model.predict([img_to_predict, input_stat])
    
    view = view_scaler.inverse_transform(ans[0])
    like = like_scaler.inverse_transform(ans[1])

    print(view)
    print(like)

    return [view, like]






# Actual Views here

QUICK_PREDICT_COST = 1
CATEGORY_CHOICES = {
    1 : 'Film and Animation',
    2 : 'Autos and Vehicles',
    10 : 'Music',
    15 : 'Pets and Animals',
    17 : 'Sports',
    18 : 'Short Movies',
    19 : 'Travel and Events',
    20 : 'Gaming',
    21 : 'Video Blogging',
    22 : 'People and Blogs',
    23 : 'Comedy',
    24 : 'Entertainment',
    25 : 'News and Politics',
    26 : 'Howto and Style',
    27 : 'Education',
    28 : 'Science and Technology',
    29 : 'Nonprofits and Activism',
    30 : 'Movies',
    31 : 'Anime/Animation',
    32 : 'Action/Adventure',
    33 : 'Classics',
    34 : 'Comedy',
    35 : 'Documentary',
    36 : 'Drama',
    37 : 'Family',
    38 : 'Foreign',
    39 : 'Horror',
    40 : 'Sci-Fi/Fantasy',
    41 : 'Thriller',
    42 : 'Shorts',
    43 : 'Shows',
    44 : 'Trailer'
}

def tools(request):
    return render(request, 'tools.html', {})



def quick_predict2(request):
    if request.user.is_authenticated == False:                          # No user
        messages.error(request, "You need to login first!")
        return redirect("/accounts/login/")

    if request.method == 'GET':                                         # Simple GET
        context_dict = {'txt': 'Prediction Model 1'}
        form = PredictionForm1()
        context_dict['form'] = form

        return render(request, 'quick_predict.html', context_dict)

    
    elif request.method == 'POST':                                      # AJAX request!
        if request.user.tokenBalance - QUICK_PREDICT_COST < 0:          # Token check!
            return JsonResponse({'messages':[
                                                {'warning' : "You don't have enough tokens!"},
                                            ],
                                            'tokens' : request.user.tokenBalance
                                })
        form = PredictionForm1(request.POST, request.FILES)
        if form.is_valid():
            f_instance = form.save(commit=False)                        # Step 1
            f_instance.user = request.user                              # Step 2
            f_instance.save()                                           # Step 3 - This is how you set the user in the model!

            input_data = []
            input_data.append(['Category:', CATEGORY_CHOICES[f_instance.category]])
            input_data.append(["Channel publish:", str(f_instance.channel_pub_time)[:10]])
            input_data.append(["Video release:", str(f_instance.video_pub_time)[:10]])
            input_data.append(["Subscribers:", f_instance.subscribers])
            input_data.append(["Total Videos:", f_instance.videos])
            input_data.append(["Total Views:", f_instance.views])

            # category, seconds_since_published, subscribers, total_videos, total_views, publishing_date
            time_rn = datetime.now(timezone.utc)
            time_since_channel_published = (time_rn-f_instance.channel_pub_time)
            time_since_video_published = (time_rn-f_instance.video_pub_time)

            time_change = timedelta(days=DAY_CHANGE)

            full_stats = []
            for i in range(CUMM_PRED):
                stats = [f_instance.category, time_since_channel_published.total_seconds(), f_instance.subscribers, f_instance.videos, f_instance.views, time_since_video_published.total_seconds()]

                full_stats.append(stats)
                
                time_since_channel_published = time_since_channel_published + time_change
                time_since_video_published = time_since_video_published + time_change

            
            p = quick_multi_predict_script(full_stats, f_instance.thumb.url[1:])

            # p = quick_multi_predict_script(stats, f_instance.thumb.url[1:])       # Slicing to remove first character '/'

            # print(p)

            # if p:
            #     request.user.tokenBalance -= QUICK_PREDICT_COST             # Step 1
            #     request.user.totalPredictions += 1
            #     request.user.save()                                         # Step 2 - This is how you change user attributes!

            #     prediction_results = {
            #         'messages' : [
            #             {'success' : 'Prediction done successfuly!'}
            #         ],
            #         'result_data' : {
            #             'views' : round(p[0][0][0]),
            #             'likes' : round(p[1][0][0])
            #         },
            #         'tokens' : request.user.tokenBalance
            #     }

            #     return JsonResponse(prediction_results)
            # else:
            #     prediction_results = {
            #         'messages' : [
            #             {'error' : 'Your image cannot be processed! It might be corrupted.'}
            #         ],
            #         'tokens' : request.user.tokenBalance
            #     }

            #     return JsonResponse(prediction_results)



def quick_predict(request):
    if request.user.is_authenticated == False:                          # No user
        messages.error(request, "You need to login first!")
        return redirect("/accounts/login/")

    if request.method == 'GET':                                         # Simple GET
        context_dict = {'txt': 'Prediction Model 1'}
        form = PredictionForm1()
        context_dict['form'] = form

        return render(request, 'quick_predict.html', context_dict)

    
    elif request.method == 'POST':                                      # AJAX request!
        if request.user.tokenBalance - QUICK_PREDICT_COST < 0:          # Token check!
            return JsonResponse({'messages':[
                                                {'warning' : "You don't have enough tokens!"},
                                            ],
                                            'tokens' : request.user.tokenBalance
                                })
        form = PredictionForm1(request.POST, request.FILES)
        if form.is_valid():
            f_instance = form.save(commit=False)                        # Step 1
            f_instance.user = request.user                              # Step 2
            f_instance.save()                                           # Step 3 - This is how you set the user in the model!

            input_data = []
            input_data.append(['Category:', CATEGORY_CHOICES[f_instance.category]])
            input_data.append(["Channel publish:", str(f_instance.channel_pub_time)[:10]])
            input_data.append(["Video release:", str(f_instance.video_pub_time)[:10]])
            input_data.append(["Subscribers:", f_instance.subscribers])
            input_data.append(["Total Videos:", f_instance.videos])
            input_data.append(["Total Views:", f_instance.views])

            # category, seconds_since_published, subscribers, total_videos, total_views, publishing_date
            time_rn = datetime.now(timezone.utc)
            time_since_channel_published = (time_rn-f_instance.channel_pub_time)
            time_since_video_published = (time_rn-f_instance.video_pub_time)

            stats = [f_instance.category, time_since_channel_published.total_seconds(), f_instance.subscribers, f_instance.videos, f_instance.views, time_since_video_published.total_seconds()]
            p = quick_predict_script(stats, f_instance.thumb.url[1:])       # Slicing to remove first character '/'

            print(p)

            if p:
                request.user.tokenBalance -= QUICK_PREDICT_COST             # Step 1
                request.user.totalPredictions += 1
                request.user.save()                                         # Step 2 - This is how you change user attributes!

                prediction_results = {
                    'messages' : [
                        {'success' : 'Prediction done successfuly!'}
                    ],
                    'result_data' : {
                        'views' : round(p[0][0][0]),
                        'likes' : round(p[1][0][0])
                    },
                    'tokens' : request.user.tokenBalance
                }

                return JsonResponse(prediction_results)
            else:
                prediction_results = {
                    'messages' : [
                        {'error' : 'Your image cannot be processed! It might be corrupted or of an invalid type'}
                    ],
                    'tokens' : request.user.tokenBalance
                }

                return JsonResponse(prediction_results)


def about(request):
    if request.method == 'GET':
        return render(request, "about.html", {})
    
    elif request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            f_instance = form.save(commit=False)                        # Step 1
            f_instance.user = request.user                              # Step 2
            f_instance.save()                                           # Step 3 - This is how you set the user in the model!

            return JsonResponse({'messages':[
                                                {'success' : "Thank you for submitting a review! 😙"},
                                            ]
                                })
        
        return JsonResponse({'messages':[
                                            {'warning' : "Your review form was invalid 😩"},
                                        ]
                            })