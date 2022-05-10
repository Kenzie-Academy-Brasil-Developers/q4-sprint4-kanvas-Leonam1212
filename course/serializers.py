from rest_framework import serializers


class CourseSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField()
    demo_time = serializers.TimeField()
    link_repo = serializers.CharField()


class PatchCourseSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    demo_time = serializers.TimeField(required=False)
    link_repo = serializers.CharField(required=False)
