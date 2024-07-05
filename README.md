# Ofir backend task

Pull the git repository from <https://github.com/ofir-as/backend_task> and
place the attached sqlite database inside ./backend_task (next to manage.py).

This is a simple application with a [DRF](https://www.django-rest-framework.org/)
based API that allows users to sign up, log in, log out and get
a password reset e-mail if they forgot their password. The database that you
were sent via e-mail includes a few users.

## Bugs

The user with the e-mail address <mr.inconsistent@example.com> is unable to
log in. Password reset doesn't work for him either. You need to fix this.

 * Identify the issues.
 * Write unit tests to prove the problems.
 * Come up with some solutions.
 * Fix the issues.

## New features

Users have asked for the possibility to keep their data up to date. Some would
also like to be able to delete their account.

 * Add API views and serializers to allow users to retrieve and update their
   data: `email`, `first_name`, `last_name`.
 * Allow users to delete their account. But instead of deleting, anonymise
   their data and mark the user as inactive. Staff users must not be able to
   delete their account.
 * Create a function that will ultimately delete anonymized users after
   14 days.
 * Make sure the new features are covered by unit tests.

## Process

Please keep a record of your thoughts and decisions underway, to be used as the basis for a discussion later.

Push your changes to a public repository somewhere (easiest is probably to just fork it on GitHub) and let us know where to find it.

# Findings


## Identifying the issue, and notes on building local 

Here are my notes on installing and getting the system up and running.

Building and retrieving dependencies 

`$ pip3 install --break-system-packages -r requirements.txt`

Testing 

`$ python3 backend_task/manage.py test`

I enabled the django-admin interface for easier debugging and created a superuser

`$ python3 backend_task/manage.py createsuperuser`

Then started the server local

`$ python3 backend_task/manage.py runserver`

Browsed the admin-interface http://localhost:8000/admin/ and found that there were four user records; me (the superuser), mr. consistent and mr. inconsistent. The user mr.inconsistent@example.com had two records.

* Mr.Inconsistent@example.com
* mr.Inconsistent@example.com

That's the *first issue*, and why mr. inconsistent can't login. Multiple user records.

## Testing

Further investigation revealed that it was possible to create several new users with the same email address using the sign-up form http://127.0.0.1:8000/api/users/sign-up/ and pasting the following json
```json
{
    "email": "mr.inconsistent@example.com",
    "password": "password"
}
```
In order to prevent this from happening again a new test `test_sign_up_existing_user_capitalletters` which tests that an existing user is not able to signup with the same email address with letters in different casing i.e. capitalletters, was added to `test_serializers`. The test failed, thus *proving* there was a problem.

## Solution

The signup serializer had a bug, and the *solution* is quite simple. The user input needs sanitizing. In this case, lowercasing the e-mail and username in both the `create` and `validate` methods fixes the problem with case sensitivity. In case there might be external scripts or integrations creating users, both methods have been changed. The form could be hardened further.

There is still one test case failing that needs fixing...
