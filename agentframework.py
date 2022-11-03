# -*- coding: utf-8 -*-

import random
import matplotlib.pyplot


class Agent:
    """
    Represents the Agents interacting in the model
    """

    def __init__(self, idx: str, environment: list, agents: list, y: int, x: int):
        # Agent's index
        self.idx = idx
        # List of agents
        self.agents = agents
        # Y coordinate for agent
        self._y = y
        # X coordinate for agent
        self._x = x
        # Environment in which agent will move
        self._environment = environment
        # Agent's storage
        self.store = 0
        # Agent's level of tiredness
        self.tiredness = 0
        # Agent is alive
        self.is_alive = True

    def __str__(self) -> str:
        """
        Allows agents attributes to be printed in a string
        
            Returns: Aggregation of agent's attributes
        """
        return "Name: " + self.idx + ", " + "Position: " + "(x: " + str(
            self.x
        ) + "," " y: " + str(self.y) + ")" + ", " + "Store: " + str(self.store)

    def _get_x(self) -> int:
        """
        Get coordinate x
        
            Returns: Agent's coordinate
        """
        return self._x

    def _set_x(self, x: int) -> int:
        """
        Set coordinate x
        """
        self._x = x

    def _get_y(self) -> int:
        """
        Get coordinate y
        
            Returns: Agent's coordinates
        """
        return self._y

    def _set_y(self, y: int):
        """
        Set coordinate y
        """
        self._y = y

    x = property(fget=_get_x, fset=_set_x, doc="The x coordinate property")

    y = property(fget=_get_y, fset=_set_x, doc="The y coordinate property")

    def _sleep(self) -> None:
        """
        If sheep has tiredness level above 0, it will not move, eat or share, but recover
        by losing one tiredness point

        """
        self.tiredness -= 1

        # Display action
        matplotlib.pyplot.annotate(f"sleeping", (self._x, self._y - 2.5), size=10)

    def _distance_between(self, other_agent: object) -> float:
        """
        Calculates the distance between two given agents.

        Args:
            other_agent: agent whose distance from the referred object we wish to calculate.

        Returns:
            The distance between the two agens.

        """

        return (
            ((self.x - other_agent.x) ** 2) + ((self.y - other_agent.y) ** 2)
        ) ** 0.5


class Sheep(Agent):
    def __init__(
        self, idx: int, environment: list, agents: list, y: int = None, x: int = None
    ):

        # Sheep takes attributes from general Agent class
        super(Sheep, self).__init__(idx, environment, agents, y, x)
        # Agent's type
        self.type = "Sheep"
        self.color = "white"

    def move(self) -> None:
        """
        Moves the agents considering the limits of the environment.
        """
        # Sheep will only move if it is not tired
        if self.tiredness == 0:

            # Sheep's movements are defined randomly, but always one step at a time
            if random.random() < 0.5:
                self._x = (self._x + 1) % 100

            else:
                self._x = (self._x - 1) % 100

            if random.random() < 0.5:
                self._y = (self._y + 1) % 100
            else:
                self._y = (self._y - 1) % 100

        # Sheep will sleep if it is tired
        else:
            self._sleep()

    def _sick_up(self) -> None:
        """
        If the agent has over 100 resources in store, this function will sick up so that the
        resources are returned to their environment and store is set to zero.
        """

        #
        self._environment[self._y][self._x] += self.store
        self.store = 0
        matplotlib.pyplot.annotate(f"feeling sick", (self._x, self._y - 2.5), size=10)

    def eat(self) -> None:
        """
        Makes the agents eat. If the environment at that specific location has more than 10
        resources to be eaten, agents will eat them and this will increase their store by 10.
        If there are not enough resources, they will eat whatever is left. If they have eaten 100
        or more, this function will call _sick_up().
        """

        # Sheep will only eat if it is not tired
        if self.tiredness == 0:

            # If environment offers more than 10 resources, sheep will eat
            if self._environment[self._y][self._x] > 10:
                # 10 will be taken from environment
                self._environment[self._y][self._x] -= 10
                # 10 mill be added to store
                self.store += 10

            # If environment offers less than 10 resources, sheep will eat whatever is left
            else:
                # Whatever is left will be taken from environment
                self._environment[self._y][self._x] = 0
                # Whatever is left will be added to store
                self.store += self._environment[self._y][self._x]

            # If sheep has more than 100 in store, it will get sick
            if self.store >= 100:
                self._sick_up()

            # If an agent reaches between 90-99 store, it will become sleepy
            elif 90 <= self.store <= 99:
                self.tiredness += 20

            # If there are no resources, the sheep will move to another location
            else:
                self.move()

        # Sheep will sleep if it is tired
        else:
            self._sleep()

    def share_with_neighbours(self) -> None:
        """
        If there are agents close, the agent will share their resources
        """

        # Sheep will only share if it is not tired
        if self.tiredness == 0:

            # Looks for neighboors (sheep) in the area by calculating the distance from them
            for neighbour in range(len(self.agents)):
                if self.agents[neighbour].type == "Sheep":
                    distance = self._distance_between(self.agents[neighbour])

                    # If it finds neighboors not further than 20 steps, it will share resources
                    if distance <= 20:
                        avgstore = (self.store + self.agents[neighbour].store) / 2
                        # Each sheep will get half of the resources
                        self.store = avgstore
                        self.agents[neighbour].store = avgstore

        # Sheep will sleep if it is tired
        else:
            self._sleep()


