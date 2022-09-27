from random_generator import RandomGenerator
from random_generator import rn_generator_helper
from random_generator import exp_generator_helper

import numpy as np
import matplotlib.pyplot as plt

class InvetorySystem():
    
    def __init__(self,
        termination_time, big_s, small_s, initial_inv_level,
        demand_interarrival_obj, order_delay_obj, demand_amount_obj,
        fix_cost, unit_cost, holding_cost, shortage_cost):
        
        # Attributes
        self.termination_time = termination_time
        self.big_s = big_s
        self.small_s = small_s
        self.initial_inv_level = initial_inv_level
        self.fix_cost = fix_cost
        self.unit_cost = unit_cost
        self.holding_cost = holding_cost
        self.shortage_cost = shortage_cost
        self.num_weeks = self.termination_time/7
        
        # Simulation Clock
        self.sim_time = None
        
        # Next Event 
        self.next_event_type = None
        self.time_next_event = {}
        
        # State Variables 
        self.inv_level = None 
        self.time_last_event = 0.0

        # Statistical Counters. 
        self.total_ordering_cost = 0.0
        self.area_holding = 0.0
        self.area_shortage = 0.0
        
    
        # Historical Invetory level
        self.inv_lvl_hist = []

        # Weeks with Negative Inventory Level
        self.perc_shortage_week = 0
        self.shortage_week = 0

        # Weekly Inventory Level Data 
        self.weeks = {}
        
        # Random generator
        self.demand_interarrival_obj = demand_interarrival_obj
        self.order_delay_obj = order_delay_obj
        self.demand_amount_obj = demand_amount_obj
        
        
    def initialize(self):
        """
        Initialize Routine: Set the initial value for attributes. 
        """
        # Initialize the simulation clock
        self.sim_time = 0.0

        # Initialize the state variables 
        self.inv_level = self.initial_inv_level
        self.time_last_event = 0.0

        # Initialize the statistical counters. 
        self.total_ordering_cost = 0.0
        self.area_holding = 0.0
        self.area_shortage = 0.0

        # Initialize the event list. 
        # There is no order at start of the simulation,so the order arrival event is eliminated from consideration.
        self.time_next_event['order_arrival'] = np.inf
        self.time_next_event['demand'] = self.sim_time + rn_generator_helper(self.demand_interarrival_obj)
        self.time_next_event['termination'] = self.termination_time
        self.time_next_event['evaluation'] = 0.0
    
        
    
    def timing(self):
        """
        Timing Routine: Advnance the simulation clock to the next event and store the inventory data at each event. 
        """
        # Storing the invetory data.
        self.inv_lvl_hist.append((self.sim_time,self.inv_level,self.next_event_type))
        
        # Finding the next event time.
        self.min_time_next_event = min(self.time_next_event.values())
        self.sim_time = self.min_time_next_event
        
        for event in self.time_next_event.keys():
            if self.time_next_event[event] == self.min_time_next_event :
                self.next_event_type = event
            else :
                pass

            
        
    def order_arrival(self):
        """
        Order Arrival Event: Increase the inventory level and eliminate the order arrival event from next event list. 
        """
        # Increase the inventory level by the amount ordered.
        self.inv_level += self.ordered_amount

        # Eliminate order arrival event from event list.
        self.time_next_event['order_arrival'] = np.inf
        
      
    
    def demand(self):
        """
        Demand Event: Decrease the inventory level and schedule the time of next demand event.
        """
        # Decrease the inventory level by amount of generated demand.
        self.inv_level -= exp_generator_helper(self.demand_amount_obj)

        # Schedule the time of the next demand.
        self.time_next_event['demand'] = self.sim_time + rn_generator_helper(self.demand_interarrival_obj)
     
    

    def evaluate(self):
        """
        Evaluation Event: Check the inventory level and determine the amount of order.
        """
        # Check the invetory level based on (s,S) policy.
        if self.inv_level < self.small_s:
            # Order the required amount and add its ordering cost to the total ordering cost.
            self.ordered_amount = self.big_s - self.inv_level 
            self.total_ordering_cost += self.fix_cost + self.unit_cost*self.ordered_amount
            # Schedule the arrival of the order.
            self.time_next_event['order_arrival'] = self.sim_time + rn_generator_helper(self.order_delay_obj)
        else :
            pass

        # Schedule the next evaluation event. (Evaluation is done weekly.)
        self.time_next_event['evaluation'] = self.sim_time + 7.0
        # If the evalution event is coincide with termination event, then eliminate evalution event.
        if self.time_next_event['evaluation'] == self.time_next_event['termination']:
            self.time_next_event['evaluation'] = np.inf
        
        
    
    def report(self):
        """
        Report Routine
        """
        # Compute the statistical counters at the end of the simulation.
        # Costs 
        self.holding = (self.holding_cost/364) * self.area_holding
        self.shortage = (self.shortage_cost/364) * self.area_shortage
        self.total_cost = self.total_ordering_cost+self.holding+self.shortage
        
        print(f'Perctange of Weeks with Negative Inventory Level : {self.perc_shortage_week}')
        print('----------------------------')
        print('Costs:')
        print(f'Ordering Cost: ${self.total_ordering_cost}',
          f'Holding Cost: ${self.holding}',
          f'Shortage Cost: ${self.shortage}',
          f'Total Cost: ${self.total_cost}',
          sep='\n')
        
        
        
    def update_time_avg_stats(self):
        """
        Update the area under holding and shortage diagram.
        """
        # Compute time since last event and update last event time to the simulation time after updating stats.
        self.time_since_last_event = self.sim_time - self.time_last_event
        self.time_last_event = self.sim_time

        # According to the inventory levels during the current interval, update the stats.

        # Case 1 : In case of Shortage.
        # Increase the area under shortage-time diagram, aka I- (I minus).
        if self.inv_level < 0 :
            self.area_shortage += (-self.inv_level) * self.time_since_last_event

        # Case 2 : The inventory level in the given interval was positive.
        # Increase the area under holding-time diagram, aka I+ (I plus).
        elif self.inv_level > 0 :
            self.area_holding += self.inv_level * self.time_since_last_event

        # Case 3 : The inventory level in the givent interval was 0 
        # Do nothing
        elif self.inv_level == 0 :
            pass


        
    def week_shortage(self):
        """
        Storing inventory level in each week and determining weeks with shortage.
        """
        # Number of weeks
        self.num_weeks = self.termination_time/7

        # Creating Dictionary Containing Historical Invetory levels
        self.weeks = {}
        
        # Spliting historical invetory levels to chunks for each week.
        for i in np.arange(self.num_weeks):
            week_num = i+1
            self.weeks[week_num] = []
            for k in self.inv_lvl_hist :
                if k[0]>=i*7 and k[0]<7*(i+1):
                    self.weeks[week_num].append(k)
        
        # Looping through weeks to check if the inventory level had become negative or not.
        self.shortage_week = 0            
        for w in self.weeks.keys():
            for element in self.weeks[w]: 
                if element[1] < 0:
                    self.shortage_week +=1
                    break
                else :
                    pass

        # Percentage of weeks which invetory level became negative.
        self.perc_shortage_week = self.shortage_week / self.num_weeks
        
        
        
    def plot_result(self):
        """
        Visualizing the inventory level over the simulation.
        """
        
        event_times = []
        inventory_levels = []

        for key in self.weeks.keys():
            for i in self.weeks[key]:
                event_times.append(i[0])
                inventory_levels.append(i[1])

        plt.rcParams['figure.figsize']=(20,6)
        plt.axhline(y=0 , color='c', linewidth=2)
        plt.plot(event_times, inventory_levels, color='r', marker='.', linestyle='--', markersize=7.5)
        plt.ylabel('$Invetory$ $Level$', size=14, fontweight='bold')
        plt.xlabel('$Time(days)$',size=15, fontweight='bold')
        plt.title(f'Policy(s,S):({self.small_s},{self.big_s}) | Elapsed Time:{int(self.num_weeks)} Weeks',size=14, fontweight='bold')
        plt.show()