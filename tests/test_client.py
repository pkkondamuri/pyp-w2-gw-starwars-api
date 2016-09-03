import responses

from tests import BaseStarWarsAPITestCase
from starwars_api.exceptions import SWAPIClientError


class ClientTestCase(BaseStarWarsAPITestCase):

    @responses.activate
    def test_api_client_get_people_id(self):
        luke = self.api_client.get_people(1)
        self.assertEqual(luke['name'], 'Luke Skywalker')
        self.assertEqual(luke['name'], 'Luke Skywalker')
        self.assertEqual(luke['height'], '172')
        self.assertEqual(luke['mass'], '77')
        self.assertEqual(luke['hair_color'], 'blond')
        self.assertEqual(luke['skin_color'], 'fair')
        self.assertEqual(luke['eye_color'], 'blue')
        self.assertEqual(luke['birth_year'], '19BBY')
        self.assertEqual(luke['gender'], 'male')
    

    @responses.activate
    def test_api_client_get_people(self):
        resp = self.api_client.get_people()
        for key in ['count', 'next', 'previous', 'results']:
            self.assertTrue(key in resp)
        self.assertEqual(len(resp['results']), 10)
        self.assertEqual(resp['results'][0]['name'], 'Luke Skywalker')

    @responses.activate
    def test_api_client_get_people_custom_page(self):
        resp = self.api_client.get_people(**{'page': 2})
        for key in ['count', 'next', 'previous', 'results']:
            self.assertTrue(key in resp)
        self.assertEqual(len(resp['results']), 5)
        self.assertEqual(resp['results'][0]['name'], 'Anakin Skywalker')

    @responses.activate
    def test_api_client_get_people_page_not_found(self):
        error = ('Request to SWAPI "/api/people" failed with status "404". '
                 'Reason: {"detail": "Not found"}')
        with self.assertRaisesRegexp(SWAPIClientError, error):
            self.api_client.get_people(**{'page': 3})

    @responses.activate
    def test_api_client_get_films_id(self):
        film = self.api_client.get_films(1)
        self.assertEqual(film['title'], 'A New Hope')
        self.assertEqual(film['episode_id'], 4)
        self.assertEqual(film['director'], 'George Lucas')
        self.assertEqual(film['producer'], 'Gary Kurtz, Rick McCallum')
        self.assertEqual(film['release_date'], '1977-05-25')

    @responses.activate
    def test_api_client_get_films(self):
        resp = self.api_client.get_films()
        for key in ['count', 'next', 'previous', 'results']:
            self.assertTrue(key in resp)
        self.assertEqual(len(resp['results']), 7)
        self.assertEqual(resp['results'][0]['title'], 'A New Hope')

    @responses.activate
    def test_api_client_get_films_page_not_found(self):
        error = ('Request to SWAPI "/api/films" failed with status "404". '
                 'Reason: {"detail": "Not found"}')
        with self.assertRaisesRegexp(SWAPIClientError, error):
            self.api_client.get_films(**{'page': 2})
