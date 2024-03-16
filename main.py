import Game
import pygame



def main():
    game=Game.Game() #Setting up the screen and the basic enviorment

    run = True #This is for the game loop
    str="start"
    menu = True #Menu on or off


    while run:


        game.clock.tick(game.FPS) #Refresh rate

        if menu:
            game.menu(str)

        # Goes through a list of all events happening - Event handler
        for event in pygame.event.get():
            # Checks if the user quit the window
            if event.type == pygame.QUIT:
                run = False
            #Check for pressed keys
            if event.type == pygame.KEYDOWN:
                #Getting out of the menus (end game manu and start manu)
                if event.key == pygame.K_SPACE:
                    if menu:
                        menu=False
                    if game.win:
                        game.newGame()

                #Pause the game
                if event.key == pygame.K_ESCAPE and not menu:
                    str="continue"
                    menu=True


        #Running the game
        if not menu:
            game.gameManager()

        #Update the screen
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    pygame.display.set_caption('HEX --- Created by Yogev Ben Ivgy')
    # pygame.display.set_icon(pygame.image.load('images/icon.jpeg'))
    main()


