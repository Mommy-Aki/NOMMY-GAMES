###################################
# Imports

import pygame
import tkinter
import datetime
import pathlib
import os
from subprocess import run 
import json
import wx
from colorama import Fore as TextColour
from time import sleep as Wait
import webbrowser
from random import randint
###########################################

PlayersCreated = 1

def DefultText():
    Prefix = ["Evil", "Cheesey", "Buggy", "Salty", "Silly", "Funky", "Funny", "Dummy", "Delicious", "Shitty", "Awakened", "Crazy", "Cheeky", "Heavy", "Sensitive", "Fast", "Sexy", "Broken-down", "Broken", "Forgetful", "Needy", "Unbelievable", "R-Rated", "Sporty", "Minecraft", "Rotten", "Alien", "Hot", "Burning"]
    Noun = ["Furry", "Dog", "Robot", "Door", "Duck", "Animal", "Muscular", "Turkey", "Camera", "Olive", "Chicken", "Cheese", "Gk Barry", "Heavy", "Computer", "Demoman", "Barney", "Squid", "Video", "F1", "Rat", "Catley", "Techno", "Spelling", "Football", "Diamond", "School", "Gladiator", "Alien", "Fury", "Steph", "Hot", "Adventure", "Toilet"]
    Suffix = ["Rabies", "Cheese", "Rapper", "Invasion", "Infection", "Danger", "Podcast", "Shipper", "Science", "Toilet", "Dinosour", "Racing", "Games", "Racing car", "War", "Poison", "Music", "Crossing", "Minecart", "Gladiator", "Dance", "Time", "Moment", "Catley", "Babies", "Spelling"]

    NewText = f"{Prefix[randint(0,len(Prefix) - 1)]} {Noun[randint(0,len(Noun) - 1)]} {Suffix[randint(0,len(Suffix) - 1)]}"
    return NewText

def Error(text):
    if str(text).strip() != "":
        print(f"{TextColour.RED}{text}{TextColour.RESET}")
    exit()

def Info(text):
    print(f"{TextColour.MAGENTA}{text}{TextColour.RESET}")

def Warn(text):
    print(f"{TextColour.YELLOW}{text}{TextColour.RESET}")

class Images():
    BaseImages = { # Name : FilePath

        "Player" : "Assets\Images\Players\Player.png",
        "Enemy" : "Assets\Images\Enemy\Enemy.png",
        "Boss" : "Assets\Images\Enemies\Boss.png",
        "Robot" : "Assets\Images\Friendly\Good_Robot.png",
        "UpArrow": "Assets\Images\Objects\Arrow_Up.png",
    }

class Events():
    def __init__(self):

        self.Events = ["quit"]
        self.CurrentEventID = ""
    
    def SendEvent(self, EventName:str = ""):
        self.CurrentEventID = str(EventName)

