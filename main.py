from flask import Flask,render_template
import requests as rq
import bs4
from threading import Thread
from time import sleep

app = Flask(__name__)

@app.route('/')
def rt():
    return render_template('index.html')

@app.route('/uid/<uid>')
def rest(uid):
	global htm
	htm = ''
	find(uid)
	return htm
	
@app.route('/class/<uid>')
def main(uid):
	uid = int(uid[:-3])*1000
	global htm,k
	k = 0
	htm = ''
	#htm = 'hi<br>'
	#for i in range(1,51):
	#	find(uid+i)
	for i in range(1,51):
		globals()['thr'+str(i)] = Thread(target=find,args=(uid+i,))
		globals()['thr'+str(i)].start()
	for i in range(1,51):
		globals()['thr'+str(i)].join()
	return htm



def find(uida):
	global htm,k
	new = ''
	head =''
	loyola = rq.get('http://202.53.11.226:8080/lastudentportal/online/report/onlineResultNewInner.jsp?registerno={}&iden=1'.format(uida)).content
	loy_parse = bs4.BeautifulSoup(loyola,'html.parser')
	table = loy_parse.find('table',attrs={'id':'table1'})
	details = loy_parse.find_all('td',attrs={'class':'dynaColorTR1'})
	try:
		head = "<h2> UID :-  "+details[3].text + "</h2>\n<h2>Name :- " + details[1].text+"</h2>"
		new += str(head) + str(table)
		htm += new
	except:
		htm += '<br><br><h1>Not Available</h1></br></br>'










app.run(host='0.0.0.0', port=8080)
