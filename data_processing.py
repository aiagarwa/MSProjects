# -*- coding: utf-8 -*-
"""Data_Processing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ciPsV04neyaJc45Po9ka710rgDy-ka0P
"""

import pandas as pd
import numpy as np

from google.colab import drive 
drive.mount('/content/gdrive')

"""## Simulating data for recipe selections in different mood and weather

Method to generate random values within a given range
"""

import random

def generate_simulated_data(maxVal, size):
  data = []
  for i in range(size):
    data.append(random.randint(0,maxVal))
  return data

"""Generating random values for recipe selection for different moods and weather"""

# food_ratings = pd.read_csv('gdrive/My Drive/interactions_less_data_v3.csv',engine='python')
# food_ratings.head()

# food_ratings.insert(len(food_ratings.columns), "cold", generate_simulated_data(25, len(food_ratings)))
# food_ratings.insert(len(food_ratings.columns), "sunny", generate_simulated_data(25, len(food_ratings)))
# food_ratings.insert(len(food_ratings.columns), "angry", generate_simulated_data(25, len(food_ratings)))
# food_ratings.insert(len(food_ratings.columns), "happy", generate_simulated_data(25, len(food_ratings)))
# food_ratings.insert(len(food_ratings.columns), "rainy", generate_simulated_data(25, len(food_ratings)))
# food_ratings.insert(len(food_ratings.columns), "sad", generate_simulated_data(25, len(food_ratings)))

# food_ratings.head()

"""Dowmload the simulated data"""

from google.colab import files

food_ratings.to_csv('interactions_with_simulated_data.csv',index=False) 
files.download('interactions_with_simulated_data.csv')

"""Count the number of times a recipe is selected in a particular mood or weather by a user"""

def count_weather_mood_selection():
  data= pd.read_csv('gdrive/My Drive/sample_data2.csv',engine='python')
  # For Weather
  df_temp_weather=data[["user_id","recipe_id","weather"]]
  df_weather = pd.DataFrame(df_temp_weather.groupby([data.user_id, data.recipe_id, data.weather]).count().unstack(fill_value=0).reset_index())
  df_weather.drop([('user_id',  'cold'),('user_id', 'rainy'),('user_id', 'sunny'),('recipe_id','cold'),('recipe_id', 'rainy'),('recipe_id', 'sunny')], inplace=True, axis=1)
  df_weather.columns = df_weather.columns.get_level_values(1)
  df_weather.columns = ['user_id','recipe_id', 'cold', 'rainy','sunny']
  
  # For Mood
  df_temp_mood=data[["user_id","recipe_id","mood"]]
  df_mood = pd.DataFrame(df_temp_mood.groupby([data.user_id, data.recipe_id, data.mood]).count().unstack(fill_value=0).reset_index())
  df_mood.drop([('user_id',  'happy'),('user_id', 'angry'),('user_id', 'sad'),('recipe_id','happy'),('recipe_id', 'angry'),('recipe_id', 'sad')], inplace=True, axis=1)
  df_mood.columns = df_mood.columns.get_level_values(1)
  df_mood.columns = ['user_id','recipe_id', 'angry', 'happy','sad']

  # Combining Data
  data_combined = pd.concat([df_weather, df_mood['angry']], axis=1)
  data_combined = pd.concat([data_combined, df_mood['happy']], axis=1)
  data_combined = pd.concat([data_combined, df_mood['sad']], axis=1)
  data_combined["total_selection"] = data_combined["angry"]+data_combined["happy"]+data_combined["sad"]
  return data_combined

# data = count_weather_mood_selection()

"""Convert the number of times a recipe is selected in range of 1-5"""

def get_ratings_weather_mood(data, weather, mood):
  # For weather
  wthr_rcp_sel = data[weather].values
  for i, cnt in enumerate(wthr_rcp_sel):
    if cnt>17:
      wthr_rcp_sel[i] = 5
    elif cnt<18 and cnt>14:
      wthr_rcp_sel[i] = 4
    elif cnt<15 and cnt>10:
      wthr_rcp_sel[i] = 3
    elif cnt<11 and cnt>4:
      wthr_rcp_sel[i] = 2
    elif cnt<5 and cnt>=1:
      wthr_rcp_sel[i] = 1
    else:
      wthr_rcp_sel[i] = 0
  data.drop(weather, inplace=True, axis=1)
  data[weather] = wthr_rcp_sel 
  # For mood
  mood_rcp_sel = data[mood].values
  for i, cnt in enumerate(mood_rcp_sel):
    if cnt>17:
      mood_rcp_sel[i] = 5
    elif cnt<18 and cnt>14:
      mood_rcp_sel[i] = 4
    elif cnt<15 and cnt>10:
      mood_rcp_sel[i] = 3
    elif cnt<11 and cnt>4:
      mood_rcp_sel[i] = 2
    elif cnt<5 and cnt>=1:
      mood_rcp_sel[i] = 1
    else:
      mood_rcp_sel[i] = 0
  data.drop(mood, inplace=True, axis=1)
  data[mood] = mood_rcp_sel 

  # # For General Selection
  # tot_rcp_sel = data["total_selection"].values
  # for i, cnt in enumerate(mood_rcp_sel):
  #   if cnt>20:
  #     tot_rcp_sel[i] = 5
  #   elif cnt<21 and cnt>15:
  #     tot_rcp_sel[i] = 4
  #   elif cnt<16 and cnt>10:
  #     tot_rcp_sel[i] = 3
  #   elif cnt<11 and cnt>4:
  #     tot_rcp_sel[i] = 2
  #   elif cnt<5 and cnt>=1:
  #     tot_rcp_sel[i] = 1
  #   else:
  #     tot_rcp_sel[i] = 0
  # data.drop("total_selection", inplace=True, axis=1)
  # data["rating"] = tot_rcp_sel 
  return data

# data_new = get_ratings_weather_mood(data, "rainy", "sad")