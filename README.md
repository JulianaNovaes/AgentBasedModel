# Agent-based Model

GitHub repository link: https://github.com/JulianaNovaes/AgentBasedModel

## Overview

This project aims to create an agent-based model to simulate the behaviour of sheep and wolves interacting in an environment

## The agents
In this program, you will find two types of agents: sheep and wolves. 
Certain behaviours are common to both of these agents, but some are specific to their species. 
The agents are defined in the `agentframework.py` file. There, you will find the definition of three classes. 

### Class Agent
This class is built to be a generic Agent's class, where attributes and behaviour that are common to both of the agents are defined.

#### Agent's attributes
Each agent, regardless if wolf or sheep, will receive:

| Attribute   | Description                                                          |
|-------------|----------------------------------------------------------------------|
| x           | X coordinate.                                                        |
| y           | Y coordinate.                                                        |
| environment | Pre-defined environemnt, composed of a simulated terrain with grass. |
| agents      | List of other agents sharing the same environment.                   |
| idx         | Agent's index in the list of agents.                                 |
| store       | Amount of resources stored by agents (food).                         |
| tiredness   | Level of sleepiness of agent.                                        |
| type        | Shows if agent is sheep or wolf.                                     |
| is_alive    | Shows if agent is dead or alive.                                     |
| color       | Color of marker in matplotlib. Wolves are black and sheep white      |

#### Common behaviour
Behaviour that is common to both sheep and wolves and is defined in class `Agent`

| Behaviour        | Description                                                                         |
|------------------|-------------------------------------------------------------------------------------|
| distance_between | Calculates the Euclidian distance between agents.                                   |
| sleep            | Stops agent from perfoming any other behaviour and reduces agent's tiredness level. |

### Class Sheep
This class defines the behaviour specific to sheep. 

| Behaviour             | Description                                           |
|-----------------------|-------------------------------------------------------|
| eat                   | Eats the grass available from the environment.        |
| move                  | Moves 1 step in the x,y coordinate per frame.         |
| share_with_neighbours | Shares the resources in their store with other sheep. |

### Class Wolf
This class defines the behaviour specific to wolves.

| Behaviour             | Description                                           |
|-----------------------|-------------------------------------------------------|
| hunt                  | Searches for nearby sheep and follows them            |
| kill                  | When it reaches a sheep, it will kill it              |

## Running the agent-based model

### As an executable file: This option is only available for Mac users as this App was developed for Mac. 
Run the model file from the dst folder.

### With your local Python setup:

To run the agent-based model in your machine, please, clone this repository and run the `abm.py` file., install the dependencies in the `requirements.txt` with `pip instlal -r requirements.txt` file and run.   
It may take a bit of time for it to appear in your screen.

## Packages and dependencies

The list of libraries and dependencies for the project can be found in the `requirements.txt` file. 
In summary, the main libraries used are `random`, `matplotlib`, `tkinter` and `pytest`.
## Tests
Tests were built using `pytest` and can be found in the `abm_test.py` file. The report containing the results of the tests 
can be found in the `report.html` file.


