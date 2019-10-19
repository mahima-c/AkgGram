from django.core import signing
#from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User,Group
from django.conf import settings as django_settings
from rest_framework.authtoken.models import Token
from insta.models import Profile
from insta.auth import settings as auth_settings
import re

class AuthTools:
    #"auth tool"
    password_salt = auth_settings.AUTH_PASSWORD_SALT
    token_age = auth_settings.AUTH_TOKEN_AGE

    @staticmethod
    def issue_user_token(user,salt):
       # "issue token for user"
       if user is not None:
            if (salt == 'login'):
               token,_=Token.objects.get_or_create(user=user)
            else:
               token = signing.dumps({'pk':user.pk},salt=salt)
            return token


       return None

    @staticmethod
    def get_user_from_token(token,salt):
        '''verify token '''
        try:
            value = signing.loads(token, salt = AuthTools.password_salt,max_age=900)
        except signing.SignatureExpired:
            return None
        except signing.BadSignature:
            return None

        user = User.objects.get(pk=value['pk'])        

        if user is not None:
            return 
            
        return None    

    @staticmethod
    def sent_registration_email(user):
        '''send email'''
        html_template ='email/welcome_email_confirmation.html'    

        context = {
            'username': user.username,
            'email': user.email,
        }
    @staticmethod
    def authenticate(username,password):
        '''authenticate user by username'''
        try:
            user = authenticate(username=username,password=password)
            if user is not None:
                return user
        except:
            pass   

        return None     

    @staticmethod
    def authenticate_email(email,password):
        #check email is valid 
        if re.match(r'[^@]+@[^@]+\.[^@]+',email):
            user = AuthTools.get_user_by_email(email)
            if user is not None:
                return AuthTools.authenticate(user.username,password)
        else:
            #as username
            return AuthTools.authenticate(email,password)

    @staticmethod 
    def get_user_by_email(email):
        '''get user by email'''
        if email:
            try:
                user = User.objects.filter(email=email,is_active=True)[0]
                return user

            except:
                pass
        return None    

    @staticmethod 
    def get_user_by_username(username):
        '''get user by username'''
        if username:
            try:
                user = User.objects.filter(username=username,is_active=True)[0]
                return user

            except:
                pass
        return None    

    @staticmethod
    def login(request,user):
        if user is not None:
            try:
                login(request,user)
                return True
            except Exception as ex:
                template = "An exeption of type{0} ocuured.Arguments:\n{1!r}"
                message = template.formate(type(ex).__name__,ex.args)
        return False


    @staticmethod
    def logout(request,user):
        if request:
            try:
                Token.objects.filter(user=request.user).delete()     
                logout(request)
                return True
            #except Exception, e:
                #print e
                #pass
            except:
                pass    


        return False    

    @staticmethod
    def register(user_data,profile_data,Group):
        '''
        register user:
        user_data={username,email,password}
        profile data= role position'''
        user_data['email']= user_data['email']
        user_data['username']= user_data['username']

        try:
            #determine if email exist
            user_exists = User.objects.filter(email=user_data['email'])
            if user_exists:
                return {
                    'user': user_exists[0],
                    'is_new':False
    
                }
            #username check
            username_exists = User.objects.filter(username=user_data['username'])
            if username_exists:
                return {
                    'user': username_exists[0],
                    'is_new':False
                }

            user = User.objects.create_user(**user_data)

            profile_data['user'] = user
            profile = Profile(**profile_data)
            profile.save()

            group = Group.objects.get(name=group)
            group.user_set.add(user)
            #AuthTools.send_registration_email(user)
            return {
                    'user': user,
                    'is_new':True
                }
        #except Exception , e:
            #print str(e) 
            #raise Exception(e.message)  
        except:
            pass
        return False 


    @staticmethod
    def validate_username(username):
        min_username_length = 3
        stats = 'invalid'

        if len(username) < min_username_length:
            stats = 'invalid'
        elif re.match("^[a-zA-Z0-9_-]+$",username) is None:
            stats = 'invalid'
        else:
            user = AuthTools.get_user_by_username(username)

            if user is not None:
                stats = 'taken'        

        return stats   


    @staticmethod
    def validate_email(email):
        '''validate the email'''
        status ='valid'

        try:
            validate_email(email)    
            user = AuthTools.get_user_by_email(email)

            if user is not None:
                status = 'taken'

        except:
            status = "invalid"  

        return status

    @staticmethod
    def validate_password(password):
        min_password_length = 7
        is_valid = True

        if len(password) < min_password_length:
            is_valid= False

        return is_valid               








               

