from django.shortcuts import render,get_object_or_404,redirect
from  BlogApp.models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from  django.views.generic import ListView,CreateView,DeleteView
from BlogApp.forms import EmailSendForm,CommentForm,SignupForm,postform
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

# Create your views here.
def post_list_view(request):
    post_list = Post.objects.all()
    return render(request,'BlogApp/post_list.html',{"post_list":post_list})

def post_detail_view(request, year,month,day,post):
    post=get_object_or_404(Post,slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day)
    return render(request, "BlogApp/post_detail.html",{'post':post})
@login_required
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    for post in post_list:
        print(post.images.name[-3::])
    tag = None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])
    paginator=Paginator(post_list,2)		#no.of.pages(20/2-rec=>10-pages)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'BlogApp/post_list.html',{"post_list":post_list,'tag':tag})

class PostListView(ListView):
    model=Post
    paginate_by=1


#def homepage(request):
#print(send_mail('Hello', 'Very imp msg....','srinivas.kosuru456@gmail.com',['pogularani397@gmail.com','venkatchouhan01@gmail.com']))

def mail_send_view(request,id):
    print('hi')
    post = get_object_or_404(Post,id=id,status = 'published')
    sent = False
    form = EmailSendForm()
    if request.method =='POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommeds you to read"{}"'.format(cd['name'],cd['email'],post.title)
            message = "Read Post At:\n{}\n\n{} 'comments:\n{}".format(post_url,cd['name'],cd['comment'])
            send_mail(subject,message,'srinivas.kosuru456@gmil.com',[cd['to']])
            sent=True
        else:
            form=EmailSendForm()
    return render(request,'BlogApp/sharebymail.html',{'post':post,'form':form,'sent':sent})



def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug = post,
                           status = 'published',
                           publish__year=year,
                           publish__month = month,
                           publish__day = day)
    post_tags_ids = post.tags.values_list('id',flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))
    comment = post.comments.filter(active=True)
    csubmit = False
    if request.method=='POST':
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit =True
    else:
        form = CommentForm()
    return render(request,'BlogApp/post_detail.html',{'post':post,'form':form,'comment':comment,'csubmit':csubmit,'similar_posts':similar_posts})


def Postview(request):
    return render(request,'BlogApp/postmain.html')

def signup_view(request):
    sent = False
    formobj=SignupForm()
    if request.method=="POST":
        formobj=SignupForm(request.POST)
        if formobj.is_valid():
            user=formobj.save()
            user.set_password(user.password)
            user.save()
            sent = True
        return HttpResponseRedirect('/accounts/login/',{'sent':sent})
    else:
        formobj = SignupForm()
    return render(request, 'BlogApp/signup.html',{'formobj':formobj,'sent':sent})

def logoutview(request):
    request.session.clear()
    return render(request, 'BlogApp/logout.html')


def post_view(request):
    sent = False
    form=postform()
    print('welcome')
    if request.method=='POST':
        form=postform(request.POST, request.FILES)
        if form.is_valid():
            print('hi')
            user=form.save(commit=True)
            print('hello')
            return HttpResponseRedirect('/thankyou/',)
    print('bye')
    return render(request,'BlogApp/postlogin.html',{'form':form,'sent':sent,})


def thankyou_view(request):
    return render(request,'BlogApp/thankyou.html')

def homepageview(request):
    return render(request, 'BlogApp/homepage.html')

class commentdeleteview(DeleteView):
    model = Comment
    success_url = reverse_lazy('succ')

def succview(request):
    return render(request, 'BlogApp/delete.html')

class postdeleteview(DeleteView):
    model = Post
    success_url = reverse_lazy('postsucc')

def postsuccview(request):
    return render(request, 'BlogApp/delete.html')
