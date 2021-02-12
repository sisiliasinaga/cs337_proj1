'''Version 0.35'''

import json
import nltk
import re
from nltk.corpus import stopwords
from textblob import TextBlob
import string

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    with open('gg' + str(year) + '.json') as f:
        data = json.load(f)
    bigrams = []
    stop_words = set(stopwords.words('english'))
    stop_words.add("goldenglobes")

    host_exp = re.compile('(host(s|ed|ing))')

    for tweet in data:
        tweet_text_words = tweet['text']
        tweet_match = re.search(host_exp, tweet_text_words)
        if tweet_match is not None:
            curr_bigrams = nltk.bigrams(w.lower() for w in re.findall(r"[A-Z]+[a-z]+\b", tweet_text_words) if w.lower() not in stop_words)
            for b in curr_bigrams:
                bigrams.append(b)

    most_freq = nltk.FreqDist(bigrams).most_common(2)
    host1 = list(most_freq[0][0])
    host2 = list(most_freq[1][0])
    hosts = [host1[0] + " " + host1[1], host2[0] + " " + host2[1]]
    print(hosts)

    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    with open('gg' + str(year) + '.json') as f:
        data = json.load(f)

    stop_words = set(stopwords.words('english'))
    stop_words.add("goldenglobes")
    stop_words.add("golden")
    stop_words.add("globes")
    stop_words.remove("of")

    presenters = {}
    two_presenter_exp = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+\sand\s[A-Z][a-z]+\s[A-Z][a-z]+(?=\spresent|\sintroduc|\sannounc)')
    one_presenter_exp = re.compile(r'[A-Z][a-z]+\s[A-Z][a-z]+(?:.[A-Z][a-z].)(?=\spresent|\sintroduc|\sannounc)')

    if year == 2013 or year == 2015:
        official_awards = OFFICIAL_AWARDS_1315.copy()
    else:
        official_awards = OFFICIAL_AWARDS_1819.copy()

    award_tokens = []
    for award in official_awards:
        award_no_punct = award
        for char in string.punctuation:
            award_no_punct = award_no_punct.replace(char, " ")
        curr_award_tokens = [x.lower() for x in award_no_punct.split() if x.lower() not in stop_words]
        for token in curr_award_tokens:
            if token not in award_tokens:
                award_tokens.append(token)

    award_stop_words = stop_words.copy()
    for t in award_tokens:
        award_stop_words.add(t)

    for award in official_awards:
        print(award)
        presenters[award] = []
        two_presenters = False
        award_no_punct = award
        for char in string.punctuation:
            award_no_punct = award_no_punct.replace(char, " ")
        award_words = [x.lower() for x in award_no_punct.split() if x.lower() not in stop_words]
        if 'television' in award_words:
            award_words.append('tv')
            award_words.append('show')
        if ('motion' in award_words and 'picture' in award_words) or 'film' in award_words:
            award_words.append('movie')
        if 'mini' in award_words:
            award_words.append('miniseries')
        print(award_words)

        ngrams = []

        for tweet in data:
            tweet_text_words = tweet['text']
            if "RT" in tweet_text_words:
                continue
            for char in string.punctuation:
                tweet_text_words = tweet_text_words.replace(char, "")
            tweet_matches = re.search(two_presenter_exp, tweet_text_words)
            if tweet_matches is not None:
                new_tweet_matches = re.search(one_presenter_exp, tweet_text_words)
                if new_tweet_matches is not None:
                    two_presenters = True
            else:
                new_tweet_matches = tweet_matches
            if new_tweet_matches is not None:
                tweet_tokens = [t.lower() for t in tweet_text_words.split() if t.lower() not in stop_words]

                common = [value for value in award_words if value in tweet_tokens]
                percent = float(len(common) / (len(award_words) - 1))

                if percent >= 0.5:
                    curr_bigrams = nltk.bigrams(
                        w for w in re.findall(r"[A-Z]+[a-z]+\b", tweet_text_words) if w.lower() not in award_stop_words)
                    for b in curr_bigrams:
                        ngrams.append(b)
                    curr_trigrams = nltk.trigrams(w for w in re.findall(r"[A-Z]+[a-z]+\b", tweet_text_words) if w.lower() not in award_stop_words)
                    for t in curr_trigrams:
                        ngrams.append(t)

        most_freq = nltk.FreqDist(ngrams).most_common(10)
        print(len(most_freq))
        if len(most_freq) == 1 or two_presenters is False:
            presenter = list(most_freq[0][0])
            print(presenter)
            presenters[award].append(presenter[0] + " " + presenter[1])
        elif len(most_freq) > 1:
            presenter1 = list(most_freq[0][0])
            presenter2 = list(most_freq[1][0])
            print(presenter1)
            next_pres = 2
            while (presenter2[0] in presenter1 or presenter2[1] in presenter1) and next_pres < len(most_freq):
                presenter2 = list(most_freq[next_pres][0])
                next_pres += 1
            print(presenter2)

            presenters[award].append(presenter1[0] + " " + presenter1[1])
            presenters[award].append(presenter2[0] + " " + presenter2[1])

    return presenters

def get_sentiments(year):
    with open('gg' + str(year) + '.json') as f:
        data = json.load(f)
    for tweet in data:
        tweet_text = tweet['text'].lower()
        blob = TextBlob(tweet_text)
        tweet_sentiment = blob.sentences[0].sentiment.polarity

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    return

if __name__ == '__main__':
    get_presenters(2013)
