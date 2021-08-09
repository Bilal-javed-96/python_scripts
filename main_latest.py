import os
from pprint import pprint
from typing import TextIO
from datetime import datetime
from datetime import timedelta
from tabulate import tabulate
import requests
from tabulate import TableFormat
'''
Pre-requisites : SMTP should be installed
                 mail command 
                 GIT
'''
#https://gitlab.com/ndctech2/clos_ubl/userpanel_ubl
#os.system('rm -rf userpanel_ubl')
repo_url = input("Enter the Link to Repository : ") or "https://gitlab.com/ndctech2/clos_ubl/userpanel_ubl"
clone_link = "git clone " + repo_url
#os.system(clone_link)                          #executing git clone command

folder_name = repo_url.split('/')              #line 14-18 is used to cd into the repo folder
folder_1 = folder_name[len(folder_name)-1]     #created locally
temp_c = "rm -rf " + folder_1
os.system(temp_c)
os.system(clone_link)
dir = os.popen('pwd').read().strip() 
cmd=dir+"/"+folder_1
os.chdir(cmd)                                  
os.system('touch commit.txt && chmod 666 commit.txt')  #creating file in which all commit info will be stored for processing
output = os.popen('git log --pretty=format:" %an, %ar " --all --after="2.days.ago"').read()
fh = open ('commit.html','w+')   # writing the output of git log command in commit.txt file
fh.write(output)
fh.close()

#----------------------------------------------------------
#opening commit file and sorting the developer names and days on which commit
#was done
#----------------------------------------------------------
fh = open('commit.html','r')
read_line = fh.readlines()
t0_name = []
t1_name = []
t2_name = []
#t3_name = []
#t4_name = []
for line in read_line:
    main_line = line.split(',')
 
    temp = main_line[1].split(' ')

    if temp[2] == 'minutes' or temp[2] == 'hours':
        t0_name.append(main_line[0])
    elif temp[2] == 'days' and temp[1] == '1':
        t1_name.append(main_line[0])
    elif temp[2] == 'days' and temp[1] == '2':
        t2_name.append(main_line[0])
'''   elif temp[2] == 'days' and temp[1] == '3':
        t3_name.append(main_line[0])
    elif temp[2] == 'days' and temp[1] == '4':
        t4_name.append(main_line[0])
'''
t0_name = list(set(t0_name))  #removing duplicate names from the list
t1_name = list(set(t1_name))
t2_name = list(set(t2_name))
#t3_name = list(set(t3_name))
#t4_name = list(set(t4_name))

fh.close()

#-----------------------------------------------------
# making a table for data sorted in above section
#-----------------------------------------------------
s=datetime.today()
t0_date=s.strftime("%d"+"-"+"%m"+"-"+"%Y")
t1_date = (datetime.today() - timedelta(days=1)).strftime("%d"+"-"+"%m"+"-"+"%Y")
t2_date=(datetime.today() - timedelta(days=2)).strftime("%d"+"-"+"%m"+"-"+"%Y")
#t3_date = (datetime.today() - timedelta(days=3)).strftime("%d"+"-"+"%m"+"-"+"%Y")
#t4_date = (datetime.today() - timedelta(days=4)).strftime("%d"+"-"+"%m"+"-"+"%Y")

table = {t0_date : t0_name,t1_date : t1_name,t2_date : t2_name}#,t3_date : t3_name , t4_date :t4_name }
head_1 = "Commits on "+ folder_1 +" repo"
headers = [head_1]
table1 = tabulate(table,headers='keys',tablefmt="html")
#print(table1)
fh = open ('Repo_Report.html','w+')
fh.write("Subject: This email contains repo details for " +folder_1+"\n\n")
fh.write(table1)
fh.close()
#------------------------------------------------
#API to list all users in repo
#------------------------------------------------
my_headers = {'Authorization' : 'Bearer ev2Ca9KHvZ2rM53yfSPs'}
response = requests.get('https://gitlab.com/api/v4/projects/27744775/users', headers=my_headers)
resjson = response.json()
userlist = []
#print(resjson)
for i in range(len(resjson)-1):
    print(resjson[i]['username'])
    userlist.append(resjson[i]['username'])
