# import pillow to handle media and os to handle files
import os
from PIL import Image


def create_folder():
    """
    creates a folder for converted images and ascii art text file to be saved to
    :return: nothing
    """
    folderExists = os.path.exists("outputFolder")
    if not folderExists:
        os.mkdir("outputFolder")


def create_density_map(densityString):
    """
    creates a map of the density map to be used when generating ascii art
    :param mapString: a string representing the pallet
    :return: nothing
    """

    densityMap = dict.fromkeys(densityString, 0)
    n = len(densityString)
    for character in densityString:
        n = n - 1
        densityMap[character] = n

    densityMap = dict((v, k) for k, v in densityMap.items())
    return densityMap


def intensity_to_ascii(intensityValue, densityMap):
    """
    given a greyscale intensity value returns the corresponding ascii value from densityMap
    :param intensityValue: 0-255 the value representing how dark (0) or light (255) a pixel is
    :param densityMap: the values the intensity corresponds to in the ascii art
    :return: characterSelected, string, ascii value from densityMap
    """
    distanceBetweenValues = 255 / len(densityMap)
    characterSelectedFlag = False
    currentIter = 0
    distanceBetweenValuesCopy = 0

    while not characterSelectedFlag:

        if distanceBetweenValuesCopy <= intensityValue <= (distanceBetweenValuesCopy + distanceBetweenValues):
            characterSelected = densityMap[currentIter]
            characterSelectedFlag = True
        else:
            distanceBetweenValuesCopy += distanceBetweenValues
        currentIter = currentIter + 1

    return characterSelected


def save_array_to_textfile(array):
    file = open('outputFolder/ASCII.txt', 'w')
    for line in array:
        for letter in line:
            file.write(letter)
        file.write("\n")
    file.close()


def generate_ascii(fileName, asciiWidth):
    """
    generates the ascii version of an image
    :param fileName: string the name of the file to convert (.gif in this case)
    :param asciiWidth: integer the width of the outputted converted art
    :return: ascii_array, array, array representation of the ascii art
    """

    # densityMap = create_density_map('#o|-~^,. ')  # use for black background
    densityMap = create_density_map(' .,^~=|o#')  # use for white background

    image = Image.open(fileName)
    image = image.convert('L')  # open in greyscale mode

    array_width = asciiWidth
    array_height = int(array_width * (image.size[1] / image.size[0]))
    ratio_adjuster = 0.42  # change depending on art use, 0.42 good w/ courier font
    array_height = int(array_height * ratio_adjuster)
    ascii_array = [[" "] * array_width for i in range(array_height)]

    image = image.resize((array_width, array_height))

    if "outputFolder/" in fileName:
        string = fileName + "reduced.png"
    else:
        string = "outputFolder/" + fileName + "reduced.png"

    for i in range(0, (image.size[1]) - 1, 1):
        for j in range(0, (image.size[0]) - 1, 1):
            r = image.getpixel((j, i))
            ascii_array[i][j] = intensity_to_ascii(r, densityMap)

    return ascii_array


def gif_to_ascii(fileName, asciiWidth, num_key_frames):
    """
    generates a javascript array of ascii art that when rapidly changed gives the illusion of a gif

    :param fileName: name of the .gif file to convert
    :param asciiWidth: the width of the outputted "video"
    :param num_key_frames: number of frames to grab from  the gif (more frames = more smooth)
    :return: nothing
    """
    # create keyframes to generate animation with
    with Image.open(fileName) as im:
        for i in range(num_key_frames):
            im.seek(im.n_frames // num_key_frames * i)
            im.save('outputFolder/{}.png'.format(i))

    for x in range(num_key_frames):
        # keyframes were named 0 -> num_key_frames
        ascii_array = generate_ascii("outputFolder/" + str(x) + ".png", asciiWidth)

        filename = "outputFolder/ASCII_Animation.txt"
        file = open(filename, 'a')  # append mode cause you need to add each frame each loop

        if x == 0:
            file.write("text = [")
        file.write("\"")
        for line in ascii_array:

            for letter in line:
                file.write(letter)
            file.write("<br>")

        if x == num_key_frames - 1:  # if last iteration
            file.write("\"];")
        else:
            file.write("\",")

        file.close()

    # remove all the images created
    for imageNumber in range(num_key_frames):
        os.remove("outputFolder/" + str(imageNumber) + ".png")


# main ------------------------------------------------------------------
# TO CHANGE PALLET/INVERT PALLET change createDensityMap string in generate_ascii method
# you might need to adjust the aspect ratio of the ascii art, change ratio_adjuster in generate_ascii method

array = generate_ascii("IMAGE_NAME.jpg", 150)
save_array_to_textfile(array)  # save ascii art to a file to copy/paste
gif_to_ascii("GIF_NAME.gif", 50, 7)  # create array for javascript animation
