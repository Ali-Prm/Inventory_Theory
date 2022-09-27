import time

def run_simulation(obj):
    """
    Helper function for simulating an inventory system.
    """
    
    start = time.time()

    # Initialize the inventory object 
    obj.initialize()
    
    # Run the simulation until it reaches the termination event.
    while True :
        # determine the next event and update simulation clock.
        obj.timing()
        # update time-continuous statistical counters.
        obj.update_time_avg_stats()
        
        # Call the appropriate event function.
        if obj.next_event_type == 'order_arrival':
            obj.order_arrival()

        elif obj.next_event_type == 'demand':
            obj.demand()

        elif obj.next_event_type == 'evaluation':
            obj.evaluate()
            
        elif obj.next_event_type == 'termination':
            obj.timing()
            obj.update_time_avg_stats()
            obj.week_shortage()
            break
    
    
    end = time.time()   
    running_time = end-start
    
    print(f'Policy (s,S) : ({obj.small_s},{obj.big_s}) | Elapsed Time:{int(obj.num_weeks)} Weeks')
    print('----------------------------')
    obj.report()
    print('----------------------------') 
    print(f'Running Time : {running_time}')