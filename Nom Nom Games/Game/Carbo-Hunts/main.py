# Imports
from PAIDE import *
from random import randint
##########

GameInstance = Instance("Carbo-Hunts", False, 832, 832)

PlayerService = PlayerManager

PlayerList = PlayerService.Players

class SoundService():
    Sounds = {
        "Meet Heavy" : pygame.mixer.Sound("Game\Carbo-Hunts\Assets\Sounds\Meet Hoovy.wav")

    }

    PlayingSounds = []

    def PlaySound(Sound:str = "Meet Heavy"):
        BadList = []
        for each in SoundService.PlayingSounds:
            each[1] += 0.016
            print(each[0].get_length() - each[1])
            if each[1]  > each[0].get_length():
                BadList.append(each)
        
        for item in BadList:
            SoundService.PlayingSounds.remove(item)
        
        NewSound = SoundService.Sounds.get(Sound, None)

        if NewSound == None:
            return None
        
        for each in SoundService.PlayingSounds:
            if each[0].get_raw() == NewSound.get_raw():

                return None
        

        SoundService.PlayingSounds.append([NewSound, 0])
        NewSound.play()



        





class Creation():
    TileList = {}
    TileNumber = 0
    StartX = -1
    StartY = 0
    AllTilesUsed = False
    def CreateIcon():        
        try:
            NewIconImage = pygame.image.load("Game\Carbo-Hunts\Assets\Images\Icon\Icon.png")
        except:
            try:
                NewIconImage = pygame.image.load("Game\Carbo-Hunts\Assets\Images\Icon\Icon.jpeg")
            except:
                Warn("No icon was found, using default icon for pygame")
                return None
        
        pygame.display.set_icon(NewIconImage)

        

    def CreateTile(TileDesign:int = None, IsLocked:bool = False, NameStart:str = "Tile_"):
        if Creation.AllTilesUsed:
             return None
        
        if TileDesign == None:
             TileDesign = randint(1,6)
        
        Creation.TileNumber += 1
        NewTile = {
             
             "Design" : None,
             "Locked" : IsLocked,
             "Item" : None,
             "Position" : [(Creation.StartX) * 64, (Creation.StartY) * 64],
             "Centre" : [((Creation.StartX) * 64) + 32, ((Creation.StartY) * 64) + 32]
        }

        if TileDesign == 1:
             NewTile.update({"Design" : "Foli_1"})
        else:
             NewTile.update({"Design" : "Blank"})
        
        Creation.StartX += 1

        if NewTile["Position"][0] >= 768:
            Creation.StartX = 0
            Creation.StartY += 1
        if NewTile["Position"][1] >= 800:
             Creation.AllTilesUsed = True
        
        Creation.TileList.update({f"{NameStart}{Creation.TileNumber}" : NewTile})

        
        
        
class Display():
    Designs = {
           
            "Blank" : [],
            "Foli_1" : [],

    }


    Designs["Blank"].append(pygame.image.load("Game\Carbo-Hunts\Assets\Images\Foliage\Blank_Unlocked_Tile.png"))
    Designs["Blank"].append(pygame.image.load("Game\Carbo-Hunts\Assets\Images\Foliage\Blank_Locked_Tile.png"))

    Designs["Foli_1"].append(pygame.image.load("Game\Carbo-Hunts\Assets\Images\Foliage\Foli_1_Unlocked_Tile.png"))
    Designs["Foli_1"].append(pygame.image.load("Game\Carbo-Hunts\Assets\Images\Foliage\Foli_1_Locked_Tile.png"))

    def ObjectDisplay():
        for tile in Creation.TileList:
            if Creation.TileList[tile]["Design"] == "Foli_1":
                if Creation.TileList[tile]["Locked"] == True:
                    GameInstance.Screen.blit(Display.Designs["Foli_1"][1], Creation.TileList[tile]["Position"])
                else:
                    GameInstance.Screen.blit(Display.Designs["Foli_1"][0], Creation.TileList[tile]["Position"])
            else:
                if Creation.TileList[tile]["Locked"] == True:
                    GameInstance.Screen.blit(Display.Designs["Blank"][1], Creation.TileList[tile]["Position"])
                else:
                    GameInstance.Screen.blit(Display.Designs["Blank"][0], Creation.TileList[tile]["Position"])
        
        pygame.display.flip()

    def PlayerDisplay():
        pass

    def IntroDisplay(): # needs editing to resolve no response error
        

        IdleIcon = pygame.image.load("Game\Carbo-Hunts\Assets\Images\Intro\Intro_Idle_v1.png")
        SelectedIcon = [pygame.image.load("Designs\Logo\Game\Intro_Pressed_White_v2.png"),pygame.image.load("Designs\Logo\Game\Intro_Pressed_Black_v2.png"), IdleIcon]
        
        GameInstance.Screen.blit(IdleIcon, (366, 366))
        pygame.display.flip()   
        Flag = True
        while Flag:
            
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        Flag = False
        
        
        for index in range(35):
            
            for image in SelectedIcon:
                GameInstance.Clock.tick(40)
                GameInstance.Screen.blit(image, (366, 366))
                GameInstance.Clock.tick(60)
                pygame.display.flip()
        return

    def MainDisplay():
        pass
Creation.CreateIcon()


while not Creation.AllTilesUsed:
     Creation.CreateTile()

Display.IntroDisplay()

for tile in Creation.TileList:
    print(Creation.TileList[tile])





while GameInstance.Running:
    GameInstance.Clock.tick(60)
    SoundService.PlaySound("Meet Heavy")
    Display.ObjectDisplay()
    