#print(userlist)
#------------------------------------------------
#Removing Users with commit and displaying users with no commit
#------------------------------------------------
#exist_count = test_list.count(15)
if len(t0_name) != 0:
    for i in t0_name:
        if userlist.count(i) > 0 :
            userlist.remove(i)
fb = open('branch.html','w+')
temp_c = "<h3>Repository Name : "+folder_1+"</br></h3>"
fb.write(temp_c)
fb.write("<h3>Users with No Commit :\n<br/></h3>")
fb.close()
#print(userlist)
fb = open('branch.html','a')
for i in userlist:
    temp_c = "<p>" +i +"</p>"
    fb.write(temp_c)
fb.close()
#------------------------------------------------
#commit history on each branch
#------------------------------------------------
output = os.popen('git branch -a').read().split('\n')
del output[0:2]
len1=len(output)
output1 = {}
output_f={}
for i in range(len1-1):
    #git log remotes/origin/dev --pretty=format:" %an, %ar " --after="2.days.ago"
    cmd = 'git log '+output[i] +' --pretty=format:" %an, %ar " --after="2.days.ago"'
    output1[output[i]] = (list(set(os.popen(cmd).read().split('\n'))))
    output_f[output[i]] = []
    print(output1[output[i]])

    if len(output1[output[i]]) != 0:
        temp_br = []
        print(output1[output[i]])
        for j in output1[output[i]]:
            temp_br = []
            sp_j = j.split(",")
            if len(sp_j) != 0:   #individual username and time([' Aakash Panhwar', ' 2 days ago '])
                #print(sp_j)
                if len(sp_j) > 1 :
                    sp_k = sp_j[1].split(" ")
                    if len(sp_k) != 0:
                        print(sp_k[2])
                        if sp_k[2] == "hours" and int(sp_k[1]) < 24:
                            t=datetime.today() - timedelta(days=1)#int(sp_k[1]))
                            time_1 = t.strftime("%d"+"-"+"%m"+"-"+"%Y")
                            test = [sp_j[0],time_1]
                            temp_br.append(test)
                        elif sp_k[2] == "hours" and int(sp_k[1]) < 24:
                            t=datetime.today() - timedelta(days=2)#int(sp_k[1]))
                            time_1 = t.strftime("%d"+"-"+"%m"+"-"+"%Y")
                            test = [sp_j[0],time_1]
                            temp_br.append(test)
                        else:
                            t=datetime.today() - timedelta(days=int(sp_k[1]))
                            time_1 = t.strftime("%d"+"-"+"%m"+"-"+"%Y")
                            test = [sp_j[0],time_1]
                            temp_br.append(test)
            #print(temp_br)
            #set(temp_br)
            output_f[output[i]] = temp_br
            s=datetime.now()
            t0_date=s.strftime("%d"+"-"+"%m"+"-"+"%Y")
            t=datetime.today() - timedelta(days=1)

out_em_br = []       # list of branches with no commits
for key in output_f:
    temp = output_f[key]
    if len(temp) != 0:
        temp.sort(key = lambda x:x[1],reverse = True)#= Sort(temp)#,key=lambda x :x[0])#itemgetter(1))
    elif len(temp) == 0:
        out_em_br.append(key)
        
    out_x=tabulate(temp,tablefmt="html")#,showindex="always") 
    fg = open ('Repo_Report.html','a')   # writing the output of git log command in commit.txt file
    fg.write("<h2>-------------------<br/></h2>")
    key_temp = "<h1>"+key+"<br/></h1>"
    fg.write(key_temp)
    fg.write("<h2>-------------------<br/></h2>")
    fg.write(out_x)
    fg.close() 
#------------------------------------------------
#Printing List of Branches with no commits
#------------------------------------------------
fi = open('branch.html','a')
fi.write('<h3>\n\nBranches with No Commits : \n</br></h3>')
for i in out_em_br:
    print(i)
    temp_c = "<p>" +i +"</p>"
    fi.write(temp_c)
fi.close()
os.system('mutt -e "set content_type=text/html" -s "PFA the GIT Repository Commit Report" Bilal.javed@ndctech.net < branch.html')
#os.system('mutt -e "set content_type=text/html" -s "PFA the GIT Repository Commit Report" Rizwan.nasir@ndctech.net < branch.html')
#------------------------------------------------------

os.chdir(dir)
dir = "rm -rf "+folder_1
#os.system(dir)