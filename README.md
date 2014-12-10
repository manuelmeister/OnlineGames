NetGameAPI
==========

##Install

Add the gameserver folder to your Project

Embed the API with:

<code>from gameserver.netgameapi import \*
</code>

##Transmitting Data

1. **Create a instance of the netgameapi class** \[optional parameters\]  
   self.reciever is a function with one parameter, the parameter is in the protocol standart dictionary form  
<code>self.api = NetGameApi("name", "game", lambda: self.reciever, \[serveraddress\], \[port\])
</code>  
  
2. **Connect to server**  
<code>self.api.makeConnection()
</code>
    * If the username is already taken you'll get the [error](#errors) 'doubleusername'
    
3. **Make a new Thread that listens to the server**  
<code>self.tcpthread = Thread(name='tcp', target=self.api.startReceiving())
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

###<a name="errors">Error</a>
Errors returned by the server
<pre><code>
{
    "action":"error",
    "data":{
        "errorinfo":"doubleusername",
        "helpmessage":"Please connect with different username."
    }
}
</code></pre>
