import random

from locust import HttpUser, task, between

users_data = [
        {"email": "john@simplylift.co", "club": "Simply Lift", "competition": "Spring Festival"},
        {"email": "admin@irontemple.com", "club": "Iron Temple", "competition": "Fall Classic 2"},
        {"email": "kate@shelifts.co.uk", "club": "She Lifts", "competition": "Spring Festival 2"},
        {"email": "contact@powerhouse.com", "club": "Power House", "competition": "Summer Challenge"},
        {"email": "info@fitnessfirst.com", "club": "Fitness First", "competition": "Winter Championship"},
        {"email": "support@gladiatorgym.com", "club": "Gladiator Gym", "competition": "Spring Festival"}
    ]



class PerformanceTests(HttpUser):
    wait_time = between(1, 2)


    def on_start(self):
        self.user_data = users_data.pop(0)

    @task
    def test_prf(self):
        self.client.get('/')

        self.client.post('/showSummary', {'email': self.user_data['email']})

        self.client.get(f"/book/{self.user_data['competition']}/{self.user_data['club']}")

        self.client.post('/purchasePlaces', {
            'competition': self.user_data['competition'],
            'club': self.user_data['club'],
            'places': '1'
        })
