NetGameAPI
==========

##Install

Add the gameserver folder to your Project

Embed the API with:

<code>from gameserver.netgameapi import \*
</code>

##Transmitting Data

1. **Create a instance of the netgameapi class**
<code>api = NetGameApi(name, game, lambda: receiver, \[address\], \[port\])
</code> 
_parameters_  
    * <code>name</code>     = your username  
    * <code>game</code>     = name of your game
    * <code>receiver</code> = a function with one parameter, the parameter is in the protocol standart dictionary form  
    * <code>address</code>  = the ip address or the domainname of the server \[optional\]  
    * <code>port</code>     = port of the server \[optional\]  
  
2. **Connect to server**  
<code>api.makeConnection()
</code>
    * If the username is already taken you'll get the [error](#errors) 'doubleusername'
    
3. **Make a new Thread that listens to the server**  
<code>tcpthread = Thread(name='tcp', target=api.startReceiving())
</code>

4. **You'll receive the [playerlist](#listplayers)**   
   It will only contain the players that play your game and are currently not playing  
   
5. **Select a player from the playerlist**  
   Use the username given in the playerlist  
<code>api.connectToPlayer(username_of_opponent)
</code>




###Make a connection using makeConnection()
<pre><code>{
    "action":"connection",
    "data":{
        "username":"your_username",
        "game":"your_game_name"
    }
}
</code></pre>


###Connect to player
Use <code>connectToPlayer(playername)</code> to invite the other player
<pre><code>{
    "action":"connect",
    "data":{
        "master": "your_username",
        "opponent": "user_you_wish_to_connect"
    }
}
</code></pre>


###<a name="listplayers">Playerlist</a>
Format of playerlist
<pre><code>{
    "action": "listplayers",
    "data": [
        {"playing": 0,"username": "manuel", "game": "tictactoe"},
        {"playing": 1,"username": "lukas", "game": "tictactoe"}
    ]
}
</code></pre>
  
###<a name="errors">Error</a>
Errors returned by the server
####doubleusername
<pre><code>{
    "action":"error",
    "data":{
        "errorinfo":"doubleusername",
        "helpmessage":"Please connect with different username."
    }
}
</code></pre>
