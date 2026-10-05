from django.test import Client, TestCase, override_settings


@override_settings(
    STORAGES={
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
)
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

    def test_site_displays_the_provided_logo(self):
        response = self.client.get('/')

        self.assertContains(response, 'img/groupe-omega-embleme.png')
        self.assertContains(response, 'img/groupe-omega-logo.png')

    def test_homepage_lists_all_six_domains_with_original_illustrations(self):
        response = self.client.get('/')

        for domain, image in (
            ('BTP', 'btp.svg'),
            ('Énergie', 'energie.svg'),
            ('Mines', 'mines.svg'),
            ('Immobilier', 'immobilier.svg'),
            ('Négoce', 'negoce.svg'),
            ('Conseil', 'conseil.svg'),
        ):
            with self.subTest(domain=domain):
                self.assertContains(response, domain)
                self.assertContains(response, f'img/services/{image}')

    def test_homepage_carousel_autoplays_every_five_seconds(self):
        response = self.client.get('/')

        for image in (
            'hero-btp.jpg',
            'hero-energie.jpg',
            'hero-mines.jpg',
            'hero-immobilier.jpg',
            'hero-negoce.jpg',
            'hero-conseil.jpg',
        ):
            with self.subTest(image=image):
                self.assertContains(response, f'img/services/{image}')
        self.assertContains(response, 'data-hero-carousel')
        self.assertNotContains(response, 'id="services-track"')
        self.assertContains(response, 'const autoplayInterval = 5000;')

    def test_site_uses_a_locally_hosted_mixed_case_font(self):
        response = self.client.get('/')

        self.assertContains(response, "font-family: 'Manrope'")
        self.assertContains(response, 'fonts/manrope-latin.woff2')
        self.assertNotContains(response, 'fonts.googleapis.com')

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
