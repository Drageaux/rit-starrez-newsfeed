import argparse
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

def update_website(g_conn,files,week):
    names = {"Sean_Time":"Sean Klei","Adam_Time":"Adam Audycki","David_Time":"David Thong Nguyen","Matt_Time":"Matt Pitcher"}
    unix = "git pull"
    os.popen(unix).read()
    gsheet = g_conn.open("Team_Time")
    wsheet = gsheet.worksheet('1-Wk'+str(week))
    html = '<h3 class=h3-week>Week '+str(week)+'<div class="top-border-div"><table class="table-timesheets"><tr class="tr-timesheets"><th>Team Member</th><th>Accomplished</th><th>Planned</th></tr>'
    idx = 2
    for f in files:
        html += '<tr class="tr-timesheets"><td>'+names[f].replace('_',' ')+'</td><td>'+wsheet.cell(idx,2).value+'</td><td>'+wsheet.cell(idx,3).value+'</td></tr>'
        idx += 1
    html += '</table></div></h3>'
    file = open('index.html','r')
    lines = file.readlines()
    file.close()
    file = open('index.html','w')
    idx = 0
    for line in lines:
        if '<h1 class="ui centered huge header">Timesheets</h1>' in line:
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
