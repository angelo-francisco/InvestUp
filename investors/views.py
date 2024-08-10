from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from companies.modelChoices import area_choices
from companies.models import Company, AttachDocument, Metrics
from django.contrib.auth.decorators import login_required
from .models import InvestmentProposal
from django.contrib import messages


@login_required
def sign_contract(request, id):
    investment_proposal = get_object_or_404(InvestmentProposal, id=id)
    context = {"investment_proposal": investment_proposal}
    if investment_proposal.status not in "AS":
        messages.warning(request, "this proposal isn't waiting for sign")
        return redirect(
            reverse(
                "seeCompanyInvestors", kwargs={"slug": investment_proposal.company.slug}
            )
        )

    if request.method == "POST":
        rg = request.FILES.get("rg")
        selfie = request.FILES.get("selfie")

        investment_proposal.selfie = selfie
        investment_proposal.rg = rg
        investment_proposal.status = "PE"

        investment_proposal.save()
        messages.success(request, "Proposl added successfully")
        return redirect(
            reverse(
                "seeCompanyInvestors", kwargs={"slug": investment_proposal.company.slug}
            )
        )
    return render(request, "investors/sign_contract.html", context=context)


@login_required
def newProposalInvestors(request, slug):
    _company = get_object_or_404(Company, slug=slug)
    value = request.POST.get("value")
    percentual = request.POST.get("percentual")

    accepted_proposals = InvestmentProposal.objects.filter(company=_company).filter(
        status="PA"
    )
    total = 0

    for ap in accepted_proposals:
        total += ap.percentual

    if total + int(percentual) > _company.percentual_equity:
        messages.warning(request, "Equity percentual will be over the limit")
        return redirect(reverse("seeCompanyInvestors", kwargs={"slug": slug}))

    valuation = (int(value) * 100) / int(percentual)
    if valuation < int(_company.get_valuation):
        messages.warning(
            request,
            f"You're valuation was {valuation:.2f}, but need to be equal or upper than {_company.get_valuation:.2f} ",
        )
        return redirect(reverse("seeCompanyInvestors", kwargs={"slug": slug}))

    investment_proposal = InvestmentProposal(
        value=value,
        percentual=percentual,
        company=_company,
        investor=request.user,
    )

    investment_proposal.save()
    return redirect(reverse("sign_contract", kwargs={"id": investment_proposal.id}))


@login_required
def seeCompanyInvestors(request, slug):
    company = get_object_or_404(Company, slug=slug)
    documents = AttachDocument.objects.filter(company=company)
    metrics = Metrics.objects.filter(company=company)
    percentual = sum(InvestmentProposal.objects.filter(company=company).filter(status='PA').values_list('percentual', flat=True))
    up_80 = False
    limiar = (company.percentual_equity * 80) / 100
    disp_percentual = company.percentual_equity - percentual

    if percentual >= limiar:
        up_80 = True

    context = {
        "company": company, 
        "docs": documents, 
        "metrics": metrics,
        "percentual": int(percentual),
        'up_80': up_80,
        'disp_percentual': disp_percentual
    }
    return render(request, "investors/see.html", context=context)


@login_required
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
        search = True
        # # TODO: use advanced Django ORM functions, like annotate with ExpressionWrapper(), and F()
        companies_list = []
        for company in companies:
            percentual = (float(value) * 100) / float(company.get_valuation)

            if percentual >= 1:
                companies_list.append(company)

        if len(companies_list) == 0:
            search = False

        context["companies"] = companies_list
        context["search"] = search

    return render(request, "investors/sugest.html", context=context)
