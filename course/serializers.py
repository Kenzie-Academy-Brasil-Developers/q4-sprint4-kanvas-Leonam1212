from pkg_resources import Requirement
from rest_framework import serializers

from accounts.serializers import AccountsSerializer


class CourseSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField()
    demo_time = serializers.TimeField()
    link_repo = serializers.CharField()
    instructor = AccountsSerializer(read_only=True)
    students = AccountsSerializer(many=True, read_only=True)


class PatchCourseSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    demo_time = serializers.TimeField(required=False)
    link_repo = serializers.CharField(required=False)

class PutCreateInstructorSerializer(serializers.Serializer):
    instructor_id = serializers.CharField(required=True)

class PutCreateStudentsSerializer(serializers.Serializer):
    students_id = serializers.ListField(required=True)