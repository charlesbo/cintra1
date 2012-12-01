from cintra.models.users import User, UserFolder, saltPeper, wash
from cintra.models.books import Book
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
import logging


class UserViews(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    @view_config(name='reg_user', context=UserFolder, renderer="cintra:templates/edit_user.pt")
    def reg_user(self):
        return self._generate_user(group='user', actionname='reg_user')

    @view_config(name='add_user', context=UserFolder, renderer="cintra:templates/edit_user.pt", permission='add_user')
    def add_user(self):
        return self._generate_user(group='', actionname='add_user')

    def _generate_user(self, group='', actionname='reg_user'):
        '''
        Add new user
        '''
        save_url = self.request.resource_url(self.context, actionname)
        if 'form.submitted' in self.request.params:
            username = self.request.params['username']
            nickname = self.request.params['nickname']
            cintraid = str(int(self.request.params['cintraid']))
            email = self.request.params['email']
            balance = self.request.params['balance']
            points = self.request.params['points']
            experience = self.request.params['experience']
            group = self.request.params['group']
            logging.debug( 'Creating user: %s, cintraid: %s'%(username, cintraid) )
            user = User( username=username, nickname=nickname,
                         cintraid=cintraid, email=email,
                         balance=balance, points=points,
                         experience=experience, group=[group] )
            pwd = self.request.params['pwd']
            pwd2 = self.request.params['pwd2']
            user.__name__ = cintraid
            user.__parent__ = self.context
            warnings = {}
            if pwd <> pwd2:
                warnings['pwd']='password not matching'
                return dict(user=user, save_url=save_url, warnings=warnings)

            user.pwd = saltPeper(pwd)
            self.context[cintraid] = user
            self.context['cintraids'].append(cintraid)
            approot = self.context.__parent__
            bk = Book(user=user)
            approot['books'][cintraid] = [bk]
            user.books = [bk]
            return HTTPFound( location = self.request.resource_url(self.context, cintraid) )

        user = User()
        user.__name__ = ''
        user.__parent__ = self.context
        cintraids = sorted([int(cintraid) for cintraid in self.context])
        user.cintraid = str(int(cintraids[-1])+1)
        user.group = group or ''
        return dict(user=user, save_url=save_url, message={})

    @view_config(context=User, renderer='cintra:templates/view_user.pt')
    def view_user(self):
        user = self.context
        return dict(user=user)

    @view_config(name='edit', context=User, renderer='cintra:templates/edit_user.pt')
    def edit_user(self):
        user = self.context
        save_url = self.request.resource_url(self.context)
        return dict(user=user, save_url=save_url, message={'edit':True})

    @view_config(context=UserFolder, renderer='cintra:templates/view_users.pt')
    def view_users(self):
        return dict(users=self.context.items())

    @view_config(name='login', context=UserFolder, renderer='cintra:templates/login.pt')
    @forbidden_view_config(renderer='cintra:templates/login.pt')
    def login(self):
        login_url = self.request.resource_url(self.request.context, 'login')
        referrer = self.request.url
        if referrer == login_url:
            referrer = '/' # never use the login form itself as came_from
        came_from = self.request.params.get('came_from', referrer)
        message  = ''
        login    = ''
        password = ''
        if 'form.submitted' in self.request.params:
            login = self.request.params['login']
            password = self.request.params['password']
            user = self.context.get(login, None)

            if user and wash(user.pwd) == password:
                headers = remember( self.request, login )
                return HTTPFound(location = came_from, headers = headers )
            message = 'Failed Login'

        return dict( message   = message, 
                     url       = self.request.application_url + '/users/login',
                     came_from = came_from,
                     login     = login,
                     password  = password,
                     )

    @view_config( context=UserFolder, name = 'logout')
    def logout(self):
        headers = forget(self.request)
        return HTTPFound(location=self.request.resource_url(self.context), headers=headers)

