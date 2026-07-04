import time

class SnowflakeIDGenerator:
    """
    Snowflake ID Generator inspired by Twitter's Snowflake algorithm.
    """
    def __init__(self, machine_id: int):
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1

        # bits
        self.machine_id_bits = 10
        self.sequence_bits = 12
        self.max_sequence = (1 << self.sequence_bits) - 1 # bit shift to get max sequence value 

        self.machine_id_shift = self.sequence_bits # 
        self.timestamp_shift = self.sequence_bits + self.machine_id_bits
        self.epoch = 1704067200000
        
    @property
    def current_millis(self):
        return int(time.time() * 1000)
    
    def next_id(self):
        """
        Generate the next unique ID
        """
        timestamp = self.current_millis

        if timestamp == self.last_timestamp:
            # if we are in the same millisecond, increment the sequence
            self.sequence = (self.sequence + 1) & self.max_sequence
            if self.sequence == 0:                 
                while timestamp <= self.last_timestamp:
                    timestamp = self.current_millis # wait for the next millisecond
        else:
            self.sequence = 0 # reset sequence for new millisecod

        self.last_timestamp = timestamp # update last timestamp

        return (
            ((timestamp - self.epoch) << self.timestamp_shift)
            | (self.machine_id << self.machine_id_shift)
            | self.sequence            
        )

        
            
            
        
