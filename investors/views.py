from django.shortcuts import render
from companies.modelChoices import area_choices
from companies.models import Company


def sugest(request):
    context = {"areas": area_choices}

    if request.method == "POST":
        type = request.POST.get("type")
        area = request.POST.getlist("area")
        value = request.POST.get("value")

        if type == "C":
            companies = Company.objects.filter(existence_time="+5").filter(
                internship="E"
            )
        if type == "S":
            companies = Company.objects.filter(
                existence_time__in=["+6", "-6", "+1"]
            ).exclude(internship="E")

        companies = companies.filter(area__in=area)

        # # TODO: use advanced Django ORM functions, like annotate with ExpressionWrapper(), and F()
        companies_list = []
        for company in companies:
            percentual = (float(value) * 100) / float(company.get_valuation)

            if percentual >= 1:
                companies_list.append(company)

        print(companies_list)
        if len(companies_list) == 0:
            companies_list = None

        context["companies"] = companies_list

    return render(request, "investors/sugest.html", context=context)
