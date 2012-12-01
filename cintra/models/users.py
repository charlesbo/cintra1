from persistent import Persistent
from persistent.mapping import PersistentMapping


def saltPeper(pwd_raw):
    '''Encoding pwd_raw '''
    pwd_cooked = pwd_raw
    return pwd_cooked


def wash(pwd_cooked):
    '''Decoding pwd_cooked '''
    pwd_raw = pwd_cooked
    return pwd_raw


class UserFolder( PersistentMapping ):
    pass


class User( Persistent ):
    def __init__(self, books=[], username='', nickname='', cintraid='0', 
                 pwd='', email='', address='', balance=0.0, points=0.0, 
                 experience=0.0, group=[] ):
        self.books = books
        self.username = username
        self.nickname = nickname
        self.cintraid = cintraid
        self.pwd = pwd
        self.group = group
        self.email = email
        self.address = ''
        self.balance = balance    # cash
        self.points = points    # game points
        self.experience = experience    # game experience

    def level(self):
        return len(str(int(self.experience)))


GROUPS = ['group:user', 'group:superuser', 'group:manager', 'group:admin']
#class Group( Persistent ):
#    def __init__(self, name='', members=[]):
#        self.memebers = members
#        self.name = self.__name__ = name