class Wolf(Agent):
    """
    Represents the wolves
    """

    def __init__(self, idx: int, environment: list, agents: list, y: int, x: int):

        # Wolves takes attributes from general Agent class
        super(Wolf, self).__init__(idx, environment, agents, y, x)
        # Agent's type
        self.type = "Wolf"
        self.color = "black"

    def hunt(self) -> None:
        """
        Wolves will hunt agents based on the smallest distance
        """

        # Wolf will only hunt if it is not tired
        if self.tiredness == 0:

            # Identify sheep nearby
            sheeps = [
                agent
                for agent in self.agents
                if agent.type == "Sheep" and agent.is_alive == True
            ]

            # Find the closest sheep
            smallest_distance = len(self._environment)
            selected_sheep = None
            for sheep in sheeps:
                if self._distance_between(sheep) <= smallest_distance:
                    smallest_distance = self._distance_between(sheep)
                    selected_sheep = sheep

            # Calculate necessary steps in each coordinate
            x_steps = selected_sheep.x - self.x
            y_steps = selected_sheep.y - self.y

            # Display action
            matplotlib.pyplot.annotate(f"hunting", (self._x, self._y - 2.5), size=10)

            # Move towards sheep
            if x_steps in [-2, -1, 1, 2]:
                self._x = (self._x + x_steps) % 100

            if x_steps > 2:
                self._x = (self._x + 2) % 100

            if x_steps < -2:
                self._x = (self._x - 2) % 100

            if y_steps in [-2, -1, 1, 2]:
                self._y = (self._y + y_steps) % 100

            if y_steps > 2:
                self._y = (self._y + 2) % 100

            if y_steps < -2:
                self._y = (self._y - 2) % 100

            if x_steps == 0 and y_steps == 0:
                self.kill(selected_sheep)

        # Wolf will sleep if it is tired
        else:
            self._sleep()

    def kill(self, selected_sheep: object) -> None:

        """
        Wolf kills sheep and takes their storage
        """

        # Wolf takes resources from sheep
        self.store += selected_sheep.store

        # Wolf becomes tired after hunting
        self.tiredness = 40

        # Display action
        matplotlib.pyplot.annotate(
            f"{selected_sheep.idx} died", (70, 70), size=14, weight="bold", color="red"
        )

        # Change sheep status to dead
        selected_sheep.is_alive = False

        # Remove agents from list of agents
        self.agents.remove(selected_sheep)
