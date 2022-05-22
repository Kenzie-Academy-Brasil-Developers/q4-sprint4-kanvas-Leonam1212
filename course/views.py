from django.shortcuts import render
from django.shortcuts import get_object_or_404
from accounts.models import Accounts
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
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from course.permissions import IsAdmin
from course.serializers import (
    CourseSerializer,
    PatchCourseSerializer,
    PutCreateInstructorSerializer,
    PutCreateStudentsSerializer,
)
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

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
                {"message": "Course already exists"}, HTTP_422_UNPROCESSABLE_ENTITY
            )

        course = Course.objects.create(**serializer.validated_data)
        course.save()

        serializer = CourseSerializer(course)

        return Response(serializer.data, HTTP_201_CREATED)

    def patch(self, request: Request, course_uuid=""):
        serializer = PatchCourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if course_uuid:

            try:
                found_course = Course.objects.filter(
                    name=serializer.validated_data["name"]
                ).exists()

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

    def put(self, request: Request, course_uuid=""):
        serializer = PutCreateInstructorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        found_course = Course.objects.filter(pk=course_uuid).exists()

        try:
            if not found_course:
                return Response(
                    {"message": "Course does not exist"}, HTTP_404_NOT_FOUND
                )

            is_adm = Accounts.objects.filter(
                pk=serializer.data["instructor_id"]
            ).first()

            if not is_adm.is_admin:
                return Response(
                    {"message": "Instructor id does not belong to an admin"},
                    HTTP_422_UNPROCESSABLE_ENTITY,
                )

            course = Course.objects.filter(pk=course_uuid).first()

            course.instructor = is_adm
            course.save()

            serializer = CourseSerializer(course)

            return Response(serializer.data , HTTP_200_OK)

        except:
            return Response({"message": "Invalid instructor_id"}, HTTP_404_NOT_FOUND)

    def delete(self, request: Request, course_uuid=""):
        if course_uuid:
           
            course = Course.objects.filter(pk=course_uuid)
            # course = get_object_or_404(Course, pk=course_uuid)
            if not course.exists():
                return Response(
                {"message": "Course does not exist"}, HTTP_404_NOT_FOUND
            )
            course.first().delete()

            return Response("", HTTP_204_NO_CONTENT)

       
                


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def put_students(request: Request, course_uuid=""):

    serializer = PutCreateStudentsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    found_course = Course.objects.filter(pk=course_uuid)
    list_students = []
    try:
        if not found_course.exists():
            return Response({"message": "Course does not exist"}, HTTP_404_NOT_FOUND)

        for student in serializer.data["students_id"]:        
            is_student = Accounts.objects.filter(pk=student)

            if is_student.first().is_admin:
                return Response({"message": "Some student id belongs to an Instructor"}, HTTP_422_UNPROCESSABLE_ENTITY)
                
            list_students.append(is_student.first())
        
        found_course.first().students.set(list_students) 
        
        serializer = CourseSerializer(found_course.first())
        
        return Response(serializer.data, HTTP_200_OK)


    except:
        return Response({ "message": "Invalid students_id list"}, HTTP_404_NOT_FOUND)
