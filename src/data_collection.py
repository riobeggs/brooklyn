import csv
import os
import os.path

from colorthief import ColorThief
from PIL import Image


class Data:
    """Collects relative data for poster automation."""

    def __init__(self) -> None:
        self._count = 0
        self._images = []
        self._names = []
        self._colour_palette = []
        self._colour_1 = []
        self._colour_2 = []
        self._colour_3 = []
        self._colour_4 = []
        self._colour_5 = []

    def get_images(self) -> None:
        """
        Stores full paths of images in a list of strings.
        """
        path = "./examples"
        for file in os.listdir(path):
            image = os.path.abspath(f"examples/{file}")
            self._images.append(image)
            self._count += 1

    def get_names(self) -> None:
        """
        Stores names of dogs in a list of strings.
        """
        for name in self._images:
            name: str = name.split("/")
            name = name[-1]
            name = name.split(".")
            name = name[0]
            name = name.capitalize()

            self._names.append(name)

    def get_colours(self) -> None:
        """
        Uses colour thief to generate a 5 colour palette from the image.
        Stores the hex values as strings in a list.
        """
        for image in self._images:

            palette = []

            rgb_palette = ColorThief(image).get_palette(5)

            for colour in rgb_palette:

                hex_colour = f"#{colour[0]:02x}{colour[1]:02x}{colour[2]:02x}"

                palette.append(hex_colour)

            self._colour_palette.append(palette)

        self.download_colour_palette_images()

    def download_colour_palette_images(self) -> None:
        """
        Downloads hexcode colours as images as stores their file paths as strings.
        """
        if not os.path.exists("colour_palette_img"):
            os.mkdir("colour_palette_img")

        colour_number = 0

        for palette in self._colour_palette:

            paths = []

            for colour in palette:

                colour_number += 1

                image_path = f"colour_palette_img/colour_{colour_number}.jpg"

                image = Image.new("RGB", (100, 100), colour)
                image.save(image_path)

                paths.append(os.path.abspath(image_path))

            self._colour_1.append(paths[0])
            self._colour_2.append(paths[1])
            self._colour_3.append(paths[2])
            self._colour_4.append(paths[3])
            self._colour_5.append(paths[4])

    def create_csv(self) -> None:
        """
        Creates a csv file containing relative data about the album.
        """
        if not os.path.exists("csv_files"):
            os.mkdir("csv_files")

        columns = [
            "dog_name",
            "dog_image",
            "colour_1",
            "colour_2",
            "colour_3",
            "colour_4",
            "colour_5",
        ]

        with open("csv_files/album_data.csv", "w", encoding="UTF8", newline="") as f:
            writer = csv.writer(f)

            writer.writerow(columns)

            for row in range(self._count):
                writer.writerow(
                    [
                        self._names[row],
                        self._images[row],
                        self._colour_1[row],
                        self._colour_2[row],
                        self._colour_3[row],
                        self._colour_4[row],
                        self._colour_5[row],
                    ]
                )

    def run(self) -> None:
        """
        Runs methods for retrieving relative data.
        """
        self.get_images()
        # print(self._images)
        self.get_names()
        # print(self._names)
        self.get_colours()
        # print(self._colour_1)
        # print(self._colour_2)
        # print(self._colour_3)
        # print(self._colour_4)
        # print(self._colour_5)
        self.create_csv()
        # print(self._count)
