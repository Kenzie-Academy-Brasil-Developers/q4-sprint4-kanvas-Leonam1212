from django.shortcuts import render
from django.shortcuts import get_object_or_404
from course.models import Course
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_409_CONFLICT,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
)
from rest_framework.authentication import TokenAuthentication

from course.permissions import IsAdmin
from course.serializers import CourseSerializer, PatchCourseSerializer

# Create your views here.


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request: Request, course_uuid=""):
        if course_uuid:
            try:
                course = Course.objects.get(uuid=course_uuid)
                serializer = CourseSerializer(course)
                return Response(serializer.data, HTTP_200_OK)

            except:
                return Response(
                    {"message": "Course does not exist"}, HTTP_404_NOT_FOUND
                )

        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data, HTTP_200_OK)

    def post(self, request: Request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        found_course = Course.objects.filter(
            name=serializer.validated_data["name"]
        ).exists()

        if found_course:
            return Response(
                {"message": "Course name already exists"}, HTTP_409_CONFLICT
            )

        course = Course.objects.create(**serializer.validated_data)
        course.save()

        serializer = CourseSerializer(course)
        print(serializer.data)

        return Response(serializer.data, HTTP_201_CREATED)

    def patch(self, request: Request, course_uuid=""):
        serializer = PatchCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if course_uuid:

            try:
                found_course = Course.objects.filter(
                    name=serializer.validated_data["name"]
                ).exists()
                print(found_course)

                course = Course.objects.filter(pk=course_uuid)

                if not found_course:
                    course.update(**serializer.validated_data)
                    serializer = CourseSerializer(course.first())

                    return Response(serializer.data, HTTP_200_OK)
                else:
                    return Response(
                        {"message": "Course name already exists"}, HTTP_409_CONFLICT
                    )
            except:
                return Response(
                    {"message": "Course does not exist"}, HTTP_404_NOT_FOUND
                )

    def delete(self, request: Request, course_uuid=""):
        if course_uuid:
            try:
                course = get_object_or_404(Course, pk=course_uuid)
                course.delete()

                return Response("", HTTP_204_NO_CONTENT)
            except:
                return Response(
                    {"message": "Course does not exist"}, HTTP_404_NOT_FOUND
                )
