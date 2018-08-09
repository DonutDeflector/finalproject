# Final Project

Web Programming with Python and Javascript

## Premise

`Suburban Dictionary` is a clone of Urban Dictionary. The main goal of the
project is to allow users to create, edit, and vote on definitions.

## Functionality Rundown

### User Login, Registration, and Logout

Users are able to register an account by choosing a username, inputting their
email, and selecting their password. They are able to then login using their
username and password. Once logged in, users can logout by clicking on the
`logout` button in the navbar.

### New Definition

Users are able to add a new definition via a form submission. Users input the
term that they want to define, create definition for it, and use it in a
sentence. Afterwards, they are redirected to the page for the term that they
have defined.

### Displaying Definitions of Terms

Users are able to view the submitted definitions of terms. By default, these
terms are sorted by recency in order to bring fresh content to the user. In
addition to displaying the name, definition, and examples of the term, it also
displays the author, date of submission, and user votes. If the author and the
user are the same, the edit and delete buttons are also displayed.

### Searching for a Term

Users are able to use the search bar at the top of each page to find a term.
If only one result if returned for the search query, the user will be
automatically redirected to the term's page. If multiple results are found,
they are taken to a search results page in which they can find the term they are
looking for.

### Voting on Definitions

Users are able to vote on terms to either show approval or disapproval of a
definition. This allows other users to gage the quality of definitions.

### Editing Definitions

If a user feels like their definition could be better defined, or an example
sentence that they provided was inadequate, they are able to edit their
definition.

### Deleting Definitions

If a user feels like their definition is inadequate or not well received, and
they are unable to edit it to make it better, they are able to delete it.
When the delete button is pressed, a popup message is displayed in order to
confirm that the user actually wants to delete the definition. It gives the user
a chance to cancel the action if they don't actually want to delete the
definition and allows them to delete it if the action was purposeful.

## File Overview

### /finalproject/

#### settings.py

I had to make a few modifications here while deploying to Heroku. I turned the
secret key and database url into environment variables for the sake of security.
I also changed the timezone to `America/New_York` so that timezones would be
displayed properly here. I also set up `whitenoise` to server and cache static
files.

### /suburban_dictionary/

#### admin.py

This is where I registered tables and customized how items were displayed in the
the admin interface.

#### models.py

This is where I declared each of the models for my table. It contains models for
terms and definitions.

#### urls.py

This file contains paths to each of the views for the application.

#### views.py

The back-end workhorse of the project. This file handles user login,
registration, and logout. It also handles the displaying of definitions for
terms and the searching of terms. Additionally, it fields the creation,
deletion, and editing of definitions. Lastly, it handles the displaying and
updating of user votes for each definition.

### /suburban_dictionary/static/suburban_dictionary/js

#### suburban_dictionary.js

The front-end workhorse of the project. It sends ajax requests to fetch the
number of likes and dislikes for definitions. It also sends ajax requests when
the user likes or dislikes a definition and fetches the result from the
back-end. Additionally, it handles the coloring of the like and dislike arrows.
Lastly, it handles the popup message the comes up when a user attempts to
delete a definition.

### /suburban_dictionary/templates/suburban_dictionary/

#### edit_definition.html

This is the form that users are redirected to when they want to edit a
definition.

#### index.html

When users are logged in, this template is used to display the latest 20
definitions submitted.

#### landing_page.html

When users are not logged in, this template offers a bit of information about
the project and has buttons at the top right to allow users to login or
register.

#### login.html

A simple login form in a nice card.

#### new_definition.html

This is the from that users use in order to create a new definition submission.

#### no_term.html

This template is displayed whenever a term is searched up by the user but is not
found.

#### register.html

A simple registration form in a nice card.

#### search_results.html

This template is used to display the results from a search query by the user.

#### term.html

This template is used to display all of the definitions of a term. It is sorted
by recency.

### /suburban_dictionary/templates/suburban_dictionary/layouts

#### default.html

The template from which all of the pages are built off of. It loads all of the
relevant font, CSS, and JS files.

### /suburban_dictionary/templates/suburban_dictionary/includes

#### alert.html

Allows alerts sent from the back-end to be displayed on the front-end.

#### back_home.html

A button placed at the bottom of the login and register cards that allows users
to go back to the landing page.

#### definition_card.html

The template for definitions. It displays the term with a hyperlink to it,
the definition, an example of how it's used in a sentence, the author, the
date of creation, and edit/delete buttons if the user is the same as the author.

#### navbar.html

The main navigation bar of the website. If the user is not logged in, it has
buttons that direct the user to the login and registration pages. If the user is
logged in, it has links to the home page, the new definition form, and logout.

#### popup_message_container.html

This container houses popup messages. The only one utilized is the one that asks
user to confirm the deletion of a term that they have created.

#### terms_searchbar.html

This is a simple search input that allows users to find a term they would like
to know the meaning of.

### /suburban_dictionary/templates/suburban_dictionary/handlebars

#### popup_message.html

A template for popup messages. It is used to display users an alert confirming
the deletion of their definition if they attempt to delete it.
