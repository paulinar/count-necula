__author__ = 'paulina'

from django.db import models

SUCCESS = 1
ERR_BAD_CREDENTIALS = -1
ERR_USER_EXISTS = -2
ERR_BAD_USERNAME = -3
ERR_BAD_PASSWORD = -4
MAX_USERNAME_LENGTH = 128
MAX_PASSWORD_LENGTH = 128



class UsersModel(models.Model):

    user = models.CharField(max_length = 128)
    password = models.CharField(max_length = 128)
    count = models.PositiveIntegerField(default = 1)

    # checks: user doesn't already exist & username not empty
    def add(self, user, password):

	    # checks if username invalid
        if not valid_user(user):
            return ERR_BAD_USERNAME

        # checks if password invalid
        if not valid_password(password):
            return ERR_BAD_PASSWORD

        # checks if username + password invalid
        if not valid_user(user) and not valid_password(password):
            return ERR_BAD_USERNAME

        # checks if user already exists in db
        if UsersModel.objects.filter(user = user).exists():
            return ERR_USER_EXISTS

        else:
            newUser = UsersModel(user = user, password = password)
            newUser.save()
            return newUser.count


    # checks user/pw in database (case sensitive)
    def login(self, user, password):
        # On success, updates the count of logins in the database.
        # On success, result is the count of logins (including this one) (>= 1)
        # On failure, result is ERR_BAD_CREDENTIALS (-1)
        try:
            myUser = UsersModel.objects.get(user = user, password = password)
            myUser.count += 1
            myUser.save()
            return myUser.count
        except UsersModel.DoesNotExist: # DoesNotExist is an attribute of the Model class
            return ERR_BAD_CREDENTIALS


    # for testing only
    def TESTAPI_resetFixture(self):
        UsersModel.objects.all().delete() # delete all rows in database
        return SUCCESS


def valid_user(user):
    if user == '' or user == None or len(user) > MAX_USERNAME_LENGTH or len(user) == 0:
        return False
    return True


def valid_password(password):
    if password == None or len(password) > MAX_PASSWORD_LENGTH:
        return False
    return True