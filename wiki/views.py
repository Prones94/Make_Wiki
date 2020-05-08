from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.utils.text import slugify

from wiki.models import Page
from wiki.forms import PageForm


class PageListView(ListView):
    """ Renders a list of all Pages. """
    model = Page

    def get(self, request):
        """ GET a list of Pages. """
        pages = self.get_queryset().all()
        return render(request, 'list.html', {
          'pages': pages
        })

class PageDetailView(DetailView):
    """ Renders a specific page based on it's slug."""
    model = Page

    def get(self, request, slug):
        """ Returns a specific wiki page by slug. """
        page = self.get_queryset().get(slug__iexact=slug)
        return render(request, 'page.html', {
          'page': page,
          'form': PageForm()
        })

    def post(self, request, slug, *args, **kwargs):
      form = PageForm(request.POST)

      if form.is_valid:
        Page = self.get_queryset().get(slug__iexact=slug)
        Page.title  = request.POST['title']
        Page.content = request.POST['content']
        Page.modified = datetime.now()
        Page.slug = slugify(Page.title, allow_unicode=True)
        # Page = form.save(commit=False)
        Page.author = request.user
        Page.save()
        return HttpResponseRedirect(reverse('wiki-details-page', args=[Page.slug]))
      return render(request, 'page.html', { 'form': form })


class PageCreateView(LoginRequiredMixin, CreateView):
  
  def get(self, request, *args, **kwargs):
    context = {
      'form': PageForm()
    }
    return render(request, 'create.html', context)

  def post(self, request, *args, **kwargs):
    form = PageForm(request.POST)

    if form.is_valid:
      Page = form.save(commit=False)
      Page.author = request.user
      Page = form.save()
      return HttpResponseRedirect(reverse('wiki-details-page', args=[Page.slug]))
    return render(request, 'create.html',{ 'form': form })