import fresh_tomatoes
import media

# instances of different set of movies
# with title, story , poster link and trailer link
avengers = media.Movie("Avengers",
                       "Marvel heroes come together to "
                       "fight off evil Loki and save the earth from"
                       "alies attack",
                       "http://is2.mzstatic.com/image/thumb/Video/v4/87/4d/"
                       "a5/874da577-ec6f-c53d-36bc-cb140a41b807/source/"
                       "1200x630bb.jpg",
                       "https://www.youtube.com/watch?v=eOrNdBpGMv8")

civil_war = media.Movie("Captain America: Civil War",
                        "Friction arises between the superheroes when one "
                        "group supports the government's decision to implement"
                        " a law to control their powers while the"
                        " other opposes it.",
                        "https://img00.deviantart.net/e74b/i/2016/089/e/1/"
                        "captain_america__civil_war___poster_by"
                        "_touchboyj_hero-d9x1y8o.jpg",
                        "https://www.youtube.com/watch?v=dKrVegVI0Us")

due_date = media.Movie("Due Date",
                       "Peter Highman must reach Los Angeles to make it in"
                       " time for his child's birth. However, he is"
                       " forced to ride"
                       " with Ethan, who frequently lands him in trouble.",
                       "https://images-na.ssl-images-amazon.com/images/M/"
                       "MV5BMTU5MTgxODM3Nl5BMl5BanBnXkFtZTcwMjMxNDEwNA@@._V1_"
                       "UY1200_CR90,0,630,1200_AL_.jpg",
                       "https://www.youtube.com/watch?v=uuqb9iq_QKo")

sherlock = media.Movie("Sherlock Holmes",
                       '''Sherlock Holmes is a fictional private detective
                        created by British author Sir Arthur Conan Doyle. Known
                        as a "consulting detective" in the stories,
                        Holmes is known for his proficiency with
                        observation''',
                       "http://www.goldenglobes.com/sites/default/files/films/"
                       "sherlockholmesposter.jpg",
                       "https://www.youtube.com/watch?v=iKUzhzustok")

iron_man2 = media.Movie("Iron Man 2",
                        '''Tony Stark is under pressure from various sources,
                         including the government, to share his technology
                         with the world. He must find a way to fight them
                         while also tackling his other enemies.''',
                        "https://www.wired.com/images_blogs/underwire/2010/03"
                        "/iron_man_int_1200.jpg",
                        "https://www.youtube.com/watch?v=DIfgxIv5xmk")

the_judge = media.Movie("The Judge",
                        "Years after he returns to his home town, Hank decides"
                        " to fight the case for his father, Joseph, an"
                        " adjudicator who is accused of murder.",
                        "https://i.ytimg.com/vi/kjj4HFyJZps/movieposter.jpg",
                        "https://www.youtube.com/watch?v=ZBvK6ni97W8")

# creating a list of instances
movies = [
    sherlock,
    iron_man2,
    the_judge,
    due_date,
    avengers,
    civil_war
]
# passing the list as parameters to fresh_tomatoes.py
fresh_tomatoes.open_movies_page(movies)
