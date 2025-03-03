'''
Author: doodhwala, leezeeyee
Python3 script to fetch papers
'''

import os, re, requests, codecs

filename='README.md'
directory = 'papers'
if not os.path.exists(directory):
    os.makedirs(directory)
papers = []
with codecs.open(filename, encoding='utf-8', mode='r', buffering=1, errors='strict') as f:
    lines = f.read().split('\n')
    heading, section_path = '', ''
    for line in lines:
        if('## 20' in line):
            heading = line.strip().split('##')[1]
            win_restricted_chars = re.compile(r'[\^\/\\\:\*\?\"<>\|]')
            heading = win_restricted_chars.sub("", heading)
            section_path = os.path.join(directory, heading)
            if not os.path.exists(section_path):
                os.makedirs(section_path)
        if('[`[pdf]`]' in line):
            # The stars ensure you pick up only the top 100 papers
            # Modify the expression if you want to fetch all other papers as well
            result = re.search('(.*?)\[`\[pdf\]`\]\((.*?)\)', line)
            if(result):
                paper, url = result.groups()
                paper = win_restricted_chars.sub("", paper)
                paper=paper.strip('- ')
                # Auto - resume functionality
                if(not os.path.exists(os.path.join(section_path, paper + '.pdf'))):
                    print('Fetching', paper)
                    try:
                        print("url: ", url)
                        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
                        headers = {'User-Agent' : user_agent,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}  #here is the most importent
                        response = requests.get(url, headers=headers)
                        with open(os.path.join(section_path, paper + '.pdf'), 'wb') as f:
                            f.write(response.content)
                    except requests.exceptions.RequestException as e:
                        print("Error: {}".format(e))
