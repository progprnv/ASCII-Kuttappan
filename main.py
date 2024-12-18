''' 
import pygame
import pygame.camera
from pygame import Surface

# Window dimensions
windWidth = 1080
windHeight = 720

# pygame setup
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (windWidth, windHeight), "RGB")
cam.start()

screen = pygame.display.set_mode((windWidth, windHeight), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

# ASCII art settings
resFact = 12.0  # Resolution factor (lower = more detail)
resChangeSense = 0.1
contrast = 1  # Default contrast
contrastChangeSense = 0.2

# Density strings for each color channel
dens = 'N@#W$9876543210?!abc;:+=-,._ '
densR = 'WEBOCIwxzuiL(|:. '
densG = 'GHSQUJsgqpj[)/;, '
densB = 'MKFDYVabdko{]!=` '

# State tracking
incrRes = False
decRes = False
incCont = False
decCont = False
img = False
file_image = pygame.image.load('pygame_logo.png')  # Default image
help = False

# Fonts
text = pygame.font.Font("Courier_Prime/CourierPrime-Regular.ttf", round(resFact))
desc = pygame.font.Font("Courier_Prime/CourierPrime-Regular.ttf", 20)

def getChar(pix):
    """
    Converts a pixel's color (RGB) to an ASCII character based on its average brightness.
    """
    avg = (pix[0] + pix[1] + pix[2]) / 3
    dens = 'N@#W$9876543210?!abc;:+=-,._ '
    return dens[round((1 - avg / 255) * (len(dens) - 1))]

def getChar2(pix):
    """
    Converts a pixel's color (RGB) to an ASCII character based on the color channel with the highest brightness.
    Adjusts based on contrast and uses separate density levels for each color channel.
    """
    ch = ""
    spc = ""
    for _ in range(round(contrast)):
        spc += " "
    
    densR = 'WEBOCIwxzuiL(|:. '
    densG = 'GHSQUJsgqpj[)/;, '
    densB = 'MKFDYVabdko{]!=` '
    dens = 'N@#W$9876543210?!abc;:+=-,._ '

    if pix[0] > pix[1] and pix[0] > pix[2]:
        s = densR + spc
        ch = s[round((1 - pix[0] / 255) * (len(s) - 1))]
    elif pix[1] > pix[0] and pix[1] > pix[2]:
        s = densG + spc
        ch = s[round((1 - pix[1] / 255) * (len(s) - 1))]
    elif pix[2] > pix[1] and pix[2] > pix[0]:
        s = densB + spc
        ch = s[round((1 - pix[2] / 255) * (len(s) - 1))]
    else:
        s = dens + spc
        ch = s[round((1 - pix[0] / 255) * (len(s) - 1))]
    
    return ch

while running:
    # Handle window resizing
    if screen.get_width() != windWidth or screen.get_height() != windHeight:
        windWidth = screen.get_width()
        windHeight = screen.get_height()
        cam.stop()
        cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (windWidth, windHeight), "RGB")
        cam.start()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_UP:
                incrRes = True
            if event.key == pygame.K_DOWN:
                decRes = True
            if event.key == pygame.K_LEFT:
                decCont = True
            if event.key == pygame.K_RIGHT:
                incCont = True
            if event.key == pygame.K_ESCAPE:
                img = False
                help = False
            if event.key == pygame.K_h:
                help = not help
            if event.key == pygame.K_SPACE:
                help = not help
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                incrRes = False
            if event.key == pygame.K_DOWN:
                decRes = False
            if event.key == pygame.K_LEFT:
                decCont = False
            if event.key == pygame.K_RIGHT:
                incCont = False
        if event.type == pygame.DROPFILE:
            # Load the dropped file as an image
            filetype = event.file[-3:].lower()
            if filetype in ["png", "bmp", "jpg", "jpeg"]:
                file_image = pygame.image.load(event.file).convert()
                img = True

    # Adjust resolution and contrast
    if incrRes and resFact < 30:
        resFact += resChangeSense
    if decRes and resFact > 5:
        resFact -= resChangeSense
    if incCont and contrast < 5:  # Limit contrast to prevent distortion
        contrast += contrastChangeSense
    if decCont and contrast > 0.5:
        contrast -= contrastChangeSense

    # Fill the screen
    screen.fill("black")

    # Camera feed or image rendering
    if img:
        imgSurf = pygame.transform.scale(file_image, (screen.get_width() // round(resFact), screen.get_height() // round(resFact)))
        imgSurf = pygame.transform.rotate(imgSurf, 90)  # Rotate image to landscape mode
        imgMat = pygame.surfarray.pixels3d(imgSurf)
    else:
        camSurf = pygame.Surface((screen.get_width() // round(resFact), screen.get_height() // round(resFact)))
        camSurf.blit(pygame.transform.scale(cam.get_image(), (screen.get_width() // round(resFact), screen.get_height() // round(resFact))), (0, 0))
        camSurf = pygame.transform.rotate(camSurf, 90)  # Rotate camera feed to landscape mode
        imgMat = pygame.surfarray.pixels3d(camSurf)

    # Render ASCII art
    text = pygame.font.Font("Courier_Prime/CourierPrime-Regular.ttf", round(resFact))
    for i in range(len(imgMat)):
        for j in range(len(imgMat[i])):
            char = getChar2(imgMat[i][j])  # Use getChar2 for color-based density selection
            # Here we're using the color combination from R, G, and B channels
            screen.blit(text.render(char, True, "white"), (j * round(resFact), i * round(resFact)))

    # Help menu
    if help:
        pygame.draw.rect(screen, "white", (screen.get_width() // 2 - 200, screen.get_height() // 2 - 200, 400, 400))
        screen.blit(desc.render("Keyboard Shortcuts", True, "black"), (screen.get_width() // 2 - 180, screen.get_height() // 2 - 150))
        screen.blit(desc.render("Q - Quit", True, "black"), (screen.get_width() // 2 - 180, screen.get_height() // 2 - 100))
        screen.blit(desc.render("Left/Right Arrow - Adjust Contrast", True, "black"), (screen.get_width() // 2 - 180, screen.get_height() // 2 - 50))
        screen.blit(desc.render("Up/Down Arrow - Adjust Resolution", True, "black"), (screen.get_width() // 2 - 180, screen.get_height() // 2))
        screen.blit(desc.render("Drag and Drop - Load Image", True, "black"), (screen.get_width() // 2 - 180, screen.get_height() // 2 + 50))
        screen.blit(desc.render("ESC - Exit Image Mode", True, "black"), (screen.get_width() // 2 - 180, screen.get_height() // 2 + 100))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
'''


