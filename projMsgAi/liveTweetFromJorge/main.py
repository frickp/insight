import parse_tweets
import twitterstream
import map_dict
import matplotlib.pyplot as plt
import time
import ftplib


def main():

    state_happiness_cumulative = {}
    

    fetching_time = 10 # secs

    time0 = time.time()

    run = True
    

    while run:
        
	while True:
            try: 
                twitterstream.fetchsamples(fetching_time)
	    except:
		continue
	    else:
		break
  	    
        state_happiness =  parse_tweets.parse_tweets()
                
        for state in state_happiness:
            if state not in state_happiness_cumulative:
                state_happiness_cumulative[state] = state_happiness[state]
            else:
                state_happiness_cumulative[state] += state_happiness[state]

        map_dict.map_dict('map1.png',state_happiness)
        map_dict.map_dict('map2.png',state_happiness_cumulative)

        session = ftplib.FTP('ftp.jorgeabernatem.com','jbernate@jorgeabernatem.com','EH@jab&41982')
        filetosend = open('map1.png','rb')                    # file to send
        session.storbinary('STOR map1.png',filetosend)      # send the file
        filetosend.close() 

        filetosend = open('map2.png','rb')                    # file to send
        session.storbinary('STOR map2.png',filetosend)      # send the file
        filetosend.close()
        session.quit()

    

if __name__ == '__main__':
    main()
