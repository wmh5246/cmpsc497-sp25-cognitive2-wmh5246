##------
# Code last modified by Chris Dancy @ Penn State (2023-Sept)
#  from codebase written by Terry Stewart @ University of Waterloo
# Builds environment grid-like environment and creates a vacuum agent to clean up "mud"
##------

from AgentSupport import MotorModule, CleanSensorModule, MyCell
import AgentSupport
import python_actr
from python_actr.lib import grid
from python_actr.actr import *
from python_actr.actr.hdm import *
import random
import time

class VacuumAgent(python_actr.ACTR):
    goal = python_actr.Buffer()
    body = grid.Body()
    motorInst = MotorModule()
    cleanSensor = CleanSensorModule()
    retrieval = Buffer()
    #Finst number and time should be plenty for us to keep things simple (even if theoretically impractical!)
    DM_module = Memory(retrieval, finst_size=22, finst_time=100.0)

    def init():
        goal.set("start_recall_dirt")
        self.home = None

    #----ROOMBA----#

    # Retrieve the position of dirty blocks from declarative memory.
    def recall_dirty_spots_dm(goal="start_recall_dirt", DM_module="busy:False error:False"):
        # Request the position of dirty blocks
        DM_module.request("square:dirty location_x:?x location_y:?y")
        goal.set("check_dm_retrieval")

    # Check whether a dirty block position has been retrieved
    def check_dm_retrieval(goal="check_dm_retrieval", retrieval="square:dirty location_x:?x location_y:?y", DM_module="busy:False error:False"):
        # If a dirty block position is found, move to that location
        goal.set("move_to_dirt")

    # Handle the case when retrieval fails
    def no_memory_retrieval(goal="check_dm_retrieval", DM_module="error:True"):
        # If the dirty block is not found, start a scanning mode
        # Set initial search distance to 3, rotate to 0, and current distance to 3
        goal.set("rsearch left 3 0 3")

    # Move to the retrieved dirty block position
    def move_to_dirt(goal="move_to_dirt", retrieval="square:dirty location_x:?x location_y:?y", motorInst="busy:False"):
        # Use go_towards
        motorInst.go_towards(x, y)
        # Check if the target position is reached
        if body.x == int(x) and body.y == int(y):
            goal.set("clean_dirt")
        else:
            goal.set("move_to_dirt")

    # Clean the dirty block at the target location
    def clean_dirt(goal="clean_dirt", cleanSensor="dirty:True"):
        # Add the location to declarative memory
        DM_module.add(f"square:dirty location_x:{body.x} location_y:{body.y}")

        motorInst.clean()
        # Request the next dirty block location，specifying require_new=True to avoid duplicate visits
        DM_module.request("square:dirty location_x:?x location_y:?y", require_new=True)
        goal.set("check_dm_retrieval")

    # Handle the case when current location is not dirty
    def not_dirty(goal="clean_dirt", cleanSensor="dirty:False"):
        # Request the next dirty block location
        DM_module.request("square:dirty location_x:?x location_y:?y", require_new=True)
        goal.set("check_dm_retrieval")

    #----ROOMBA----#

    # When a dirty block is detected during the cleaning process, store its location in declarative memory
    def clean_cell(cleanSensor="dirty:True", utility=0.6):
        # Add the dirty block location to declarative memory
        DM_module.add(f"square:dirty location_x:{body.x} location_y:{body.y}")
        # Clean the dirty block
        motorInst.clean()

    # Spiral search - Forward movement
    def forward_rsearch(goal="rsearch left ?dist ?num_turns ?curr_dist",
                        motorInst="busy:False", body="ahead_cell.wall:False"):
        motorInst.go_forward()
        # Reduce the remaining distance by 1
        curr_dist = str(int(curr_dist) - 1)
        goal.set("rsearch left ?dist ?num_turns ?curr_dist")

    # Spiral search - Left
    # After turning twice, increase the search distance to expand the search area
    def left_rsearch(goal="rsearch left ?dist ?num_turns 0", motorInst="busy:False",
                    utility=0.1):
        motorInst.turn_left(2)
        # Increase the number of turns
        num_turns = str(int(num_turns) + 1)
        
        # After every two turns (completing a right angle), increase the search distance
        if int(num_turns) % 2 == 0:
            dist = str(int(dist) + 1)
        
        # After turning, reset the current distance
        goal.set("rsearch left ?dist ?num_turns ?dist")

    # Handle the case when encountering a wall, turn to find a new path
    def wall_rsearch(goal="rsearch left ?dist ?num_turns ?curr_dist",
                     motorInst="busy:False", body="ahead_cell.wall:True"):
        motorInst.turn_left(2)
        goal.set("rsearch left ?dist ?num_turns ?curr_dist")


rand_inst = random.Random()
rand_inst.seed(1)

world=grid.World(MyCell,map=AgentSupport.mymap)
agent=VacuumAgent()
agent.home=()
world.add(agent,5,5,dir=0,color="black")

python_actr.log_everything(agent, AgentSupport.my_log)
window = python_actr.display(world)
world.run()
time.sleep(1)
world.reset_map(MyCell,map=AgentSupport.mymap)
world.add(agent,5,5,dir=0,color="black")
world.run() 
