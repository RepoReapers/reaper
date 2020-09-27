import sys
from lib.utilities import url_to_dom_value

QUERY = '''
SELECT url FROM projects WHERE id={0}
'''

def run(project_id, repo_path, cursor, **options):
    print("----- METRIC: PULL REQUESTS -----")
    pr_rate = 0
    cursor.execute(QUERY.format(project_id))
    url = cursor.fetchone()[0].replace("api.","").replace("repos/","")
    url_opr = url + "/pulls"
    url_cpr = url + "/pulls?q=is%3Apr+is%3Aclosed+"
    url_mpr = url + "/pulls?q=is%3Apr+is%3Amerged+"
    mpr = 0
    cpr = 0
    opr = 0
    token_avail = False
    git_tokens = options['tokens']
    # Making a request for open pull requests count with the tokens provided
    for token in git_tokens:
        if(token_avail == True):
            break 
        else:
            try: 
                opr = url_to_dom_value(url_opr,[git_tokens[token], token],"Open")
                token_avail = True
                break
            except:
                continue
    # Making a request for open pull requests count without token, in the case all OAuth tokens got expired or incorrect tokens provided  
    if(token_avail == False):
        try:
            opr = url_to_dom_value(url_opr,"Open")
            print('without token - open pull requests - fetch ok')
        except Exception as ex:
            print(ex)
            opr = 0     
    token_avail = False
    # Making a request for closed pull requests count with the tokens provided
    for token in git_tokens:
        if(token_avail == True):
            break 
        else:
            try: 
                cpr  = url_to_dom_value(url_cpr,[git_tokens[token], token],"Closed")
                token_avail = True
                break
            except:
                continue
    # Making a request for closed pull requests count without token, in the case all OAuth tokens got expired or incorrect tokens provided  
    if(token_avail == False):
        try:
            cpr  = url_to_dom_value(url_cpr,"Closed")
            print('without token - closed pull requests - fetch ok')
        except Exception as ex:
            print(ex)
            cpr = 0
    token_avail = False
    # Making a request for merged pull requests with the tokens provided
    for token in git_tokens:
        if(token_avail == True):
            break 
        else:
            try: 
                mpr  = url_to_dom_value(url_mpr,[git_tokens[token], token],"Total")
                token_avail = True
                break
            except:
                continue
    # Making a request for merged pull requests count without token, in the case all OAuth tokens got expired or incorrect tokens provided  
    if(token_avail == False):
        try:
            mpr  = url_to_dom_value(url_mpr,"Total")
            print('without token - merged pull requests - fetch ok')
        except Exception as ex:
            print(ex)
            mpr = 0
    pr = mpr+cpr+opr
    if(pr > 0):
        pr_rate = float(mpr+cpr)/float(pr*1.0)    
    threshold = options['threshold']
    pr_rate >= threshold, pr_rate
    print("PR Rate: ",pr_rate)
    return (pr_rate >= threshold, pr_rate)


if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
    sys.exit(1)
