from django.test import Client, TestCase


class PublicPagesTests(TestCase):
    def test_public_pages_render_with_group_identity(self):
        pages = ('/', '/a-propos/', '/contact/')

        for path in pages:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Groupe Omega et Partenaires')
                self.assertNotContains(response, 'Entité X')

    def test_contact_page_uses_reference_phone_number(self):
        response = self.client.get('/contact/')

        self.assertContains(response, 'tel:+224611384485')
        self.assertContains(response, '+224 611 384 485')

    def test_contact_form_is_protected_by_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(
            '/contact/',
            {'name': 'Test', 'email': 'test@example.com', 'message': 'Bonjour'},
        )

        self.assertEqual(response.status_code, 403)

    def test_security_headers_are_set(self):
        response = self.client.get('/')

        self.assertEqual(response.headers['X-Frame-Options'], 'DENY')
        self.assertEqual(response.headers['X-Content-Type-Options'], 'nosniff')
