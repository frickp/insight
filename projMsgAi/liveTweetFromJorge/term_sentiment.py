import sys
import string
import pprint
import json



def lines(fp):
    print str(len(fp.readlines()))

def alphabetize(input_string):  
    alphabetic_character_list = []
    for character in input_string:
        if ( character.isalpha() ):
            alphabetic_character_list.append(character)
    alphabetic_string = ''.join(alphabetic_character_list)
    return alphabetic_string
    
def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    
    #afinnfile = open("afinn-111.txt")
    scores = {} # initialize an empty dictionary
    sentiment_terms = []
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
        sentiment_terms.append(term)

    derived_sentiment_terms = {};
    derived_sentiment_terms_counts = {}
    for tweet in tweet_file:
        tweet_score = 0
        tweet_dict =  json.loads(tweet)
        if 'text' in tweet_dict:
            tweet_text = tweet_dict['text']

            tokenized_tweet = tweet_text.split()

            alphabetic_tweet_terms = []
            for tweet_token in tokenized_tweet:
                alphabetic_tweet_term = alphabetize(tweet_token)
                alphabetic_tweet_terms.append(alphabetic_tweet_term)

            sentiment_terms_in_tweet = {}
            for index, term in enumerate(alphabetic_tweet_terms):
                if term in scores:
                    sentiment_terms_in_tweet[term] = index

            for index, alphabetic_tweet_term in enumerate(alphabetic_tweet_terms):
                scored = False
                alphabetic_tweet_term = alphabetic_tweet_term.encode('ascii', 'ignore')

                if alphabetic_tweet_term is None:
                    continue
                if len(alphabetic_tweet_term) == 0:
                    continue
                
                for sentiment_term in sentiment_terms:
                    if alphabetic_tweet_term == sentiment_term:
                        scored = True
                        continue
                    if alphabetic_tweet_term in sentiment_term:
                        if 'dis'+alphabetic_tweet_term == sentiment_term:
                            term_score = -scores[sentiment_term]
                            scored = True
                            if alphabetic_tweet_term not in derived_sentiment_terms:
                                derived_sentiment_terms[alphabetic_tweet_term] = term_score
                                derived_sentiment_terms_counts[alphabetic_tweet_term] = 1
                            else:
                                derived_sentiment_terms[alphabetic_tweet_term] += term_score
                                derived_sentiment_terms_counts[alphabetic_tweet_term] += 1
                            break
                        else:   
                            term_score = scores[sentiment_term]
                            scored = True
                            #print alphabetic_tweet_term, ' ', term_score
                            if alphabetic_tweet_term not in derived_sentiment_terms:
                                derived_sentiment_terms[alphabetic_tweet_term] = term_score
                                derived_sentiment_terms_counts[alphabetic_tweet_term] = 1
                            else:
                                derived_sentiment_terms[alphabetic_tweet_term] += term_score
                                derived_sentiment_terms_counts[alphabetic_tweet_term] += 1
                            break
                if scored == True:
                    continue
                if len(sentiment_terms_in_tweet) == 0:
                    term_score = 0
                    #print alphabetic_tweet_term, ' ', term_score
                    if alphabetic_tweet_term not in derived_sentiment_terms:
                        derived_sentiment_terms[alphabetic_tweet_term] = term_score
                        derived_sentiment_terms_counts[alphabetic_tweet_term] = 1
                    else:
                        derived_sentiment_terms[alphabetic_tweet_term] += term_score
                        derived_sentiment_terms_counts[alphabetic_tweet_term] += 1
                    continue
                else:
                   term_score = 0
                   for sentiment_term in sentiment_terms_in_tweet:
                       term_score += 1.0/abs(index-sentiment_terms_in_tweet[sentiment_term])*scores[sentiment_term]
                       if alphabetic_tweet_term not in derived_sentiment_terms:
                           derived_sentiment_terms[alphabetic_tweet_term] = term_score
                           derived_sentiment_terms_counts[alphabetic_tweet_term] = 1
                       else:
                           derived_sentiment_terms[alphabetic_tweet_term] += term_score
                           derived_sentiment_terms_counts[alphabetic_tweet_term] += 1
                       #print term.encode('ascii','ignore'), ' ', term_score

    for term in derived_sentiment_terms:
        derived_sentiment_terms[term] /= derived_sentiment_terms_counts[term]

    for term in derived_sentiment_terms:
        print term, ' ' , derived_sentiment_terms[term]



if __name__ == '__main__':
    main()
