from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APIClient
from .models import StoredString
from .utils import sha256_of

class StringApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_and_get_and_delete(self):
        payload = {"value": "Able was I ere I saw Elba"}
        # create
        res = self.client.post('/strings/', payload, format='json')
        self.assertEqual(res.status_code, 201)
        data = res.json()
        sid = data['id']
        # get by value
        get_res = self.client.get('/strings/' + payload['value'])
        self.assertEqual(get_res.status_code, 200)
        # delete
        del_res = self.client.delete('/strings/' + payload['value'])
        self.assertEqual(del_res.status_code, 204)
        # confirm gone
        get_res2 = self.client.get('/strings/' + payload['value'])
        self.assertEqual(get_res2.status_code, 404)

    def test_conflict_on_duplicate(self):
        payload = {"value": "hello"}
        r1 = self.client.post('/strings/', payload, format='json')
        self.assertEqual(r1.status_code, 201)
        r2 = self.client.post('/strings/', payload, format='json')
        self.assertEqual(r2.status_code, 409)

    def test_list_filtering_and_nl(self):
        # create some strings
        self.client.post('/strings/', {"value": "aba"}, format='json')  # palindrome single word
        self.client.post('/strings/', {"value": "abba"}, format='json')
        self.client.post('/strings/', {"value": "notpalin"}, format='json')
        # filter palindromes
        r = self.client.get('/strings/?is_palindrome=true')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertTrue(data['count'] >= 2)
        # nl filter
        r2 = self.client.get('/strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings')
        self.assertEqual(r2.status_code, 200)
        d2 = r2.json()
        self.assertTrue(d2['count'] >= 2)
