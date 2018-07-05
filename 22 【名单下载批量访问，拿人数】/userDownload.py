#!/var/bin/python
#coding:utf-8
import ConfigParser
import requests

cf = ConfigParser.ConfigParser()
cf.readfp(open('param.ini'))

SECTION_LOGIN = 'login'
SECTION_UPLOAD = 'upload'
SECTION_REQUEST = "request"
secs = cf.sections()
print secs

emailOrPhone = cf.get(SECTION_LOGIN, 'account')
password = cf.get(SECTION_LOGIN, 'password')
fileName = cf.get(SECTION_UPLOAD, 'file')
registerPhone = cf.get(SECTION_UPLOAD, 'register_phone')
print emailOrPhone, password, fileName, registerPhone

reqs = cf.items(SECTION_REQUEST)
#print reqs

s = requests.Session()
nicknames = []


def login():
	URL_LOGIN = "http://analysis.datastory.com.cn/account/ajax/login"
	login_info = {'emailOrPhone': emailOrPhone, 'password':password}
	login_res = s.post(URL_LOGIN, login_info)
	print login_res.text

def getWeiboUser(nickname):
	getWeiboUserAPI = "http://analysis.datastory.com.cn/data/ajax/getWeiboUser"
	post_data = {"nickName": nickname}

	r = s.post(getWeiboUserAPI, post_data)
	print r.text

def upload():
	URL = "http://analysis.datastory.com.cn/temp/vfengyunImport"

	post_data = {
	    "registerPhone":registerPhone, 
	    "taskName": "VfengyunImport", 
	    }
	r = s.post(URL, post_data, files={'file': open(fileName, "rb")})

	print URL
	print r.text
	print post_data

def main():
	
	login()
	with open(fileName, "rb") as reader:
		#nicknames = list(reader)
		for lin in reader:
			print lin
			break;

	#print nicknames[0]
#	getWeiboUser()


	#upload()

if __name__ == "__main__":
	main()