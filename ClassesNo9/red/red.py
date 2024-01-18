import fr 
import redis

host='localhost'
port=6379
qname= 'myqueue'


server = fr.Server()

@server.route('/')
def index(environ, start_response):
    print('Show index 0')
    with redis.Redis(host=host, port=port, decode_responses=True) as r:
        print('Show index 1')
        queue = r.lrange(qname, 0, -1)
    return fr.out_html({'queue':queue}, 'index.html', start_response)

@server.route('/add')
def addEl(environ, start_response):
    newel = fr.form_data(environ, ['newel'])['newel']
    if newel != '':
        with redis.Redis(host=host, port=port, decode_responses=True) as r:
            r.rpush(qname, newel)
    return fr.redir303('/', start_response)

@server.route('/pop')
def popEl(environ, start_response):
    print('Pop\n')
    with redis.Redis(host=host, port=port, decode_responses=True) as r:
        print('Pop2\n')
        r.blpop(qname)
    return fr.redir303('/', start_response)
    
server.run()


