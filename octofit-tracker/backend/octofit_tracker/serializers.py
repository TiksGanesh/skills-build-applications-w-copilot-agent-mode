from rest_framework import serializers
from .models import User, Team, Activity, Workout, Leaderboard


def _stringify(value):
    return str(value) if value is not None else None


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name']

    def get_id(self, obj):
        return _stringify(obj.pk)


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    team = TeamSerializer(read_only=True)
    team_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'team', 'team_id']

    def get_id(self, obj):
        return _stringify(obj.pk)

    def get_team_id(self, obj):
        return _stringify(obj.team_id)


class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'user', 'user_id', 'type', 'duration', 'distance']

    def get_id(self, obj):
        return _stringify(obj.pk)

    def get_user_id(self, obj):
        return _stringify(obj.user_id)


class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'duration']

    def get_id(self, obj):
        return _stringify(obj.pk)


class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    team = TeamSerializer(read_only=True)
    team_id = serializers.SerializerMethodField()

    class Meta:
        model = Leaderboard
        fields = ['id', 'team', 'team_id', 'points']

    def get_id(self, obj):
        return _stringify(obj.pk)

    def get_team_id(self, obj):
        return _stringify(obj.team_id)
