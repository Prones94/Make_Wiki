from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect


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

    def get(self, **kwargs):
        """ Returns a specific wiki page by slug. """
        # page = self.get_queryset().get(slug__iexact=slug)
        # return render(request, 'page.html', {
        #   'page': page
        # })
        context = super().get_context_data(**kwargs)
        context['edit_form'] = PageForm()
        return context

    def post(self, request, pk):
      form = PageForm(request.POST)
      if form.is_valid:
        page = form.save(commit=False)
        page.author = request.user
        return HttpResponseRedirect(reverse('page:detail', args=[pk]))

      context = {
        'edit_form': form,
        'page': Page.objects.get(pk=pk)
      }
      return render(request, 'wiki/detail.html', context)


class PageCreateView(LoginRequiredMixin, CreateView):
  login_url = reverse_lazy('create')
  def get(self, request, *args, **kwargs):
    context = {
      'page': PageForm()
    }
    return render(request, 'page.html', context)

  def post(self, request, *args, **kwargs):
    form = PageForm(request.POST)
    if form.is_valid:
      page = form.save(commit=False)
      page.author = request.user
      page = form.save()
      return HttpResponseRedirect(reverse('wiki-create-page', args=[page.id]))
    return render(request, 'create.html',{'form': form})