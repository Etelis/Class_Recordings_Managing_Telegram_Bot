# Telegram Class Recordings Managing Bot
A telegram bot, which handels zoom / class recordings for its members.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

 I guess all students can relate that after the passing two years and the extensive usage of the zoom there are alot of recordings of classes wondering around the varios telegram groups.
 pesonally I have had enough with trying to orginize a decent group to hold all those recordings, everything gets to messy around telegram trying to orginize them.
 So I came with the idea to deploy a Bot that will orginize them easily for the user.

### Features:
- **User Authorization**: A very simple mechanism, by editing the premission file you could allow users to access the bot by their ID.
- **Clear Chat On Click:** Every time a user clicks on inline keyboard button to move into the following stage the bot will clean all previous message to achive message flow.
- **Recordings Managment:** The bot will forward recordings from pre-defined groups/channels, so adding new subjects/courses is user-friendly and easy.

### Configuration
To configure this bot first you should first access:
```
authorized_usrs.json
```
File and add users by their IDs, also you could assign a custom wellcoming message.
This dictionary will be loaded everytime the bot runs.

Next you should access:
```
buttons_utils.py
```
And change subjects, course's names and course IDs.

Now about the forwarding mechanism:
First, you should access the main code and change 
```
@YOUR_GROUP_IDENTIFIER
```
to an identifier you want.

Let's assume you have a class names Linear Algebra, after edditing button's file you have given it the ID of 'LA'
Also, let's asume you have picked an identifier of 'BOSTON_UNIVERSITY' in the previous stage.

So now for the lecturer's recordings you will have to open a group with the following name: '@BOSTON_UNIVERSITY_LA_1'
now you should upload all recordings in the right order to that group.
Do the following for each course and you're all done, *Make sure bot has been added to the group!*


### Installing Requirements
Install the required Python Modules in your machine.
```
pip3 install -r requirements.txt
```
### Deployment
With python3.7 or later.
```
python3 -m recordingBOT
```

### Support
- That bot came as an idea to solve the hussle around keeping track of recordings made in the zoom/corona time, feel free to add features and submit any issues :)
- hope that comes in handy :)
