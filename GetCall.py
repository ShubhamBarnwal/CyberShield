import requests as rq
from TableScript import InsertTable,getRecentDate,checkComment
from apiTest import apiNLCTest 
from apiTest import apiToneTest
import os


def GetCall(accessToken):
    filePath="Log.txt"
#    accessToken='11639557926.5d4680b.faec56455bd04f7ab2389f26c17cbb01'
    accessToken=accessToken.rstrip(',')
#    logfile=open('Log.txt','a')
#    logfile.write('access token in get call{}\n'.format(accessToken))
#    logfile.close()
    endpointLink= "https://api.instagram.com/v1/users/self/media/recent?access_token={}".format(accessToken)
    if os.path.exists(filePath):
        os.remove(filePath)
        logfile=open('Log.txt','a')
        logfile.write('previous log file deleted')
        logfile.close()
    else:
        
        logfile=open('Log.txt','a')
        logfile.write('Can not delete the file as it does not exists\n')
        logfile.close()
    

    #endpointLink1="https://api.instagram.com/v1/media/1998460770850257087_11639557926/comments?access_token=11639557926.7897a2c.127898c631cd41a3b4300e1e29d560d3"
    
    r = rq.get(endpointLink)
    r = r.json()
    main_user = r["data"][0]["user"]["full_name"]
#    print(str(r))
    logfile=open('Log.txt','a')
    logfile.write('json present')
    logfile.close()
    while r is None:
        logfile=open('Log.txt','a')
        logfile.write('waiting for json\n')
        logfile.close()
    if r is not None:
        
#        print(r["data"])
        #data = json.loads(r.text)
        #for t in r:
        #    print(t)
        media_id_list=[]
        for ids in range(len(r['data'])):
            media_id_list.append(r['data'][ids]['id'])
            logfile=open('Log.txt','a')
            logfile.write('media list inserted\n')
            logfile.close()
    else:
        media_id_list=[]
        
    
    
    
    comments=[]
    if len(media_id_list)!=0:
        
        for i in range(len(media_id_list)):
            comments_data=(rq.get("https://api.instagram.com/v1/media/{0}/comments?access_token={1}".format(media_id_list[i],accessToken))).json()
        #    print(media_id_list[i],len(comments_data["data"]))
            for j in range(len(comments_data['data'])):
        #        comments_temp.append(comments_data["data"][j])
        #        print(comments_data["data"][j],"___________")
        #        print(comments_data["data"][j]["text"],apiToneTest(comments_data["data"][j]["text"])[1])
                
                media_id,comments_id, username, comment_text, created_time, NlcLabel, ToneLabel = media_id_list[i],comments_data["data"][j]["id"],comments_data["data"][j]["from"]["username"],comments_data["data"][j]["text"],comments_data["data"][j]["created_time"],apiNLCTest(comments_data["data"][j]["text"])[0][0],apiToneTest(comments_data["data"][j]["text"])[1]
        ##        print(media_id,comments_id, username, comment_text, created_time)
                comments.append([media_id,comments_id, username, comment_text, created_time, NlcLabel, ToneLabel])
        
        logfile=open('Log.txt','a')
        logfile.write('Comment list inserted')
        logfile.close()
        #print((comments))
    else:
        comments=[]
     
        
    if len(comments)!=0:
        for i in range(len(comments)): 
            if checkComment(int(comments[i][1])) is None:
                InsertTable(comments[i])
                logfile=open('Log.txt','a')
                logfile.write('Inserted\n')
                logfile.close()
            else:
                logfile=open('Log.txt','a')
                logfile.write('already present\n')
                logfile.close()
    return main_user
        
