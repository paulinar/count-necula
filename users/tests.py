"""
Unit tests for the server.py module.
This is just a sample. You should have more tests for your model (at least 10)
"""

import unittest
import sys
import models
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'logincounter.settings'
import django
django.setup()

class TestUsers(unittest.TestCase):
    """
    Unittests for the UsersModel class
    """

    users = models.UsersModel()
        
    def testAdd1(self):
        """
        Tests that adding a user works
        """
        self.assertEquals(models.SUCCESS, self.users.add("userA", "password"))

    def testAddExists(self):
        """
        Tests that adding a duplicate user name fails
        """
        self.assertEquals(models.SUCCESS, self.users.add("userB", "password"))
        self.assertEquals(models.ERR_USER_EXISTS, self.users.add("userB", "password"))

    def testAdd2(self):
        """
        Tests that adding two users works
        """
        self.assertEquals(models.SUCCESS, self.users.add("userC", "password"))
        self.assertEquals(models.SUCCESS, self.users.add("userD", "password"))

    def testAddEmptyUsername(self):
        """
        Tests that adding an user with empty username fails
        """
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.add("", "password"))

    def testAddAndDatabaseUpdates(self):
        """
        Test that database reflects newly added user
        """
        self.users.TESTAPI_resetFixture()
        self.assertEqual(len(models.UsersModel.objects.all()), 0)
        self.users.add("count", "necula")
        self.assertEqual(len(models.UsersModel.objects.all()), 1)
        self.users.add("george", "necula")
        self.assertEqual(len(models.UsersModel.objects.all()), 2)

#############################################
##                                         ##
##  additional unit tests for adding users ##
##                                         ##
#############################################

    def testAddEmptyPassword(self):
        """
        Tests that adding a user with empty password doesn't fail
        """
        self.assertEquals(models.SUCCESS, self.users.add("userE", ""))

    def testAddNonePassword(self):
        """
        Tests that adding a user with a None password fails
        """
        self.assertEquals(models.ERR_BAD_PASSWORD, self.users.add("userF", None))

    def testAddNoneUsername(self):
        """
        Tests that adding a user with a None username fails
        """
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.add(None, "password"))

    def testAddNoneUsernameAndPassword(self):
        """
        Tests that adding a user with both username and password as None fails
        """
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.add(None, None))

    def testAddNoneUsernameAndPassword(self):
        """
        Tests that adding a user with both a blank username and password fails
        """
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.add("", ""))

    def testAddLongUsername(self):
        """
        Tests that adding a user with a long username fails
        """
        original_username = "thiswillbelong"
        longer_username = original_username*10
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.add(longer_username, "password"))

    def testAddLongPassword(self):
        """
        Tests that adding a user with a long password fails
        """
        original_password = "thiswillbelong"
        longer_password = original_password*10
        self.assertEquals(models.ERR_BAD_PASSWORD, self.users.add("paulinarocks", longer_password))

    def testAddLongUsernameAndPassword(self):
        """
        Tests that adding a user with both a long username and long password fails
        """
        original_username = "thisgonnabelong"
        longer_username = original_username*10
        original_password = "thisalsogonnabelong"
        longer_password = original_password*10
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.add(longer_username, longer_password))

#############################################
##                                         ##
##  additional unit tests for user logins  ##
##                                         ##
#############################################

    def testLogin(self):
        """
        Tests that user login works
        """
        self.assertEquals(models.SUCCESS, self.users.add("userG", "password"))
        self.assertTrue(self.users.login("userG", "password"))

    def testLoginTwice(self):
        """
        Tests that user login works for multiple logs
        """
        self.assertEquals(models.SUCCESS, self.users.add("userG2", "password"))
        self.assertEquals(self.users.login("userG2", "password"), 2)
        self.assertEquals(self.users.login("userG2", "password"), 3)

    def testLoginUsername(self):
        """
        Tests that logging in with invalid username fails
        """
        self.assertEquals(models.SUCCESS, self.users.add("userH", "password"))
        self.assertEquals(models.ERR_BAD_CREDENTIALS, self.users.login("userHX", "password"))

    def testLoginPassword(self):
        """
        Tests that logging in with invalid password fails
        """
        self.assertEquals(models.SUCCESS, self.users.add("userI", "password"))
        self.assertEquals(models.ERR_BAD_CREDENTIALS, self.users.login("userI", "passw0rd"))

    def testLoginBadUsernameAndPassword(self):
        """
        Tests that logging in with both an invalid username and invalid password fails
        """
        self.assertEquals(models.SUCCESS, self.users.add("userJ", "password"))
        self.assertEquals(models.ERR_BAD_CREDENTIALS, self.users.login("nobody_user", "nobody_password"))

    def testLoginTwoUniqueUsersConsecutively(self):
        """
        Ensure that adding and logging in another user after logging in another user doesn't
        mess up previous user's login count
        """
        self.users.TESTAPI_resetFixture()

        self.users.add("happy", "birthday")
        self.users.login("happy", "birthday")
        self.users.login("happy", "birthday")
        respData = self.users.login("happy", "birthday")
        self.assertEquals(respData, 4)

        self.users.add("merry", "christmas")
        respData = self.users.login("merry", "christmas")
        self.assertEquals(respData, 2)
        respData = self.users.login("happy", "birthday")
        self.assertEquals(respData, 5)

########################################
##                                    ##
##  additional unit tests for resets  ##
##                                    ##
########################################

    def testResetFixture(self):
        """
        Another test to test database reset
        """
        self.users.TESTAPI_resetFixture()
        self.users.add("katie", "password")
        self.assertEqual(len(models.UsersModel.objects.all()), 1)
        self.users.TESTAPI_resetFixture()
        self.assertEqual(len(models.UsersModel.objects.all()), 0)

# If this file is invoked as a Python script, run the tests in this module
if __name__ == "__main__":
    # Add a verbose argument
    sys.argv = [sys.argv[0]] + ["-v"] + sys.argv[1:]
    unittest.main()