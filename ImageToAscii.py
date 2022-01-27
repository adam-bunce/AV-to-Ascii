def create_density_map(mapString):
    densityString = mapString

    densityMap = dict.fromkeys(densityString, 0)
    n = len(densityString)
    for character in densityString:
        n = n - 1
        densityMap[character] = n

    print(densityMap)
    densityMap = dict((v, k) for k, v in densityMap.items())
    return densityMap


def intensity_to_ascii(intensityValue, densityMap):
    mapSize = len(densityMap)
    distanceBetweenValues = 255 // mapSize




densityMap = create_density_map('#o|-~^\',. ')

import numpy as np
from PIL import Image, ImageOps

# store image into variable
image = Image.open("red-apple-fruit.jpg")

# store the image into a numpy array so each pixel can be accessed
image_data = np.asarray(image)
image = image.convert('L')  # open in greyscale mode

print("image size: ", end="")
print(image.size[0], image.size[1])

# need math here to make array right size for pixel chunk selection

# array_width = int(input("Desired Width: "))
print("desired Width: 70")
array_width = 70
array_height = int(array_width * (image.size[1] / image.size[0]))
array_height = int(array_height * .5)
ascii_array = [[" "] * array_width for i in range(array_height)]

print(ascii_array)
print("array size: ", end="")
print(array_width, array_height)

image = image.resize((array_width, array_height))
image.save("reduced.jpg")
for i in range(0, (image.size[1]) - 1, 1):
    for j in range(0, (image.size[0]) - 1, 1):
        r = image.getpixel((j,i))

        ascii_array[i][j] = densityMap[r%len(densityMap)]


print(image_data.shape)
print(ascii_array)

file = open('ASCII.txt', 'w')

for line in ascii_array:
    for letter in line:
        file.write(letter)
    file.write("\n")

file.close()
