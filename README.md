# A Telegram bot for self learning

## Background
Started learning korean early this year, however its hard to recall and quiz myself on words, especially on-the-go. So an idea kept stuck on my mind to have a place to store my learnings and test myself any time any where. There were alot of learning app around, but they didn't quite suit my needs. Well technically I go for physical korean classes, but their teaching are base on their textbook, so learning app doesn't help if I have to work on weekly spelling tests etc etc... 


Sometime back, someone introduced me to telegram bot which I could consider as a mini quiz place, instead of hosting a webpage. 


## How it works
1. Reads json files in the data folder. each json file will be listed as an option user wants to quiz on.
2. After which, user has the choice of random 10, 20, 50 or all the words in that json to be tested.
3. Then you can start your quiz!


Currently there's no scoring system, as I dont have the need for it. But it's in my TO-DO listing, though not priority yet.


## What you need
1. First you need a data folder to store all the words. (I'm at the level of eng-kr so i think the code will change as time goes by.) They are in json format. Created multiple jsons as I work on them weekly, and only merge them after completing a term.
2. token.txt contains the token string for telegram bot.
3. I hosted this on heroku, it wil only run the script when prompted. Need to input the path to the webhook.


## To-Do
- [ ] Add audio to each word for better pronuciation learning
- [ ] Selecting words base on category
- [ ] Auto-create question to test sentencing (but first need to have words sort nicely at Noun, Adj, Verb etc) --> meant for learning markers etc etc.
- [ ] Scoring system, where weaker words will be shown more.

