# Cognitive Systems Assignment 2: Beyond Procedural Memory: Integrating and using declarative memory

**Remember that you should be making changes in your own repo (e.g., `cmpsc497-sp25-assignments-cld5070`) and NOT the main assignment repo. If the sync doesn't work, you may need to copy the new assignment folder from the main assignment repo to your own, reach out.**

For this assignment, we are, once again, going to use the <a href="https://cld5070.github.io/cmpsc497-sp25/help/Introduction to ACT-R/">Python ACT-R</a> Cognitive Architecture to build a few cognitive models

## Make sure you activate your venv & now reinstall python_actr

A reminder that you'll want to activate your virtual environment (the one to which you installed python_actr)

## Your first Python ACT-R agent with declarative memory

Create a new file called `pizza_dm.py` wthing

The first thing you'll need in this file is the important statements to use the Python ACT-R library
```python

# import python_actr module library for Python ACT-R classes
import python_actr
from python_actr.actr import *
from python_actr.actr.hdm import *

```

Now let's have a reminder of how we build our pizza before

```python

class PizzaBuilder(ACTR):
	goal = Buffer()
	my_pizza = []

	def cook_pizza(self, pizza_ingred):
		'''
		Takes in list of "ingrediants" and outputs a "pizza"
		Inputs: pizza_ingred [list of strings]
		Output: cooked_pizza [string]
		'''
		# Whats going on here? - https://docs.python.org/3/library/stdtypes.html#str.join
		return ("_".join(pizza_ingred))

	def init():
		goal.set("build_pizza prep")

	def prep_ingredients(goal="build_pizza prep"):
		#start building our Pizza!
		goal.set("build_pizza thincrust")

	def place_crust(goal="build_pizza ?crust"):
		#Place the crust
		my_pizza.append(crust)
		goal.set("build_pizza prev:crust next:sauce")

	def place_sauce_pepperoni(goal="build_pizza prev:crust next:sauce"): #utility=0.1
		my_pizza.append("sauce")
		goal.set("build_pizza prev:sauce next:mozzarella")

	def place_sauce_bbq(goal="build_pizza prev:crust next:sauce"):
		my_pizza.append("bbq")
		goal.set("build_pizza prev:bbq next:cheddar")

	#... (Other Code)

	def place_cook_pizza(goal="cook_pizza"):
		my_pizza = self.cook_pizza(my_pizza)
		print("Mmmmmm my " + my_pizza + " pizza is gooooood!")
		self.stop()

```

You'll notice that we did this basically through only using _procedural_ memory. Typically (when thinking about about behavior through ACT-R & a [declarative to procedural learning theory](https://www.tandfonline.com/doi/abs/10.1080/1464536X.2011.573008)), you'd think of this type of model as an _expert_ type of model. We want declarative memory and the (theoratical) possibility of learning through proceduralization/procedural composition.

So, let's modify our models so that we now are using more general rules and instead procedural memory to tell us what our next step should be. (See some previous work on using [declarative memory for next goals/steps](https://onlinelibrary.wiley.com/doi/abs/10.1207/s15516709cog2601_2) to get a theoretical way to think about this idea.)

```python

class PizzaBuilder_DM(ACTR):
	goal = Buffer()
	retrieval = Buffer()
	DM_module = HDM(retrieval)
	my_pizza = []

	def cook_pizza(self, pizza_ingred):
		'''
		Takes in list of "ingrediants" and outputs a "pizza"
		Inputs: pizza_ingred [list of strings]
		Output: cooked_pizza [string]
		'''
		# Whats going on here? - https://docs.python.org/3/library/stdtypes.html#str.join
		return ("_".join(pizza_ingred))

	def init():
		#Add memory chunks to declarative memory module
		# (More chunks needed in DM!)
		DM_module.add("prev:pepperoni next:onion")
		#Set goal so that we can prep ingredients

	def prep_ingredients(goal="start_pizza" ):
		#start building our pizza!
		goal.set("build_pizza")
		#Request next step from DM 
		
	###Rules to request from declarative memory for next step/ingredient and place that ingredient on your pizza and make sure you can more on to cooking pizza

	def cook_pizza_step(goal="cook_pizza"):
		my_pizza = self.cook_pizza(my_pizza)
		print("Mmmmmm my " + my_pizza + " pizza is gooooood!")
		self.stop()

class EmptyEnvironment(python_actr.Model):
	pass

env_name = EmptyEnvironment()
agent_name = PizzaBuilder()
env_name.agent = agent_name
python_actr.log_everything(env_name)
env_name.run()
```

