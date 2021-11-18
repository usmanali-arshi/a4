import random
import sys
import argparse

class HashTable:
    def __init__(self, num_slots, cap_per_slot, occupancy, total_trials, hash_type):
        self.num_slots = num_slots
        self.cap_per_slot = cap_per_slot
        self.occupancy = occupancy
        self.total_trials = total_trials
        self.hash_type = hash_type

        self.num_elements = int(occupancy * num_slots * cap_per_slot)
        self.trials_with_collisions = 0

    def run_hash_table(self):
        self.trials_with_collisions = 0
        for seed in range(self.total_trials):
            random.seed(seed)
            occupancy_at_slot = [0] * self.num_slots
            for i in range(self.num_elements):
                if self.hash_type == "standard":
                    slot_number = self.standard_hashing(occupancy_at_slot)
                elif self.hash_type == "2choice":
                    slot_number = self.two_choice_hashing(occupancy_at_slot)
                elif self.hash_type == "2left":
                    slot_number = self.two_left_hashing(occupancy_at_slot)
                occupancy_at_slot[slot_number] += 1
            
            if any([counter > self.cap_per_slot for counter in occupancy_at_slot]):
                self.trials_with_collisions += 1

        trials_did_not_exceed = 1.0 - (self.trials_with_collisions/self.total_trials)
        print("Fraction of trials in which slot size did not exceed capacity ", trials_did_not_exceed)
        return trials_did_not_exceed


    def standard_hashing(self, occupancy_at_slot):
        #TODO: Implement standard hashing by picking a slot number randomly between 0 and NUM_SLOTS - 1
        s_slot = random.randint(0, self.num_slots -1)

        # Return the final slot number that you pick.
        return s_slot

    def two_choice_hashing(self, occupancy_at_slot):
        #TODO: Implement 2 choice hashing: pick two slot numbers randomly and then pick the less occupied of the 2
        slot1 = random.randint(0, self.num_slots -1)
        slot2 = random.randint(0, self.num_slots -1)
        # Break ties randomly.
        if (occupancy_at_slot[slot1]  == occupancy_at_slot [slot2]):
            choose = random.randint(0,1)
            if choose == 0:
                return slot1
            else:
                return slot2
        if (occupancy_at_slot[slot1] < occupancy_at_slot[slot2]):
            return slot1
        else:
            return slot2
        
        # Return the final slot number that you pick.
        # return 0

    def two_left_hashing(self, occupancy_at_slot):
        #TODO: Implement 2 left hashing: pick two slots numbers from two sub tables and pick the less occupied of the 2
        half = self.num_slots/2
        slot1 = random.randint(0, half-1)
        slot2 = random.randint(half, self.num_slots-1)
        # Always break ties towards one sub table
        if (occupancy_at_slot[slot1]  == occupancy_at_slot [slot2]):
            return slot1
        if (occupancy_at_slot[slot1] < occupancy_at_slot[slot2]):
            return slot1
        else:
            return slot2
        
        # Return the final slot number that you pick.
        # return 0

def check_hash_type(hash_type):
    if hash_type not in ["standard", "2choice", "2left"]:
        raise argparse.ArgumentTypeError("In valid hash type.  Valid hash types include standard, 2choice, and 2left.")
    return hash_type

def main(args):
    if args.occupancy > 1:
        raise("Occupancy should be less than or equal to 1")

    ht = HashTable(100, 5, args.occupancy, 1000, args.hash_type)
    ht.run_hash_table()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A hash table.')
    parser.add_argument('--occupancy', type=float,
                        help='how occupied is the table')
    parser.add_argument('--hash_type', type=check_hash_type,
                        help='type of table:  standard, 2choice, 2left')

    arguments = parser.parse_args()
    main(arguments)


