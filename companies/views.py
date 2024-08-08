from .forms import CompanyForm, AttachDocumentForm
from .models import Company as CompanyModel
from .models import AttachDocument, Metrics

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404


def addMetric(request, slug):
    try:
        company = get_object_or_404(CompanyModel, slug=slug)
    except Http404:
        messages.info(request, "Company can't be found")
        return redirect(reverse("seeCompany", kwargs={"slug": slug}))

    metrics = Metrics.objects.create(
        company=company,
        title=request.POST.get("title"),
        value=request.POST.get("value"),
    )

    metrics.save()
    messages.success(request, "Metric added successfully")

    return redirect(reverse("seeCompany", kwargs={"slug": slug}))


def removeDocument(request, slug):
    try:
        document = get_object_or_404(AttachDocument, slug=slug)
    except Http404:
        messages.info(request, "Documents can't be found")
        return redirect(reverse("seeCompany", kwargs={"slug": document.company.slug}))

    if document.company.user != request.user:
        messages.warning(request, "You can't delete this document")
        return redirect(reverse("seeCompany", kwargs={"slug": document.company.slug}))

    document.delete()
    messages.success(request, "Document deleted sucessfully")

    return redirect(reverse("seeCompany", kwargs={"slug": document.company.slug}))


def seeCompany(request, slug):
    try:
        _company = get_object_or_404(CompanyModel, slug=slug)
    except Http404:
        messages.info(request, "Company can't be found")
        return redirect(reverse("showCompany"))

    documents = AttachDocument.objects.all()
    form = AttachDocumentForm()
    context = {"company": _company, "form": form, "documents": documents}

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


def showCompany(request):
    companies = CompanyModel.objects.all()

    if request.method == "POST":
        name = request.POST.get("company", None)

        if not name:
            messages.info(request, "Please, enter the company name")
            return redirect("/")

        companies = CompanyModel.objects.filter(name__icontains=name)

    context = {"companies": companies}
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
