from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from account.forms import RegistrationForm, AccountAuthenticationForm
from account.models import FriendRequest,Account

color=["grey","green","aqua","blue","yellow","orange","red"]

def registration_view(request):
    context={}
    if request.POST:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            raw_password=form.cleaned_data.get('password')
            account=form.save()
            login(request,account)
            return redirect('home')
        else:
            context['registration_form']=form
    else:
        form=RegistrationForm()
        context['registration_form']=form
    return render(request,'account/register.html',context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context={}
    user=request.user
    if user.is_authenticated:
        return redirect("home")
    
    if request.POST:
        form=AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(email=email,password=password)

            if user:
                login(request,user)
                return redirect("home")
    else:
        form=AccountAuthenticationForm()
    
    context['login_form']=form
    return render(request,'account/login.html',context)

def profile_view(request):
    user=request.user
    context={}
    if user.is_authenticated:
        allusers=Account.objects.exclude(username=user.username)
        allnonfriends=[]
        allfriends=[val for val in user.friends.all()]
        fr=FriendRequest.objects.filter(to_user=user)
        for user in allusers:
            if not user in allfriends:
                allnonfriends.append(user)
        context["add_friends"]=allnonfriends
        context["allfriends"]=allfriends
        context["fr"]=fr
        accounts=Account.objects.order_by('score')
        ScoreList=[val.score for val in accounts]
        rank=0
        last=-1
        cnt=0
        end=0
        n=len(ScoreList)
        for sc in ScoreList:
            if end==1 and sc!=request.user.score:
                break
            if sc==request.user.score:
                end=1
                rank+=1
            else:
                rank+=1
        print(rank)
        context["user_color"]=color[min(6,request.user.score//400)]
        context["rank"]=n-rank+1
        context["users"]=len(accounts)
        return render(request,'account/profile.html',context)

def send_request(request,id):
    from_user=request.user
    to_user=Account.objects.get(id=id)
    frequest=FriendRequest.objects.get_or_create(from_user=from_user,to_user=to_user)
    return redirect('profile')

def accept_request(request,id):
    frequest=FriendRequest.objects.get(id=id)
    user1=request.user
    user2=frequest.from_user
    user1.friends.add(user2)
    user2.friends.add(user1)
    frequest.delete()
    return redirect('profile')

def other_profile_view(request,id):
    user=request.user
    context={}
    other_user=Account.objects.get(id=id)
    if not user==other_user:
        allfriends=[val for val in other_user.friends.all()]
        context["allfriends"]=allfriends
        context["other_user"]=other_user
        accounts=Account.objects.order_by('score')
        ScoreList=[val.score for val in accounts]
        rank=0
        last=-1
        cnt=0
        end=0
        n=len(ScoreList)
        for sc in ScoreList:
            if end==1 and sc!=other_user.score:
                break
            if sc==other_user.score:
                end=1
                rank+=1
            else:
                rank+=1
        print(rank)
        context["rank"]=n-rank+1
        context["users"]=len(accounts)
        return render(request,'account/other_profile.html',context)
    if user==other_user:
        return redirect('profile')