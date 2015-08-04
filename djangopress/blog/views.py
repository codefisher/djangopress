import datetime

from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from djangopress.blog.models import Blog, Entry, Tag, Category, Comment, Flag
from django.utils.translation import ugettext as _
from django.conf import settings
from djangopress.core.util import get_client_ip, choose_form
from django.core.urlresolvers import reverse
from django.utils import timezone

try:
    import akismet
except:
    pass


def get_blog(blog_slug):
    return get_object_or_404(Blog, slug=blog_slug, sites__id__exact=settings.SITE_ID)

def get_entries_for_page(paginator, page):
    try:
        page = int(page)
    except ValueError:
        page = 1
    try:
        return paginator.page(page)
    except (EmptyPage, InvalidPage) as e:
        raise e # this must be handeled

def index(request, blog_slug, page=1):
    blog = get_blog(blog_slug)
    entries_list = Entry.objects.get_entries(blog=blog)
    paginator = Paginator(entries_list, 10)
    try:
        entries = get_entries_for_page(paginator, page)
    except (EmptyPage, InvalidPage):
        if page != 1:
            return redirect(blog.get_absolute_url(paginator.num_pages))
    data =  {
        "blog": blog,
        "entries": entries,
        "title": blog.name,
        "respond": True,
    }
    return render(request, 'blog/index.html' , data)

def archive(request, blog_slug, year, month=None):
    blog = get_blog(blog_slug)
    data = {"format": "YEAR_MONTH_FORMAT"}
    year = int(year)
    with timezone.override(None):
        entries_list = Entry.objects.get_entries(blog=blog).filter(posted__year=year)
        if month is None:
            month = 1
            data["format"] = "Y"
        else:
            month = int(month)
            entries_list = entries_list.filter(posted__month=month)
    data["date"] = datetime.date(year=year, month=month, day=1)
    paginator = Paginator(entries_list, 10)
    try:
        entries = get_entries_for_page(paginator, request.GET.get('page', 1))
    except (EmptyPage, InvalidPage):
        if request.GET.get('page', 1) != 1:
            kwargs = {'blog_slug':blog_slug, 'year':year, 'month':month}
            return redirect("%s?page=%s" % (reverse('blog-archive', kwargs=kwargs), paginator.num_pages))
    data.update({
        "blog": blog,
        "entries": entries,
        "title": blog.name,
        "respond": True,
    })
    return render(request, 'blog/date_archive.html' , data)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user_name', 'user_email', 'user_url', 'comment_text')
        
    user_name = forms.CharField(required=True)
    user_email = forms.CharField(required=True)
        
class CommentUserForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text', )
        
def check_askmet_spam(request, entry, comment_form):
    api = akismet.Akismet()
    api.setAPIKey(settings.AKISMET_API_KEY)
    if api.verify_key():
        data = {
                "user_ip": get_client_ip(request),
                "user_agent": request.META.get("HTTP_USER_AGENT"),
                "referrer": request.META.get("HTTP_REFERER"),
                "permalink": entry.get_absolute_url(),
        }
        if request.user.is_authenticated():
            data.update({
                "comment_author": request.user.username,
                "comment_author_email": request.user.email,
                "comment_author_url": request.user.profile.homepage,
            })
        else:
            data.update({
                "comment_author": comment_form.cleaned_data["user_name"],
                "comment_author_email": comment_form.cleaned_data["user_email"],
                "comment_author_url": comment_form.cleaned_data["user_url"],
            })
        return api.comment_check(comment_form.cleaned_data["comment_text"], data)
    return False

def post(request, blog_slug, year, month, day, slug):
    blog = get_blog(blog_slug)
    with timezone.override(None):
        entry = get_object_or_404(Entry, blog=blog, slug=slug, posted__year=year, posted__month=month, posted__day=day)
    try:
        previous_post = Entry.get_previous_by_posted(entry, blog=blog)
    except Entry.DoesNotExist:
        previous_post = None
    try:
        next_post = Entry.get_next_by_posted(entry, blog=blog)
    except Entry.DoesNotExist:
        next_post = None
    comments = Comment.objects.filter(entry=entry, is_public=True, is_spam=False).order_by('submit_date')
    comment_message = ""
    if entry.comments_open and blog.comments_enabled and request.method == 'POST':
        comment_form = choose_form(request, CommentUserForm, CommentForm, request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            if request.user.is_authenticated():
                comment.user = request.user
            comment.ip_address = get_client_ip(request)
            comment.entry = entry
            comment.user_agent = request.META.get("HTTP_USER_AGENT")

            try:
                comment.is_spam = check_askmet_spam(request, entry, comment_form)
            except:
                pass # it is not installed, no problem
            
            comment.save()
            comment_message = "Your comment has been saved."
    else:
        comment_form = choose_form(request, CommentUserForm, CommentForm)
    data = {
        "title": entry.title,
        "entry": entry,
        "respond": False,
        "next": next_post,
        "previous": previous_post,
        "blog": blog,
        "comments": comments,
        "comment_count": comments.count(),
        "comment_form": comment_form,
        "comment_message": comment_message,
    }
    return render(request, "blog/post.html", data)

def tag(request, blog_slug, slug, page=1):
    blog = get_blog(blog_slug)
    post_tag = get_object_or_404(Tag, slug=slug, blog=blog)
    entries_list = Entry.objects.get_entries(blog=blog).filter(tags__slug=slug)
    paginator = Paginator(entries_list, 10)
    try:
        entries = get_entries_for_page(paginator, page)
    except (EmptyPage, InvalidPage):
        if page != 1:
            kwargs = {'blog_slug':blog_slug, 'page':page}
            return redirect(reverse('blog-tag', kwargs=kwargs))
    data =  {
        "blog": blog,
        "entries": entries,
        "title": blog.name,
        "respond": True,
        "blog_heading": _("Posts Tagged '%s'") % post_tag.name
    }
    
    return render(request, 'blog/category.html' , data)

def category(request, blog_slug, slug, page=1):
    blog = get_blog(blog_slug)
    post_category = get_object_or_404(Category, slug=slug, blog=blog)
    entries_list = Entry.objects.get_entries(blog=blog).filter(categories__slug=slug)
    paginator = Paginator(entries_list, 10)
    try:
        entries = get_entries_for_page(paginator, page)
    except (EmptyPage, InvalidPage):
        if page != 1:
            kwargs = {'blog_slug':blog_slug, 'page':page}
            return redirect(reverse('blog-category', kwargs=kwargs))
    data =  {
        "blog": blog,
        "entries": entries,
        "title": blog.name,
        "respond": True,
        "blog_heading": _("Archive for the '%s' Category") % post_category.name
    }
    return render(request, 'blog/category.html' , data)

def moved(request, blog_slug, post):
    blog = get_blog(blog_slug)
    entry = get_object_or_404(Entry, pk=post, blog=blog)
    return redirect(entry.get_absolute_url(), permanent=True)
