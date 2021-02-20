'''Version 0.35'''

import json
import nltk
import re
from nltk.corpus import stopwords
import string
from imdb import IMDb
from difflib import SequenceMatcher
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    with open('gg' + year + '.json') as f:
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
    #print(hosts)

    return hosts

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def removePunctuation(line):
    symbols = "!#$%&()*+,-./:;<=>?@[\]^_`{'~}"
    symbols += '"1234567890'
    for s in symbols:
        line = line.replace(s, '')
    return line

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    with open('gg' + str(year) + '.json') as f:
        data = json.load(f)
    stop_words = set(stopwords.words('english')
)

    stop_words.add("goldenglobes")
    award_words = ['-', 'performance', 'actress', 'actor', 'supporting', 'role', 'director', 'motion', 'picture',
                   'drama', 'animated', 'feature', 'film', 'song', 'comedy', 'musical', 'language', 'foreign',
                   'screenplay', 'original', 'television', 'tv', 'series', 'mini-series', 'mini']
    result = {}
    for tweet in data:
        tweet_text = tweet['text'].lower().split()
        if "best" in tweet_text:
            for word in award_words:
                if word in tweet_text:
                    best_index = tweet_text.index("best")
                    word_index = tweet_text.index(word)
                    if best_index < word_index:
                        award_txt = tweet_text[best_index:word_index+1]

                        if '-' in award_txt:
                            if len(award_txt) >= 4:
                                key = " ".join(i for i in award_txt)
                                if key not in result:
                                    result[key] = 1
                                else:
                                    result[key] += 1
    res = []
    temp = sorted(result.items())
    for x in temp:
        length = len(removePunctuation(x[0]).split())
        if length <= 3:
            continue
        s = x[0].replace('tv', 'television')
        if 'comedy' in s and 'musical' not in s:
            res.append(s.replace('comedy', 'comedy or musical'))
        elif 'musical' in s and 'comedy' not in s:
            res.append(s.replace('musical', 'comedy or musical'))
        else:
            res.append(s)

    awards = [i for i in res if i in OFFICIAL_AWARDS_1315 or i in OFFICIAL_AWARDS_1819]

    # print(awards)

    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    ia = IMDb()

    stop_words = set(stopwords.words('english'))
    stop_words.add("golden")
    stop_words.add("globe")
    stop_words.add("globes")
    stop_words.add("goldenglobes")
    stop_words.add("goldenglobe")
    stop_words.add("video")
    stop_words.add("present")
    stop_words.add("goes")
    stop_words.add("http")

    winners = get_winner(year)

    nominee_words = ['best', 'award', 'nominee', 'nominees', 'nominating', 'nominate', 'nominated', 'nominates']

    nominee_stop_words = ['year', 'next', 'made', 'performance', 'role', 'miniseries',
                          'video', 'present', 'wins', 'win', 'winner', 'winning', 'yes', 'goes', 'http',
                          'actress', 'actor', 'award', 'takes', 'congratulations', 'yep', 'rt', 'yay', 'series', 'mini',
                          'miniseries', 'picture', 'live', 'motion', 'b', 'presenting', 'co', 'mtvnews', 'hollywood', 'ever',
                          'cool', 'years', 'film', 'along', 'excellent', 'job', 'w', 'funny', 'day', 'celebrates']

    nominees_tweets = []

    if year is "2013" or year is "2015":
        official_awards = OFFICIAL_AWARDS_1315
    else:
        official_awards = OFFICIAL_AWARDS_1819

    nominees = {}

    with open('gg' + str(year) + '.json') as f:
        data = json.load(f)
        data = random.sample(data, 50000)

    for award in official_awards:
        nominees[award] = []

    #find all tweets that have nominee words
    for tweet in data:
        tweet_text_words = tweet['text']
        if tweet_text_words[:2] == "RT":
            continue
        for char in string.punctuation:
            tweet_text_words = tweet_text_words.replace(char, " ")
            tweet_text_words = tweet_text_words.lower()

        tweet_words = [t.lower() for t in tweet_text_words.split() if t.lower() not in stop_words]

        for word in nominee_words:
            if word in tweet_words:
                nominees_tweets.append(tweet_words)


    for award in official_awards:
        winner = winners[award]
        award_no_punct = award
        for ch in string.punctuation:
            award_no_punct = award.replace(ch, "")
        award_tokens = [t.lower() for t in award_no_punct.split() if t.lower() not in stop_words]
        if 'television' in award_tokens:
            award_tokens.append('tv')

        if 'tv' in award_tokens:
            if 'motion' in award_tokens:
                award_tokens.remove('motion')
            if 'picture' in award_tokens:
                award_tokens.remove('picture')
        possible_nominees = {}
        human_name = False
        bgms = []
        winner_tokens = [t.lower() for t in winner.split()]
        if 'actor' in award_tokens or 'actress' in award_tokens or "director" in award_tokens or "cecil" in award_tokens:
            human_name = True

        for tweet_tokens in nominees_tweets:
            combined_tokens = [value for value in award_tokens if value in tweet_tokens]
            percent = float(len(combined_tokens) / len(award_tokens))

            if percent > .6:
                nominee_name = [word for word in tweet_tokens if word not in award_tokens and word not in nominee_stop_words]
                if human_name:
                    bgms.extend(nltk.bigrams(nominee_name))
                else:
                    nominee_name = " ".join(nominee_name)
                    if nominee_name not in possible_nominees:
                        possible_nominees[nominee_name] = 1
                    else:
                        possible_nominees[nominee_name] += 1
        if human_name:
            freq = nltk.FreqDist(bgms)
            top_4 = []
            sorted_bigrams = (sorted(freq, key=freq.get, reverse=True))
            x = 1
            while len(top_4) != 4:
                if x >= len(sorted_bigrams):
                    break
                already_done = False
                for t in sorted_bigrams[x]:
                    if (t in winner_tokens):
                        already_done = True

                if already_done == True:
                    x += 1
                    continue
                else:
                    name = " ".join(sorted_bigrams[x])
                    try:
                        person = ia.search_person(name)
                        new_name = person[0]['name']
                        new_name = new_name.lower()
                        if similar(name, new_name) > 0.6:
                            top_4.append(name)
                            x += 1
                        else:
                            x += 1
                    except:
                        x += 1
                        continue
            nominees[award] = top_4
        else:
            top_4 = []
            x = 1
            possible_noms = sorted(possible_nominees, key=possible_nominees.get, reverse=True)
            while len(top_4) != 4:
                if x >= len(possible_noms):
                    break
                already_done = False
                nom_tokens = possible_noms[x].split()
                for t in nom_tokens:
                    if (t in winner_tokens):
                        already_done = True
                if already_done == True:
                    x += 1
                    continue
                else:
                    name = possible_noms[x]
                    try:
                        movie = ia.search_movie(name)
                        new_name = movie[0]['title']
                        new_name = new_name.lower()
                        if similar(new_name, name) > 0.6:
                            top_4.append(name)
                            x += 1
                        else:
                            x += 1
                    except:
                        x += 1
                        continue
            nominees[award] = top_4
            # nominees[award] = sorted(possible_nominees, key=possible_nominees.get, reverse=True)[:4]

    # print(nominees)

    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    winners = dict()
    stop_words = set(stopwords.words('english'))
    stop_words.add("goldenglobes")
    stop_words.add("golden")
    stop_words.add("globes")
    stop_words.remove("of")

    winner_stop_words = ["actor", "actress", "comedy", "musical", "score", "goldenglobes", "“ontheredcarpet"]

    with open('gg' + str(year) + '.json') as f:
        data = json.load(f)
        data = random.sample(data, 50000)

    if year is "2013" or year is "2015":
        official_awards = OFFICIAL_AWARDS_1315
    else:
        official_awards = OFFICIAL_AWARDS_1819

    for award in official_awards:
        winners[award] = ''

    for award in official_awards:
        award_no_punct = award
        for char in string.punctuation:
            award_no_punct = award_no_punct.replace(char, " ")
        award_words = [x.lower() for x in award_no_punct.split() if x.lower() not in stop_words]
        if 'television' in award_words:
            award_words.append('tv')

        person = False
        if 'actor' in award_words or 'actress' in award_words or 'cecil' in award_words:
            person = True

        bigrams = []
        possible_winners = {}
        # check to see if tweet has words in award name
        # remove award words and stop words
        for tweet in data:
            tweet_text_words = tweet['text']

            if tweet_text_words[:2] == "RT":
                continue

            for char in string.punctuation:
                tweet_text_words = tweet_text_words.replace(char, "")
            tweet_tokens = [t.lower() for t in tweet_text_words.split() if t.lower() not in stop_words]

            common = [value for value in award_words if value in tweet_tokens]
            percent = float(len(common) / len(award_words))

            if percent >= .8:
                winner_name = [word for word in tweet_tokens if
                               word not in award_words and word not in winner_stop_words]
                for x in winners.values():
                    for y in x.split():
                        if y in winner_name:
                            winner_name.remove(y)
                if person:
                    bigrams.extend(nltk.bigrams(winner_name))
                else:
                    winner_name = " ".join(winner_name)
                    if winner_name not in possible_winners:
                        possible_winners[winner_name] = 1
                    else:
                        possible_winners[winner_name] += 1
        if person:
            try:
                freq = nltk.FreqDist(bigrams)
                winners[award] = " ".join(sorted(freq, key=freq.get, reverse=True)[:1][0])
            except:
                winners[award] = "could not find"

        else:
            try:
                if sorted(possible_winners, key=possible_winners.get, reverse=True)[0]:
                    winners[award] = sorted(possible_winners, key=possible_winners.get, reverse=True)[0]
            except:
                winners[award] = "could not find"
    # find tweets that contain certain percentage of award name,
    # remove stop words and award words,

    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''

    ia = IMDb()

    with open('gg' + year + '.json') as f:
        data = json.load(f)
        data = random.sample(data, 50000)

    stop_words = set(stopwords.words('english'))
    stop_words.add("goldenglobes")
    stop_words.add("golden")
    stop_words.add("globe")
    stop_words.add("globes")
    stop_words.add("awards")
    stop_words.add("los")
    stop_words.add("angeles")
    stop_words.remove("of")

    presenters = {}
    presenter_tweets = []
    present_exp = re.compile(r'(\spresent|\sannounc|\sintroduc)')

    if year is "2013" or year is "2015":
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
    # print(award_tokens)

    award_stop_words = stop_words.copy()
    for t in award_tokens:
        award_stop_words.add(t)

    for tweet in data:
        tweet_text_words = tweet['text']
        if "RT" in tweet_text_words:
            continue
        for char in string.punctuation:
            if char != '-':
                tweet_text_words = tweet_text_words.replace(char, "")

        tweet_matches = re.search(present_exp, tweet_text_words)
        if tweet_matches is not None:
            presenter_tweets.append(tweet_text_words)

    for award in official_awards:
        # print(award)
        presenters[award] = []
        award_no_punct = award
        for char in string.punctuation:
            award_no_punct = award_no_punct.replace(char, " ")
        award_words = [x.lower() for x in award_no_punct.split() if x.lower() not in stop_words]
        if 'television' in award_words:
            award_words.remove('television')
            award_words.append('tv')
            award_words.append('show')
        if 'motion' in award_words and 'picture' in award_words:
            award_words.append('movie')
            # award_words.remove('motion')
            # award_words.remove('picture')
        if 'mini' in award_words:
            award_words.append('miniseries')
            award_words.append('mini-series')
        if 'performance' in award_words:
            award_words.remove('performance')
        if 'role' in award_words:
            award_words.remove('role')
        # print(award_words)

        ngrams = []

        for p_tweet in presenter_tweets:
            tweet_tokens = [t.lower() for t in p_tweet.split() if t.lower() not in stop_words]

            common = [value for value in award_words if value in tweet_tokens]
            percent = float(len(common) / len(award_words))

            if percent >= 0.5:
                curr_bigrams = nltk.bigrams(
                    w for w in re.findall(r"[A-Z]+[a-z]+\b", p_tweet) if w.lower() not in award_stop_words)
                for b in curr_bigrams:
                    ngrams.append(b)

        most_freq = nltk.FreqDist(ngrams).most_common(10)
        # print(most_freq)
        if len(most_freq) == 1:
            presenter = list(most_freq[0][0])
            # print(presenter)
            presenters[award].append((presenter[0] + " " + presenter[1]).lower())
        elif len(most_freq) > 1:
            next_pres = 1
            presenter1 = list(most_freq[0][0])
            # print(presenter1)
            presenter1_results = ia.search_person(presenter1[0] + " " + presenter1[1])
            # print(presenter1_results)
            while not presenter1_results or similar(presenter1[0] + " " + presenter1[1], presenter1_results[0]['name']) < 0.5:
                presenter1 = list(most_freq[next_pres][0])
                # print(presenter1)
                presenter1_results = ia.search_person(presenter1[0] + " " + presenter1[1])
                next_pres += 1

            if next_pres < len(most_freq):
                presenter2 = list(most_freq[next_pres][0])
                presenter2_results = ia.search_person(presenter2[0] + " " + presenter2[1])
                # print(presenter2)
                # print(presenter2_results)
                while (not presenter2_results or similar(presenter2[0] + " " + presenter2[1], presenter2_results[0]['name']) < 0.5) and \
                        next_pres < len(most_freq):
                    presenter2 = list(most_freq[next_pres][0])
                    presenter2_results = ia.search_person(presenter2[0] + " " + presenter2[1])
                    next_pres += 1

                if not presenter1_results:
                    presenters[award].append((presenter1[0] + " " + presenter1[1]).lower())
                else:
                    presenters[award].append(presenter1_results[0]['name'].lower())

                if not presenter2_results:
                    presenters[award].append((presenter2[0] + " " + presenter2[1]).lower())
                else:
                    presenters[award].append(presenter2_results[0]['name'].lower())

            else:
                if not presenter1_results:
                    presenters[award].append((presenter1[0] + " " + presenter1[1]).lower())
                else:
                    presenters[award].append(presenter1_results[0]['name'].lower())

            # print(presenter1_results[0]['name'])
            # print(presenter2_results[0]['name'])

    # print(presenters)
    return presenters

