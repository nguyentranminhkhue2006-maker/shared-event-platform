# shared-event-platform

* Users can create an account and log in to the application.
* Users can create events and act as the host of those events.
* Users can edit and delete their own events.
* Users can view events added to the application including their own and other users' events.
* Users can search for events by name, datetime, or other criteria.
* The application includes user profile pages that show statistics and events created by the user.
* Users can categorize events as work, study, leisure, networking.
* Users can comment on events created by other users.

Sovelluksen asennus
Asenna flask-kirjasto:

$ pip install flask

Luo tietokannan taulut ja lisää alkutiedot:

$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql

Voit käynnistää sovelluksen näin:

$ flask run
