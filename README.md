# Inventory Theory 
An inventory system is implemented with the (S,s) policy.


## How to Run
First, run the following in your terminal to add project root directory to python search path:
```
export PYTHONPATH=${PWD}
```

Then, run the main project script by:
```
python src/run.py
```


## Problem Statement
A Company tries to optimize its operation using optimal `(S,s)` policy. The owner uses periodic order strategy; at the beginning of each week they reviews the inventory level and decides how many items to order from its supplier. <br>
If the company orders Z items, it incurs a cost of `K+iZ`, where `K` is the fix order cost and `i` is the incremental cost per item ordered. <br>
When an order is placed, the time required for it to arrive (called the delivery lag or lead time) is a random variable that is distributed uniformly between 0 and 1 day. <br>
When a demand occurs, it is satisfied immediately if the inventory level is at least as large as the demand. If the demand exceeds the inventory level, the excess of demand over supply is backlogged and satisfied by future deliveries. When an order arrives, it is fi rst used to eliminate as much of the backlog (if any) as possible; the remainder of the order (if any) is added to the inventory. <br>
Most real inventory systems also have two additional types of costs, holding and shortage costs. Let I(t) be the inventory level at time t [note that I(t) could be positive, negative, or zero]; let I+(t)=max{I(t), 0} be the number of items physically on hand in the inventory at time t [note that I+(t)>=0]; and let I-(t)=max{-I(t), 0} be the backlog at time t [I-(t)>=0 as well]. The holding and shortage costs are computed when we have I+(t) and I-(t) respectively.



## Assumptions 
1. Demand interarrival time is U(0,1) IID. (Daily)
2. Order delay time, interval between placing and receiving order, is U(0,1) IID. (Daily)
3. Demand Amount is Expo(5) IID. (Tone)
4. The inventory level is reviewed at the beginning of the week. (Periodic order)
5. Random numbers are generated using the LINEAR CONGRUENTIAL GENERATORS method.
6. Exponential variets are generated using the the Inverse Transform method.


## Description
The model is implemented based on the inventoty theory's assumptions introduced in the following reference.
- The `inventory.py` is the object-oriented implementation of periodic order inventory system with (S,s) policy.
- The `random_generator.py` is the object-oriented implemntation of random number and exponential varites generator. 
- The `run_simulation.py` is the helper function for running the simulation model. 
- The `results.ipynb` contains comparison between two inventory system with different (S,s) policy.

## References:
Law, A.M.: Simulation Modeling and Analysis, 5th edition. McGraw-Hill, Boston.(2015)