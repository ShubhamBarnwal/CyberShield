#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 14:33:56 2019

@author: hardikuppal
"""

import sqlite3


def createTable():
    conn = sqlite3.connect('cyberShield.db')
    c = conn.cursor()
    
    c.execute('''DROP TABLE Comments''')
    c.execute('''CREATE TABLE Comments
                 (media_id NUMERIC, comments_id NUMERIC, username text, comment_text text, created_time NUMERIC, NlcLabel text, ToneLabel text)''')
    
    
    
    
    # Save (commit) the changes
    conn.commit()
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
    
    
def InsertTable(comment_data):
    conn = sqlite3.connect('cyberShield.db')
    c = conn.cursor()
    
    c.execute('INSERT INTO Comments VALUES (?,?,?,?,?,?,?)', comment_data)
    
    conn.commit()
    conn.close()
    
def getRecentDate():
    conn = sqlite3.connect('cyberShield.db')
    c = conn.cursor()
    
    time=c.execute("SELECT created_time FROM Comments ORDER BY created_time DESC LIMIT 1").fetchone()
    return(time)
    
def checkComment(comments_id):
    conn = sqlite3.connect('cyberShield.db')
    c = conn.cursor()
    
    flag=c.execute("SELECT 1 FROM Comments where comments_id={}".format(comments_id)).fetchone()
    return(flag) 
    

def ExecuteReader(sql):
    conn = sqlite3.connect('cyberShield.db')
    c = conn.cursor()

    dt = c.execute(sql).fetchall()

    conn.close()
    return dt  