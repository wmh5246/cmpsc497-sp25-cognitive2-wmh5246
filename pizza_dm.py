# import python_actr module library for Python ACT-R classes
import python_actr
from python_actr.actr import *
from python_actr.actr.hdm import *

class PizzaBuilder_DM(ACTR):
    goal = Buffer()
    retrieval = Buffer()
    DM_module = HDM(retrieval, finst_size=22, finst_time=100.0)
    my_pizza = []

    def cook_pizza(self, pizza_ingred):
        '''
        Takes in list of "ingredients" and outputs a "pizza"
        Inputs: pizza_ingred [list of strings]
        Output: cooked_pizza [string]
        '''
        return ("_".join(pizza_ingred))

    def init():
        # Add memory chunks to declarative memory module
        # Pepperoni
        DM_module.add("prev:crust next:marinara")
        DM_module.add("prev:marinara next:mozzarella")
        DM_module.add("prev:mozzarella next:pepperoni")
        DM_module.add("prev:pepperoni next:onion")
        DM_module.add("prev:onion next:cook_pizza")
        
        # BBQ Pizza
        DM_module.add("prev:crust next:bbq")
        DM_module.add("prev:bbq next:cheddar")
        DM_module.add("prev:cheddar next:bacon")
        DM_module.add("prev:bacon next:onion")
        DM_module.add("prev:onion next:cook_pizza")

        
        goal.set("start_pizza")

    def prep_ingredients(goal="start_pizza"):
        # Start building pizza
        goal.set("build_pizza first")

    def place_first_ingredient(goal="build_pizza first"):
        my_pizza.append("crust")
        DM_module.request("prev:crust next:?next")
        goal.set("build_pizza")

    def add_ingredient(goal="build_pizza", retrieval="prev:?prev next:?next", DM_module="busy:False"):
        # add next ingredients
        my_pizza.append(next)
        
        # Cook pizza if no ingredient to add
        if next == "cook_pizza":
            goal.set("cook_pizza")
        else:
            DM_module.request("prev:?next next:?next2")

    def cook_pizza_step(goal="cook_pizza"):
        # Cook the pizza
        my_pizza.pop()  # Remove "cook_pizza" tag
        my_pizza = self.cook_pizza(my_pizza)
        print("Mmmmmm my " + my_pizza + " pizza is gooooood!")
        self.stop()

class EmptyEnvironment(python_actr.Model):
    pass

env_name = EmptyEnvironment()
agent_name = PizzaBuilder_DM()
env_name.agent = agent_name
python_actr.log_everything(env_name)
env_name.run()
