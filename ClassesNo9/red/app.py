import fr 
import http.cookies as hc 
from model import Login

server = fr.Server()
login = Login()

def get_session(environ):
    cookie = hc.SimpleCookie()
    cookie.load(environ.get('HTTP_COOKIE', ''))
    morsel = cookie.get('session')
    if morsel is None:
        return None 
    else:
        return morsel.value

@server.route('/')
def index(environ, start_response):
    user = login.checkSession(get_session(environ))
    return fr.out_html({'user':user}, 'index.html', start_response)

@server.route('/login')
def login_form(environ, start_response):
    return fr.out_html(dict(), 'login.html', start_response) 

@server.route('/trylogin')
def trylogin(environ, start_response):
    data = fr.form_data(environ, ['user', 'passwd'])
    session = login.checkPassword(data['user'], data['passwd'])
    headers = []
    if session is not None:
        headers = [('Set-Cookie', f'session={session}')]
    return fr.redir303('/', start_response, headers = headers)
    
@server.route('/logout')
def logout(environ,start_response):
    login.delSession(get_session(environ))
    return fr.redir303('/', start_response)

server.run()

