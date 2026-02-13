from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer,
    TeamSerializer,
    ActivitySerializer,
    LeaderboardSerializer,
    WorkoutSerializer
)
from datetime import datetime


class UserModelTests(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            email='test@example.com',
            name='Test User',
            team_id='team123'
        )
    
    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.name, 'Test User')
        self.assertEqual(str(self.user), 'Test User')


class TeamModelTests(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team'
        )
    
    def test_team_creation(self):
        """Test that a team can be created"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTests(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_id='user123',
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories=300,
            date=datetime.now()
        )
    
    def test_activity_creation(self):
        """Test that an activity can be created"""
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(str(self.activity), 'Running - 30 min')


class LeaderboardModelTests(TestCase):
    """Test cases for Leaderboard model"""
    
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            user_id='user123',
            total_points=100,
            total_activities=10,
            rank=1
        )
    
    def test_leaderboard_creation(self):
        """Test that a leaderboard entry can be created"""
        self.assertEqual(self.leaderboard.total_points, 100)
        self.assertEqual(self.leaderboard.rank, 1)


class WorkoutModelTests(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Morning Run',
            description='A refreshing morning run',
            difficulty_level='Intermediate',
            duration=45,
            category='Cardio'
        )
    
    def test_workout_creation(self):
        """Test that a workout can be created"""
        self.assertEqual(self.workout.name, 'Morning Run')
        self.assertEqual(str(self.workout), 'Morning Run')


class UserAPITests(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'api@example.com',
            'name': 'API User',
            'team_id': 'team456'
        }
    
    def test_create_user(self):
        """Test creating a user via API"""
        response = self.client.post(
            reverse('user-list'),
            self.user_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_users(self):
        """Test retrieving users via API"""
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamAPITests(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team_data = {
            'name': 'API Team',
            'description': 'A team created via API'
        }
    
    def test_create_team(self):
        """Test creating a team via API"""
        response = self.client.post(
            reverse('team-list'),
            self.team_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_teams(self):
        """Test retrieving teams via API"""
        response = self.client.get(reverse('team-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActivityAPITests(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.activity_data = {
            'user_id': 'user789',
            'activity_type': 'Cycling',
            'duration': 60,
            'distance': 20.0,
            'calories': 500,
            'date': datetime.now().isoformat()
        }
    
    def test_create_activity(self):
        """Test creating an activity via API"""
        response = self.client.post(
            reverse('activity-list'),
            self.activity_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_activities(self):
        """Test retrieving activities via API"""
        response = self.client.get(reverse('activity-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITests(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.leaderboard_data = {
            'user_id': 'user999',
            'total_points': 200,
            'total_activities': 20,
            'rank': 5
        }
    
    def test_create_leaderboard(self):
        """Test creating a leaderboard entry via API"""
        response = self.client.post(
            reverse('leaderboard-list'),
            self.leaderboard_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_leaderboard(self):
        """Test retrieving leaderboard via API"""
        response = self.client.get(reverse('leaderboard-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITests(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.workout_data = {
            'name': 'Evening Yoga',
            'description': 'Relaxing yoga session',
            'difficulty_level': 'Beginner',
            'duration': 30,
            'category': 'Flexibility'
        }
    
    def test_create_workout(self):
        """Test creating a workout via API"""
        response = self.client.post(
            reverse('workout-list'),
            self.workout_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_workouts(self):
        """Test retrieving workouts via API"""
        response = self.client.get(reverse('workout-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIRootTests(APITestCase):
    """Test cases for API root endpoint"""
    
    def test_api_root(self):
        """Test that the API root returns all endpoints"""
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)
