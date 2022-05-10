from django.urls import path

from course.views import CourseView

urlpatterns = [
    path("courses/", CourseView.as_view()),
    path("courses/<str:course_uuid>", CourseView.as_view())
]
