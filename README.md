League of Legends stats: Creating new/unique stats, interesting visualizations of the major league of legends professional leagues.

First major milestone, MVP (minimum viable product): A website that displays adjusted creep score differentials for pro players. Creep score differentials already exist but are limited because they do not factor in champion usage. By adjusting a player's creep score differential for the champions they use, we can more accurately tell who is outperforming expectations in a clear, quantitative manner.

The MVP will consist of a website which makes api calls to the database, which is updated daily with the matches played by the best (challenger) players on each server. This data will be collected from the riot games api.

This is currently a WIP (work in progress). So far, I have most of the data pipeline built, however I will eventually need to adjust it when I figure out where I want it to run (i.e. linux server, all on my local machine, AWS, docker etc.) Next steps are to build a robust api for the front end to interact with, and then design the front end. Once those are complete, I will refactor the code to deploy using cloud computing resources to host my website and ensure scalability.

In the distant future, I will consider new statistics to track, or new visualizations to create and am open to suggestions.


After setting up the initial data collection, it appears that the trends are too random and no meaningful insights can be taken from the data. Happy to have learned a lot about API's and databases, but didnt work out :(
