from django import forms
from django_filters import FilterSet
from django_filters.filters import ModelChoiceFilter, BooleanFilter
from .models import Task
from task_manager.labels.models import Label


class TaskFilter(FilterSet):
    label = ModelChoiceFilter(
        queryset=Label.objects.all(), field_name='labels', label='Метка')
    is_author = BooleanFilter(
        field_name='author',
        widget=forms.CheckboxInput,
        label='Только свои задачи',
        method='filter_author_tasks'
    )

    def filter_author_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor']
