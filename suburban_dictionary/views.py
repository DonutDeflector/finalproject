from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as logout_request
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse
from django.db.models import F

from .models import Term, Definition

import json


# Create your views here.


def index(request):
    # redirects users to the login page if they are not logged in
    if not request.user.is_authenticated:
        return redirect("login")

    # fetch latest 20 definitions
    definitions = Definition.objects.all().order_by("created_date")[:20][::-1]

    return render(request, "suburban_dictionary/index.html",
                  {"definitions": definitions})


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


def new_definition(request):
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
            return render(request, "suburban_dictionary/new_definition.html",
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

        return redirect("term", name)

    return render(request, "suburban_dictionary/new_definition.html")


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
    # define search_results in anticipation for access check
    search_results = None

    if request.method == "POST":
        # capture form inputs
        search_query = request.POST["search_query"]

        # convert name to lowercase
        search_query = search_query.lower()

        # search for matches in the database
        search_results = Term.objects.filter(name__icontains=search_query)

        # if no results are returned, render page to notify user
        if search_results.count() == 0:
            return render(request, "suburban_dictionary/no_term.html")

        # if only one term is returned, return page with only that term
        if search_results.count() == 1:
            term_name = Term.objects.values_list(
                "name", flat=True).get(name__icontains=search_query)
            print(term_name)

            return redirect("term", term_name)

    # if user is just accessing the page via url, search_results will still be
    # None; deny them access
    if search_results == None:
        return redirect("index")

    # render search page with results
    return render(request, "suburban_dictionary/search_results.html", {
        "search_results": search_results, "search_query": search_query})


def like_definition(request):
    if request.method == "POST":
        # fetch the user making the request
        current_user_id = request.user.id

        # capture ajax request data
        data = json.loads(request.body)

        # capture liked term id
        definition_id = data["definition_id"]

        # capture the liked term's definition object
        definition = Definition.objects.get(pk=definition_id)

        # fetches the definition, returns queryset if user has liked the post
        definition_likes = Definition.objects.values(
            "likes").filter(pk=definition_id, likes=current_user_id)

        # if user already liked, remove user's like and decrements like counter
        if definition_likes:
            # removes user from the liked list
            definition.likes.remove(current_user_id)

            # set variable to denote state of user's like
            liked = False

        # else, add their like and increment the likes counter
        else:
            # add user to the liked list
            definition.likes.add(User.objects.get(pk=current_user_id))

            # set variable to denote state of user's like
            liked = True

        # fetch definition, returns queryset if user has disliked it
        definition_dislikes = Definition.objects.values(
            "dislikes").filter(pk=definition_id, dislikes=current_user_id)

        # check to see if the user has disliked the definition
        if definition_dislikes:
            # remove user from the disliked list
            definition.dislikes.remove(current_user_id)

        # find number of definition likes and dislikes
        likes_count = definition.likes.count()
        dislikes_count = definition.dislikes.count()

        # return number of likes and user's like and dislike status as JSON
        return JsonResponse({"liked": liked, "likes_count": likes_count,
                             "dislikes_count": dislikes_count})

    return HttpResponseForbidden()


def dislike_definition(request):
    if request.method == "POST":
        # fetch the user making the request
        current_user_id = request.user.id

        # capture ajax request data
        data = json.loads(request.body)

        # capture disliked term id
        definition_id = data["definition_id"]

        # capture the disliked term's definition object
        definition = Definition.objects.get(pk=definition_id)

        # fetch definition, returns queryset if user has disliked it
        definition_dislikes = Definition.objects.values(
            "dislikes").filter(pk=definition_id, dislikes=current_user_id)

        # if user already disliked, remove user's dislike and decrements dislike
        # counter
        if definition_dislikes:
            # removes user from the list
            definition.dislikes.remove(current_user_id)

            # set variable to denote state of user's dislike
            disliked = False
        # else, add their dislike and increment the dislikes counter
        else:
            # add user to the list
            definition.dislikes.add(User.objects.get(pk=current_user_id))

            # set variable to denote state of user's dislike
            disliked = True

        # fetches the definition, returns queryset if user has liked the post
        definition_likes = Definition.objects.values(
            "likes").filter(pk=definition_id, likes=current_user_id)

        # if user already liked, remove user's like and decrements like counter
        if definition_likes:
            # removes user from the liked list
            definition.likes.remove(current_user_id)

        # find number of definition likes and dislikes
        likes_count = definition.likes.count()
        dislikes_count = definition.dislikes.count()

        # return number of likes and user's like status as JSON
        return JsonResponse({"disliked": disliked,
                             "dislikes_count": dislikes_count,
                             "likes_count": likes_count})

    return HttpResponseForbidden()


def user_vote(request):
    if request.method == "POST":
        # fetch current user making the request
        current_user_id = request.user.id

        # capture ajax request data
        data = json.loads(request.body)

        # capture disliked term id
        definition_id = data["definition_id"]

        # fetch definition, returns queryset if user has liked the post
        definition_likes = Definition.objects.values(
            "likes").filter(pk=definition_id, likes=current_user_id)

        # if user has liked the definition, set variables accordinly
        if definition_likes:
            liked = True
            disliked = False
        # else, see if user had disliked defintion
        else:
            # fetch definition, returns queryset if user has disliked the post
            definition_dislikes = Definition.objects.values(
                "dislikes").filter(pk=definition_id, dislikes=current_user_id)

            # if user has disliked the definition, set variables accordingly
            if definition_dislikes:
                liked = False
                disliked = True
            # if user hasn't voted, set variables accordingly
            else:
                liked = False
                disliked = False

        # return JSON response
        return JsonResponse({"liked": liked, "disliked": disliked})

    return HttpResponseForbidden()


def edit_definition(request, definition_id):
    # find correct definition entry
    definition_entry = Definition.objects.get(pk=definition_id)

    # extract name of the term
    term_name = definition_entry.term

    # pathway for submissions
    if request.method == "POST":

        # capture definition and example
        definition = request.POST["definition"]
        example = request.POST["example"]

        # update definition_entry
        definition_entry.definition = definition
        definition_entry.example = example
        definition_entry.save()

        # redirect to terms page with success message
        return redirect("term", term_name=term_name)

    # extract definition and example content
    definition = definition_entry.definition
    example = definition_entry.example

    # render page with pre-populated fields
    return render(request, "suburban_dictionary/edit_definition.html",
                  {"term_name": term_name, "definition_id": definition_id,
                   "definition": definition, "example": example})


def delete_definition(request):
    if request.method == "POST":
        # fetch the user making the request
        current_user_id = request.user.id

        # capture ajax request data
        data = json.loads(request.body)

        # capture liked term id
        definition_id = data["definition_id"]

        # find corresponding definition, make sure username matches current user
        definition = Definition.objects.get(
            pk=definition_id, username=current_user_id)

        # delete definition and reload page with alert if found, else inform
        # the user
        if definition:
            # extract term name from definition
            term_name = definition.term

            # construct alert content
            status = "success"
            message = "Definition successfully deleted."

            # delete definition from database
            definition.delete()

            # construct url with argument
            url = reverse("term", args={term_name})

            return JsonResponse({"success": True, "url": url})
        else:
            return JsonResponse({"error": "Definition failed to be deleted."})
