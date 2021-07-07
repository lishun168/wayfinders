from django.shortcuts import render
from django.views import View
from .models import SearchTags

class Search(View):
    template_name = 'search/search.html'

    def get(self, request, search_string):
        search_results = SearchTags.models.filter(tag__contains=search_string)

        context = {
            'results': search_results
        }

        return (request, context, self.template)