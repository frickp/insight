import sys
import string
import json


def alphabetize(input_string):  
    alphabetic_character_list = []
    for character in input_string:
        if ( character.isalpha() ):
            alphabetic_character_list.append(character)
    alphabetic_string = ''.join(alphabetic_character_list)
    return alphabetic_string

statesAbbreviations = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

statesNames = {}
for abbreviation in statesAbbreviations:
    statesNames[statesAbbreviations[abbreviation]] = abbreviation

def parse_tweets():

    sent_file = open('AFINN-111.txt')
    tweet_file = open('tweets.txt')
    
    scores = {} # initialize an empty dictionary
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = float(score)  # Convert the score to an integer.
    
    states_happiness = {}
    for tweet in tweet_file:
        try:
            tweet_dict = json.loads(tweet)
	except ValueError:
	    continue

        states_abbreviations = [] 
        states_abbreviations_from_place = []
        states_names_from_place = []
        states_abbreviations_from_location = []
        states_names_from_location = []

        state = ''
        tweet_score = 0.0
        if 'text' in tweet_dict:
            if 'place' and 'user' not in tweet_dict:
                continue

            #print tweet_dict 
            if 'place' in tweet_dict:
                place = tweet_dict['place']
                #if place is not None:
                if place:
                    name = place['name']
                    #if name is not None:
                    if name:
                        tokenized_name = name.split()
                        states_abbreviations_from_place = []
                        states_names_from_place = []
                        for name_token in tokenized_name:
                            alphabetic_name_token = alphabetize(name_token)
                            if alphabetic_name_token in statesAbbreviations:
                                states_abbreviations_from_place.append(alphabetic_name_token)
                            if alphabetic_name_token in statesNames:
                                states_names_from_place.append(alphabetic_name_token)
                        #if len(states_names_from_place) != 0:
                            #print 'state name from place: ', states_names_from_place
                        #if len(states_abbreviations_from_place) != 0:
                            #print 'state abbreviation from place: ', states_abbreviations_from_place
            

                #if 'name' in tweet_dict['place']:
                #    print tweet_dict['place']['name']

            if 'user' in tweet_dict:
                user = tweet_dict['user']
                #if user is not None:
                if user:
                    location = user['location']
                    #if location is not None:
                    if location:
                        tokenized_location = location.split()
                        states_abbreviations_from_location = []
                        states_names_from_location = []
                        for location_token in tokenized_location:
                            alphabetic_location_token = alphabetize(location_token)
                            if alphabetic_location_token in statesAbbreviations:
                                states_abbreviations_from_location.append(alphabetic_location_token)
                            if alphabetic_location_token in statesNames:
                                states_names_from_location.append(alphabetic_location_token)
                        #if len(states_names_from_location) != 0:                    
                            #print 'state name from location: ', states_names_from_location
                        #if len(states_abbreviations_from_location) != 0:
                            #print 'state abbreviation from location: ', states_abbreviations_from_location
                #if 'location' in tweet_dict['user']:
                #    print tweet_dict['user']['location']
            for state_name in states_names_from_place:
                if state_name in statesNames:
                    states_abbreviations.append(statesNames[state_name])
            for state_name in states_names_from_location:
                if state_name in statesNames:
                    states_abbreviations.append(statesNames[state_name])
            for state_abbreviation in states_abbreviations_from_place:
                if state_abbreviation in statesAbbreviations:
                    states_abbreviations.append(state_abbreviation)
            for state_abbreviation in states_abbreviations_from_location:
                if state_abbreviation in statesAbbreviations:
                    states_abbreviations.append(state_abbreviation)

            #if len(states_abbreviations) != 0:
            if len(states_abbreviations):
                if len(set(states_abbreviations)) == 1: # We have an unambiguous state
                    state = states_abbreviations[0]
            else:
                continue # if ambiguity

            if state == '':
                continue

            # Compute tweet score
            tweet_text = tweet_dict['text']
            tokenized_tweet = tweet_text.split()
            for tweet_token in tokenized_tweet:
                alphabetic_tweet_token = alphabetize(tweet_token)

                if len(alphabetic_tweet_token) == 0:
                    continue

                if alphabetic_tweet_token in scores:
                    tweet_score += scores[alphabetic_tweet_token]

            if state not in states_happiness:
                states_happiness[state] = tweet_score
            else:
                states_happiness[state] += tweet_score
    
    states_happiness_by_state_name = {}
    for state in states_happiness:
        states_happiness_by_state_name[statesAbbreviations[state]] = float(states_happiness[state])
            
    return states_happiness_by_state_name
    
if __name__ == '__main__':
    parse_tweets()
