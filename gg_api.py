'''Version 0.35'''

import json
import nltk
import re
from nltk.corpus import stopwords
from textblob import TextBlob
import string
from imdb import IMDb

ia = IMDb()

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
    #print(hosts)

    return hosts

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
    stop_words = set(stopwords.words('english'))
    stop_words.add("goldenglobes")
    award_words = ['-', 'performance', 'actress', 'actor', 'supporting', 'role', 'director', 'motion', 'picture', 'drama','animated', 'feature', 'film', 'song','comedy', 'musical', 'language', 'foreign','screenplay', 'original', 'television', 'tv', 'series', 'mini-series', 'mini']
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
    awards = []
    temp = sorted(result.items())
    for x in temp:
        length = len(removePunctuation(x[0]).split())
        if length <= 3:
            continue
        s = x[0].replace('tv', 'television')
        if 'comedy' in s and 'musical' not in s:
            awards.append(s.replace('comedy', 'comedy or musical'))
        elif 'musical' in s and 'comedy' not in s:
            awards.append(s.replace('musical', 'comedy or musical'))
        else:
            awards.append(s)
    print(awards)

    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    stop_words = set(stopwords.words('english'))
    stop_words.add("goldenglobes")
    stop_words.add("golden")
    stop_words.add("globes")
    stop_words.remove("of")

    bigrams = []
    nominees = dict()
    nominees_tweets = []
    nominee_words = ['nominee', 'nominees', 'nominating', 'nominate', 'nominated', 'nominates']
    # nominee_words = ['nominee', 'nominees', 'nominate', 'nominates', 'nominated','nominating']

    # generic words that are likely to appear that will not be human names
    final_stopwords = ['Fair', 'Best', 'She', 'He', 'Hooray' 'Supporting', 'Actor', 'Actress', 'The', 'A', 'Life',
                       'Good', 'Not', 'Drinking', 'Eating', 'And', 'Hooray', 'Nshowbiz', 'TMZ', 'VanityFair', 'People',
                       'CNN', 'CBS', 'Magazine', 'Television', 'Mejor', 'Better', 'Score', 'Movie', 'Film', 'Picture',
                       'All', 'This', 'That', 'Anyway', 'However', 'Song', 'Tune', 'Music', 'Drama', 'Comedy', 'So',
                       'Better', 'Netflix', 'Someone', 'Mc', 'Newz', 'Season', 'Should', 'Fashion', 'Has', 'How',
                       'Oscar', 'Grammy', 'Oscars', 'Oscars', 'Drink', 'Because', 'Interesting', 'Although', 'Though',
                       'Yay', 'Congrats']

    winners = get_winner(year)

    if (year == 2013 or year == 2015):
        official_awards = OFFICIAL_AWARDS_1315
    else:
        official_awards = OFFICIAL_AWARDS_1819

    pat = re.compile('.*(hop(ed|ing|e|es))\s(@)?(\w+)\s(w(o|i)(n|ns|nning)).*', re.IGNORECASE)
    with open('gg' + str(year) + '.json') as f:
        data = json.load(f)

    for award in official_awards:
        nominees[award] = []
        award_no_punct = award
        for char in string.punctuation:
            award_no_punct = award_no_punct.replace(char, " ")
        award_words = [x.lower() for x in award_no_punct.split()]
        if 'television' in award_words:
            award_words.append('tv')
        person = False
        if 'actor' in award_words or 'actress' in award_words or 'cecil' in award_words:
            person = True

        bigrams = []
        possible_nominees = {}

        for tweet in data:
            tweet_text_words = tweet['text']
            if tweet_text_words[:2] == "RT":
                continue
            for char in string.punctuation:
                tweet_text_words = tweet_text_words.replace(char, " ")
                tweet_text_words = tweet_text_words.lower()

            tweet_words = tweet_text_words.split(" ")

            for word in nominee_words:
                if word in tweet_words:
                    nominees_tweets.append(tweet_text_words)

                    common = [value for value in award_words if value in tweet_words]
                    percent = float(len(common) / len(award_words))

                    if percent >= .8:
                        nominee_name = [word for word in tweet_words if word not in award_words]
                        if person:
                            bigrams.extend(nltk.bigrams(nominee_name))
                        else:
                            nominee_name = " ".join(nominee_name)
                            if nominee_name not in possible_nominees:
                                possible_nominees[nominee_name] = 1
                            else:
                                possible_nominees[nominee_name] += 1

        if person:
            try:
                freq = nltk.FreqDist(bigrams)
                nominees[award] = " ".join(sorted(freq, key=freq.get, reverse=True)[:1][0])
            except:
                nominees[award] = "could not find"

        else:
            try:
                if sorted(possible_nominees, key=possible_nominees.get, reverse=True)[0]:
                    nominees[award] = sorted(possible_nominees, key=possible_nominees.get, reverse=True)[0]
            except:
                nominees[award] = "could not find"

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

    if (year == 2013 or year == 2015):
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
    with open('gg' + str(year) + '.json') as f:
        data = json.load(f)

    stop_words = set(stopwords.words('english'))
    stop_words.add("goldenglobes")
    stop_words.add("golden")
    stop_words.add("globes")
    stop_words.remove("of")

    presenters = {}
    present_exp = re.compile(r'(\spresent|\sannounc|\sintroduc)')

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
    print(award_tokens)

    award_stop_words = stop_words.copy()
    for t in award_tokens:
        award_stop_words.add(t)

    for award in official_awards:
        print(award)
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
        print(award_words)

        ngrams = []

        for tweet in data:
            tweet_text_words = tweet['text']
            if "RT" in tweet_text_words:
                continue
            for char in string.punctuation:
                if char != '-':
                    tweet_text_words = tweet_text_words.replace(char, "")
            tweet_matches = re.search(present_exp, tweet_text_words)

            if tweet_matches is not None:
                tweet_tokens = [t.lower() for t in tweet_text_words.split() if t.lower() not in stop_words]

                common = [value for value in award_words if value in tweet_tokens]
                percent = float(len(common) / len(award_words))

                # tokens_for_bigrams = [t.lower() for t in tweet_tokens if t.lower() not in award_tokens]

                if percent >= 0.5:
                    curr_bigrams = nltk.bigrams(
                        w for w in re.findall(r"[A-Z]+[a-z]+\b", tweet_text_words) if w.lower() not in award_stop_words)
                    for b in curr_bigrams:
                        ngrams.append(b)
                    '''
                    curr_trigrams = nltk.trigrams(w for w in re.findall(r"[A-Z]+[a-z]+\b", tweet_text_words) if w.lower() not in award_stop_words)
                    for t in curr_trigrams:
                        ngrams.append(t)
                    '''

        most_freq = nltk.FreqDist(ngrams).most_common(10)
        print(most_freq)
        if len(most_freq) == 1:
            presenter = list(most_freq[0][0])
            print(presenter)
            presenters[award].append(presenter[0] + " " + presenter[1])
        elif len(most_freq) > 1:
            next_pres = 0
            presenter1 = list(most_freq[next_pres][0])
            # print(presenter1)
            presenter1_results = ia.search_person(presenter1[0] + " " + presenter1[1])
            # print(presenter1_results)
            while not presenter1_results or presenter1[0] != presenter1_results[0]['name'].split()[0]:
                next_pres += 1
                presenter1 = list(most_freq[next_pres][0])
                # print(presenter1)
                presenter1_results = ia.search_person(presenter1[0] + " " + presenter1[1])

            presenter2 = list(most_freq[next_pres+1][0])
            presenter2_results = ia.search_person(presenter2[0] + " " + presenter2[1])
            while (not presenter2_results or presenter2[0] != presenter2_results[0]['name'].split()[0]) and \
                    next_pres < len(most_freq):
                presenter2 = list(most_freq[next_pres+1][0])
                presenter2_results = ia.search_person(presenter2[0] + " " + presenter2[1])
                next_pres += 1
            # print(ia.search_person(presenter2))

            presenters[award].append(presenter1_results[0]['name'])
            presenters[award].append(presenter2_results[0]['name'])

            print(presenter1_results[0]['name'])
            print(presenter2_results[0]['name'])

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
