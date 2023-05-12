import unittest
from unittest.mock import patch
from views import apiSearchflight,apiBookflight
from django.shortcuts import render,redirect,reverse
class TestApiSearchflight(unittest.TestCase):

    def test_book_result(self):
        # Create a POST request to the book_result view
        url = reverse('book_result', args=['city1', 'city2', '2022-06-01T10:00:00Z', '123456'])
        response = self.client.post(url)

        # Assert that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # Assert that the redirect URL is correct
        redirect_url = reverse('getpaymentmethods', args=['123456'])
        self.assertEqual(response.url, redirect_url)

        # Create a GET request to the book_result view
        response = self.client.get(url)

        # Assert that the response is OK
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the expected context data
        self.assertContains(response, 'city1')
        self.assertContains(response, 'city2')
        self.assertContains(response, '2022-06-01T10:00:00Z')
        self.assertContains(response, '123456')

    @patch('my_module.requests.get')
    def test_apiSearchflight_success(self, mock_get):
        # Mock the requests.get() function to return a successful response
        mock_response = {'code': 0, 'data': [{'Flight_id': 1}]}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Call the apiSearchflight function with mock data
        result = apiSearchflight(1, 2)

        # Assert that the response matches the expected mock data
        self.assertEqual(result, mock_response)

    @patch('my_module.requests.get')
    def test_apiSearchflight_error(self, mock_get):
        # Mock the requests.get() function to return an error response
        mock_response = 'Error: No flights found'
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = mock_response

        # Call the apiSearchflight function with mock data
        result = apiSearchflight(1, 2)

        # Assert that the response matches the expected mock data
        self.assertEqual(result, mock_response)

    @patch('mymodule.requests.post')
    def test_apiBookflight(self, mock_post):
        expected_result = {"status": "success", "message": "Booking confirmed."}

        # Configure the mock to return a response with status code 200 and our expected JSON response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = expected_result

        # Call the function to be tested
        result = apiBookflight(flight_id=1, seat_id=1, name="John Doe", customer_id=123, email="johndoe@example.com",
                               phone="1234567890")

        # Assert that the mock was called with the correct parameters
        mock_post.assert_called_once_with('http://sc19tq.pythonanywhere.com/api/bookflight/', data={
            "flight_id": 1,
            "seat_id": 1,
            "name": "John Doe",
            "customer_id": 123,
            "email": "johndoe@example.com",
            "phone": "1234567890"
        })

        # Assert that the function returned the expected result
        self.assertEqual(result, expected_result)

    def test_post_request_with_available_seat(self):
        response = self.client.post(self.url, {
            'flight_id': '2',
            'name': 's',
            'customer_id': 's',
            'email': 'power@qq.com',
            'phone': '18750354636',
            'seat_id': 'economy'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_result', args=['New York', 'London', '20230501', '00000001']))

    def test_post_request_with_unavailable_seat(self):
        response = self.client.post(self.url, {
            'flight_id': '3',
            'name': 't',
            'customer_id': 't',
            'email': 'test@test.com',
            'phone': '1234567890',
            'seat_id': 'first'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('noSeatAvai'))

    def test_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flight_result.html')


if __name__ == '__main__':
    unittest.main()
