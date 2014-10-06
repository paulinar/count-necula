__author__ = 'paulina'

import models
import json
import StringIO
import unittest
import tests

from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotAllowed
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home(request):
    if (request.method == "GET"):
        jsonObj = {
                   'user' : request.user
                  }
        return render_to_response('home.html', jsonObj)
    else: # if "POST" or "PUT" request
        return HttpResponseNotAllowed(['GET']) # 405

@csrf_exempt
def login(request):
    if (request.method == "POST"):
        data = json.loads(request.body)
        myModel = models.UsersModel()
        result = myModel.login(data['user'], data['password'])
        if result == models.SUCCESS or result > 1:
            jsonObj = {
                       'errCode' : models.SUCCESS,
                       'count' : result
                      }
            return HttpResponse(json.dumps(jsonObj), content_type = 'application/json')

        elif result == models.ERR_BAD_CREDENTIALS or result == models.ERR_BAD_PASSWORD or result == models.ERR_BAD_USERNAME or result == models.ERR_USER_EXISTS:
            jsonObj = {
                       'errCode' : result
                      }
            return HttpResponse(json.dumps(jsonObj), content_type = 'application/json')

        else:
            return HttpResponseServerError() # 500

    else: # if any other request, like "GET" or "PUT"
        return HttpResponseNotAllowed(['POST']) # 405
    
@csrf_exempt
def add(request):
    if (request.method == "POST"):
        data = json.loads(request.body)
        myModel = models.UsersModel()
        result = myModel.add(data['user'], data['password'])
        if result == models.SUCCESS or result > 1:
            jsonObj = {
                       'errCode' : models.SUCCESS,
                       'count' : result
                      }
            return HttpResponse(json.dumps(jsonObj), content_type = 'application/json')

        elif result == models.ERR_BAD_CREDENTIALS or result == models.ERR_BAD_PASSWORD or result == models.ERR_BAD_USERNAME or result == models.ERR_USER_EXISTS:
            jsonObj = {
                       'errCode' : result
                      }
            return HttpResponse(json.dumps(jsonObj), content_type = 'application/json')

        else:
            return HttpResponseServerError() # 500

    else: # if any other request, like "GET" or "PUT"
        return HttpResponseNotAllowed(['POST']) # 405

@csrf_exempt
def resetFixture(request):
    if (request.method == "POST"):
        myModel = models.UsersModel()
        result = myModel.TESTAPI_resetFixture()
        jsonObj = {
                   'errCode' : result
                  }
        return HttpResponse(json.dumps(jsonObj), content_type = 'application/json')
    else: # if any other request, like "GET" or "PUT"
        return HttpResponseNotAllowed(['POST']) # 405

@csrf_exempt
def unitTests(request):
    if (request.method == "POST"):

        # guide: http://stackoverflow.com/questions/8308435/how-to-unittest-unittest-testcases

        # Load tests from tests.TestUsers
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(tests.TestUsers)

        # Create runner, and run tests.TestUsers
        io = StringIO.StringIO()
        runner = unittest.TextTestRunner(stream = io, verbosity = 2)
        result = runner.run(suite)

        jsonObj = {
                   'nrFailed' : len(result.failures),
                   'output' : io.getvalue(),
                   'totalTests' : result.testsRun
                  }

        return HttpResponse(json.dumps(jsonObj), content_type = 'application/json')
    else: # if any other request, like "GET" or "PUT"
        return HttpResponseNotAllowed(['POST']) # 405