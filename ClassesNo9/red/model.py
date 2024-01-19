from redis import Redis
import bcrypt 
import secrets
import sys

class Login:
    def __init__(self, host='localhost', port = 6379, ttl = 60):
        self._args = {
            'host': host,
            'port': port,
            'decode_responses': True
        }
        self._ttl = ttl
    
    def setPassword(self, user, passwd):
        hash = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
        with Redis(**self._args) as r:
            r.set(f'user:{user}', hash)

    def checkPassword(self, user, passwd):
        session = None 
        with Redis(**self._args) as r:
            hash = r.get(f'user:{user}')
            if hash is not None:
                if bcrypt.checkpw(passwd.encode('utf-8'), hash.encode('utf-8')):
                    session = secrets.token_hex(20)
                    r.set(f'session:{session}', user, self._ttl)
        return session 

    def checkSession(self, session):
        user = None 
        if session is not None:
            with Redis(**self._args) as r:
                user = r.get(f'session:{session}')
                if user is not None:
                    r.set(f'session:{session}', user, self._ttl)
        return user 

    def delSession(self, session):
        if session is not None:
            with Redis(**self._args) as r:
                r.delete(f'session:{session}')

if __name__ == '__main__' and len(sys.argv) == 3:
    user = sys.argv[1]
    passwd = sys.argv[2]
    login = Login()
    login.setPassword(user, passwd)
    