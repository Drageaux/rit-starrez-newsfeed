import argparse
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

def update_timesheets(g_conn,files,week):
    names = {"Sean_Time":"Sean Klei","Adam_Time":"Adam Audycki","David_Time":"David Thong Nguyen","Matt_Time":"Matt Pitcher","Team_Time":"Team Total"}
    unix = "git pull"
    os.popen(unix).read()
    gsheet = g_conn.open("Team_Time")
    wsheet = gsheet.worksheet('1-Wk'+str(week))
    html = '<div class="data-week"><h2 class="ui header">Week '+str(week)+'</h2><div class="top-border-div"><table class="table-timesheets"><tr class="tr-timesheets"><th>Team Member</th><th>Accomplished</th><th>Next Week\'s Plan</th></tr>'
    idx = 2
    for f in files:
        print(f)
        print(idx)
        html += '<tr class="tr-timesheets"><td>'+names[f].replace('_',' ')+'</td><td>'+wsheet.cell(idx,2).value+'</td><td>'+wsheet.cell(idx,3).value+'</td></tr>'
        idx += 1
    html += '</table></div></div>'
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

def update_fourups(g_conn,date):
    gsheet = g_conn.open("FourUps")
    wsheet = gsheet.worksheet('FourUps ' + str(date))
    fourup = wsheet.get_all_values()
    #date = fourup[0][0]
    html = '<h3 class="h3-week">'+str(date)+'<div class="top-border-div"><table class="table-fourup">'
    date = fourup[0][0]
    html = '<div class="data-week data-fourup"><h2 class="ui header">'+str(date)+'</h2><div class="top-border-div"><table class="table-fourup">'
    cells = {'progress':'<table class="table-cell"><tr><th>Progress</th></tr>',
                                'risks':'<table class="table-cell"><tr><th>Risks</th></tr>',
                                'plan':'<table class="table-cell"><tr><th>Plan</th></tr>',
                                'needs':'<table class="table-cell"><tr><th>Needs</th></tr>'}
    idx = 1
    for entry in fourup[1:]:
        entry = entry[1:]
        if len(entry[0]) > 0:
            cells['progress'] +=  '<tr><td>' + str(idx) + '. ' + str(entry[0]) + '</tr></td>'
        if len(entry[1]) > 0:
            cells['risks'] +=  '<tr><td>' + str(idx) + '. ' + str(entry[1]) + '</tr></td>'
        if len(entry[2]) > 0:
            cells['plan'] +=  '<tr><td>' + str(idx) + '. ' + str(entry[2]) + '</tr></td>'
        if len(entry[3]) > 0:
            cells['needs'] +=  '<tr><td>' + str(idx) + '. ' + str(entry[3]) + '</tr></td>'
        idx += 1
    for key in cells:
        cells[key] += '</table>'

    html += '<tr><td>'+cells['progress']+'</td><td>'+cells['risks']+'</td></tr>'
    html += '<tr><td>'+cells['plan']+'</td><td>'+cells['needs']+'</td></tr>'
    html += '</table></div></div>'

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


def push_github(week):
    unix = "git add ."
    os.popen(unix).read()
    unix = 'git commit -m "script update - week '+week+'"'
    os.popen(unix).read()
    unix = 'git push origin master'
    os.popen(unix).read()


def main():
    parser = argparse.ArgumentParser(prog='update_site')
    parser.add_argument('week', type=int)
    parser.add_argument('date', type=str, nargs='?')

    args = parser.parse_args()
    week = args.week
    date = args.date

    scope = "https://spreadsheets.google.com/feeds"
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
    g_conn = gspread.authorize(credentials)

    files = ['Sean_Time', 'Matt_Time', 'David_Time', 'Adam_Time', 'Team_Time']
    update_timesheets(g_conn,files,week)
    if date:
        update_fourups(g_conn,date)

    push_github(str(week))


if __name__ == '__main__':
    main()
