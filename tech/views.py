from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.conf import settings
from django.views import generic
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string, get_template
from django.forms import modelformset_factory
from django.db import models
from django.db.models import Q, signals
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import MultipleObjectMixin
from django.contrib.sites.models import Site
from .models import *
from .forms import *
from .decorators import *
from . import helpers

@unauthenticated_user
def RegisterPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='member')
            user.groups.add(group)

            messages.success(request, 'Account successfully created for ' + username)
            return redirect('login')
        else:
            messages.info(request, 'Error encountered! Check if data is valid.')

    context = {'form': form}
    return render(request, 'user/register.html', context)

@unauthenticated_user
def LoginPage(request):  
    redirect_to = request.GET.get('next', '/')
    if request.method == 'POST':
        userinput = request.POST.get('username')
        try:
            username = User.objects.get(email=userinput).username
        except User.DoesNotExist:
            username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(redirect_to)
        else:
            messages.info(request, 'Username or password incorrect.')

    return render(request, 'user/login.html')

@login_required
def ProfileUpdate(request):
    if request.method == 'POST':
        u_form = UpdateUserForm(request.POST, instance=request.user)
        p_form = UpdateProfileForm(request.POST, 
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile updated successfully.')
            return redirect('profile_update')
    else:
        u_form = UpdateUserForm(instance=request.user)
        p_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'user/profile_update.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('login')

def BlogCategory(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    blog = get_list_or_404(Blog.objects.order_by('-id'), category=category)
    blog = helpers.pg_records(request, blog, 12)
    cat_menu_list = Category.objects.all()
        
    template = 'techsite/blog/article_category.html'
    context = {'blog': blog, 'category': category, 'cat_menu_list': cat_menu_list} 
    return render(request, template, context)
    

def ForumSection(request, section_slug):
    section = get_object_or_404(Section, slug=section_slug)
    forum = get_list_or_404(Forum.objects.order_by('-id'), section=section)
    forum = helpers.pg_records(request, forum, 15)
    sec_menu_list = Section.objects.all()
        
    template = 'techsite/forum/forum_section.html'
    context = {'forum': forum, 'section': section, 'sec_menu_list': sec_menu_list}  
    return render(request, template, context)

def privacy_policy(request):
    return render(request, 'techsite/privacy_policy.html')

def terms_and_conditions(request):
    return render(request, 'techsite/terms_and_conditions.html')

def advertise(request):
    return render(request, 'techsite/advertise.html')

def contact_us(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['olaoluwasamsmith@gmail.com'])
                messages.success(request, 'Message sent successfully. You will receive a response as soon possible.')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact_us')
    return render(request, 'techsite/contact_us.html', {'form': form})


class ServiceListView(generic.ListView):
    model = Service
    template_name = 'techsite/service/service_list.html'


class ServiceDetailView(generic.DetailView):
    model = Service
    template_name = 'techsite/service/service_detail.html'
    slug_field ='slug'
    query_pk_and_slug = True


@method_decorator(admin_only, name='dispatch')
class ServiceCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Service
    template_name = 'techsite/service/service_form.html'
    form_class = ServiceForm
    slug_field = 'slug'
    query_pk_and_slug = True
    success_message = 'Post created successfully.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    model = Service
    template_name = 'techsite/service/service_form.html'
    fields = ['title', 'image', 'content']
    slug_field = 'slug'
    query_pk_and_slug = True
    success_message = 'Post updated successfully.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        service = self.get_object()
        if self.request.user == service.author:
            return True
        return False

    
class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Service
    template_name = 'techsite/service/service_delete.html'
    slug_field ='slug'
    query_pk_and_slug = True
    success_url = '/services/'

    def test_func(self):
        service = self.get_object()
        if self.request.user == service.author:
            return True
        return False

    def get_success_url(self):
        messages.warning(self.request, 'Post deleted successfully.')
        return reverse('service_list')


class ReviewListView(generic.ListView):
    model = Review
    template_name = 'techsite/review/review_list.html'
    paginate_by = 12

def ReviewDetailView(request, pk, slug):
    review = get_object_or_404(Review, pk=pk, slug=slug)
    review_related = review.tags.similar_objects()[:6]

    context = {
        'review': review,
        'review_related': review_related,
    }

    return render(request, 'techsite/review/review_detail.html', context)


@method_decorator(admin_only, name='dispatch')
class ReviewCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Review
    template_name = 'techsite/review/review_form.html'
    form_class = ReviewForm
    slug_field = 'slug'
    query_pk_and_slug = True
    success_message = 'Post created successfully.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    model = Review
    template_name = 'techsite/review/review_form.html'
    fields = ['title', 'image', 'content', 'tags']
    slug_field = 'slug'
    query_pk_and_slug = True
    success_message = 'Post updated successfully.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False

    
class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Review
    template_name = 'techsite/review/review_delete.html'
    slug_field = 'slug'
    query_pk_and_slug = True

    def test_func(self):
        review = self.get_object()
        if self.request.user == review.author:
            return True
        return False

    def get_success_url(self):
        messages.warning(self.request, 'Post deleted successfully.')
        return reverse('review_list')


class BlogListView(generic.ListView):
    model = Blog
    template_name = 'base.html'
    paginate_by = 12 

def BlogDetailView(request, pk, slug):
    blog = get_object_or_404(Blog, pk=pk, slug=slug)
    blog_related = blog.tags.similar_objects()[:6]

    context = {
        'blog': blog,
        'blog_related': blog_related,
    }

    return render(request, 'techsite/blog/article_detail.html', context)


@method_decorator(admin_only, name='dispatch')
class BlogCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Blog
    template_name = 'techsite/blog/article_form.html'
    form_class = ArticleForm
    query_pk_and_slug = True
    success_message = 'Post created successfully.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        form =self.form_class
        return render(request, 'techsite/blog/article_form.html', {'form': form})


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    model = Blog
    template_name = 'techsite/blog/article_form.html'
    fields = ['title', 'category', 'image', 'content', 'tags']
    slug_field = 'slug'
    query_pk_and_slug = True
    success_message = 'Post updated successfully.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.author:
            return True
        return False

    
class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Blog
    template_name = 'techsite/blog/article_delete.html'
    slug_field ='slug'
    query_pk_and_slug = True

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.author:
            return True
        return False

    def get_success_url(self):
        messages.warning(self.request, 'Post deleted successfully.')
        return reverse('homepage')


class ForumListView(generic.ListView):
    model = Forum
    template_name = 'techsite/forum/forum_list.html'
    paginate_by = 15

    def get_context_data(self, *args, **kwargs):
        sec_menu = Section.objects.all()
        context = super(ForumListView, self).get_context_data(*args, **kwargs)
        context['sec_menu'] = sec_menu
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(title__icontains=query)|
                Q(author__username=query)
                )
        else:
            object_list =  self.model.objects.all()
        return object_list


def ForumDetailView(request, pk, slug):
    forum = get_object_or_404(Forum, pk=pk, slug=slug)
    forum_related = forum.tags.similar_objects()[:6]
    comments = ForumComment.objects.filter(forum=forum, reply=None)
    total_comments = ForumComment.objects.filter(forum=forum, reply=None).count()
    comments = helpers.pg_records(request, comments, 10)
    is_liked = False
    is_favourite = False
    if forum.likes.filter(id=request.user.id).exists():
        is_liked = True

    if forum.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            messages.success(request, f'Submitted successfully.')
        
            if reply_id:
                comment_qs = ForumComment.objects.get(id=reply_id)
            comment = ForumComment.objects.create(forum=forum, user=request.user, content=content, reply=comment_qs)
            comment.save()
            return HttpResponseRedirect(forum.get_absolute_url())
    else:
        comment_form = CommentForm

    context = {
        'forum': forum,
        'forum_related': forum_related,
        'is_liked': is_liked,
        'is_favourite': is_favourite,
        'total_likes': forum.total_likes(),
        'comments': comments,
        'total_comments': total_comments,
        'comment_form': comment_form,
    }

    return render(request, 'techsite/forum/forum_detail.html', context)

@login_required
def FavouritePostView(request):
    user = request.user
    favourite_posts  = user.favourite.all()
    favourite_posts = helpers.pg_records(request, favourite_posts, 15)
    context = {
        'favourite_posts': favourite_posts,
    }
    return render(request, 'techsite/forum/favourite_posts.html', context)

@login_required
def FavouritePost(request, pk, slug):
    forum = get_object_or_404(Forum, pk=pk, slug=slug)
    if forum.favourite.filter(id=request.user.id).exists():
        forum.favourite.remove(request.user)
        messages.warning(request, f'Post removed from favourites.')
    else:
        forum.favourite.add(request.user)
        messages.success(request, f'Post added to favourites.')
    return HttpResponseRedirect(forum.get_absolute_url())

@login_required
@csrf_exempt
def like_forum(request):
    forum = get_object_or_404(Forum, id=request.POST.get('id'))
    is_liked = False
    if forum.likes.filter(id=request.user.id).exists():
        forum.likes.remove(request.user)
        is_liked = False
    else:
        forum.likes.add(request.user)
        is_liked = True
    
    context = {
        'forum': forum,
        'is_liked': is_liked,
        'total_likes': forum.total_likes(),
    }
#    return HttpResponseRedirect(forum.get_absolute_url())

    if request.is_ajax(): 
        html = render_to_string('techsite/forum/like_section.html', context, request=request)
        return JsonResponse({'form': html})

@login_required
def ForumCreateView(request):
    ImageFormset = modelformset_factory(ForumImages, fields=('image',), extra=2)
    if request.method == 'POST':
        form = ForumForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            forum = form.save(commit=False)
            forum.author = request.user
            forum.save()

            for f in formset:
                try:
                    photo = ForumImages(forum=forum, image=f.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    break
            messages.success(request, 'Post created successfully.')
            return HttpResponseRedirect(forum.get_absolute_url())
    else:
        form = ForumForm()
        formset = ImageFormset(queryset=ForumImages.objects.none())
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'techsite/forum/forum_form.html', context)

@login_required
def ForumImageUpdate(request, pk, slug):
    forum = get_object_or_404(Forum, pk=pk, slug=slug)
    ImageFormset = modelformset_factory(ForumImages, fields=('image',), extra=2, max_num=2)
    if forum.author != request.user:
        raise Http404()

    if request.method == 'POST':
#        form = ForumUpdateForm(request.POST or None, instance=forum)
        formset = ImageFormset(request.POST, request.FILES)
#        if form.is_valid() and formset.is_valid():
        if formset.is_valid():
#            formset.save()
            print(formset.cleaned_data)
            data = ForumImages.objects.filter(forum=forum)
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        photo = ForumImages(forum=forum, image=f.cleaned_data.get('image'))
                        photo.save()
                    elif f.cleaned_data['image'] is False:
                        photo = ForumImages.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                        photo.delete()
                    else:
                        photo = ForumImages(forum=forum, image=f.cleaned_data.get('image'))
                        d = ForumImages.objects.get(id=data[index].id)
                        d.image = photo.image
                        d.save()

            messages.success(request, 'Image uploaded successfully.')                
            return HttpResponseRedirect(forum.get_absolute_url())
    else:
#        form = ForumUpdateForm()
        formset = ImageFormset(queryset=ForumImages.objects.filter(forum=forum))
    context = {
#        'form': form,
        'forum': forum,
        'formset': formset,
    }
    return render(request, 'techsite/forum/forum_update_image.html', context)


class ForumUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    model = Forum
    template_name = 'techsite/forum/forum_form.html'
    fields = ['title', 'section', 'content']
    slug_field ='slug'
    query_pk_and_slug = True
    success_message = 'Post updated successfully.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        forum = self.get_object()
        if self.request.user == forum.author:
            return True
        return False

   
class ForumDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Forum
    template_name = 'techsite/forum/forum_delete.html'
    slug_field ='slug'
    query_pk_and_slug = True

    def test_func(self):
        forum = self.get_object()
        if self.request.user == forum.author or admin_only:
            return True
        return False

    def get_success_url(self):
        messages.warning(self.request, 'Post deleted successfully.')
        return reverse('forum_list')

class ForumCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = ForumComment
    template_name = 'techsite/forum/comment_delete.html'
    slug_field ='slug'
    query_pk_and_slug = True

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user or admin_only:
            return True
        return False

    def get_success_url(self):
        messages.warning(self.request, 'Deleted successfully.')
        return reverse('forum_detail', kwargs={'slug': self.object.forum.slug, 'pk': self.object.forum.id})


class ProfileView(LoginRequiredMixin, generic.DetailView, MultipleObjectMixin):
    model = Forum
    template_name = 'user/profile_view.html'
    paginate_by = 10

    queryset = User.objects.all()

    def get_object(self):
        UserName = self.kwargs.get("username")
        return get_object_or_404(User, username=UserName)

    def get_context_data(self, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        object_list = Forum.objects.filter(author=user).order_by('-created_date')
        context = super(ProfileView, self).get_context_data(object_list=object_list, *args, **kwargs)
        return context  