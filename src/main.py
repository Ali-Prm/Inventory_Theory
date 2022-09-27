from inventory import InvetorySystem
from random_generator import RandomGenerator
from random_generator import rn_generator_helper
from random_generator import exp_generator_helper
from run_simulation import run_simulation


import numpy as np
import matplotlib.pyplot as plt 
import time 


# Intial value for LINEAR CONGRUENTIAL GENERATORS random-number generator.
initial_sequence_interarrival_demand = 1985072130  #(seed)
initial_sequence_order_delay = 748932582   #(seed)
initial_sequence_demand_amount = 1631331038 #(seed)
multiplier = 16807
modulus = 2147483648

# mean demand amount 
mean_demand = 5 #(tone)



# Creating demand interarrival, order delay, and demand amount objects
demand_interarrival_obj = RandomGenerator(
                    initial_sequence=initial_sequence_interarrival_demand,
                    mean=0, modulus=modulus, multiplier=multiplier)
order_delay_obj = RandomGenerator(
                    initial_sequence=initial_sequence_order_delay,
                    mean=0, modulus=modulus, multiplier=multiplier)
demand_amount_obj = RandomGenerator(
                    initial_sequence=initial_sequence_demand_amount,
                    mean=mean_demand, modulus=modulus, multiplier=multiplier)

# parameters for invetory system
simulation_time = 365*2
big_s = 175
small_s = 25

# Ordering fix cost, dollar per order
fix_cost = 15  

# Ordering unit cost, dollar per tone
unit_cost = 2

# Yearly Holding cost (dollar per tone)
holding_cost = 5.2

# Yearly Shortage cost (dollar per tone)
shortage_cost = 520

# Creating inventory system object
inv_obj = InvetorySystem(termination_time=simulation_time,
                         big_s=big_s, small_s=small_s,
                         initial_inv_level=40,
                         demand_interarrival_obj=demand_interarrival_obj,
                         order_delay_obj=order_delay_obj,
                         demand_amount_obj=demand_amount_obj,
                         fix_cost=fix_cost, unit_cost=unit_cost, holding_cost=holding_cost, shortage_cost=shortage_cost)

run_simulation(inv_obj)

inv_obj.plot_result()