from flask import Flask
import os
from flask import render_template,session,redirect,url_for,jsonify
from flask import request
from apscheduler.schedulers.background import BackgroundScheduler
from TableScript import ExecuteReader
from GetCall import GetCall
from watson_developer_cloud import NaturalLanguageClassifierV1
import requests as rq

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    # f = open("accessToken.txt", "r")
    # tempList=f.readline().split(',')
    # accessToken=tempList[0]
    # main_user=tempList[1]

    logfile = open('routesLog.txt', 'a')
    logfile.write('session index:' + session['accessToken'])
    logfile.close()
    if 'accessToken' in session:
        #    logfile=open('routesLog.txt','a')
        #    logfile.write("session value:{0}".format(accessToken))
        #    logfile.close()
        main_user = session["main_user"]
        logfile = open('routesLog.txt', 'a')
        logfile.write('session index read')
        logfile.close()
        comment_count_chart1 = []
        users_chart1 = []
        dt_chart1 = ExecuteReader(
            "select count(*) as count,username from Comments Group by username order by count desc limit 5")
        for i in range(len(dt_chart1)):
            comment_count_chart1.append(dt_chart1[i][0])
            users_chart1.append(dt_chart1[i][1])

        # chart2
        comment_count_chart2 = [0] * 5
        nlcLabel = ['Identity Hate', 'Neutral', 'Obscene', 'Threat', 'Toxic']
        dt_chart2 = ExecuteReader("select count(*) as count,NlcLabel from Comments Group by NlcLabel order by NlcLabel")
        for i in range(len(dt_chart2)):
            for j in range(len(nlcLabel)):
                if nlcLabel[j].lower() == dt_chart2[i][1]:
                    comment_count_chart2[j] = dt_chart2[i][0]

        # titlecount
        count_media_id = ExecuteReader("select count(distinct media_id) from Comments")
        explicit_comments = ExecuteReader(
            "select count(*) from (select * from Comments where NlcLabel!='neutral' union select * from Comments where NlcLabel='neutral' and ToneLabel in ('Anger'))")

        ##Comment table
        comment_text = []
        commentTable = []
        tone = []
        nlc = []
        user_table = []
        dt_table1 = ExecuteReader(
            "select comment_text,username,NlcLabel,ToneLabel,DATETIME(created_time, 'unixepoch') AS date from (select * from Comments where NlcLabel!='neutral' union select * from Comments where NlcLabel='neutral' and ToneLabel in ('Anger'))")
        length_comment_table = len(dt_table1)
        for i in range(len(dt_table1)):
            commentTable.append([dt_table1[i][0], dt_table1[i][1], dt_table1[i][2], dt_table1[i][3], dt_table1[i][4]])
            comment_text.append(dt_table1[i][0])
            user_table.append(dt_table1[i][1])
            tone.append(dt_table1[i][2])
            nlc.append(dt_table1[i][3])

        ##graph

        count_explicit_graph = []
        date_graph = []
        dt_graph = ExecuteReader(
            "select count(*) as count,DATE(created_time, 'unixepoch') AS date from (select * from Comments where NlcLabel!='neutral' union select * from Comments where NlcLabel='neutral' and ToneLabel in ('Anger')) group by date")
        for i in range(len(dt_graph)):
            date_graph.append(dt_graph[i][1])
            count_explicit_graph.append(dt_graph[i][0])

        return render_template('index.html', main_user=main_user, option_list=comment_text, users=users_chart1,
                               commentTable=commentTable, length_comment_table=length_comment_table,
                               comment_count=comment_count_chart1, categories=nlcLabel,
                               cat_comment_count=comment_count_chart2, count_explicit_graph=count_explicit_graph,
                               date_graph=date_graph, count_media_id=count_media_id[0][0],
                               explicit_comments=explicit_comments[0][0])

    return redirect(url_for('login'))


@app.route('/accessToken', methods=['GET', 'POST'])
def ExtractToken():
    if request.method == "POST":
        if request.form['token'] is not None:
            accessToken = request.form['token']
            while accessToken is None:
                logfile = open('routesLog.txt', 'a')
                logfile.write('waiting for access token')
                logfile.close()
            filePath = 'accessToken.txt';
            if os.path.exists(filePath):
                os.remove(filePath)

            # As file at filePath is deleted now, so we should check if file exists or not not before deleting them

            accessToken1 = accessToken.rstrip(',')
            session['accessToken'] = accessToken1
            endpointLink = "https://api.instagram.com/v1/users/self/media/recent?access_token={}".format(accessToken1)
            r = rq.get(endpointLink)
            r = r.json()
            main_user = r["data"][0]["user"]["full_name"]
            # logfile=open('accessToken.txt','w+')
            # logfile.write("{0}{1}".format(accessToken,main_user))
            # logfile.close()
            logfile = open('routesLog.txt', 'a')
            logfile.write('session accessToken:' + session['accessToken'])
            logfile.close()
            GetCall(accessToken)
            session['main_user'] = main_user

            scheduler = BackgroundScheduler()
            scheduler.add_job(lambda: GetCall(accessToken), trigger="interval", seconds=30)
            scheduler.start()
            return redirect(url_for('index'))
    return render_template('accessToken.html')


@app.route('/analyze', methods=['GET', 'POST'])
def Analyze():
    api_key = "LiI3o53WHaOU02ATKIwKhSQdirvntK1lZUPA6rhdEwCZ"
    workspace_ID = "6deb62x509-nlc-477"
    natural_language_classifier = NaturalLanguageClassifierV1(iam_apikey=api_key)
    comment_text = request.form['text']
    classes = {}
    result = ""
    if comment_text != "":
        classes = natural_language_classifier.classify(workspace_ID, comment_text)
    result = classes.result
    return jsonify(result)


@app.route('/contactUs')
def contactUs():
    # f = open("accessToken.txt", "r")
    # tempList = f.readline().split(',')
    # main_user = tempList[1]
    main_user = session['main_user']
    return render_template('contactUs.html', main_user=main_user)


@app.route('/faq')
def faq():
    # f = open("accessToken.txt", "r")
    # tempList = f.readline().split(',')
    # main_user = tempList[1]
    main_user = session['main_user']
    return render_template('faq.html', main_user=main_user)


@app.route('/logout')
def logout():
    session.pop('accessToken', None)
    session.pop('main_user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)