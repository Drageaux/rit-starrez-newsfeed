import argparse
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def retrieve_sheets(g_conn, term, week, files):	
	worksheets = {}
	for f in files:
		gsheet = g_conn.open(f)
		wsheet = gsheet.worksheet(str(term)+'-Wk'+str(week))
		worksheets[f] = wsheet
	return worksheets

def retrieve_data(wsheets):
	data = {}
	for w in wsheets:
		data[w] = wsheets[w].get_all_values()
	return data

def upload_data(sheet, files, data):
	sheet.update_cell(1,1,'Team Member')
	sheet.update_cell(1,2,'Accomplished')
	sheet.update_cell(1,3,'Planned')
	
	row_idx = 2
	time_count = 0
	accomplished = 0
	planned = 0
	for f in files:
		sheet.update_cell(row_idx,1,f + 'sheet ')
		rows = data[f]
		for row in range(2,len(rows)):
			for col in range(len(rows[row])):
				if len(rows[row][col]) > 0:
					value = rows[row][col]
					if value == 'TOTAL TIME':
						if time_count == 0:
							hours = rows[row][col-2]
							sheet.update_cell(row_idx,2,hours)
							accomplished += float(hours)
							time_count += 1
						else:
							hours = rows[row][col-1]
							sheet.update_cell(row_idx,3,hours)
							planned += float(hours)
							time_count = 0
		row_idx += 1
		sheet.update_cell(row_idx,1,'Team_Total')
	sheet.update_cell(row_idx,2,accomplished)
	sheet.update_cell(row_idx,3,planned)
	
def main():	
	term = 1
	parser = argparse.ArgumentParser(prog='timesheets')
	parser.add_argument('week', type=int)

	args = parser.parse_args()
	week = args.week

	scope = "https://spreadsheets.google.com/feeds"
	credentials = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)
	g_conn = gspread.authorize(credentials)
	
	files = ['Sean_Time', 'Matt_Time', 'David_Time', 'Adam_Time']
	worksheets = retrieve_sheets(g_conn, term, week, files)
	data = retrieve_data(worksheets)

	team_file = g_conn.open("Team_Time")
	team_sheet = team_file.worksheet(str(term)+'-Wk'+str(week))
	upload_data(team_sheet,files,data)
	
	
if __name__ == '__main__':
   main()