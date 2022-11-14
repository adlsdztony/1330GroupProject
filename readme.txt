Quick start:
    **remember to enlarge the terminal**
    Run 'start_game.py' to start

    Control:
        'P' is the player
        Press  'w / a / s / d + Enter' to move up / left / down / right 
        Press 'E + Enter' to exit

        ('keyboard' package is not supported on Ed so we use input() instead
        It's the reason why you need press 'Enter' after every command)
        **It is recommended to download all files to run locally(windows) for the best experience.**

    Goal:
        Escape from the dungeon (the gap in the wall)
        Do not caught by the monster 'M'
    
    Type of Monsters:
        H: Simlpy move left and right
        V: Simlpy move up and down
        M: Move randomly but will catch player when player approach
        S: Do not move but will catch player when player approach
        (Sometimes they will hide behind one another, be careful!)
    
    10 levels in total.
    Speed up after you pass all 10 levels! 
    Enjoy!!!


Development:
    **DIY your own games!**

    Config:
        1. FPS: Frame Per Second
        2. MONSTER_SPEED: the initial speed of monsters (e.g. set to 2 to double the speed)
        3. MOVE_DICT: change the key
        4. SHOW_TYPE_OF_MONSTER: wheather show the type of monster (default: False)

    Monsters:
        1. Edit monsters in 'monster_functions.py'
        2. input of function should be around and state
            around: list -3*3 matrix around the monster
            state: int -time pass from start (s) * FPS
        3. the output should be the list of position change with length 2
            [x-axis, y-axis]
            x-axis: -1 for left, 1 for right
            y-axis: -1 for up, 1 for down
        4. save the name of monster and function as the key and value of dictionary 'MONSTERS'
            e.g. {'M': CatchOrRandom}

    Maps:
        1. Edit maps in 'maps.py'
        2. Add '#' to add obstacles
        3. Add '{name of the monster}' to add different monsters
            monster should be created in 'monster_functions.py'
        4. Delete the wall to add exit