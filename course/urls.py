from django.urls import path

from course.views import CourseView, put_students

urlpatterns = [
    path("courses/", CourseView.as_view()),
    path("courses/<str:course_uuid>", CourseView.as_view()),
    path("courses/<str:course_uuid>/registrations/instructor/", CourseView.as_view()),
    path("courses/<str:course_uuid>/registrations/students/", put_students),
]
