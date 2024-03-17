from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views import View
from django.views.generic import ListView
from django.db.models import Count
from django.core.paginator import Paginator

from .forms import TagForm, AuthorForm, QuoteForm
from .models import Author, Tag, Quote


class AuthorDetail(View):
    template_name = 'authordetail.html'

    def get(self, request, author_id):
        author = get_object_or_404(Author, pk=author_id)
        return render(request, self.template_name, {'author': author})


class Quotes(View):
    template_name = 'quotes.html'
    paginate_by = 5

    def get(self, request):
        queryset = Quote.objects.all()
        tag = request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__name__icontains=tag)
            query_string = f'&tag={tag}'
        else:
            query_string = ''
        paginator = Paginator(queryset, self.paginate_by)
        page_obj = paginator.get_page(request.GET.get('page'))

        top_tags = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
        return render(request, self.template_name, {'top_tags': top_tags,
                                                    'page_obj': page_obj,
                                                    'query_string': query_string})


@method_decorator(login_required, name='dispatch')
class AddTag(View):
    template_name = 'addtag.html'
    form_class = TagForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='noteapp:addtag')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class AddAuthor(View):
    template_name = 'addauthor.html'
    form_class = AuthorForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='noteapp:addauthor')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class AddQuote(View):
    template_name = 'addquote.html'
    form_class = QuoteForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class,
                                                    'tags': Tag.objects.all(),
                                                    'authors': Author.objects.all()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='noteapp:addquote')
        return render(request, self.template_name, {'form': form,
                                                    'tags': Tag.objects.all(),
                                                    'authors': Author.objects.all()})
