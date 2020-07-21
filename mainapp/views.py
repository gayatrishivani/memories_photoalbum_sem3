from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.core.files.storage import FileSystemStorage
from .forms import profileForm
from user.models import User
from django.http import HttpResponseRedirect
# Create your views here.
@login_required(login_url='/login/')
def index(request):
    user = request.user
    album = Album.objects.filter(user__exact=user)
    # album_id = []
    # for al in album:
    #     album_id.append(al.album_id)
    # print(album_id)
    
    context = {
        "album":album,

    }
    return render(request,'index.html',context)

def others_profile(request,username=None):
    user = request.user
    user.pk = request.user.pk
    print(user)
    profile_user = get_object_or_404(User,username=username)
    print(profile_user.pk)
    following = Following.objects.filter(user__exact=user)
    
    

    if profile_user.pk == user.pk:
        return redirect('/')
    else:
        
        album = Album.objects.filter(user__exact=profile_user)
        context = {
            "album":album,
            "profile_user":profile_user,
        }
    
        return render(request,'ui1.html',context)


def search(request):
    if request.method =="POST":
        q = request.POST.get('msearch')

    
        print(q)
        profiles_search = User.objects.filter(username__icontains=q)
        for p in profiles_search:
            print(p.username)
        context={
            "p_search":profiles_search,
        }

        return render(request,'search.html',context)

def single(request,pk=None,title=None):
    album = get_object_or_404(Album,pk=pk)
    sub = sub_album.objects.filter(main_title__exact=album)
    
    context={
        "title":title,
        "sub":sub,
        "al_id":pk,
    }


    return render(request, 'single.html',context)


def add_sub_album(request,album_id=None):
    if request.method == 'POST':
        new_sub_album = sub_album()

        new_sub_album.sub_title = request.POST.get('sub_title')
        main_album = get_object_or_404(Album,pk=album_id)
        main_id = album_id
        new_sub_album.main_title = main_album
        
        images = request.FILES.get('images')
        new_sub_album.images = images
        content = images
        
        fs = FileSystemStorage()
        fs.save('User_' + str(new_sub_album.main_title.user)+"/" + str(new_sub_album.main_title.album_id)+"/"+images.name,images)
        
        new_sub_album.sub_description = request.POST.get('sub_description')        

        if new_sub_album.main_title.album_id is None:
            return render(request, 'add_sub_album.html')
        else:
            new_sub_album.save()
            
            return redirect('add_sub_album',album_id=main_album.album_id)

    else:
        
        return render(request, 'add_sub_album.html')




@login_required(login_url='/login/')
def add_album(request):
    if request.method == 'POST':
        user = request.user
        
        
        new_album = Album()

        new_album.title = request.POST.get('title')
        new_album.user = user
        new_album.memory_date = request.POST.get('memory_date')
        new_album.description = request.POST.get('description')
        new_album.Album_cover_img = request.FILES.get('imagi')
        print(new_album.Album_cover_img)
        
        if  new_album.Album_cover_img:
            
        
            images = new_album.Album_cover_img
            fs = FileSystemStorage()
            fs.save('User_' + str(user)+"/" + 'album_cov_' + str(new_album.pk)+"/"+images.name,images)
        
        something = len(new_album.title)
        if something == 0 :
            messages.error(request,'please enter a title for your album to continue')
            return render(request, 'add_album.html')

        else:
            new_album.save()
            
            
            return redirect('add_sub_album',album_id=new_album.album_id)

    else:
        new_album = Album()
        return render(request, 'add_album.html')


def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        
        print(user)
        new_profile = Profile()

        
        new_profile.user = user
        print(new_profile.user)
        new_profile.bio = request.POST.get('bio')
        print(new_profile.bio)
        new_profile.name = request.POST.get('fname')
        print(new_profile.name)
        new_profile.gender = 3
        print(new_profile.gender)
        images = request.FILES.get('images')
        if images is None:
            new_profile.save()
            return redirect('/')
        else:


            new_profile.images = images
            content = images
        
            fs = FileSystemStorage()
            fs.save('User_' + str(user)+"/"+images.name,images)
            new_profile.save()
            return redirect('/')


    return render(request, 'edit.html')

def edit_profile(request,id=None):
    if request.method == 'POST':
        user = request.user
        
        print(user)
        new_profile = get_object_or_404(Profile,up_id=id)

        
        
        
        new_profile.bio = request.POST.get('bio')
        print(new_profile.bio)
        new_profile.name = request.POST.get('fname')
        print(new_profile.name)
        new_profile.gender = 3
        print(new_profile.gender)
        images = request.FILES.get('images')
        if images is None:
            new_profile.save()
            return redirect('/')
        else:
            new_profile.images = images
            content = images
        
            fs = FileSystemStorage()
            fs.save('User_' + str(user)+"/"+images.name,images)
            new_profile.save()
            return redirect('/')


    return render(request, 'edit.html')


def profile(request):
    if request.method == 'POST':
        p_form = profileForm(request.POST,request.FILES, instance=request.user.profile)
        
        if p_form. is_valid():
            p_form.save()
            messages.success(request,'your account has been updated' )
            return redirect('profile')
    else:
        p_form = profileForm(instance=request.userr.profile)
        context = {
            'p_form': p_form
        }
        
        return render(request,'edit.html',context)


def follow_request(request,id=None):
    user = request.user
    print(user)
    user_following = get_object_or_404(User,id=id)#user that is following. me following others
    follow_tab = Following()
    follow_tab.user = user
    follow_tab.user_following = user_following
    follow_tab.relation = False

    follow_tab.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def follow_accept(request,follow_id=None):
    user = request.user
    follow_req_accept = get_object_or_404(Following,pk=follow_id)
    follow_req_accept.relation = True
    follow_req_accept.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def follow_del_or_rej(requset,follow_id=None):#unfollow also
    del_tab = get_object_or_404(Following,pk=follow_id)
    del_tab.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def block_user(request,b_id=None):
    user = request.user
    
    b_user= get_object_or_404(User,id=b_id)

    block_tab = Blocked()
    block_tab.user = user
    block_tab.user_following = user_following.pk

    block_tab.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ui_profile(request):

    return render(request,'ui1.html')