from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with ObjectId to string conversion"""
    id = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'team_id', 'created_at']
        read_only_fields = ['created_at']


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model with ObjectId to string conversion"""
    id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model with ObjectId to string conversion"""
    id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'activity_type', 'duration', 'distance', 'calories', 'date', 'created_at']
        read_only_fields = ['created_at']


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model with ObjectId to string conversion"""
    id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'total_points', 'total_activities', 'rank', 'updated_at']
        read_only_fields = ['updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model with ObjectId to string conversion"""
    id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'difficulty_level', 'duration', 'category', 'created_at']
        read_only_fields = ['created_at']
