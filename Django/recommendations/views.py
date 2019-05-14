from django.views import generic
from django.shortcuts import render
from recommendations.models import Rule
from recommendations.forms import enteringForm
from django.db.models import Q
from itertools import combinations

class entering(generic.CreateView):
    model = Rule
    template_name = 'entering.html'
    context_object_name = 'entering'
    form_class = enteringForm

    def get_context_data(self, **kwargs):
        context = super(entering, self).get_context_data(**kwargs)
        context['entering'] = enteringForm()
        return context


class results(generic.ListView):
    model = Rule
    template_name = 'results.html'
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super(results, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        inputCodes = self.request.GET['lhs']
        inputRules = inputCodes.split(",")
        inputRules.sort()

        lhs = []
        for i in range(len(inputRules)):
            lhs += list(combinations(inputRules,i+1))
            
        new_lhs = []
        for entry in lhs:
            empty = ''
            for i in range(len(entry)):
                empty += entry[i] + ","
            new_lhs.append(empty[:-1])

        code_filter = Q()
        for lhs in new_lhs:
            code_filter |= Q(lhs__iexact=lhs)
        qs = Rule.objects.filter(code_filter).values('rhs').distinct()
        for lhs in new_lhs:
            qs = qs.exclude(rhs__iregex=r'(' + '|'.join(new_lhs) + ')')
        return qs
