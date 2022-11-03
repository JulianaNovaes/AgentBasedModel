#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 00:30:36 2022

@author: juliananovaes
"""

from agentframework import Agent, Sheep, Wolf
from model import environment, agents
import pytest
import random


@pytest.fixture
def sheep():
    """
    Defines the sheep to be used for testing
    """
    return Sheep(idx=1, environment=environment, agents=agents, x=50, y=40)


@pytest.fixture
def other_sheep():
    """
    Defines the second sheep object to be used for testing
    """
    return Sheep(idx=2, environment=environment, agents=agents, x=10, y=15)


@pytest.fixture
def wolf():
    """
    Defines the wolf to be used for testing
    """
    return Wolf(idx=3, environment=environment, agents=agents, x=80, y=90)


def test_get_x(sheep):
    """
    Test the get x function
    """
    # Asserts that function gets the given value for x
    assert sheep._get_x() == 50


def test_get_y(sheep):
    """
    Test the get y function
    """
    # Asserts that function gets the given value for y
    assert sheep._get_y() == 40


def test_set_x(sheep):
    """
    Test the set x function
    """
    # Sets x to 20
    sheep._set_x(20)
    # Asserts x value is now 20
    assert sheep._x == 20


def test_set_y(sheep):
    """
    Test the set y function
    """
    # Sets y to 30
    sheep._set_y(30)
    # Asserts y value is now 30
    assert sheep._y == 30


def test_sleep(sheep):
    """
    Test the sleep method by passing level of tiredness 9 to the object 
    to verify if this number is substracted by 9 as expected in the method.
    """

    # Pass 10 as tiredness level
    sheep.tiredness = 10
    # Call the sleep method
    sheep._sleep()
    # Assert 1 has been subtracted
    assert sheep.tiredness == 9


def test_distance_between(sheep, other_sheep):
    """
    Test the distance between two agents
    """
    # Calculate the distance using the _distance_between method and rounding up the result
    rounded_distance = "{:.2f}".format(sheep._distance_between(other_sheep))
    # Assert that result matched the rounded euclidean distance
    assert float(rounded_distance) == 47.17


def test_move(sheep):
    """
    Test the move function by mocking the behaviour of random.randint()
    """

    # Call the move method
    sheep.move()

    # Assert that the agent has move at least 1 position either backwards or forward in both axis
    assert sheep._x != 50
    assert sheep._y != 40

    # Assert that the agent has not moved more than one position at once either backwards or forward on both axis
    assert sheep._x != 52
    assert sheep._x != 48
    assert sheep._y != 42
    assert sheep._y != 38


def eat(sheep):
    """
    Test the eat method by simulating different values for environment
    """

    # Test method when the amount of resources in the environment is more than 10
    sheep._environment[sheep._y][sheep._x] > 10
    # Assert agent has eaten 10 resources
    assert sheep.store == 10

    # Test method when the amount of resources in the environment is less than 10
    sheep._environment[sheep._y][sheep._x] = 3
    # Assert agent has eaten the available resources
    assert sheep.store == 3


def test_sick_up(sheep):
    """
    Test the sick up method by verifying if the enviromnent gains the resources in the 
    sheep's store and 
    """

    # Set the environment to 100
    sheep._environment[sheep._y][sheep._x] = 100
    # Set the sheep's store to 101
    sheep.store = 101
    # Call the sick up method
    sheep._sick_up()
    # Assert that environment becomes the sum of the two values defined above
    assert sheep._environment[sheep._y][sheep._x] == 201

    return Sheep(idx=1, environment=environment, agents=agents, x=50, y=40)


def test_share_with_neighbours(sheep):
    """
    Test the share with neighbours method by verifying if the store has increased
    """

    # Initializing the store at 30
    sheep.store = 30

    # Define variable previous store
    previous_store = sheep.store

    # Call method and set neighbourhood size to incorporate all agents in the environment
    sheep.share_with_neighbours()

    # Assert sheep store is different from previous store after running moethod
    assert sheep.store != previous_store


def test_kill(wolf, sheep):
    """"
    Test the kill function by verifying if the wolf's store is increased after killing sheep.
    """
    wolf.agents = [sheep]
    previous_store = wolf.store = 30
    sheep.store = 70
    wolf.kill(sheep)

    assert wolf.store == previous_store + sheep.store
