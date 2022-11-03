#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 19:22:50 2022

@author: juliananovaes
"""

import random
import matplotlib.animation
import matplotlib.pyplot
matplotlib.use("TKAgg")
import agentframework
import csv
import requests
import bs4
import tkinter
from data import environment

# Getting the coordinates to initialize the agents
r = requests.get(
    "http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html",
    verify=False,
)
content = r.text
soup = bs4.BeautifulSoup(content, "html.parser")
td_ys = soup.find_all(attrs={"class": "y"})
td_xs = soup.find_all(attrs={"class": "x"})


# Creating the initial figure to plot the agents
fig = matplotlib.pyplot.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1])
fig.patch.set_facecolor("#696969")

# Initializing the agents list
agents = []


# Make the agents

##Make sheep
def make_sheep(num_of_sheep: int):
    """
    This function initializes the sheep and puts them in a predetermined coordinate
    
        Args: Number of sheep to be initialized 
    """

    global agents
    for idx in range(num_of_sheep):
        if idx >= len(td_ys):
            y = random.randint(0, 99)
            x = random.randint(0, 99)
        else:
            y = int(td_ys[idx].text)
            x = int(td_xs[idx].text)
        agents.append(agentframework.Sheep(f"Sheep {idx}", environment, agents, y, x))


##Make wolf
def make_wolf(num_of_wolves: int) -> None:
    """
    This function initializes the wolf
        
        Args: Number of wolves to be initialized
    """

    global agents
    for idx in range(num_of_wolves):
        # if (idx >= len(td_ys)):
        y = random.randint(0, 99)
        x = random.randint(0, 99)
        # else:
        # y = int(td_ys[idx].text)
        # x = int(td_xs[idx].text)
        agents.append(agentframework.Wolf(f"Wolf {idx}", environment, agents, y, x))


# Initialize carry on as True
carry_on = True


# Move the agents.
def run(n_of_sheep: int, n_of_wolves: int):
    
    """
    This function runs the model by creating the agents and plotting the animation.
    """
    global agents 
    if len(agents) == 0:
        make_sheep(n_of_sheep)
        make_wolf(n_of_wolves)

    else:
        print("You have already created agents. Wait for this round to finish")

    # canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=app)
    # canvas.get_tk_widget().grid(column=0,row=1)
    animation = matplotlib.animation.FuncAnimation(
        fig, update, frames=gen_function, repeat=False
    )
    canvas.draw()

def update(frame):
    """"
    Defines the loops for the animation to be displayed
    """

    fig.clear()
    global carry_on

    # random.shuffle(agents)
    for i in range(len(agents)):
        if agents[i].type == "Sheep":
            agents[i].move()
        else:
            agents[i].hunt()
    for i in range(len(agents)):
        if agents[i].type == "Sheep":
            agents[i].eat()
            agents[i].share_with_neighbours()

    # The game ends when all the sheep have died
    if len(agents) == 1:
        carry_on = False

        # Display game-over message
        matplotlib.pyplot.annotate(
            "Game over, the wolf has won",
            (50, 50),
            ha="center",
            va="center",
            weight="bold",
            size=14,
            color="white",
        )

    # Plot the environment
    matplotlib.pyplot.xlim(0, 99)
    matplotlib.pyplot.ylim(0, 99)
    matplotlib.pyplot.imshow(environment)

    # Plot the agents as markers moving in a loop
    for i in range(len(agents)):
        matplotlib.pyplot.scatter(agents[i].x, agents[i].y, color=agents[i].color, s=60)
        matplotlib.pyplot.annotate(
            agents[i].idx, (agents[i].x, agents[i].y + 2), size=10, weight="bold"
        )


def gen_function() -> None:
    """
    Defines the stopping conditions for the animation.
    """
    global carry_on
    while carry_on:
        yield


# Saves the environment file after run
with open("dataout.csv", "w", newline="") as f2:
    writer = csv.writer(f2, delimiter=",")
    for row in environment:
        writer.writerow(row)

# Tkinter GUI

##Defines the theme for the GUI
# customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
# customtkinter.set_default_color_theme(
#     "green"
# )  # Themes: "blue" (standard), "green", "dark-blue"

##Initializes the app
app = tkinter.Tk()

# Defines the proportions of the app
app.geometry("800x800")

# Names the app
app.title("Agent Based Model")

# Creates columns and rows that will define the app's grid
app.columnconfigure(0, weight=1)
app.columnconfigure(1, weight=2)
app.rowconfigure(1, weight=2)
app.rowconfigure(2, weight=0)

# Define canvas where animation will be displayed
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=app)
canvas._tkcanvas.grid(column=0, row=1, sticky="nswe", columnspan=2)
canvas._tkcanvas.configure(background="black")

# Creates frame where menu will be displayed
frame_1 = tkinter.Frame(master=app)
frame_1.grid(row=0, column=0, sticky="nswe", columnspan=3)

# Provides text for the menu
label_1 = tkinter.Label(
    master=frame_1, text="Customize your agent-based model", justify=tkinter.LEFT
)
label_1.pack(pady=12, padx=10)

# Allows users to choose how many sheep they want to add to the model

label_2 = tkinter.Label(
    master=frame_1, text="Select the amount of sheep", justify=tkinter.LEFT
)
label_2.pack(pady=12, padx=10)

sheeps = tkinter.StringVar(frame_1)
sheeps.set("1")

optionmenu_1 = tkinter.OptionMenu(frame_1, sheeps, *["2", "5", "10"])
optionmenu_1.pack(pady=12, padx=10)

# Allows users to choose how many wolves they want to add to the model
label_3 = tkinter.Label(
    master=frame_1, text="Select the amount of wolves", justify=tkinter.LEFT
)
label_3.pack(pady=12, padx=10)


wolves = tkinter.StringVar(frame_1)
wolves.set("1")

optionmenu_2 = tkinter.OptionMenu(frame_1, wolves, *["1"])
optionmenu_2.pack(pady=12, padx=10)


# Start button initializes the model
button_1 = tkinter.Button(
    master=frame_1,
    text="Start",
    command=lambda: run(int(sheeps.get()), int(wolves.get())),
)
button_1.pack(pady=12, padx=10)

# Tkinter's mainloop
app.mainloop()