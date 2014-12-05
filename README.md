NetGameAPI
==========

Install
-------

<code>from gameserver.netgameapi import *
</code>

Transmitting Data
-----------------

Make a connection using makeConnection()
<pre><code>
{
    "action":"connection",
    "data":{
        "username":"your_username",
        "game":"your_game_name"
    }
}
</code></pre>

Send connect to Player request
<pre><code>
{
    "action":"connect",
    "data":{
        "username":"user_you_wish_to_connect"
    }
}
</code></pre>

Playerlist
<pre><code>
{
    "action": "listplayers",
    "data": [
        {"name": "henzi","game": "3gewinnt", "playing": 0},
        {"name": "lukas","game": "3gewinnt", "playing": 1}
    ]
}
</code></pre>