You'll notice that the setup is very similar to the previous pizza builder with a few important additions:

1) We now have a _Declarative Memory_ module (`DM_module`) (using Kelly's HDM, but it doesn't affect us too much here) and a `retrieval` buffer. We'll use these to request declarative memories (steps to building the pizza), test whether the module request isn't busy (and _possibly_ hasn't failed), and what is in the retrieval buffer.
 - When you create your DM_module instance, create it with the following \[optional\] parameters set:
  - `finst_size=22` and `finst_time=100.0`
  - You specify parameters in a manner similar to the normal way you specify them for an instance of a python class you might create

2) We now should go from the many rules down to ~3-6 rules. Rules now are used as an action that queries declarative memory for steps. Thus they'll be much more _general_.
 a) One way to think about this is a person might look at and commit the steps of a recipe to (_declarative_) memory. After practice, these declarative memories turn into _procedural memories_ (which are represented as rules in ACT-R)


For this task, we have to make a model that can create two pizzas- a marinara, mozzarella, pepperoni, onion pizza OR a bbq, cheddar, bacon, onion pizza. The trace below shows what your pizza has to return for the two pizza.

**For you to get the full credit for your `pizza_dm.py` model, you must end with cooked pizzas matching the two traces below. Which steps your model falls can be _pseudo-random_ as they were for the procedural memory version of this model from the previous assignment.**

> Here, we are building a bbq, cheddar, bacon, onion pizza
```
   0.710 agent.goal.chunk cook_pizza
   0.710 agent.production cook_pizza_step
   0.760 agent.production None
Mmmmmm my crust_bbq_cheddar_bacon_onion pizza is gooooood!
```
> Here, we are building a marinara, mozzarella, pepperoni, onion pizza
```
   0.711 agent.production cook_pizza_step
   0.761 agent.production None
Mmmmmm my crust_marinara_mozzarella_pepperoni_onion pizza is gooooood!
```

As with the previous assignment, you'll run `python pizza_dm.py` to run your model


If you don't see those ending lines (`cook_pizza_step` and the output pizza), then you likely don't have a correct model.

You can re-run the model until it creates the two different pizzas. You'll notice that there is an initial similar ingredient, and then they branch into different ingredients.

### Keep your work in your folder!
Make sure that your pizza_dm.py file is in your `03-cogsys2` directory

## Using declarative memory with your vacuum Robot

For this part of the assignment, you'll be expanding the vacuum agent that you created for the Cognitive Systems Assignment \#1. Do not worry if you did not get everything working exactly right (that is, the swirl and wall-following pattern).

For this assignment, you'll need to expand your agent in a few ways (note that you should only need to expand upon the agent _class_ setup and agent itself. As with the previous submission, **you** should **not** be mod the code beginning at `world=grid.World(MyCell,map=AgentSupport.mymap)` or any of the AgentSupport file).

There are a few modifications/expansions you'll need to make to get full credit for this part of the assignment:

### 1) Add your own code to the starter file, vacuum_agent_dm.py
- Take the new rules/information you used within your Cognitive System Assignment 1 (`vacuumAgent.py`) file.
- While you technically could take the changes from this file and add them to your existing vacuumAgent.py (and copy that file to your new assignment folder), **it's most likely going to be easiest/less problematic if you import your new rules into this file as opposed to just modifying your original file, there is important setup within the file for assignment requirements.**