class PlayerManager():
    Players = []
    
        
        
    
    def AddPlayer(self, Name:str = f"Player_{PlayersCreated}", Position:list = [0,0], HitboxRadius:int = 5, DisplayImage:str = Images.BaseImages.get("Player", None), Movebinds:dict = {"Up" : pygame.K_w, "Down" : pygame.K_s, "Left" : pygame.K_a, "Right" : pygame.K_d}, MovementSpeed:int = 2):
        try:
            NewPlayer = {
                # Displays
                "Display Name" : Name,
                "Team" : None,
                "Sprite" : DisplayImage,

                #Hitbox
                "HitBoxRange" : HitboxRadius,
                "Position" : Position,

                # Movement
                "WalkSpeed" : MovementSpeed,
                "RunSpeed" : MovementSpeed + 5,

                # Movement Binds
                "Move Up Bind" : Movebinds["Up"],
                "Move Down Bind" : Movebinds["Down"],
                "Move Left Bind" : Movebinds["Left"],
                "Move Right Bind" : Movebinds["Right"],


            }
            
            if len(PlayerManager.Players) > 0:

                for player in PlayerManager.Players:
                    if NewPlayer["Display Name"] == player["Display Name"]:
                        Warn(f"Player '{NewPlayer['Display Name']}' already exists")


            PlayerManager.Players.append(NewPlayer)
        except:
            Warn(f"Could not create client '{Name}'")

    def KickPlayer(self, Player):
        try:
            KickedPlayer = ""
            for each in PlayerManager.Players:
                if each['Display Name'] == Player:
                    KickedPlayer = each
                    break
            Info(f"Kicked '{KickedPlayer['Display Name']}'")
            PlayerManager.Players.remove(KickedPlayer)


        except:
            Warn(f"There are no clients called '{Player}' in the current session")

    def Movement(self):
        for player in self.Players:
            if pygame.key.get_pressed() == player['Move Up Bind']:
                player['Position'][0] -= player["WalkSpeed"]
            
            if pygame.key.get_pressed() == player['Move Down Bind']:
                player['Position'][0] += player["WalkSpeed"]

            if pygame.key.get_pressed() == player['Move Left Bind']:
                player['Position'][1] -= player["WalkSpeed"]
            
            if pygame.key.get_pressed() == player['Move Right Bind']:
                player['Position'][1] += player["WalkSpeed"]
class Instance():
    Clock = pygame.time.Clock()
    def __init__(self, Name:str = DefultText(), IsFullScreen:bool = False, Width:int = 400, Height:int = 400):

        self.External = wx.App(False)
        
        ConfigFile = pathlib.Path("Game\Carbo-Hunts\Assets\cfg\cfg.json")
        try:
            Test = open(ConfigFile)
            Test.close()
        except:
            Error("Error: Configuration file could not be found")

        with open(ConfigFile, "r+") as NewConfig:
            self.Configs = json.load(NewConfig)

            Info("""
Welcome to PAIDE
Doccumentation Can be Found at: <https://Insert-Link-Here.com>""")
        
            if self.Configs["IsNewStartup"] == True:
                Warn("We will need to install the Python interpreter as it is your first time using this program")
                #run("Dependancies\PySource.exe") # change this to open the python download menu instead
                webbrowser.open_new_tab("https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe")
                self.Configs.update({"IsNewStartup" : False})
        
        os.remove(ConfigFile)
            
        with open(ConfigFile, "x") as NewConfig: 
            json.dump(self.Configs, NewConfig, indent = 4)
                
        
        self.Init = pygame.init()
        self.Running = True
        self.ScreenHeight = Height
        self.ScreenWidth = Width
        self.NameLimit = 2

        
        
        self.Events = []
        
        try:
            if Name == None or Name.strip() == "" or len(str(Name)) < self.NameLimit:
                Error(f"Error: Instance must Require a Name with at least {self.NameLimit} characters present")
        except AttributeError:
            Error("Error: Invalid Name entered for Instance")

        if IsFullScreen == True:

            self.ScreenWidth, self.ScreenHeight = wx.GetDisplaySize()
        
        self.Screen = pygame.display.set_mode((self.ScreenWidth,self.ScreenHeight))
        
        pygame.display.set_caption(str(Name))
        

    def EventRunner(self):
        for each in self.Events:
            try:
                eval(f"{each}()")
            except:
                Warn(f"Log: {datetime.datetime.now.strftime("%H:%M:%S")}, could not find '{each}' ")

    def Display(self):
        if type(PlayerManager.Players) != list:
            Error("Error: PlayerList is not a list type")
        for player in PlayerManager.Players:
            PlayerSprite = pygame.image.load(player['Sprite']).convert()
            self.Screen.blit(PlayerSprite, (player['Position'][0] - player['HitBoxRange'], player['Position'][1]- player['HitBoxRange']))
            
        pygame.display.flip()
        Wait(0.2)
            
    
    def Leave(self):
        pygame.quit()
        Error()
        


class Object():
    def __init__(self, CollisionType:str = None, Width:int = 5, Height:int = 5, Texture:str = None):
        pass
