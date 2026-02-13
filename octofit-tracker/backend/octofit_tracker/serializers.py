from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with ObjectId to string conversion"""
    id = serializers.CharField(read_only=True)
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'name', 'team_id', 'is_active', 'date_joined', 'created_at']
        read_only_fields = ['created_at']
    
    def get_username(self, obj):
        """Generate username from email (part before @)"""
        if obj.email:
            return obj.email.split('@')[0]
        return obj.name.lower().replace(' ', '_')
    
    def get_first_name(self, obj):
        """Extract first name from name field"""
        if obj.name:
            parts = obj.name.split(' ', 1)
            return parts[0] if parts else ''
        return ''
    
    def get_last_name(self, obj):
        """Extract last name from name field"""
        if obj.name:
            parts = obj.name.split(' ', 1)
            return parts[1] if len(parts) > 1 else ''
        return ''
    
    def get_is_active(self, obj):
        """All users are active by default"""
        return True


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
