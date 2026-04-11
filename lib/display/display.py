import os
from abc import ABC, abstractmethod

import requests
from Pylette import extract_colors, Palette

from lib.api import LastFM


class Display(ABC):
    api: LastFM

    # The number of colors extracted from the album cover.
    colorNumber:int = 12

    def __init__(self, api: LastFM):
        self.api = api

    def getColorPalette(self, imageUrl:str, recur:bool = False) -> Palette:
        img = requests.get(imageUrl).content
        tempFile = open("temp.jpg", "wb")

        tempFile.write(img)
        tempFile.close()

        try:
            palette = extract_colors(image='temp.jpg', palette_size=self.colorNumber)
        except Exception as e:
            if recur:
                # get placeholder image by default, might change that in config file tho
                palette = extract_colors(image='assets/placeholder.jpeg', palette_size=self.colorNumber)
                #raise Exception(f"while getting color palette for image '{imageUrl}' the following error occured: {e}")
            else :
                # retry one time
                palette = self.getColorPalette(imageUrl, recur=True)

        os.remove("temp.jpg")
        return palette

    @abstractmethod
    def display(self): pass


