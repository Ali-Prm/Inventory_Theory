import numpy as np

class RandomGenerator():
    """
    Exponential random varites generator based on the Inverse Transform method.
    Random numbers are generated using the LINEAR CONGRUENTIAL GENERATORS method.
    """
    def __init__(self,
                initial_sequence, mean, modulus, multiplier):
        self.sequence = initial_sequence
        self.random_number = None
        self.mean = mean
        self.modulus = modulus
        self.multiplier = multiplier
        
    def sequence_next_value(self):
        next_seq = (self.multiplier*self.sequence) % self.modulus
        self.sequence = next_seq
        return next_seq
    
    def compute_random_number(self):
        self.random_number = self.sequence / self.modulus
        
    def compute_exponential_varites(self):
        exponential_varites = -self.mean * np.log(self.random_number)
        return exponential_varites


def rn_generator_helper(random_obj):
    """
    Helper function for generating random number.
    """
    random_obj.compute_random_number()
    output = random_obj.random_number
    random_obj.sequence_next_value()
    return output 

def exp_generator_helper(random_obj):
    """
    Helper function for generating exponential random variets.
    """
    random_obj.compute_random_number()
    output = random_obj.compute_exponential_varites()
    random_obj.sequence_next_value()
    return output 