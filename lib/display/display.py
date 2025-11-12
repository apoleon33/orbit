import os
from abc import ABC, abstractmethod

import requests
from Pylette import extract_colors, Palette

from lib.api import LastFM


class Display(ABC):
    api: LastFM

    # The number of colors extracted from the album cover.
    colorNumber:int = 6

    def __init__(self, api: LastFM):
        self.api = api

    def getColorPalette(self, imageUrl:str) -> Palette:
        img = requests.get(imageUrl).content
        tempFile = open("temp.jpg", "wb")

        tempFile.write(img)
        tempFile.close()

        palette = extract_colors(image='temp.jpg', palette_size=self.colorNumber)

        os.remove("temp.jpg")
        return palette

    @abstractmethod
    def display(self): pass


