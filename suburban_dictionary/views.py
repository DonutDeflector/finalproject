from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as logout_request
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse

from .models import Term, Definition

import json


# Create your views here.


def index(request):
    # redirects users to the login page if they are not logged in
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "suburban_dictionary/index.html")


def login(request):
    if request.method == "POST":
        # capture form inputs
        username = request.POST["username"]
        password = request.POST["password"]

        # authenticate the user
        user = authenticate(request, username=username, password=password)

        # if authentication is useful, login the user and redirect them to index
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # if authentication fails, render login page with error message
        else:
            return render(request, "suburban_dictionary/login.html",
                          {"message": "Invalid credentials.",
                           "status": "danger"})

    # redirect users to index if they are already logged in
    if request.user.is_authenticated:
        return redirect("index")

    return render(request, "suburban_dictionary/login.html")


def register(request):
    if request.method == "POST":
        # capture form inputs
        first_name = request.POST["first-name"]
        last_name = request.POST["last-name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm-password"]

        # Capitalize first and last name
        first_name.capitalize()
        last_name.capitalize()

        # if passwords match, proceed; else, inform the user
        if password == confirm_password:
            # if the username is already taken, inform the user
            if User.objects.filter(username=username).exists():
                return render(request, "suburban_dictionary/register.html",
                              {"message": "Username already taken.",
                               "status": "danger"})
            # if the password is too short, inform the user
            if len(password) < 8:
                return render(request, "suburban_dictionary/register.html",
                              {"message": "Passwords must be at least 8 \
                               characters in length.",
                               "status": "danger"})
            # register user
            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name,
                email=email, password=password)
            user.save()

            # redirect user to login page, display success message
            return render(request, "suburban_dictionary/login.html",
                          {"message": "Successfully registered. Please login.",
                           "status": "success"})
        # informs the user if the passwords don't match
        else:
            return render(request, "suburban_dictionary/register.html",
                          {"message": "Passwords don't match.",
                           "status": "danger"})

    # redirects user to the index if the are already logged in
    if request.user.is_authenticated:
        return redirect("index")

    return render(request, "suburban_dictionary/register.html")


def logout(request):
    logout_request(request)

    return render(request, "suburban_dictionary/login.html",
                  {"message": "Logged out.",
                   "status": "success"})


def create_definition(request):
    # redirects users to the login page if they are not logged in
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        # get username of current user
        username = request.user

        # capture form inputs
        name = request.POST["term"]
        definition = request.POST["definition"]
        example = request.POST["example"]

        # convert name to lowercase
        name = name.lower()

        # check to see if any forms are empty, return error message if true
        if name is None or definition is None or example is None:
            return render(request, "suburban_dictionary/create_definition.html",
                          {"message": "ERROR: one or more fields were submitted empty.",
                           "status": "danger"})

        # if term not already in database, add it
        if Term.objects.filter(name=name).count() == 0:
            term = Term.objects.create(name=name)
            term.save()

        # find term object for the submission
        term = Term.objects.get(name=name)

        # add definition and example to the database
        definition = Definition.objects.create(
            term=term, definition=definition, example=example, username=username)
        definition.save()

    return render(request, "suburban_dictionary/create_definition.html")


def term(request, term_name):
    # remove underscores from term name
    term_name = term_name.replace("_", " ")

    # if the term doesn't exist, return page to inform user
    if Term.objects.filter(name=term_name).count() == 0:
        return render(request, "suburban_dictionary/no_term.html")

    # fetch term
    term = Term.objects.get(name=term_name)

    # fetch definitions
    definitions = Definition.objects.filter(term=term)

    return render(request, "suburban_dictionary/term.html",
                  {"term": term, "definitions": definitions})


def search_for_term(request):
    if request.method == "POST":
        # capture form inputs
        name = request.POST["term"]

        # convert name to lowercase
        name = name.lower()

        # search for matches in the database
        search_results = Term.objects.filter(name__icontains=name)

        # if no results are returned, render page to notify user
        if search_results.count() == 0:
            return render(request, "suburban_dictionary/no_term.html")

        # if only one term is returned, return page with only that term
        if search_results.count() == 1:
            term_name = name.replace(" ", "_")

            return redirect("term", term_name)

        # render search page with results
        return render(request, "suburban_dictionary/search_results.html", {
            "search_results": search_results
        })


def like_definition(request):
    if request.method == "POST":
        # fetch the user making the request
        current_user_id = request.user.id

        # capture ajax request data
        data = json.loads(request.body)

        # capture liked term id
        definition_id = data["definition_id"]

        # fetch definition by id
        definition = Definition.objects.filter(pk=definition_id)

        # fetch list of users who liked the post
        definition_liked_by = definition.values("liked_by")

        # check to see if user has already liked the definition, if so, remove
        # their like; otherwise, submit their like
        if definition.filter(liked_by=current_user_id):
            print("who")
        else:
            print("ha")

        return JsonResponse({"success": True})
