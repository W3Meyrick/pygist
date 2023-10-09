import os
import json
import unittest
import requests_mock
from main import get_gists, save_last_query_time


class MyTestCase(unittest.TestCase):


    def test_get_updated_issues_multiple_pages(self):
        with open("test/gists_test_page_one.json", "r") as issues_first_file:
            mock_response_first_page = issues_first_file.read()

        with open("test/gists_test_page_two.json", "r") as issues_second_file:
            mock_response_second_page = issues_second_file.read()

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'http://api.github.com/users/testuser/gists', [{'text': mock_response_first_page}, {'text': mock_response_second_page}])
            gists = get_gists("testuser")

        self.assertEqual(len(gists), 3)
        self.assertEqual(gists[0]['created_at'], '2023-09-18T16:50:01Z')
        self.assertEqual(gists[1]['created_at'], '2023-09-14T11:57:06Z')
        self.assertEqual(gists[2]['updated_at'], '2023-07-16T13:43:19Z')

    def test_save_last_query_time(self):
        temp_file = 'tempfile.txt'

        sample_gist = [{'created_at': '2023-10-02T12:00:00Z'}]

        save_last_query_time('testuser', sample_gist)

        with open('pygist.testuser', 'r') as user_file:
            timestamp = user_file.read()
        self.assertEqual(timestamp, '2023-10-02T12:00:00Z')

        os.remove('pygist.testuser')