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

