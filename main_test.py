from io import BytesIO
import json
import unittest
import requests

from PIL import Image

from app import app, init_app

TEST_SCHEDULES = {
    "aaardvark": {
        "classes": [
            [
                { "period": "A", "room": "TALI-206", "name": "Advanced Spanish: Literature", "teacher_username": "kviolette", "department": "Spanish"},
                { "period": "B","room": "TMAC-300", "name": "PE: Customized Training to Maximize Performance (US)", "teacher_username": "mhayes", "department": "Physical Education" },
                { "period": "C", "room": "TMAC-103", "name": "Advanced Chemistry", "teacher_username": "aduffy", "department": "Science" }, 
                { "period": "D", "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, },   
                { "period": "E", "room": "TALI-202A", "name": "American Literature", "teacher_username": "jlarner-lewis", "department": "English" },
                { "period": "F", "room": "TALI-207", "name": "United States History: The American Question", "teacher_username": "cmclane", "department": "History/Social Science" },
                { "period": "G", "room": "TALI-305", "name": "Physics", "teacher_username": "akruger", "department": "Science" },
                { "period": "H", "room": "FG-202", "name": "Advanced Calculus", "teacher_username": "jkaminsky", "department": "Mathematics" }           
            ], 
            [
                { "period": "A", "room": "TALI-206", "name": "Advanced Spanish: Literature", "teacher_username": "kviolette", "department": "Spanish"  }, 
                { "period": "B", "room": "FG-202", "name": "Advanced Calculus", "teacher_username": "jkaminsky", "department": "Mathematics" },
                { "period": "C", "room": "TMAC-103", "name": "Advanced Chemistry", "teacher_username": "aduffy", "department": "Science" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "D" },
                { "period": "E", "room": "TALI-202A", "name": "American Literature", "teacher_username": "jlarner-lewis", "department": "English" },
                { "period": "F", "room": "TALI-207", "name": "United States History: The American Question", "teacher_username": "cmclane", "department": "History/Social Science" },  
                { "period": "G", "room": "TALI-305", "name": "Physics", "teacher_username": "akruger", "department": "Science" }, 
                { "period": "H", "room": "TMAC-300", "name": "PE: Customized Training to Maximize Performance (US)", "teacher_username": "mhayes", "department": "Physical Education" },
                { "period": "H", "room": "FG-202", "name": "Advanced Calculus", "teacher_username": "jkaminsky", "department": "Mathematics"               }
            ],
            [
                { "period": "A", "room": "TALI-206", "name": "Advanced Spanish: Literature", "teacher_username": "kviolette", "department": "Spanish" },
                { "period": "B", "room": "MS-101", "name": "Advanced Programming: Topics in Computer Science", "teacher_username": "gmein", "department": "Technology" },
                { "period": "C", "room": "TMAC-103", "name": "Advanced Chemistry", "teacher_username": "aduffy", "department": "Science" }, 
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "D" },
                { "period": "E", "room": "TALI-202A", "name": "American Literature", "teacher_username": "jlarner-lewis", "department": "English" },
                { "period": "F", "room": "TALI-207", "name": "United States History: The American Question", "teacher_username": "cmclane", "department": "History/Social Science" },
                { "period": "G", "room": "TALI-305", "name": "Physics", "teacher_username": "akruger", "department": "Science" },
                { "period": "H", "room": "FG-202", "name": "Advanced Calculus", "teacher_username": "jkaminsky", "department": "Mathematics" }
            ]
        ],
        "sid": 1,
        "nickname": None,
        "firstname": "Anthony",
        "lastname": "Aardvark",
        "gradyear": 2022,
        "username": "aaardvark",
        "advisor": "zzebra",
        "grade": 11
    },
    "bbison": {
        "classes": [
            [
                { "period": "A", "room": "TALI-206", "name": "Advanced Spanish: Literature", "teacher_username": "kviolette", "department": "Spanish"},
                { "period": "B","room": "TMAC-300", "name": "PE: Customized Training to Maximize Performance (US)", "teacher_username": "mhayes", "department": "Physical Education" },
                { "period": "C", "room": "TMAC-103", "name": "Advanced Chemistry", "teacher_username": "aduffy", "department": "Science" }, 
                { "period": "D", "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, },   
                { "period": "E", "room": "TALI-202A", "name": "American Literature", "teacher_username": "jlarner-lewis", "department": "English" },
                { "period": "F", "room": "TALI-207", "name": "United States History: The American Question", "teacher_username": "cmclane", "department": "History/Social Science" },
                { "period": "G", "room": "TALI-305", "name": "Physics", "teacher_username": "akruger", "department": "Science" },
                { "period": "H", "room": "FG-202", "name": "Advanced Calculus", "teacher_username": "jkaminsky", "department": "Mathematics" }           
            ], 
            [
                { "period": "A", "room": "TALI-206", "name": "Advanced Spanish: Literature", "teacher_username": "kviolette", "department": "Spanish"  }, 
                { "period": "B", "room": "FG-202", "name": "Advanced Calculus", "teacher_username": "jkaminsky", "department": "Mathematics" },
                { "period": "C", "room": "TMAC-103", "name": "Advanced Chemistry", "teacher_username": "aduffy", "department": "Science" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "D" },
                { "period": "E", "room": "TALI-202A", "name": "American Literature", "teacher_username": "jlarner-lewis", "department": "English" },
                { "period": "F", "room": "TALI-207", "name": "United States History: The American Question", "teacher_username": "cmclane", "department": "History/Social Science" },  
                { "period": "G", "room": "TALI-305", "name": "Physics", "teacher_username": "akruger", "department": "Science" }, 
                { "period": "H", "room": "TMAC-300", "name": "PE: Customized Training to Maximize Performance (US)", "teacher_username": "mhayes", "department": "Physical Education" },
                { "period": "H", "room": "FG-202", "name": "Advanced Calculus", "teacher_username": "jkaminsky", "department": "Mathematics"               }
            ],
            [
                { "period": "A", "room": "TALI-206", "name": "Advanced Spanish: Literature", "teacher_username": "kviolette", "department": "Spanish" },
                { "period": "B", "room": "MS-101", "name": "Advanced Programming: Topics in Computer Science", "teacher_username": "gmein", "department": "Technology" },
                { "period": "C", "room": "TMAC-103", "name": "Advanced Chemistry", "teacher_username": "aduffy", "department": "Science" }, 
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "D" },
                { "period": "E", "room": "TALI-202A", "name": "American Literature", "teacher_username": "jlarner-lewis", "department": "English" },
                { "period": "F", "room": "TALI-207", "name": "United States History: The American Question", "teacher_username": "cmclane", "department": "History/Social Science" },
                { "period": "G", "room": "TALI-305", "name": "Physics", "teacher_username": "akruger", "department": "Science" },
                { "period": "H", "room": "FG-202", "name": "Advanced Calculus", "teacher_username": "jkaminsky", "department": "Mathematics" }
            ]
        ],
        "sid": 2,
        "nickname": None,
        "firstname": "Billy",
        "lastname": "Bison",
        "gradyear": 2023,
        "username": "bbison",
        "advisor": "zzebra",
        "grade": 10
    },
    "jbriggs": {
        "classes": [
            [
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "A" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "B" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "C" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "D" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "E" },
                { "period": "F", "room": "TMAC-205A", "name": "Calculus", "teacher_username": "sfassino", "department": "Mathematics" }, 
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "G" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "H" }
            ],
            [
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "A" },
                { "period": "B", "room": "TMAC-007", "name": "Evolution of Society: Economics & Technology", "teacher_username": "mdelaney", "department": "Interdisciplinary Electives" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "C" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "D" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "E" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "F" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "G" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "H" }
            ],
            [
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "A" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "B" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "C" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "D" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "E" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "F" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "G" },
                { "room": None, "name": "Free Period", "teacher": None, "teacher_username": None, "department": None, "period": "H" }
            ]
        ],
        "sid": 106,
        "nickname": None,
        "firstname": "Jonathan",
        "lastname": "Briggs",
        "gradyear": None,
        "username": "jbriggs",
        "advisor": None,
        "grade": None
    },
}


