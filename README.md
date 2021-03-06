NetGameAPI
==========
The NetGameAPI is currently not optimized for realtime data transfer

##Install

Add the gameserver folder to your Project

Embed the API with:

 ```python
 from gameserver.netgameapi import *
 ```

</br>
Transmitting Data
------

1. **Create a instance of the netgameapi class**  
 ```api = NetGameApi(name, game, lambda: receiver, [address], [port]) ```  
    *  ```name ```     = your username  
    *  ```game ```     = name of your game
    *  ```receiver ``` = a function with one parameter, the parameter is in the protocol dictionary form  
    *  ```address ```  = the ip address or the domainname of the server \[optional\]  
    *  ```port ```     = port of the server \[optional\]  
  
2. **Connect to server**  
   ```api.makeConnection() ```
    * If the username is already taken you'll get the [error doubleusername](#error.doubleusername)
    
3. **Make a new Thread that listens to the server**  
    ```tcpthread = Thread(name='tcp', target=api.startReceiving()) ```

4. **You'll receive the [playerlist](#listplayers)**   
   It will only contain the players that play your game and are currently not playing  
   
5. **Select a player from the playerlist**  
   Use the username given in the playerlist  
   ```api.connectToPlayer(username_of_opponent) ```

6. **Server Processing**  
    * The server checks if your opponent already is ingame. If he already is, the [error notavailable](#error.notavailable) gets thrown

7. **Your opponent receives your connect as a [gameinvitation](#gameinvitation)**  
    * Your opponent can either [accept](#accept) or [refuse](#refuse) the invitation
    * If he accepts, then you'll receive a [connection_established](#connection_established)
    * If he refuses, then you'll receive the [error connection_refused](#error.connection_refused)

8. **Inform server, that you are now ready to play**  
   Send the server ```connectionEstablished(opponent) ```

9. **Now you can send your Gamedata**  
    ```api.submitGameData(content) ```

</br>
Protocol
------
###Make a connection using  ```makeConnection() ```
```python
{
    "action":"connection",
    "data":{
        "username":"your_username",
        "game":"your_game_name"
    }
}
```

###Connect to player  
Use  ```connectToPlayer(user_you_wish_to_connect) ``` to invite the other player
```python
{
    "action":"connect",
    "data":{
        "master": "your_username",
        "opponent": user_you_wish_to_connect
    }
}
```

###<a name="gameinvitation">Game Invitation</a>  
You'll receive this if the master player sends a  ```connectToPlayer(user_requesting_connection) ``` to the server
```python
{
    "action": "gameinvitation",
    "data": {
        "master": user_requesting_connection
    }
}
```

###<a name="accept">Accept Game Invitation</a>  
You accept the invitation with  ```acceptGameInvitation(user_requesting_connection) ```
```python
{
            "action": "connect_accepted",
            "data": {
                "opponent": user_requesting_connection
     }
}
```

###<a name="refuse">Refuse Game Invitation</a>  
You refuse the invitation with  ```refuseGameInvitation(user_requesting_connection) ```
```python
{
            "action": "connect_refused",
            "data": {
                "opponent": user_requesting_connection
     }
}
```

###<a name="connection_established">Connection to opponent established</a>  
You are the master of the game
```python
{
    "action":"connection_established",
    "data":{
        "username":"opponent_username"
    }
}
```

###<a name="listplayers">Playerlist</a>  
Format of playerlist
```python
{
    "action": "listplayers",
    "data": [
        {"playing": 0,"username": "manuel", "game": "tictactoe"},
        {"playing": 1,"username": "lukas", "game": "tictactoe"}
    ]
}
```

</br>
Errors
------
Errors returned by the server
####<a name="error.doubleusername">doubleusername</a>
```python
{
    "action":"error",
    "data":{
        "errorinfo":"doubleusername",
        "helpmessage":"Please connect with different username."
    }
}
```

####<a name="error.notavailable">notavailable</a>
```python
{
    "action":"error",
    "data":{
        "errorinfo":"notavailable",
        "helpmessage":"User already ingame."
    }
}
```

####<a name="error.connection_refused">connection_refused</a>
```python
{
    "action":"error",
    "data":{
        "errorinfo":"connection_refused",
        "helpmessage":"Your opponent refused."
    }
}
```
