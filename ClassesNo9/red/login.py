import fr 
import redis
import secrets
import http.cookies as hc 

red_args = {
    'host':'localhost',
    'port':6379,
    'decode_responses':True
}

server = fr.Server()

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
    user = None 
    session = get_session(environ)
    if session is not None:
        with redis.Redis(**red_args) as r:
            user = r.get('session:' + session)
    return fr.out_html({'user':user}, 'main.html', start_response)

@server.route('/login')
def login_form(environ, start_response):
    return fr.out_html(dict(), 'login.html', start_response) 

@server.route('/trylogin')
def trylogin(environ, start_response):
    data = fr.form_data(environ, ['user', 'passwd'])
    with redis.Redis(**red_args) as r:
        user = data['user']
        passwd = r.get('user:' + user)
        headers = []
        if passwd == data['passwd']:
            session = secrets.token_hex(20)
            r.set('session:'+session, user, 60)
            headers = [('Set-Cookie', f'session={session}')]
        return fr.redir303('/', start_response, headers = headers)
    
@server.route('/logout')
def logout(environ,start_response):
    session = get_session(environ)
    with redis.Redis(**red_args) as r:
        r.delete('session:'+session)
    return fr.redir303('/', start_response)

server.run()

