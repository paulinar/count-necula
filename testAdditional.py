__author__ = 'paulina'

import unittest
import os
import testLib

class TestLoginUser(testLib.RestTestCase):
    """Test user logins"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testLoginOnce(self):
        jsonObj = {
                    'user' : 'joe',
                    'password' : 'mypassword'
                  }
        respData = self.makeRequest("/users/add",
                                    method = "POST",
                                    data = jsonObj)
        respData = self.makeRequest("/users/login",
                                    method = "POST",
                                    data = jsonObj)
        self.assertResponse(respData, count = 2)

    def testLoginFiveTimes(self):
        jsonObj = {
                    'user' : 'jane',
                    'password' : 'mypassword'
                  }
        respData = self.makeRequest("/users/add",
                                    method = "POST",
                                    data = jsonObj)
        respData = self.makeRequest("/users/login",
                                    method = "POST",
                                    data = jsonObj)
        respData = self.makeRequest("/users/login",
                                    method = "POST",
                                    data = jsonObj)
        respData = self.makeRequest("/users/login",
                                    method = "POST",
                                    data = jsonObj)
        respData = self.makeRequest("/users/login",
                                    method = "POST",
                                    data = jsonObj)
        respData = self.makeRequest("/users/login",
                                    method = "POST",
                                    data = jsonObj)
        self.assertResponse(respData, count = 6)

    def testLoginBadUsernameCredential(self):
        actual_entry    = {
                           'user' : 'valid_username',
                           'password' : 'valid_password'
                          }
        attempted_entry = {
                           'user' : 'invalid_username',
                           'password' : 'valid_password'
                          }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = actual_entry)
        respData = self.makeRequest("/users/login",
                                    method="POST",
                                    data = attempted_entry)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def testLoginBadPasswordCredential(self):
        actual_entry    = {
                           'user' : 'they_know_my_username',
                           'password' : 'valid_password'
                          }
        attempted_entry = {
                           'user' : 'they_know_my_username',
                           'password' : 'invalid_password'
                          }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = actual_entry)
        respData = self.makeRequest("/users/login",
                                    method="POST",
                                    data = attempted_entry)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def testLoginBadCredentialsBothFields(self):
        jsonObj = {
                    'user' : 'nonexistent_victim',
                    'password' : 'imtrying2haxx'
                  }
        respData = self.makeRequest("/users/login",
                                    method="POST",
                                    data = jsonObj)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def testLoginUsernameCaseSensitivity(self):
        actual_entry    = {
                           'user' : 'aPPLe',
                           'password' : 'password'
                          }
        attempted_entry = {
                           'user' : 'apple',
                           'password' : 'password'
                          }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = actual_entry)
        respData = self.makeRequest("/users/login",
                                    method="POST",
                                    data = attempted_entry)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def testLoginPasswordCaseSensitivity(self):
        actual_entry    = {
                           'user' : 'cherry',
                           'password' : 'passWORD'
                          }
        attempted_entry = {
                           'user' : 'cherry',
                           'password' : 'password'
                          }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = actual_entry)
        respData = self.makeRequest("/users/login",
                                    method="POST",
                                    data = attempted_entry)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_CREDENTIALS)

# in addition to the TestAddUser tests in testSimple.py
class TestAddUser(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testAddNoUsername1(self):
        jsonObject =  {
                        'user' : '',
                        'password' : 'abc123'
                      }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObject)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_USERNAME)

    def testAddNoUsername2(self):
        jsonObject =  {
                        'user' : None,
                        'password' : 'abc123'
                      }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObject)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_USERNAME)

    def testAddLongUsername(self):
        original_username = "thisistoolong"
        longer_username = original_username*10
        jsonObject =  {
                        'user' : longer_username,
                        'password' : 'abc123'
                      }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObject)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_USERNAME)

    def testAddNoPassword(self):
        jsonObject =  {
                        'user' : 'katrina',
                        'password' : ''
                      }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObject)
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testAddNonePassword(self):
        jsonObject =  {
                        'user' : 'susan',
                        'password' : None
                      }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObject)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_PASSWORD)

    def testAddLongPassword(self):
        original_password = "thisistoolong"
        longer_password = original_password*10
        jsonObject =  {
                        'user' : 'susan',
                        'password' : longer_password
                      }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObject)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_PASSWORD)

    def testAddLongUsernameAndPassword(self):
        original_username = "thisistoolong"
        longer_username = original_username*10
        original_password = "thisisalsotoolong"
        longer_password = original_password*10

        jsonObject =  {
                        'user' : longer_username,
                        'password' : longer_password
                      }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObject)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_USERNAME)

    def testAddEmptyUsernameAndPassword(self):
        jsonObject =  {
                        'user' : '',
                        'password' : ''
                      }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObject)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_USERNAME)

    def testAddNoneUsernameAndPassword(self):
        jsonObject =  {
                        'user' : None,
                        'password' : None
                      }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObject)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_USERNAME)


    def testAddUserExists(self):
        original_user =  {
                          'user' : 'cutie_paco',
                          'password' : 'woof'
                         }
        copycat_user =   {
                          'user' : 'cutie_paco',
                          'password' : 'arf'
                         }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = original_user)
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = copycat_user)
        self.assertResponse(respData, None, testLib.RestTestCase.ERR_USER_EXISTS)

    def testAdd2(self):
        jsonObj1 = {
                    'user' : 'mariii',
                    'password' : 'poopyyy'
                   }
        jsonObj2 = {
                    'user' : 'kuma',
                    'password' : 'adorableson'
                   }
        respData1 = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObj1)
        respData2 = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObj2)
        self.assertResponse(respData1, count = 1)
        self.assertResponse(respData2, count = 1)

    def testAddUsernameCaseSensitivity(self):
        jsonObj1 = {
                    'user' : 'banker',
                    'password' : 'monies'
                   }
        jsonObj2 = {
                    'user' : 'BANKER',
                    'password' : 'monies'
                   }
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObj1)
        respData = self.makeRequest("/users/add",
                                    method="POST",
                                    data = jsonObj2)
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

class TestResetFixture(testLib.RestTestCase):
    """Test database resets"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode  }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testResetFixture(self):
        respData = self.makeRequest("/TESTAPI/resetFixture", method="POST")
        self.assertResponse(respData, None, testLib.RestTestCase.SUCCESS)