import pygame
from pygame import Surface

# Window dimensions
windWidth = 1080
windHeight = 720

# pygame setup
pygame.init()
screen = pygame.display.set_mode((windWidth, windHeight), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

# ASCII art settings
resFact = 12.0  # Resolution factor (lower = more detail)
resChangeSense = 0.1
contrast = 0
contChangeSense = 4

imgMat = [[], []]
img = False
file_image = pygame.image.load("your_image.jpg")  # Replace with your image file
help = False

# Fonts
text = pygame.font.Font("Courier_Prime/CourierPrime-Regular.ttf", round(resFact))
desc = pygame.font.Font("Courier_Prime/CourierPrime-Regular.ttf", 20)

def getChar(pix):
    avg = (pix[0] + pix[1] + pix[2]) / 3
    dens = 'N@#W$9876543210?!abc;:+=-,._ '
    return dens[round((1 - avg / 255) * (len(dens) - 1))]

def getChar2(pix):
    ch = ""
    spc = ""
    for _ in range(round(contrast)):
        spc += " "
    dens = 'N@#W$9876543210?!abc;:+=-,._ '
    densR = 'WEBOCIwxzuiL(|:. '
    densG = 'GHSQUJsgqpj[)/;, '
    densB = 'MKFDYVabdko{]!=` '
    if pix[0] > pix[1] and pix[0] > pix[2]:
        s = densR + spc
        ch = s[round((1 - pix[0] / 255) * (len(s) - 1))]
    elif pix[1] > pix[0] and pix[1] > pix[2]:
        s = densG + spc
        ch = s[round((1 - pix[1] / 255) * (len(s) - 1))]
    elif pix[2] > pix[0] and pix[2] > pix[1]:
        s = densB + spc
        ch = s[round((1 - pix[2] / 255) * (len(s) - 1))]
    else:
        s = dens + spc
        ch = s[round((1 - pix[0] / 255) * (len(s) - 1))]
    return ch

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_UP:
                resFact = min(30, resFact + resChangeSense)
            if event.key == pygame.K_DOWN:
                resFact = max(5, resFact - resChangeSense)
            if event.key == pygame.K_LEFT:
                contrast = max(1, contrast - contChangeSense)
            if event.key == pygame.K_RIGHT:
                contrast = min(50, contrast + contChangeSense)
            if event.key == pygame.K_ESCAPE:
                img = False
                help = False
            if event.key == pygame.K_h:
                help = not help
        if event.type == pygame.DROPFILE:
            # Load a new image when a file is dropped
            filetype = event.file[-3:]
            if filetype in ["png", "bmp", "jpg"]:
                file_image = pygame.image.load(event.file).convert()
                img = True

    # Clear screen
    screen.fill("black")

    # Scale image
    imgSurf = pygame.Surface((screen.get_width() // round(resFact), screen.get_height() // round(resFact)))
    file_image_surf = Surface(file_image.get_size())
    file_image_surf.blit(file_image, (0, 0))
    imgSurf.blit(pygame.transform.scale(file_image_surf, (screen.get_width() // round(resFact), screen.get_height() // round(resFact))), (0, 0))

    surf = pygame.Surface((screen.get_width(), screen.get_height()))
    imgMat = pygame.surfarray.pixels3d(imgSurf)

    # Render ASCII art
    text = pygame.font.Font("Courier_Prime/CourierPrime-Regular.ttf", round(resFact))
    for i in range(len(imgMat)):
        for j in range(len(imgMat[i])):
            surf.blit(text.render(getChar2(imgMat[i][j]), True, "white"), (round(resFact) * i, round(resFact) * j))
    screen.blit(surf, (0, 0))

    # Render help menu
    if help:
        pygame.draw.rect(screen, "white", (screen.get_width() // 2 - 200, screen.get_height() // 2 - 200, 400, 400))
        screen.blit(desc.render("Keyboard Shortcuts", True, "black"), (screen.get_width() // 2 - 100, screen.get_height() // 2 - 150))
        screen.blit(desc.render("Q - Quit", True, "black"), (screen.get_width() // 2 - 180, screen.get_height() // 2 - 100))
        screen.blit(desc.render("Left/Right - Contrast", True, "black"), (screen.get_width() // 2 - 180, screen.get_height() // 2 - 50))
        screen.blit(desc.render("Up/Down - Font Size", True, "black"), (screen.get_width() // 2 - 180, screen.get_height() // 2))
        screen.blit(desc.render("Drag and Drop to Insert Image", True, "black"), (screen.get_width() // 2 - 180, screen.get_height() // 2 + 50))
        screen.blit(desc.render("Esc - Exit Image", True, "black"), (screen.get_width() // 2 - 180, screen.get_height() // 2 + 100))

    # Flip display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
