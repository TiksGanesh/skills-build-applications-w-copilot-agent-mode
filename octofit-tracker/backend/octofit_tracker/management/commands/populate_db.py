from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Use direct MongoDB operations to bypass Djongo ForeignKey issues
        from pymongo import MongoClient
        from datetime import datetime
        
        client = MongoClient('mongodb://localhost:27017/')
        db = client['octofit_db']
        
        # Clear existing data
        db.octofit_tracker_activity.delete_many({})
        db.octofit_tracker_leaderboard.delete_many({})
        db.octofit_tracker_workout.delete_many({})
        db.octofit_tracker_user.delete_many({})
        db.octofit_tracker_team.delete_many({})
        
        # Insert teams
        marvel_id = 1
        dc_id = 2
        db.octofit_tracker_team.insert_many([
            {'_id': marvel_id, 'name': 'Marvel'},
            {'_id': dc_id, 'name': 'DC'}
        ])
        
        # Insert users with all required AbstractUser fields
        ironman_id = 1
        cap_id = 2
        batman_id = 3
        superman_id = 4
        
        now = datetime.now()
        user_template = {
            'password': 'pbkdf2_sha256$390000$placeholder$unusable',
            'last_login': None,
            'is_superuser': False,
            'first_name': '',
            'last_name': '',
            'is_staff': False,
            'is_active': True,
            'date_joined': now
        }
        
        db.octofit_tracker_user.insert_many([
            {**user_template, '_id': ironman_id, 'username': 'ironman', 'email': 'ironman@marvel.com', 'team_id': marvel_id},
            {**user_template, '_id': cap_id, 'username': 'captainamerica', 'email': 'cap@marvel.com', 'team_id': marvel_id},
            {**user_template, '_id': batman_id, 'username': 'batman', 'email': 'batman@dc.com', 'team_id': dc_id},
            {**user_template, '_id': superman_id, 'username': 'superman', 'email': 'superman@dc.com', 'team_id': dc_id}
        ])
        
        # Insert activities
        activities = []
        activity_id = 1
        for user_id in [ironman_id, cap_id, batman_id, superman_id]:
            activities.append({'_id': activity_id, 'user_id': user_id, 'type': 'run', 'duration': 30, 'distance': 5.0})
            activity_id += 1
            activities.append({'_id': activity_id, 'user_id': user_id, 'type': 'cycle', 'duration': 60, 'distance': 20.0})
            activity_id += 1
        db.octofit_tracker_activity.insert_many(activities)
        
        # Insert workouts
        db.octofit_tracker_workout.insert_many([
            {'_id': 1, 'name': 'Morning Cardio', 'description': 'Run and cycle combo', 'duration': 90},
            {'_id': 2, 'name': 'Strength Training', 'description': 'Weights and resistance', 'duration': 60}
        ])
        
        # Insert leaderboard
        db.octofit_tracker_leaderboard.insert_many([
            {'_id': 1, 'team_id': marvel_id, 'points': 100},
            {'_id': 2, 'team_id': dc_id, 'points': 90}
        ])
            
        self.stdout.write(self.style.SUCCESS('Database populated with test data using direct MongoDB inserts.'))

        # Unique index on email is enforced by Django model field