TEST_MASTER_SCHEDULE = [{
    "2020-09-09": "Remote A-D_Rem",
}]


TEST_TEACHER = "jbriggs"
TEST_STUDENT = "aaardvark"
TEST_STUDENT_NO_PIC = "bbison"


class FakeKey:
    def __init__(self, name):
        self.name = name


class FakeEntity:
    def __init__(self, key):
        self.key = key
    def get(self, prop):
        return self.key.name != TEST_STUDENT_NO_PIC
    def items(self):
        return { x: self.get(x) for x in ['share_photo', 'share_schedule']}


class FakeDatastore:
    def key(self, a, b):
        return FakeKey(b)
    def get(self, key):
        return FakeEntity(key)
    def get_multi(self, keys):
        return [FakeEntity(key) for key in keys]


TEST_CONFIG = {
    'TESTING': True,
    'SECRET_KEY': bytearray('test-key', 'ascii'),
    'TOKEN': 'test-token',
    'SCHEDULES': TEST_SCHEDULES,
    'MASTER_SCHEDULE': TEST_MASTER_SCHEDULE,
    'DATASTORE': FakeDatastore()
}


API_ENDPOINTS = [
    "/student/aaardvark",
    "/class/a",
    "/period/a",
    "/search/aaardvark"
]

class NoAuthTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        init_app(TEST_CONFIG)
        self.client = app.test_client()

    # Test that when not logged in, we're given a sign-in page.
    def test_main_login_response(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # TODO kinda fragile
        self.assertIn("Sign in to EPSchedule", str(response.data))

    # Test that when not logged in, all API endpoints fail with a 403.
    def test_api_unauthorized(self):
        for endpoint in API_ENDPOINTS:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 403)


