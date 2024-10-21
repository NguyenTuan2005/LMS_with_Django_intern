from django.urls import include, path
from . import views
from .views_type import (
    AssessmentTypeListView,
    AssessmentTypeCreateView,
    AssessmentTypeUpdateView,
    AssessmentTypeDeleteView,
)


app_name = 'assessment'

urlpatterns = [
    path('', views.assessment_list, name='assessment_list'),
    path('create/', views.assessment_create, name='assessment_create'),
    path('<int:pk>/edit/', views.assessment_edit, name='assessment_edit'),
    path('<int:pk>/', views.assessment_detail, name='assessment_detail'),
    path('<int:assessment_id>/attempt/', views.student_assessment_attempt, name='student_assessment_attempt'),
    path('get-exercise-content/<int:exercise_id>/', views.get_exercise_content, name='get_exercise_content'),
    path('save-assessment/', views.save_assessment, name='save-assessment'),

    path('assessmenttype', AssessmentTypeListView.as_view(), name='assessmenttype_list'),
    path('assessmenttype/add/', AssessmentTypeCreateView.as_view(), name='assessmenttype_create'),
    path('assessmenttype/edit/<int:pk>/', AssessmentTypeUpdateView.as_view(), name='assessmenttype_update'),
    path('assessmenttype/delete/<int:pk>/', AssessmentTypeDeleteView.as_view(), name='assessmenttype_delete'),
]


