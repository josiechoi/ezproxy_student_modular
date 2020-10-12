
import pandas as pd
import csv
import re
from urllib.parse import unquote

Class log_transform:

# MODIFED FROM CODE BY Petrina Collingwood
#Because the script is to process csv file, so the log files need to be transform into csv files.
####Maybe what I could do later is to eliminate the csv files when the process is done. ####

# create csv file from log file

    def __init__(self,filename):
        self.filename = filename
            with open(filename,'r') as fh:
                with open('csv/' + filename + '.csv','w') as outfile:
                    for line in fh:
            print(re.sub(r'\n|"','',line), file=outfile)
    # create dataframe from csv file skipping malformed lines
            df = pd.read_csv('csv/' + filename + '.csv',sep=' ', error_bad_lines=False, header=None, encoding='utf-8')
            value=['2,5,6,8,9']
            prefix='http://ezproxy.lib.ryerson.ca/login?url='
            #drop columns not needed
            df.drop(df.columns[value], axis=1, inplace=True)
            # name columns
            df.columns = ['ip', 'session_id', 'user_id', 'date_time', 'url', 'size']
            df['date_time'] = df['date_time'].map(lambda x: x.lstrip('['))
            df['date_time'] = pd.to_datetime(df['date_time'], format='%d/%b/%Y:%H:%M:%S')
        #remove blank user_id
            df = df[df.user_id != "-"]
        #add this so escape . in ezproxy prefix, which is fairly common
            prefix=prefix.replace('.','\.')
            df['url'] = df.url.apply(_decode_url)
            df['url'] = df.url.apply(_parse_url)
            df = df[df.url != \"-\"]
            df['url']=df.url.apply(_clean_url)
            df = df[df.url != \"-\"]
            #it maybe a good idea to create a child class, that would keep the ip, maybe to do something geospatial related?
            df['domain'] = df.url.apply(get_domain)
            # remove duplicate rows which have same user_id, date-time and domain. \n",
            df.drop(['ip','session_id','size'], axis=1, inplace=True)
            df.drop_duplicates(subset=['date_time','domain'], inplace=True)
            df.to_csv('student_count.csv',index=False, encoding='utf-8')

#Let's not do this for now... although this is a good idea ... However, I think by creating a separate field for values, and prefix, it should be easy enough to manipulate

    def  log_input(value="[2,5,6,8,9]",prefix="http://ezproxy.lib.ryerson.ca/login?url="):
# MODIFED FROM CODE BY Petrina Collingwood
#Goal is to remove necessary columns, but with user input
        print("This program is designed to analyze ezproxy log and will take in 6 inputs. As for the other fields, these will be eliminated")
        print("Take a look at a sample log file. Please identify the fields number that need to be eliminated. Put this into double square bracket which will appear shortly.")
        print("Note that Python is a 0-based language, so the first column = 0, the second column = 1")
        print("by default, we will eliminate columns [2,5,6,8,9], based on Ryerson's log file")
        value = input("Please enter columns number:\n")
        print(f'You entered {value}')
# remove lines where user is not logged in
        print("please enter your ezproxy prefix. By default, we use Ryerson\'s prefix, which is 'http://ezproxy.lib.ryerson.ca/login?url='")
        print('enter the prefix here {prefix}')
        prefix = input("Please enter prefix in quotation mark:\n")

# turn this into a non-public function
    def _decode_url(self):
# MODIFIED FROM Code By Petrina Collingwood
        decoded_url = unquote(self)
        return decoded_url
            # I feel like we need another function right here
            # remove ezp string from start of url

# remove excess columns for domain (since we are not really using ip right now, although this could be useful in the future for geospatial analysis)

#also turn this into non-public function
    def _parse_url(url):
        if (url.startswith(\prefix)) and (\"http\" in url):
            location = url.find(\"http\")
           return url[location:]
       elif (url.startswith(\prefix)):
            return \"-\"
        else:
            return url

        def _clean_url(url):
            url.replace(prefix, '')# remove http etc
            url.str.replace(r'^http://www\.|^https://www\.|^http://|^https://', '')
                # remove spaces introduced by unquoting
            url.str.replace(r'\\n', '')
                # remove everything after : or / or ?
            url.str.replace(r'[:/?].*$', '')
                # remove .ezp.lib.unimelb.edu.au from urls
            url.str.replace(r'ezproxy\\.lib\\.ryerson\\.ca', '')
            url.str.replace(r'ezproxy\\.lib\\.', '-')

    # create new column of domains

    def get_domain(url):
        regexp = re.compile(r'\\.com|\\.org|\\.net|\\.edu|-org|-com|\\.gov')
        if regexp.search(url) is not None:
            for match in regexp.finditer(url):
                location = match.start()
            new_url = url[:location]
           if ('.' in new_url):
                location = new_url.rfind('.')
            elif ('-' in new_url):
                location = new_url.rfind('-')
            else:
                return url
            location += 1
            if (\"-org\" in url[location:]):
                modified_url = url[location:].replace(r'-org', '.org')
            elif (\"-com\" in url[location:]):
                modified_url = url[location:].replace(r'-com', '.com')
            else:
                return url[location:]
            return modified_url
        else:
            return url
