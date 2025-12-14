from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from octofit_tracker.models import Team, Activity, Leaderboard, Workout

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()


        # Create Teams and save
        marvel = Team(name='Marvel')
        marvel.save()
        dc = Team(name='DC')
        dc.save()

        # Create Users (superheroes) without team, then assign team and save
        users = []
        ironman = User.objects.create_user(username='ironman', email='ironman@marvel.com')
        ironman.team = marvel
        ironman.save()
        users.append(ironman)

        cap = User.objects.create_user(username='captainamerica', email='cap@marvel.com')
        cap.team = marvel
        cap.save()
        users.append(cap)

        batman = User.objects.create_user(username='batman', email='batman@dc.com')
        batman.team = dc
        batman.save()
        users.append(batman)

        superman = User.objects.create_user(username='superman', email='superman@dc.com')
        superman.team = dc
        superman.save()
        users.append(superman)

        # Create Activities
        for user in users:
            Activity.objects.create(user=user, type='run', duration=30, distance=5)
            Activity.objects.create(user=user, type='cycle', duration=60, distance=20)

        # Create Workouts
        Workout.objects.create(name='Morning Cardio', description='Run and cycle combo', duration=90)
        Workout.objects.create(name='Strength Training', description='Weights and resistance', duration=60)

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))

        # Unique index on email is enforced by Django model field
