import argparse
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

def update_website(g_conn,files,week):
    unix = "git pull"
    os.popen(unix).read()
    gsheet = g_conn.open("Team_Time")
    wsheet = gsheet.worksheet(str(week)+'-Wk'+str(week))
    html = '<table><tr><td>Team Member</td><td>Accomplished</td><td>Planned</td></tr>'
    idx = 2
    for f in files:
        html += '<tr><td>'+f.replace('_',' ')+'</td><td>'+wsheet.cell(idx,2).value+'</td><td>'+wsheet.cell(idx,3).value+'</td></tr>'
        idx += 1
    html += '</table>'
    file = open('index.html','r')
    lines = file.readlines()
    file.close()
    file = open('index.html','w')
    idx = 0
    for line in lines:
        if '<h1 class="ui centered huge header">Four-Ups</h1>' in line:
            line += html
        file.write(line)
    file.close()

def push_github():
    unix = "git add ."
    os.popen(unix).read()
    unix = 'git commit -m "script update."'
    os.popen(unix).read()
    unix = 'git push origin master'
    os.popen(unix).read()


def main():
    parser = argparse.ArgumentParser(prog='timesheets')
    parser.add_argument('week', type=int)
        
    args = parser.parse_args()
    week = args.week

    scope = "https://spreadsheets.google.com/feeds"
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
    g_conn = gspread.authorize(credentials)
        
    files = ['Sean_Time', 'Matt_Time', 'David_Time', 'Adam_Time']
    update_website(g_conn,files,week)

    push_github()


if __name__ == '__main__':
    main()