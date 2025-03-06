# Cognitive Systems Assignment 2: Declarative Memory Models

This assignment implements two models using the Python ACT-R cognitive architecture, demonstrating how declarative memory can enhance rule-based systems. These models—a pizza-making model and a vacuum robot model—both utilize declarative memory for knowledge storage and retrieval, illustrating the transformation from declarative knowledge to procedural skills.

## 1. Pizza Making Model (pizza_dm.py)

This model demonstrates how to use declarative memory instead of procedural memory to make pizza. This approach more closely resembles the human learning process - from reading recipes (declarative) to skilled preparation (procedural).

### Usage
```bash
python pizza_dm.py
```

### Implementation Details
1. **Declarative Memory Structure**:
   - Uses "prev:X next:Y" format to store pizza-making steps
   - Contains two different pizza paths (marinara pizza and BBQ pizza)
   - Implements process control through chained retrieval

2. **Rule System (5 rules)**:
   - `prep_ingredients`: Prepares for pizza making (sets initial state)
   - `place_first_ingredient`: Adds the base crust
   - `add_ingredient`: Adds the next ingredient (based on declarative memory)
   - `cook_pizza_step`: Cooks and outputs the final pizza

3. **Workflow**:
   - Model begins in "start_pizza" state
   - Adds crust as the first layer
   - Retrieves next step from declarative memory
   - May follow either marinara path or BBQ path based on retrieval
   - Cooks pizza after completing all steps

### Memory Content Examples
Marinara Pizza Path:
```
prev:start next:crust
prev:crust next:marinara
prev:marinara next:mozzarella
prev:mozzarella next:pepperoni
prev:pepperoni next:onion
prev:onion next:cook_pizza
```

BBQ Pizza Path:
```
prev:start next:crust
prev:crust next:bbq
prev:bbq next:cheddar
prev:cheddar next:bacon
prev:bacon next:onion
prev:onion next:cook_pizza
```

### Output Examples
```
Mmmmmm my crust_marinara_mozzarella_pepperoni_onion pizza is gooooood!
```
or
```
Mmmmmm my crust_bbq_cheddar_bacon_onion pizza is gooooood!
```

## 2. Vacuum Robot Model (vacuum_agent_dm.py)

This model demonstrates how declarative memory can enhance a vacuum robot's efficiency, allowing it to remember and prioritize cleaning dirty spots it has previously discovered.

### Usage
```bash
python vacuum_agent_dm.py
```

### Implementation Details
1. **Declarative Memory Structure**:
   - Uses "square:dirty location_x:X location_y:Y" format to store dirty spot locations
   - Uses `require_new=True` parameter to avoid revisiting the same locations
   - Sets `finst_size=22` and `finst_time=100.0` to enhance memory performance

2. **Rule System**:
   - Memory retrieval rules:
     - `recall_dirty_spots_dm`: Retrieves dirty spot locations from declarative memory
     - `check_dm_retrieval`: Handles successful retrieval
     - `no_memory_retrieval`: Handles failed retrieval
   
   - Goal-oriented rules:
     - `move_to_dirt`: Moves to remembered dirty spot location
     - `clean_dirt`: Cleans the target location
     - `not_dirty`: Handles cases where current location is not dirty
   
   - Standard cleaning rules:
     - `forward_rsearch`: Forward movement in spiral search
     - `left_rsearch`: Left turns in spiral search
     - `wall_rsearch`: Handles wall encounters
     - `clean_cell`: Handles dirty spots discovered during standard cleaning

3. **Workflow**:
   - At initialization, the robot attempts to retrieve dirty spot locations from declarative memory
   - If found, the robot moves directly to that location and cleans it
   - If not found or all known locations have been cleaned, it begins standard spiral search
   - Locations of dirty spots encountered during cleaning are added to declarative memory
   - Uses `require_new=True` to ensure no location is visited multiple times

4. **Spiral Search Algorithm Optimization**:
   - Increases search distance after every two turns (90-degree cycle)
   - Spiral path gradually expands, covering more area
   - Automatically turns when encountering walls, finding new paths

### Memory Storage Example
```python
DM_module.add(f"square:dirty location_x:{body.x} location_y:{body.y}")
```

### Special Features
1. **Prioritization of Remembered Dirty Spots**:
   - Robot prioritizes cleaning remembered dirty spots, improving cleaning efficiency
   - This simulates the "area memory" function of intelligent vacuum robots

2. **Avoiding Repeated Visits**:
   - Uses ACT-R's finst mechanism (fingers of instantiation)
   - Ensures the robot doesn't repeatedly visit previously retrieved memories

## Design Philosophy

These models demonstrate how declarative memory enhances rule-based systems:

1. **From Declarative to Procedural**:
   - Models show how declarative knowledge (like "recipes" or "maps") guides behavior
   - This reflects the human process of transitioning from explicit to implicit skills

2. **Reducing Rule Count**:
   - Uses declarative memory to store key information instead of hardcoding in rules
   - Results in more general rules and a more flexible system

3. **Enhanced Adaptability**:
   - System can accumulate declarative memories based on experience
   - Behavior can be adjusted based on these memories without modifying rules

4. **Alignment with Cognitive Theory**:
   - Implements the theory of declarative to procedural transformation
   - Demonstrates the important role of memory in cognitive processes

## Dependencies
- Python ACT-R
- python_actr.actr.hdm module (declarative memory)
- AgentSupport module (only needed for vacuum_agent_dm.py)

## Known Issues and Limitations
- Declarative memory retrieval may occasionally fail, especially with multiple matching items
- In some cases, the robot may enter cyclical paths
- With extended runtime, the finst mechanism may cause visited locations to be "forgotten"
- Models strictly follow ACT-R rule writing conventions, avoiding complex Python features

## Running Tips
- Ensure all necessary dependencies are installed
- Running pizza_dm.py multiple times may yield different types of pizzas
- vacuum_agent_dm.py resets the map and runs again after the first run to demonstrate memory effects
- The randomness in the models may lead to different results across runs 