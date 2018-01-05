from webbrowser import *


# created a class called Movie
class Movie():
    # constructor of Movie class
    def __init__(self,
                 movie_title,
                 movie_storyline,
                 poster_image,
                 trailer_youtube):
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube
    #method to open browser and run webapp
    def show_trailer(self):
        open(self.trailer_youtube_url)