### 2) Add locations of dirty squares to declarative memory
- You'll need to modify your agent so that when it encounters a dirty square, it saves the location (x & y) of that square to declarative memory.
- How do we get the x & y in our action? Use `body`
- To simplify things, the chunk you save to declarative memory **must** take the following form:
	- `square:dirty location_x:X-VALUE-HERE location_y:Y-VALUE-HERE` (where you would fill in `[X,Y]-VALUE-HERE`)
- For this to work, you'll need to modify the `clean_cell` rule so that you make any `DM_module` requests before the Motor module cleans the floor (square).
	- This should go above the `motor_inst.clean()` call

<!--
### 3) Add locations of **_some_** clean squares to declarative memory
- You'll need to modify your agent such that some **but not all** clean squares are added to declarative memory.
- To simplify things, the chunk you save to declarative memory **must** take the following form:
	- `square:clean location_x:X-VALUE-HERE location_y:Y-VALUE-HERE` (where you would fill in `[X,Y]-VALUE-HERE`)
	-->

### 3) Make your agent move towards any dirty blocks it has in declarative memory before it goes into the initial swirl-based cleaning pattern
- We've given our agent the ability to remember dirty squares, so we should use that ability!
- Here, you'll want to create a set of rules that queries declarative memory (`DM_module`) for any dirty cells then move directly towards those cells to clean them.
	- To move towards a space on the map, you can use the `go_towards` motor command
		- `motorInst.go_towards(X,Y)`
		- Similar to other motor commands, this only moves you one space (albeit in directly towards you intended (x,y) coordinate)
	- For full credit, you'll have to make sure you do not visit the same spot more than once. But how?
		- You can accomplish this by adding `require_new=True` to your declarative memory request as a parameter after the initial request.
		- For example: `dm.request("CHUNKEDY ?CHUNK",require_new=True)`
		- Here, we're using what is called _fingers of instantiation_ or _finst_ in ACT-R. This is a fancy way for saying our declarative memory system is marking the most recent things we've recalled/retrieved from memory. (With a normal time and number of items limitation).


```python
rom AgentSupport import MotorModule, CleanSensorModule, MyCell
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
```

**Note that for the rules above, you are free to modify, they are included to provide an example possibility.**

### What should be in my solution?
There are artifacts that you'll need to create along the way. You'll want to start with your pizza_builder_dm.py, then move on to your vacuumAgent.py. You'll also need a README_models.md to explain the way your models work and how to run them.


### Deliverables (what do you need to do to get a good grade)
There are several parts to this assignment:
1. The code
	- Submit all the model code you create for this assignment. Comment the code where it makes sense
		- The only code that you are _required_ to submit is your model code, which should in `vacuumAgent_dm.py` and `pizza_dm.py`
2. The `README_models.md`
	- I expect a `README_models.md` (markdown) file that gives the detail of your code (how to use it, issues, etc.)


## Grading
This assignment has some fairly straightforward grading (some partial credit is implicit)
We can think about this assignment as being out of **10** points
- **2 points**: Have your vacuum_agent correctly add dirty spots on the map to declarative memory so that it can retrieve them later
- **2 point**: Have your vacuum_agent move towards (and clean) dirty spots it can remember at the **beginning** of the task
- **1 point**: Adequate documentation (including a minimal README)
- **2 points**:
	- vacuum_agent_dm Code only uses rules and declarative memory to accomplish actions **required for this particular assignment** and does not use any (python) functionality not previously OKed by Professor Dancy.
		- (No If/Else Statements, outside functions, etc unless I've said it's ok!)
- **2 points**
	- Pizza model (DM) is complete and creates pizzas as it should using delcarative memory
- **1 points**
	- Pizza model has no more than 6 rules

## Document your code
### Document your code
#### Document your code
##### Document your code

## References
<div>

Dancy, C. L., Ritter, F. E., Berry, K. A., & Klein, L. C. (2015). Using a cognitive architecture with a physiological substrate to represent effects of a psychological stressor on cognition. _Computational and Mathematical Organization Theory_, 21(1), 90-114.
</div>
