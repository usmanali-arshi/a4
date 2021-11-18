import random
import sys
import argparse

class Packet:
    def __init__(self, input_port, output_port, arrival_tick):
        self.input_port  = input_port
        self.output_port = output_port
        self.arrival_tick= arrival_tick

class PimSimulator:
    def __init__(self, num_ports, arrival_prob, seed, pim_iters=1, simulation_ticks=20000):
        random.seed(seed)
        self.num_ports = num_ports
        self.arrival_prob = arrival_prob
        self.simulation_ticks = simulation_ticks
        self.pim_iters = pim_iters

        # variables to compute average delay of packets transmitted out of output ports
        self.delay_count = 0
        self.delay_sum   = 0.0

        # Virtual output queues at each input                                           
        # Initialized to empty queue for each combination of input port and output port 
        # These queues sit on the input side.                                           
        self.voqs = []                                                                       
        for input_port in range(self.num_ports):                                             
            self.voqs += [[]]                                                                  
            for output_port in range(self.num_ports):                                          
                self.voqs[input_port] += [[]] 

    def run_simulator(self):
        # Main simulator loop: Loop over ticks
        for tick in range(self.simulation_ticks):
            # Tick every input port
            for input_port in range(self.num_ports):
                # Is there a packet here?
                if (random.random() < self.arrival_prob):
                  # If so, pick output port uniformly at random
                  output_port = random.randint(0, self.num_ports - 1)
                  self.voqs[input_port][output_port] += [Packet(input_port, output_port, tick)]

            self.pim(tick)

            # Average delay printing
            if (tick % 100 == 0):
                print ("Average delay after ", tick, " ticks = ", self.delay_sum / self.delay_count, " ticks")
                print()

    def pim(self, tick):
        # TODO: Implement PIM algorithm with a single iteration.
        # You can use the random.choice() function to pick one item at random from a list of items.

        # TODO: Generalize this to multiple iterations by simply running the same code in a loop a fixed number of times
        # Each iteration must only consider inputs+outputs that are still unmatched after the previous iterations.

        # For both variants of PIM, if input I is matched to output O, complete the matching by dequeueing from self.voqs[I][O].

        # Make sure to update the average delay every time a packet is dequeued from a VOQ as a result of the matching process.
        # Otherwise, your average delay will be 0/0 because no samples would have been accumulated.

if __name__ == "__main__":
    # Usage for command line arguments
    parser = argparse.ArgumentParser(
        description="Assignment 4."
    )
    parser.add_argument(
        "-p",
        "--num_ports",
        type=int,
        help="The number of ports on the router"
    )
    parser.add_argument(
        "-a",
        "--arrival_prob",
        type=float,
        help="The probability that a packet arrives"
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        help="The seed for the random number generator"
    )
    parser.add_argument(
        "-i",
        "--pim_iters",
        type=int,
        help="The number of iterations to run the PIM algorithm"
    )
    args = parser.parse_args()
    simulator = PimSimulator(args.num_ports, args.arrival_prob, args.seed, args.pim_iters)
    simulator.run_simulator()