AUTHENTICATED_USER = "aaardvark"

class AuthenticatedTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        init_app(TEST_CONFIG)
        self.client = app.test_client()
        with self.client.session_transaction() as sess:
            sess["username"] = AUTHENTICATED_USER

    def check_photo_url(self, url):
        self.assertTrue(url.startswith("https://epschedule-avatars.storage.googleapis.com/"))



"""Tests for the /search endpoint."""        

class TestStudentEndpoint(AuthenticatedTest):
    def check_username(self, username):
        response = self.client.get('/student/{}'.format(username))
        self.assertEqual(response.status_code, 200)

        obj = json.loads(response.data)
        self.assertEqual(obj["username"], username)
        self.assertIn(obj["username"], obj["email"])
        self.assertEqual(len(obj["classes"]), 3)

        for trimester in obj["classes"]:
            # Could have 9 classes due to zero period
            self.assertGreaterEqual(len(trimester), 8)

        return obj

    # Test that the student method returns valid data for students and teachers.
    def test_get_student(self):
        teacher_obj = self.check_username(TEST_TEACHER)
        student_obj = self.check_username(TEST_STUDENT)

        # Teachers have no grade or gradyear
        self.assertIsNone(teacher_obj["grade"])
        self.assertIsNone(teacher_obj["gradyear"])

        # Students should, though
        self.assertGreaterEqual(student_obj["grade"], 5)
        self.assertGreaterEqual(student_obj["gradyear"], 2020)

    # Test that we can download the photo for a teacher.
    def test_has_photo(self):
        # Download teacher's profile photo to ensure it exists
        teacher_obj = self.check_username(TEST_TEACHER)
        self.check_photo_url(teacher_obj["photo_url"])

    # Test that a student who isn't sharing their pic returns a placeholder.
    def test_urls_showing_up(self):
        student_obj = self.check_username(TEST_STUDENT_NO_PIC)
        self.assertEqual(student_obj["photo_url"], "/static/images/placeholder.png")


"""Tests for the /search endpoint."""        
TEST_SEARCH = "b"

class TestSearchEndpoint(AuthenticatedTest):
    def test_search_endpoint(self):
        response = self.client.get('/search/{}'.format(TEST_SEARCH))
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data)

        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIn(TEST_SEARCH.lower(), result["name"].lower())


"""Tests for the /class endpoint."""
class TestClassEndpoint(AuthenticatedTest):
    # Test that we can get the fall A period class for the test user.
    def test_class_endpoint(self):
        response = self.client.get('/class/a?term_id=1')
        self.assertEqual(response.status_code, 200)
        results = json.loads(response.data)

    # Test that any students who aren't sharing their pics return placeholders.
    def test_urls_inclass(self):
        response = self.client.get('/class/h?term_id=1')
        results = json.loads(response.data)
        students = results["students"]
        found_student = None
        for student in students: 
            if student["username"] == TEST_STUDENT_NO_PIC:
                found_student = student
        self.assertNotEqual(found_student, None)
        self.assertEqual(found_student["photo_url"], "/static/images/placeholder_small.png")
        

if __name__ == "__main__":
    unittest.main()
