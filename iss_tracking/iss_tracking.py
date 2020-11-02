"""Simple program for tracking current position of ISS
 based on a project from Head First Learn to Code book
 by Eric Freeman"""
import requests, json, turtle

iss = turtle.Turtle()  # one global turtle object
widget = turtle.getcanvas()
previousLongitude = 0;


def setup(screen):
    """Sets screen with earth map as background
        and iss image to show current iss position.
        Maps earth coordinates onto the screen.
        parameter screen is turtle.screen()
    """
    global iss
    screen.setup(1000, 500)  # set screen size
    screen.bgpic("./earth.gif")  # set background
    screen.setworldcoordinates(-180, -90, 180, 90)  # map earth coordinates to screen
    turtle.register_shape("./iss.gif")  # turtle module needs registration of pic to use custom turtle (pointer)
    iss.shape("./iss.gif")  # change turtle picture to iss
    iss.penup()  # lift the pen so you don't draw as you move


def get_position():
    """Sends a get request to open-notify api
        to retrieve current iss location.
        Returns {"latitude": latitude, "longitude": longitude}
        latitude and longitude are 0,0 if not successful"""
    url = "http://api.open-notify.org/iss-now.json"  # api url
    position = {"latitude": 0, "longitude": 0}
    try:
        response = requests.get(url)  # send get request to api
    except:
        print("Could not read data from API")
        return position  # return default 0,0 = middle of the coord. system

    if response.status_code == 200:
        response_dictionary = json.loads(response.text)  # deserialize json into dictionary
        position["latitude"] = float(response_dictionary["iss_position"]["latitude"])
        position["longitude"] = float(response_dictionary["iss_position"]["longitude"])
        print(position)
        return position


def move_iss(position):
    """Moves iss image on the screen based on
        the coordinates received in a position
        dictionary.
        After the first call which sets the initial
        position starts drawing the track of iss"""
    global iss
    global previousLongitude
    if position[
        "longitude"] - previousLongitude < -350:  # when iss reaches dateline (180 deg east) lift the pen since next latitude will be on the other side
        iss.penup()
    iss.goto(position["longitude"], position["latitude"])
    iss.pendown()  # start drawing track after initial setting of the position
    previousLongitude = position["longitude"]


def track_iss():
    """Asks for coordinates every 5 seconds
        and adjusts the position accordingly"""
    global widget
    move_iss(get_position())
    widget.after(5000, track_iss)  # call track_iss every 5 seconds


def main():
    """Runner for the program."""
    screen = turtle.Screen()
    setup(screen)
    track_iss()


if __name__ == "__main__":
    main()
    turtle.mainloop()