def get_sentiments(year):

    stop_words = set(stopwords.words('english'))
    stop_words.add("goldenglobes")
    stop_words.add("golden")
    stop_words.add("globes")
    stop_words.add("globe")

    red_carpet_tweets = []

    analyzer = SentimentIntensityAnalyzer()
    ia = IMDb()
    bigrams = []
    names = dict()

    with open('gg' + year + '.json') as f:
        data = json.load(f)
        data = random.sample(data, 50000)

    for tweet in data:
        tweet_text = tweet['text'].lower()
        if tweet_text[:2] == "RT":
            continue
        tweet_text_words = [t.lower() for t in tweet_text.split() if t.lower() not in stop_words]
        if "red" in tweet_text_words and "carpet" in tweet_text_words:
            red_carpet_tweets.append(tweet_text)

    for tweet in red_carpet_tweets:
        tokens = tweet.split(" ")
        try:
            tokens.remove("red")
            tokens.remove("carpet")
        except:
            pass

        bigrams.extend(nltk.bigrams(tokens))
    freq = nltk.FreqDist(bigrams)
    for bigram in sorted(freq, key=freq.get, reverse=True)[: 100]:
        person = " ".join(bigram)
        if ia.search_person(person):
            if ia.search_person(person)[0]['name'].lower() == person.lower():
                names[person] = 0

    for tweet in red_carpet_tweets:
        tokens = tweet.split(" ")
        text = " ".join(tokens)
        for n in names:
            if n in text:
                sentiment = analyzer.polarity_scores(text)
                names[n] += sentiment['compound']
    best = sorted(names, key=names.get, reverse=True)[:5]
    # print(best)
    return best

