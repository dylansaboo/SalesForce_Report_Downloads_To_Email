#! /usr/bin/env python
from simple_salesforce import Salesforce
import requests, sys, re, json
import xlsxwriter
from datetime import datetime
from collections import OrderedDict
from reports_Mail import reports_Mail
from pytz import timezone

class salesforce_data_dump(object):

    #Get Local time for EST
    def set_time(self):
        tz = timezone('EST')
        now = datetime.now(tz)
        print("Date Time: %s" % (now))

        now_Month = now.month
        now_Month = self.fix_SOQL_Bug(now_Month)
        now_Year = now.year
        now_Day = now.day
        now_Day = self.fix_SOQL_Bug(now_Day)
        now_year = str(now_Year)
        now = (("%s-%s-%s") % (now_Year,now_Month,now_Day))
        return now

    #Fix SalesForce SOQL Query Bug
    def fix_SOQL_Bug(self, bug):
        if bug < 10:
            bug = str(bug)
            bug = '0' + bug
        return bug


    def main(self):
        count = 2

        workbook = xlsxwriter.Workbook('DailyReportDownloads.xlsx')
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold':1, 'underline':1})
        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 28)
        worksheet.set_column(3, 3, 82)

        worksheet.write('A3', 'SALESFORCE ID', bold)
        worksheet.write('B3', 'NAME', bold)
        worksheet.write('C3', 'COMPANY NAME', bold)
        worksheet.write('D3', 'SUBJECT', bold)

        now = self.set_time()

        #SOQL Query to get list of downloads & Total
        data1 = "SELECT Id, Type, Subject, ActivityDate, who.Name FROM Task WHERE ActivityDate = %s AND Type = 'Research Download'" % (now)
        data1 = str(data1)
        data = self.sf.query(data1)

        Size = data['totalSize']
        Records = data['records']

        print("Total Downloads for %s | %s" % (now, Size))
        worksheet.write('A1', "Total Downloads :", bold)
        worksheet.write('B1', "Date: %s | Downloads: %s\n" % (now, Size))
        print("")

        #Populate worksheet with data of Object Items, SOQL Query Nested Loop to get each users Company Name
        for record in Records:
            count = count + 1
            worksheet.write(count, 0, '%s' % (record['Id']))
            worksheet.write(count, 3, '%s' % (record['Subject']))
            whos = record['Who']
            name = whos['Name']
            worksheet.write(count, 1, '%s' % (whos['Name']))
            Account_Name = "SELECT account.Name FROM contact WHERE Name = '%s'" % (name)
            Accounts_Names = self.sf.query(Account_Name)
            Account_Records = Accounts_Names['records']
            for i in Account_Records:
                b = i['Account']
                worksheet.write(count, 2, '%s' % (b['Name']))
        workbook.close()
        reports_Mail()
        print("Completed Run")

    def __init__(self):
        #Salesforce Authentication
        self.sf = Salesforce(username='SALESFORCE USERNAME', password='SALESFORCE PASSWORD', security_token='SALESFORCE TOKEN') 
        self.main()

if __name__ == '__main__':
    Object1 = salesforce_data_dump()
