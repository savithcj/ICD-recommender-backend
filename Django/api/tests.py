from django.test import TestCase
from api import views
from recommendations.models import Code, TreeCode, Rule
from django.test import Client
from django.urls import reverse


class TestAPIs(TestCase):
    #fixtures = ['testdata.json']

    def setUp(self):
        # test data
        self.code0001 = Code.objects.create(code='0001', parent='00', description='0001Desc')
        self.code0000 = Code.objects.create(code='0000', parent='00', description='0000Desc')
        self.code001 = Code.objects.create(code='001', parent='00', description='000Desc')
        self.code000 = Code.objects.create(code='000', children='0000,0001', parent='00', description='000Desc')
        self.code00 = Code.objects.create(code='00', children='000,001', parent='00', description='00Desc')
        self.code0 = Code.objects.create(code='0', children='00', description='0Desc')

        self.code0001 = TreeCode.objects.create(code='0001', parent='00', description='0001Desc')
        self.code0000 = TreeCode.objects.create(code='0000', parent='00', description='0000Desc')
        self.code001 = TreeCode.objects.create(code='001', parent='00', description='000Desc')
        self.code000 = TreeCode.objects.create(code='000', children='0000,0001', parent='00', description='000Desc')
        self.code00 = TreeCode.objects.create(code='00', children='000,001', parent='00', description='00Desc')
        self.code0 = TreeCode.objects.create(code='0', children='00', description='0Desc')

        self.rule1 = Rule.objects.create(lhs='001', rhs='0001')
        self.rule3 = Rule.objects.create(lhs='00', rhs='000')
        self.rule3 = Rule.objects.create(lhs='00', rhs='001')
        self.rule4 = Rule.objects.create(lhs='000,001', rhs='0000')

    def test_rules(self):
        print("\nTesting ListAllRules view")
        client = Client()
        response = client.get('/api/rules/')
        self.assertEqual(response.status_code, 200)

    def test_children(self):
        print("Testing children API")
        client = Client()

        # test existing code
        codeToCheck = "000"
        response = client.get('/api/children/'+codeToCheck+'/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertIn(data[0]['code'], ['0001', '0000'])
        self.assertIn(data[1]['code'], ['0001', '0000'])

        # test non existing code
        codeToCheck = "X00"
        response = client.get('/api/children/'+codeToCheck+'/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 0)

    def test_family(self):
        print("\nTesting family API")
        client = Client()

        # test existing code
        codeToCheck = "000"
        response = client.get('/api/family/'+codeToCheck+'/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['self']['code'], '000')
        self.assertIn(data['siblings'][0]['code'], ['000', '001'])
        self.assertIn(data['siblings'][1]['code'], ['000', '001'])
        self.assertEqual(data['parent']['code'], '00')
        self.assertIn(data['children'][0]['code'], ['0001', '0000'])
        self.assertIn(data['children'][1]['code'], ['0001', '0000'])

        # test existing code
        codeToCheck = "001"
        response = client.get('/api/family/'+codeToCheck+'/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['self']['code'], '001')
        self.assertIn(data['siblings'][0]['code'], ['000', '001'])
        self.assertIn(data['siblings'][1]['code'], ['000', '001'])
        self.assertEqual(data['parent']['code'], '00')
        self.assertEqual(data['children'], [])

        # test non existing code
        codeToCheck = "X00"
        response = client.get('/api/family/'+codeToCheck+'/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['self'], None)
        self.assertEqual(data['siblings'], None)
        self.assertEqual(data['parent'], None)
        self.assertEqual(data['children'], None)

    def test_codeDescription(self):
        print("\nTesting codeDescription API")
        client = Client()

        # test existing code
        codeToCheck = "001"
        response = client.get('/api/codeDescription/'+codeToCheck+'/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['code'], '001')
        self.assertEqual(data['description'], '000Desc')

        # test non-existing code
        codeToCheck = "100"
        response = client.get('/api/codeDescription/'+codeToCheck+'/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data, [None])
