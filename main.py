import Game
import pygame



def main():
    game=Game.Game() #Setting up the screen and the basic enviorment

    run = True #This is for the game loop


    while run:

        game.clock.tick(game.FPS) #Refresh rate
        # print(game.gameMode)
        # Goes through a list of all events happening - Event handler
        for event in pygame.event.get():
            # Checks if the user quit the window
            if event.type == pygame.QUIT:
                run = False
            #Check for pressed keys
            if event.type == pygame.KEYDOWN:
                #Getting out of the menus (end game manu and start manu)
                if event.key == pygame.K_SPACE:
                    if game.win:
                        game.newGame()

                #Pause the game
                # if event.key == pygame.K_ESCAPE:




        if game.gameManager()=="quit":
            run=False

        #Update the screen
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    pygame.display.set_caption('HEX --- Created by Yogev Ben Ivgy')
    # pygame.display.set_icon(pygame.image.load('images/icon.jpeg'))
    main()


