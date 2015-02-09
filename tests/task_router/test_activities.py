from datetime import datetime
import unittest

from mock import patch, Mock
import pytz

from tests.tools import create_mock_json
from twilio.rest.resources.task_router.activities import Activities, Activity

AUTH = ("AC123", "token")
BASE_URI = "https://taskrouter.twilio.com/v1/Accounts/AC123/Workspaces/WSaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ACTIVITY_SID = "WAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


class ActivityTest(unittest.TestCase):
    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_create(self, request):
        resp = create_mock_json('tests/resources/task_router/activities_instance.json')
        resp.status_code = 201
        request.return_value = resp

        activities = Activities(BASE_URI, AUTH)
        activity = activities.create("Test Activity", True)
        self.assertIsNotNone(activity)
        self.assertEqual(activity.date_created, datetime(2014, 5, 14, 10, 50, 2, tzinfo=pytz.utc))
        exp_params = {
            'FriendlyName': "Test Activity",
            'Available': "true"
        }

        request.assert_called_with("POST", "{}/Activities".format(BASE_URI), data=exp_params, auth=AUTH)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_delete_instance(self, request):
        resp = Mock()
        resp.content = ""
        resp.status_code = 204
        request.return_value = resp

        uri = "{}/Activities/{}".format(BASE_URI, ACTIVITY_SID)
        list_resource = Activities(BASE_URI, AUTH)
        activity = Activity(list_resource, ACTIVITY_SID)
        activity.delete()
        request.assert_called_with("DELETE", uri, auth=AUTH)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_delete_list(self, request):
        resp = Mock()
        resp.content = ""
        resp.status_code = 204
        request.return_value = resp

        uri = "{}/Activities/{}".format(BASE_URI, ACTIVITY_SID)
        list_resource = Activities(BASE_URI, AUTH)
        list_resource.delete(ACTIVITY_SID)
        request.assert_called_with("DELETE", uri, auth=AUTH)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_get(self, request):
        resp = create_mock_json('tests/resources/task_router/activities_instance.json')
        resp.status_code = 200
        request.return_value = resp

        uri = "{}/Activities/{}".format(BASE_URI, ACTIVITY_SID)
        list_resource = Activities(BASE_URI, AUTH)
        list_resource.get(ACTIVITY_SID)
        request.assert_called_with("GET", uri, auth=AUTH)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_list(self, request):
        resp = create_mock_json('tests/resources/task_router/activities_list.json')
        resp.status_code = 200
        request.return_value = resp

        uri = "{}/Activities".format(BASE_URI)
        list_resource = Activities(BASE_URI, AUTH)
        list_resource.list()
        request.assert_called_with("GET", uri, params={}, auth=AUTH)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_update_instance(self, request):
        resp = create_mock_json('tests/resources/task_router/activities_instance.json')
        resp.status_code = 201
        request.return_value = resp

        uri = "{}/Activities/{}".format(BASE_URI, ACTIVITY_SID)
        list_resource = Activities(BASE_URI, AUTH)
        activity = Activity(list_resource, ACTIVITY_SID)
        activity.update(friendly_name='Test Activity', available=True)
        exp_params = {
            'FriendlyName': "Test Activity",
            'Available': "true"
        }

        request.assert_called_with("POST", uri, data=exp_params, auth=AUTH)

    @patch('twilio.rest.resources.base.make_twilio_request')
    def test_update_list(self, request):
        resp = create_mock_json('tests/resources/task_router/activities_instance.json')
        resp.status_code = 201
        request.return_value = resp

        uri = "{}/Activities/{}".format(BASE_URI, ACTIVITY_SID)
        list_resource = Activities(BASE_URI, AUTH)
        list_resource.update(ACTIVITY_SID, friendly_name='Test Activity', available="true")
        exp_params = {
            'FriendlyName': "Test Activity",
            'Available': "true"
        }

        request.assert_called_with("POST", uri, data=exp_params, auth=AUTH)
