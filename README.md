# Simulated Cloud

Implements homomorphic encryption and data fragmentation.

## Usage

Must start all four servers before starting the user program.

### User Side

Prompts user to input their name, phone number, and credit card information.

`-e`: encrypt data with Goldwasser-Micali cryptosystem before sending to cloud

To execute, run command:
```
python3 user.py [-e]
```

### Server 1

Receives data from user, then separates data into a non-sensitive data fragment and
a sensitive data fragment.

Creates a random 5-digit `customer_id` added to the beginning of the non-sensitive data
fragment and a random 7-digit `card_id` added to the beginning of the sensitive data
fragment.

A third fragment maps the `customer_id` to the `card_id`.

Sends the mappings to Server 2, the sensitive data to Server 3, and the non-sensitive
data to Server 4.

To execute, run command:
```
python3 server1.py
```

### Servers 2-4

Receives data fragment from Server 1 and prints data for demo purposes.

Prompts executor to enter which server number to simulate.

To execute, run command:
```
python3 servers2-4.py
```