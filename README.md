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
        {"playing": 0,"username": "manuel", "game": "tictactoe"},
        {"playing": 1,"username": "lukas", "game": "tictactoe"}
    ]
}
</code></pre>
