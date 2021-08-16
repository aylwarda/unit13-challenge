# unit13-challenge (a.k.a. Project RoboAdvisor)
This project repo has a strange name, but bear with me.  This is just a name, required for some Fintech homework I did.  What this Project is about, is AWS Lex and Lambda and a Robo Advisor I built as part of the homework.

---
## Intro
This Project consists of a number of different components (see below).  One requires access to AWS Lex to test the RoboAdvisor Lex Bot as it has not been integrated into any accessible URL.

There is however, a media file which shows an interaction.  It is short and while it doesn't show the myriad of different options possible, it gives a sense of what is possible.

---
## RoboAdvisor Bot
### AWS Lex  
The RoboAdvisor Bot is where all the magic happens.  The Bot requires a set of interactions, i.e. prompts to the bot and "canned" responses from the Bot to navigate the user toward their goal of "investing for their retirement".  

The Bot then calls a lambda function which validates 'age', 'amount' to be invested and based on the chosen level of risk the user wants to take, suggests where to invest the amount entered (and at what percentages).

### AWS Lambda  
AWS Lambda is a service that enables the creation of services which can then be interacted with, from anywhere.  In this case, a Lambda Function was created which is no more than a python file which has within it, the set of funtions that allow for the integration into AWS Lex and our specific Bot, and other functions that validate the user input.

### Files
- `RoboAdvisor_Interaction.mp4` (in this repo in [`RoboAdvisor`](./RoboAdvisor) as a Zip file) shows the interaction.
- Within the [`RoboAdvisor/Icons`](./RoboAdvisor/Icons) directory you will find some of the icons I used within the Bot (see Acknowledgements section for URI and license info).
- Within the [`RoboAdvisor/LexExports`](../RoboAdvisor/LexExports) directory you will find `RoboAdvisor_Export.json` which defines the Bot, intent and slots, which can be imported into AWS Lex.
- The `lambda_function.py` python file which AWS Lambda was based on, and found in [`RoboAdvisor`](./RoboAdvisor).

---
## Acknowledgements
### Sources
- The Bot was made possible by using the services of [AWS Lex](https://us-west-2.console.aws.amazon.com/lex/home?region=us-west-2)
- The integration of the Bot with validation functions, was made possible by using the services of [AWS Lambda](https://us-west-2.console.aws.amazon.com/lambda/home?region=us-west-2)
- All icons used within the AWS Lex RoboAdvisor where downloaded from [iconfinder.com](https://www.iconfinder.com/) for free

### Licenses
The Iconfinder icons are licenced under creative commons (attribution 3.0 unported; more on that [here](https://creativecommons.org/licenses/by/3.0/)).