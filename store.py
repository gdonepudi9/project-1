

import sys
import os


class IndexEntry:
    """
    Represents a single entry in the index.
    
    Each entry stores a key and its corresponding value.
    """
    
    def __init__(self, key, value):
        """
        Create a new index entry.
        
        Args:
            key: The key string
            value: The value string
        """
        self.key = key
        self.value = value


class KVStore:
    """
    A simple key-value store with persistent storage.
    
    Supports SET, GET, and EXIT commands through a command-line interface.
    Uses a simple array-based index for in-memory storage.
    """
    
    def __init__(self, db_file="data.db"):
        """
        Initialize the key-value store.
        
        Args:
            db_file: Path to the database file for persistent storage
        """
        self.db_file = db_file
        # Simple array-based index - no built-in dict/map allowed!
        self.index = []
        
        # Replay log on startup to recover state
        self.replay_log()
        
    def find_entry(self, key):
        """
        Find an entry in the index by key using linear search.
        
        Args:
            key: The key to search for
            
        Returns:
            IndexEntry if found, None otherwise
        """
        for entry in self.index:
            if entry.key == key:
                return entry
        return None
    
    def upsert_entry(self, key, value):
        """
        Insert or update an entry in the index.
        Implements "last write wins" semantics.
        
        Args:
            key: The key to insert/update
            value: The value to store
        """
        # Try to find existing entry
        entry = self.find_entry(key)
        
        if entry is not None:
            # Update existing entry (last write wins)
            entry.value = value
        else:
            # Insert new entry
            new_entry = IndexEntry(key, value)
            self.index.append(new_entry)
    
    def append_to_log(self, key, value):
        """
        Append a SET operation to the persistent log file.
        Uses append-only writes for durability.
        
        Args:
            key: The key being set
            value: The value being set
        """
        # Format: SET key value\n
        log_entry = f"SET {key} {value}\n"
        
        # Append to file immediately for persistence
        with open(self.db_file, 'a') as f:
            f.write(log_entry)
    
    def replay_log(self):
        """
        Replay the append-only log to rebuild the in-memory index.
        Called on startup to recover state after crashes.
        
        This ensures data consistency after program restarts.
        """
        # Check if log file exists
        if not os.path.exists(self.db_file):
            return
        
        # Read and replay all log entries
        with open(self.db_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Parse the log entry (format: SET key value)
                parts = line.split(maxsplit=2)
                if len(parts) >= 3 and parts[0] == "SET":
                    key = parts[1]
                    value = parts[2]
                    # Rebuild index (last write wins)
                    self.upsert_entry(key, value)
        
    def parse_command(self, line):
        """
        Parse a command line into command and arguments.
        
        Args:
            line: Input string from user
            
        Returns:
            Tuple of (command, args) or (None, None) if invalid
        """
        line = line.strip()
        if not line:
            return None, None
            
        parts = line.split(maxsplit=1)
        command = parts[0].upper()
        args = parts[1] if len(parts) > 1 else ""
        
        return command, args
    
    def handle_set(self, args):
        """
        Handle the SET command.
        
        Args:
            args: String containing "<key> <value>"
            
        Returns:
            Success message or error
        """
        parts = args.split(maxsplit=1)
        
        if len(parts) < 2:
            return "Error: SET requires key and value"
        
        key, value = parts[0], parts[1]
        
        # Persist to disk immediately (append-only log)
        self.append_to_log(key, value)
        
        # Update in-memory index
        self.upsert_entry(key, value)
        
        return "OK"
    
    def handle_get(self, args):
        """
        Handle the GET command.
        
        Args:
            args: String containing the key
            
        Returns:
            The value if found, or error message
        """
        key = args.strip()
        
        if not key:
            return "Error: GET requires a key"
        
        # Search in-memory index
        entry = self.find_entry(key)
        
        if entry is None:
            return "Key not found"
        
        return entry.value
    
    def run(self):
        """
        Main loop for the key-value store.
        Reads commands from STDIN and outputs results to STDOUT.
        """
        while True:
            try:
                # Read command from STDIN
                line = sys.stdin.readline()
                
                # Check for EOF
                if not line:
                    break
                    
                command, args = self.parse_command(line)
                
                if command is None:
                    continue
                elif command == "EXIT":
                    break
                elif command == "SET":
                    result = self.handle_set(args)
                    print(result)
                elif command == "GET":
                    result = self.handle_get(args)
                    print(result)
                else:
                    print(f"Unknown command: {command}")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)


def main():
    """Entry point for the key-value store."""
    store = KVStore()
    store.run()


if __name__ == "__main__":
    main()
