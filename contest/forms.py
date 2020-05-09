from django import forms
from contest.models import Problem

class SubmissionForm(forms.ModelForm):
    problem_ans=forms.CharField(max_length=200)
    class Meta:
        model=Problem
        fields=('problem_ans',)