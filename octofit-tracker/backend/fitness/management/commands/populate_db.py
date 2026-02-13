from django.core.management.base import BaseCommand
from django.utils import timezone
from fitness.models import User, Team, Activity, Leaderboard, Workout
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        # Create teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earth\'s Mightiest Heroes fighting for fitness!'
        )
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League members dedicated to peak performance!'
        )
        
        # Create users (superheroes)
        self.stdout.write('Creating users...')
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'ironman@avengers.com'},
            {'name': 'Captain America', 'email': 'cap@avengers.com'},
            {'name': 'Thor', 'email': 'thor@asgard.com'},
            {'name': 'Black Widow', 'email': 'natasha@avengers.com'},
            {'name': 'Hulk', 'email': 'hulk@avengers.com'},
            {'name': 'Spider-Man', 'email': 'spidey@avengers.com'},
        ]
        
        dc_heroes = [
            {'name': 'Superman', 'email': 'superman@justiceleague.com'},
            {'name': 'Batman', 'email': 'batman@justiceleague.com'},
            {'name': 'Wonder Woman', 'email': 'diana@justiceleague.com'},
            {'name': 'The Flash', 'email': 'flash@justiceleague.com'},
            {'name': 'Aquaman', 'email': 'aquaman@justiceleague.com'},
            {'name': 'Green Lantern', 'email': 'hal@justiceleague.com'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=str(team_marvel.id)
            )
            marvel_users.append(user)
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=str(team_dc.id)
            )
            dc_users.append(user)
        
        all_users = marvel_users + dc_users
        
        # Create activities
        self.stdout.write('Creating activities...')
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Combat Training']
        
        for user in all_users:
            # Each user gets 5-10 activities
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)  # 20-120 minutes
                distance = round(random.uniform(2, 20), 2) if activity_type in ['Running', 'Cycling', 'Swimming'] else None
                calories = duration * random.randint(5, 15)  # Rough calculation
                
                Activity.objects.create(
                    user_id=str(user.id),
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories=calories,
                    date=timezone.now() - timedelta(days=random.randint(0, 30))
                )
        
        # Create leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        for user in all_users:
            user_activities = Activity.objects.filter(user_id=str(user.id))
            total_points = sum(activity.calories for activity in user_activities)
            total_activities = user_activities.count()
            
            Leaderboard.objects.create(
                user_id=str(user.id),
                total_points=total_points,
                total_activities=total_activities
            )
        
        # Update ranks
        leaderboard_entries = Leaderboard.objects.all().order_by('-total_points')
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()
        
        # Create workouts
        self.stdout.write('Creating workouts...')
        workouts_data = [
            {
                'name': 'Super Soldier Cardio',
                'description': 'High-intensity cardio workout inspired by Captain America\'s training',
                'difficulty_level': 'Advanced',
                'duration': 45,
                'category': 'Cardio'
            },
            {
                'name': 'Asgardian Strength Training',
                'description': 'Build god-like strength with Thor\'s workout routine',
                'difficulty_level': 'Advanced',
                'duration': 60,
                'category': 'Strength'
            },
            {
                'name': 'Web-Slinger Agility',
                'description': 'Improve flexibility and agility like Spider-Man',
                'difficulty_level': 'Intermediate',
                'duration': 30,
                'category': 'Agility'
            },
            {
                'name': 'Batcave Core Training',
                'description': 'Bruce Wayne\'s core strengthening routine',
                'difficulty_level': 'Intermediate',
                'duration': 40,
                'category': 'Core'
            },
            {
                'name': 'Flash Speed Training',
                'description': 'Sprint intervals to boost your speed',
                'difficulty_level': 'Advanced',
                'duration': 35,
                'category': 'Speed'
            },
            {
                'name': 'Wonder Woman Combat Basics',
                'description': 'Learn basic combat moves and defensive techniques',
                'difficulty_level': 'Beginner',
                'duration': 50,
                'category': 'Combat'
            },
            {
                'name': 'Aquaman Swimming Mastery',
                'description': 'Advanced swimming techniques for endurance',
                'difficulty_level': 'Advanced',
                'duration': 55,
                'category': 'Swimming'
            },
            {
                'name': 'Stark Industries Recovery Yoga',
                'description': 'Gentle yoga for recovery and flexibility',
                'difficulty_level': 'Beginner',
                'duration': 25,
                'category': 'Yoga'
            },
        ]
        
        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)
        
        # Print summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Teams created: {Team.objects.count()}')
        self.stdout.write(f'Users created: {User.objects.count()}')
        self.stdout.write(f'Activities created: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts created: {Workout.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\nDatabase successfully populated with superhero test data!'))
