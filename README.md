NetGameAPI
==========

##Install

<code>from gameserver.netgameapi import *
</code>

##Transmitting Data


###Make a connection using makeConnection()
<pre><code>
{
    "action":"connection",
    "data":{
        "username":"your_username",
        "game":"your_game_name"
    }
}
</code></pre>

###Connect to player
Use <code>connectToPlayer(playername)</code> to invite the other player
<pre><code>
{
    "action":"connect",
    "data":{
        "master": "your_username",
        "opponent": "user_you_wish_to_connect"
    }
}
</code></pre>

###Playerlist
Format of playerlist
<pre><code>
{
    "action": "listplayers",
    "data": [
        {"name": "henzi","game": "3gewinnt", "playing": 0},
        {"name": "lukas","game": "3gewinnt", "playing": 1}
    ]
}
</code></pre>
