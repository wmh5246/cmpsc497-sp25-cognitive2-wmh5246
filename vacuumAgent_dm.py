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
	DM_module = Memory(retrieval)#,finst_size=5,finst_time=10.0)

	def init():
		goal.set("start_recall_dirt")
		self.home = None

	#----ROOMBA----#

	def recall_dirty_spots_dm(goal="start_recall_dirt", DM_module="busy:False error:False"):
		pass

	#----ROOMBA----#

	def clean_cell(cleanSensor="dirty:True", utility=0.6):
		motorInst.clean()

	def forward_rsearch(goal="rsearch left ?dist ?num_turns ?curr_dist",
						motorInst="busy:False", body="ahead_cell.wall:False"):
		motorInst.go_forward()
		print(body.ahead_cell.wall)
		curr_dist = str(int(curr_dist) - 1)
		goal.set("rsearch left ?dist ?num_turns ?curr_dist")

	def left_rsearch(goal="rsearch left ?dist ?num_turns 0", motorInst="busy:False",
					utility=0.1):
		motorInst.turn_left(2)
		num_turns = str(int(num_turns) + 1)
		goal.set("rsearch left ?dist ?num_turns ?dist")



		###Other stuff!


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
