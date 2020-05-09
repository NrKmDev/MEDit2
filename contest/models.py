from django.db import models
from datetime import datetime,date
from account.models import Account

class Problem(models.Model):
    problem_name=models.CharField(max_length=200)
    problem_text=models.CharField(max_length=200)
    problem_ans=models.CharField(max_length=200)
    problem_score=models.IntegerField(default=0)
    solved_accounts=models.ManyToManyField(Account,blank=True,null=True)
class Contest(models.Model):
    name=models.CharField(max_length=200)
    difficulty=models.IntegerField(default=0)
    problems=models.ManyToManyField(Problem)
    date_start=models.DateTimeField(blank=True,null=True)
    date_end=models.DateTimeField(blank=True,null=True)
    submitted_accounts=models.ManyToManyField(Account,blank=True,null=True)
