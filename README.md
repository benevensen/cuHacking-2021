# cuHacking-2021
Project repository for our cuHacking 2021 submission

Components:-
	->Basic authentication (entry code)
	->REST API for random question generation
	->Back-end database
	->Front-end representation of questions stored in database
	->Front-end responsiveness


A RSS feed query is fed into the backend which is passed to the Wikipedia API using the python library 'wikipedia'. Three types of questions are possible:

1) Years are removed and replaced with a variety of three fake options with one real option. Years are checked to ensure consistency and be more difficult.
2) Person names identified with NLTK are removed and the three fake options are replaced with names associated with the original person. This is done through wikipedia queries and more NLTK
3) Locations are identified with NLTK and removed and three fake options are added with large US cities.

To emphasize, 1 real option and 3 fake options are generated and passed to the frontend which then quizzes the individual. 


## Running the code
* Run the back end by running the __main__.py
* The front end can be deployed using any cdn as it's a static project
