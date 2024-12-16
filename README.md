# Project KristyInfinityBot

KristyInfinityBot - is first version of bot. This bot has a lot of differen functions.

Comands in the bot(for command user can write a commend or press a battom with command):
<li>"/start"  - Bot says "Hello" to user and shows a keyboard with all commands</li>
<li>"/help"  - user can check which command is understanding for bot  </li>
<li>"/change_nickname" - command, which save the user nickname in context.user_data["nickname"] and in some command bot use this nickname </li>
<li>"/bot_looks"  - command, when we send a random picture started since <b>"emot"</b> and only <b>.jpg</b> format to user. </li>
<li>"/stop"  - Stop any command/game.</li>
<li>"/end" - we say "Godbay" to user</li>
<li>"/wordcount"  - this command count a word afte pressing this buttom. <b>!</b>It's stop when user use butttom "/stop">
<li>"/planet" - this command shows a planets keybord and when user choose one - show in which constellation the planet today </li>
<li> "/next_full_moon" or "When will be the next full moon?" - command find when will be next full moon from today </li>
<li>"/cities_game_ru" or "/cities_game_UK"  - two command for cities game with Russian or UK cities </li>
<li>"/guess"  - command, which wait a number from user and take a random number +- 10 from user's number< return unswer whose win(whose number more)</li>
<li>"/calc"  - command, which take and parser the user's example on mathematical part and count it with priority of operations </li>


## Instalation

1. Clone the repository from GitHub
2. Create a virtual environment 
3. Install the dependencies "pip install -r requirements.txt"
4. Create file "settings.py"
5. Write in settings.py:
    API_KEY = "API-key for bot"<br> 
    PROXY_URL = "URL for proxy"<br> 
    PROXY_USERNAME = "Login for proxy"<br> 
    PROXY_PASSWORD = "Pasword for proxy"<br> 
    USER_EMOJI = [":winking_face:", ":smiling_face_with_sunglasses:", ":ZZZ:", ":waving_hand:", ":paw_prints:", ":loudly_crying_face:"]<br> 
    CITIES_RUSSIA <br> 
6. Start the bot "Python3 bot.py"