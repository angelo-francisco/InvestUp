from .forms import CompanyForm, AttachDocumentForm
from .models import Company as CompanyModel
from .models import AttachDocument, Metrics, Notifications

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from investors.models import InvestmentProposal
from django.db.models import Sum


@login_required
def my_companies(request):
    companies = CompanyModel.objects.filter(user=request.user) or 0

    return render(
        request,
        "companies/my.html",
        {"companies": companies, "search": bool(companies)},
    )


@login_required
def manage_proposal(request, id):
    type = request.GET.get("acao")
    ip = InvestmentProposal.objects.get(id=id)

    if type == "yes":
        ip.status = "PA"
        notf = Notifications.objects.create(
            user=ip.investor,
            company=ip.company,
            title=f"You're proposal to {ip.company.name} was accepted"
        )
        notf.save()
        messages.success(request, "Proposal accepted")

    elif type == "no":
        ip.status = "PR"
        notf = Notifications.objects.create(
            user=ip.investor,
            company=ip.company,
            title=f"You're proposal to {ip.company.name} was not accepted"
        )
        notf.save()
        messages.success(request, "Proposal rejected")

    ip.save()
    return redirect(reverse("seeCompany", kwargs={"slug": ip.company.slug}))


@login_required
def addMetric(request, slug):
    company = get_object_or_404(CompanyModel, slug=slug)
    if company.user != request.user:
        messages.info(request, "This company is not your")
        return redirect(reverse("showCompany"))

    metrics = Metrics.objects.create(
        company=company,
        title=request.POST.get("title"),
        value=request.POST.get("value"),
    )

    metrics.save()
    messages.success(request, "Metric added successfully")

    return redirect(reverse("seeCompany", kwargs={"slug": slug}))


@login_required
def removeDocument(request, slug):
    document = get_object_or_404(AttachDocument, slug=slug)

    if document.company.user != request.user:
        messages.warning(request, "You can't delete this document")
        return redirect(reverse("seeCompany", kwargs={"slug": document.company.slug}))

    document.delete()
    messages.success(request, "Document deleted sucessfully")

    return redirect(reverse("seeCompany", kwargs={"slug": document.company.slug}))


@login_required
def seeCompany(request, slug):
    _company = get_object_or_404(CompanyModel, slug=slug)

    if _company.user != request.user:
        messages.info(request, "This company is not your")
        return redirect(reverse("showCompany"))

    investment_proposal = InvestmentProposal.objects.filter(company=_company)
    investment_proposal_sent = investment_proposal.filter(status="PE")
    percentual = (
        sum(
            investment_proposal.filter(status="PA").values_list("percentual", flat=True)
        )
        or 1
    )
    total_captado = sum(
        investment_proposal.filter(status="PA").values_list("value", flat=True)
    )
    total_investors = (
        investment_proposal.filter(status="PA").values("investor").distinct().count()
    )
    current_valuation = ((float(total_captado) * 100) / float(percentual)) or 0
    documents = AttachDocument.objects.filter(company=_company)
    form = AttachDocumentForm()

    context = {
        "company": _company,
        "form": form,
        "documents": documents,
        "investment_proposal_sent": investment_proposal_sent,
        "sold_percentual": int(percentual),
        "total_captado": round(total_captado, 2),
        "total_investors": total_investors,
        "current_valuation": round(current_valuation, 2),
    }

    if request.method == "POST":
        formPOST = AttachDocumentForm(
            request.POST, request.FILES, user=request.user, company=_company
        )

        if formPOST.is_valid() and formPOST.is_multipart():
            instance = formPOST.save(commit=False)
            instance.company = _company
            instance.save()

            messages.success(request, "Document attached successfully")
        else:
            context["form"] = formPOST

    return render(request, "companies/see.html", context=context)


@login_required
def showCompany(request):
    companies = CompanyModel.objects.all()
    companies_list = []

    for company in companies:
        percentual_sum = (
            InvestmentProposal.objects.filter(
                company=company,
                status="PA",
            ).aggregate(total_percentual=Sum("percentual"))["total_percentual"]
            or 0
        )

        companies_list.append({"company": company, "percentual": percentual_sum})

    if request.method == "POST":
        name = request.POST.get("company", None)

        if not name:
            messages.info(request, "Please, enter the company name")
            return redirect("/")

        companies = CompanyModel.objects.filter(name__icontains=name)
        companies_list = []

        for company in companies:
            percentual_sum = (
                InvestmentProposal.objects.filter(
                    company=company,
                    status="PA",
                ).aggregate(total_percentual=Sum("percentual"))["total_percentual"]
                or 0
            )

            companies_list.append({"company": company, "percentual": percentual_sum})

    context = {"companies": companies_list}
    return render(request, "companies/show.html", context=context)


@login_required
def addCompany(request):
    form = CompanyForm()

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)

        if form.is_valid() and form.is_multipart():
            instance = form.save(commit=False)
            instance.user = request.user

            instance.save()
            messages.success(request, "New company added successfully!")
            return redirect(reverse("showCompany"))

    context = {"form": form}
    return render(request, "companies/new.html", context=context)
