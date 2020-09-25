def log_transform(filename):

# MODIFED FROM CODE BY Petrina Collingwood  

#Because the script is to process csv file, so the log files need to be transform into csv files. 
####Maybe what I could do later is to eliminate the csv files when the process is done. ####
    
    import csv
    
    # create csv file from log file
    with open(filename,'r') as fh:
        with open('csv/' + filename + '.csv','w') as outfile:
            for line in fh:
                print(re.sub(r'\n|"','',line), file=outfile)
    import pandas as pd
    # create dataframe from csv file skipping malformed lines
    df = pd.read_csv('csv/' + filename + '.csv',sep=' ', error_bad_lines=False, header=None, encoding='utf-8')
    
def log_input(value="[2,5,6,8,9]",prefix="http://ezproxy.lib.ryerson.ca/login?url="):
    import re
# MODIFED FROM CODE BY Petrina Collingwood  
#Goal is to remove necessary columns, but with user input
    print("This program is designed to analyze ezproxy log and will take in 6 inputs. As for the other fields, these will be eliminated") 
    print("Take a look at a sample log file. Please identify the fields number that need to be eliminated. Put this into double square bracket which will appear shortly.")
    print("Note that Python is a 0-based language, so the first column = 0, the second column = 1") 
    print("by default, we will eliminate columns [2,5,6,8,9], based on Ryerson's log file") 
    value = input("Please enter columns number:\n")
    print(f'You entered {value}')
    
    df.drop(df.columns[value], axis=1, inplace=True)
    # name columns
    df.columns = ['ip', 'session_id', 'user_id', 'date_time', 'url', 'size']
    df['date_time'] = df['date_time'].map(lambda x: x.lstrip('['))
    df['date_time'] = pd.to_datetime(df['date_time'], format='%d/%b/%Y:%H:%M:%S')
# remove lines where user is not logged in
    df = df[df.user_id != "-"]
    print("please enter your ezproxy prefix. By default, we use Ryerson\'s prefix, which is 'http://ezproxy.lib.ryerson.ca/login?url='")
    print('enter the prefix here {prefix}')
    prefix = input("Please enter prefix in quotation mark:\n")
    prefix=prefix.replace('.','\.')
    
    

def decode_url(url):
    import re
    from urllib.parse import unquote
# MODIFIED FROM Code By Petrina Collingwood 
    decoded_url = unquote(url)
    return decoded_url
    df['url'] = df.url.apply(decode_url)
    # remove excess columns for domain (since we are not really using ip right now, although this could be useful in the future for geospatial analysis) 
    df.drop(['ip','session_id','size'], axis=1, inplace=True)
    # remove ezp string from start of url
    df['url'] = df['url'].str.replace(prefix, '')# remove http etc
    df['url'] = df['url'].str.replace(r'^http://www\.|^https://www\.|^http://|^https://', '')
    