def get_worst_dressed(year):
    ia = IMDb()
    worstdressed_tweets = []
    bigrams = []
    names = dict()
    stop_words = set(stopwords.words('english'))
    stop_words.add("goldenglobes")
    stop_words.add("golden")
    stop_words.add("globes")
    stop_words.add("globe")
    stop_words.add("hollywood")
    worstdressed_keywords = ["gross", "worst attire", "bad attire", "gross shoes", "bad shoes", "gross hair", "gross outfit", "bad outfit",
                             "bad fashion", "weird hair", "worst outfit", "bad hair", "worst dressed"]

    with open('gg' + year + '.json') as f:
        data = json.load(f)
        data = random.sample(data, 50000)

    for tweet in data:
        tweet_text = tweet['text'].lower()
        if tweet_text[:2] == "RT":
            continue
        tweet_text_words = [t.lower() for t in tweet_text.split() if t.lower() not in stop_words]
        if any(w in tweet_text for w in worstdressed_keywords):
            worstdressed_tweets.append(tweet_text_words)

    for tweet in worstdressed_tweets:
        for word in worstdressed_keywords:
            try:
                tweet.remove(word)
            except:
                pass

        bigrams.extend(nltk.bigrams(tweet))

    freq = nltk.FreqDist(bigrams)
    for bigram in sorted(freq, key=freq.get, reverse=True)[: 100]:
        person = " ".join(bigram)
        if ia.search_person(person):
            if ia.search_person(person)[0]['name'].lower() == person.lower():
                names[person] = 0

    worst = sorted(names, key=names.get, reverse=True)[:15]
    # print(worst)
    return worst

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
    hosts_2013 = get_hosts("2013")
    hosts_2015 = get_hosts("2015")

    awards_2013 = get_awards("2013")
    awards_2015 = get_awards("2015")

    nominees_2013 = get_nominees("2013")
    nominees_2015 = get_nominees("2015")

    winners_2013 = get_winner("2013")
    winners_2015 = get_winner("2015")

    presenters_2013 = get_presenters("2013")
    presenters_2015 = get_presenters("2015")

    best_dressed_2013 = get_sentiments("2013")
    best_dressed_2015 = get_sentiments("2015")

    worst_dressed_2013 = get_sentiments("2013")
    worst_dressed_2015 = get_sentiments("2015")

    json_2013 = {}
    json_2015 = {}

    print("Year: 2013\n")

    print("Hosts:", *hosts_2013, sep=", ")
    json_2013["Host"] = hosts_2013

    for award in OFFICIAL_AWARDS_1315:
        print("Award:", award)
        print("Presenters:", *presenters_2013[award], sep=", ")
        print("Nominees:", *nominees_2013[award], sep=", ")
        print("Winner:", winners_2013[award])
        print("\n")

        json_2013[award] = {}
        json_2013[award]["Presenters"] = presenters_2013[award]
        json_2013[award]["Nominees"] = nominees_2013[award]
        json_2013[award]["Winner"] = winners_2013[award]

    print("Best Dressed:", *best_dressed_2013, sep=", ")
    print("Worst Dressed:", *worst_dressed_2013, sep=", ")

    print("Year: 2015\n")

    print("Hosts:", *hosts_2015, sep=", ")
    json_2015["Host"] = hosts_2015

    for award in OFFICIAL_AWARDS_1315:
        print("Award:", award)
        print("Presenters:", *presenters_2015[award], sep=", ")
        print("Nominees:", *nominees_2015[award], sep=", ")
        print("Winner:", winners_2015[award])
        print("\n")

        json_2015[award] = {}
        json_2015[award]["Presenters"] = presenters_2015[award]
        json_2015[award]["Nominees"] = nominees_2015[award]
        json_2015[award]["Winner"] = winners_2015[award]

    print("Best Dressed:", *best_dressed_2015, sep=", ")
    print("Worst Dressed:", *worst_dressed_2015, sep=", ")

    predictions_2013 = open("pred2013.json", "w")
    predictions_2015 = open("pred2015.json", "w")

    json.dump(json_2013, predictions_2013)
    json.dump(json_2015, predictions_2015)

    predictions_2013.close()
    predictions_2015.close()

    return

if __name__ == '__main__':
    main()
