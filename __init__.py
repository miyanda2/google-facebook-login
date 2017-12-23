from flask import Flask,render_template,session,url_for,request,redirect
import random, string

# pip install oauth2client
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# required for session to work
app.config['SECRET_KEY']= ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(24))

# Loading Json structure which contains client id and secret Key
google_client_json_path = 'templates\\google_client_secret.json'
google_client_json = json.loads(open(google_client_json_path,'r').read())

GOOGLE_CLIENT_ID = google_client_json ['web']['client_id']


# FaceBook
facebook_client_json_path = 'templates\\facebook_client_secret.json'
facebook_client_json = json.loads(open(facebook_client_json_path,'r').read())

FACEBOOK_CLIENT_ID = facebook_client_json['web']['app_id']
FACEBOOK_CLIENT_SECRET = facebook_client_json['web']['app_secret']

@app.route('/')
def home():
        try:
                log=0
                if session.get('user_data'):
                        log=1
                return render_template("googleFacebookLogin.html",log=log)
        except Exception as e:
                return str(e)


@app.route('/index/')
def index():
        try:
                # check if user as logged in otherwise redirect to home page
                if session.get('user_data') is None:
                        return redirect('/')
                
                # ['given_name'] defined in json provided by google
                return "HELLO "+str(session.get('user_data')['given_name'])
        except Exception as e:
                return str(e)

# Route generate a state token for anti-forgery of request
@app.route('/getToken/',methods=['GET','POST'])
def getToken():
        try:
                # genertaing a state token for anti-forgery 
                state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
                session['token'] = state
                return session['token']

        except Exception as e:
                return str(e)
        
@app.route('/googleSignIn/',methods=['POST','GET'])
def googleSignIn():
        try:
                # For this to work make sure session is not saved in client side
                # ( Genertaing a state token for anti-forgery )
                # Default flask session is saved on client side
                # use Flask-Session
                if session['token']!=request.args.get('token'):
                        return "Error miss matched token"

                # One time client connect code
                client_code = request.data

                # To indicates its for one time flow only set redirect_uri='postmessage'
                flow = flow_from_clientsecrets(google_client_json_path,scope='',redirect_uri='postmessage')
                credentials = flow.step2_exchange(client_code)
                
                # Check access token is valid
                access_token = credentials.access_token

                token_url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token='+str(access_token))
                
                _http = httplib2.Http()
                
                # the returned as two values in one response header and second response itself
                # so we do _http.request(token_url,'GET')[1] but the data is in bytes form and
                # needs to be converted to string
                result = json.loads(_http.request(token_url,'GET')[1].decode('utf-8'))

                # check if the access token is valid i.e not expired
                if result.get('error') is not None:
                        return "error: token expired"
                
                # Check if the access token provided is for the user we want (not required as such)
                google_user_id =credentials.id_token['sub']
                if result['user_id'] != google_user_id:
                        return "error: invalid user "
                
                # check if the token was for us by checking the client_id provided to us
                if result['issued_to'] != GOOGLE_CLIENT_ID:
                        return "error: invalid publisher"
                
                # load user data
                user_url = ('https://www.googleapis.com/oauth2/v1/userinfo?access_token='+str(access_token))
                user_data = json.loads(_http.request(user_url,'GET')[1].decode('utf-8'))
                
                # Check if user already exists
                # If not then ask for Sign Up
                # Assuming user doesnt exist
                already = True #userExists() -> with some dbs logic
                

                # User Exists then save their data in session
                if already:
                        # saving data in login session
                        session['type']='google'
                        session['email'] = user_data['email']
                        session['acces_token'] = access_token
                        session['user_data'] = user_data

                return str(already)
        except FlowExchangeError:
                return ("Erron in generating credentials..")
        except Exception as e:
                return str(e)

@app.route('/facebookSignIn/',methods=['POST'])
def facebookSignIn():
        try:
                # For this to work make sure session is not saved in client side
                # ( Genertaing a state token for anti-forgery )
                # Default flask session is saved on client side
                # use Flask-Session
                if session['token']!=request.args.get('token'):
                        return "Error miss matched token"
                
                # One time client connect code
                access_token = request.data.decode("utf-8")
                
                # Get user details
                url = 'https://graph.facebook.com/v2.11/me?fields=name,birthday,email,gender,location,picture{url}&access_token=%s'%(access_token)
                _http = httplib2.Http()
                result = json.loads(_http.request(url,'GET')[1].decode('utf-8'))
                
                # Check if user already exists
                # If not then ask for Sign Up
                # Assuming user doesnt exist
                already = True #userExists() -> with some dbs logic

                # User Exists then save their data in session
                if already:
                        # saving data in login session
                        session['type']='facebook'
                        session['email'] = result['email']
                        session['acces_token'] = access_token
                        session['user_data'] = result
                
                return str(already)
        except Exception as e:
                return str(e)
        
@app.route('/logout/',methods=['GET'])
def logout():
        try:
                # check if logged in using facebook, google or normal method 
                login_type=session['type']
                session.pop('type', None)
                session.pop('email', None)
                session.pop('acces_token', None)
                session.pop('user_data', None)

                return login_type
        except Exception as e:
                return str(e)

if __name__=="__main__":
	app.run()


