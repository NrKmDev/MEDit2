from django.shortcuts import render
from account.models import Account
from contest.models import Contest,Problem
from contest.forms import SubmissionForm
from datetime import datetime, timedelta
from django.utils import timezone

color=["grey","green","aqua","blue","yellow","orange","red"]

def home_screen_view(request):
    context={}
    accounts=Account.objects.order_by('score').reverse()
    context['accounts']=accounts
    allcontests=Contest.objects.all()
    open_contests=[]
    contests=[]
    now_contests=[]
    for contest in allcontests:
        if contest.date_end<timezone.now():
            open_contests.append(contest)
        elif contest.date_start>timezone.now():
            contests.append(contest)
        else:
            now_contests.append(contest)
    context['contests']=contests
    context['open_contests']=open_contests
    context['now_contests']=now_contests
    return render(request,'contest/home.html',context)

def problems_view(request,contest_id):
    context={}
    user=request.user
    contest=Contest.objects.get(pk=contest_id)
    problems=[val for val in contest.problems.all()]
    context['contest']=contest
    has_not_started=0
    if contest.date_start>timezone.now():
        has_not_started=1
    context['has_not_started']=has_not_started
    if request.POST:
        if user.is_authenticated:
            submitted_accounts=[val for val in contest.submitted_accounts.all()]
            if user in submitted_accounts:
                context['warning']="You have already submitted."
                return render(request,'contest/problems.html',context)
            contest.submitted_accounts.add(user)
            problem_ans=[val.problem_ans for val in problems]
            user_ans=request.POST.getlist('user_ans')
            res=zip(problem_ans,user_ans)
            contest_score=0
            cnt=0
            results=[]
            for problem_ans,user_ans in res:
                if problem_ans==user_ans:
                    user.score+=problems[cnt].problem_score
                    contest_score+=problems[cnt].problem_score
                    problems[cnt].solved_accounts.add(user)
                    results.append('Correct')
                else:
                    results.append('Wrong')
                cnt+=1
            context['contest_score']=contest_score
            context['results']=results
            context['user_score']=user.score
            context['finished']=1
            user.color=color[min(6,request.user.score//400)]
            user.save()
            return render(request,'contest/problems.html',context)
        else:
            context['warning']="Please login."
            return render(request,'contest/problems.html',context)
    else:
        context['problems']=problems
        context['contest']=contest
    return render(request,'contest/problems.html',context)

def standings_view(request,contest_id):
    context={}
    contest=Contest.objects.get(pk=contest_id)
    problems=[val for val in contest.problems.all()]
    submitted_accounts=[val for val in contest.submitted_accounts.all()]
    n=len(problems)
    standings0=[[0 for i in range(n+2)] for j in range(len(submitted_accounts))]
    accounts=[0 for i in range(len(submitted_accounts))]
    y=0
    for account in submitted_accounts:
        x=0
        standings0[y][n+1]=account
        for problem in problems:
            solved_accounts=[val for val in problem.solved_accounts.all()]
            if account in solved_accounts:
                standings0[y][x]="Correct"
                standings0[y][n]+=problem.problem_score
            else:
                standings0[y][x]="Wrong"
            x+=1
        y+=1
    standings1=sorted(standings0,key=lambda x:(x[n]),reverse=True)
    standings=[[0 for i in range(n+1)] for j in range(len(submitted_accounts))]
    m=len(submitted_accounts)
    for i in range(m):
        accounts[i]=standings1[i][n+1]
    for i in range(m):
        for j in range(n+1):
            standings[i][j]=standings1[i][j]
    ast=dict(zip(accounts,standings))
    context["standings"]=standings
    empty=[0 for i in range(n)]
    context["empty"]=empty
    context["contest"]=contest
    context["ast"]=ast
    return render(request,'contest/standings.html',context)
