Group members: Megha Ramanathan, James White, Sisilia Sinaga

All of our code is in gg_api.py. 

External libraries: nltk.corpus, vaderSentiment, nltk.sentiment.vader, difflib, imdb

import json
import nltk
import re
from nltk.corpus import stopwords
nltk.download('stopwords')
import string
from imdb import IMDb
from difflib import SequenceMatcher
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

Bonus return features of our project include best dressed and worst dressed. 

Address for github repository: https://github.com/yuiichiiros/cs337_proj1

Github repos used as inspiration: 
https://github.com/brownrout/EECS-337-Golden-Globes/blob/master/gg_api.py
https://github.com/LJGladic/EECS-337-Project-1/blob/master/golden_globes.py
https://github.com/rromo12/EECS-337-Golden-Globes-Team
https://github.com/amitadate/EECS-337-NLP-Project-01
https://github.com/zuzivian/nlp-golden-globes