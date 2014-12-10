NetGameAPI
==========

##Install

Add the gameserver folder to your Project

Embed the API with:

<code>from gameserver.netgameapi import *
</code>

##Transmitting Data

1. Create a instance of the netgameapi class [optional parameters]
<code>self.api = NetGameApi(username, "game title", lambda: self.reciever, [ip.address.of.server], [serverport])
</code>

2. Connect to server
<code>self.api.makeConnection()
</code>


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
