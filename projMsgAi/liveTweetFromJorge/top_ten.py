import sys
import string
import json
import operator


def alphabetize(input_string):  
    alphabetic_character_list = []
    for character in input_string:
        if ( character.isalpha() ):
            alphabetic_character_list.append(character)
    alphabetic_string = ''.join(alphabetic_character_list)
    return alphabetic_string

def main():
    tweet_file = open(sys.argv[1])
    
    frequencies = {}
    for tweet in tweet_file:
        tweet_dict = json.loads(tweet)
        if 'entities' in tweet_dict:
          tweet_entities = tweet_dict['entities']
          #print tweet_entities
          if 'hashtags' in tweet_entities:
              tweet_hashtags = tweet_entities['hashtags'] 
              #print tweet_hashtags
              if tweet_hashtags is None:
                  continue
              hashtags = []
              for hashtagdict in tweet_hashtags:
                 hashtags.append(hashtagdict['text']) 
                  
              if len(hashtags) == 0:
                  continue

              #print hashtags
              for hashtag in hashtags:
                  alphabetic_hashtag = alphabetize(hashtag)

                  if len(alphabetic_hashtag) == 0:
                      continue

                  if alphabetic_hashtag not in frequencies:
                      frequencies[alphabetic_hashtag] = 1
                  else:
                      frequencies[alphabetic_hashtag] += 1


    sorted_hashtags = sorted(frequencies.iteritems(), key=operator.itemgetter(1),reverse=True)

    for i in range(10):
        hashtag = sorted_hashtags[i]
        print hashtag[0], ' ',  hashtag[1] 
    
    return


if __name__ == '__main__':
    main()
