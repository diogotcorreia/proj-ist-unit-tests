# The only purpose of this test maker is to have a relative idea of optimizations in efficiency

# The time it will take to run is machine dependant
# The idea is that you can check the difference in execution time before and after changes
# Running extensive test before and after you alter your code is just a brute observation as it will also depend on other processes running on your computer, this is by no means specific.

# The test generated does not take into account some considerations, such as:
#   - there not being two flights with the same date and time in the same origin airport, so comparing outputs is useless (also each test is random) 

# Change the values of nr_flights, nr_airports and last_command at the end to tweak the script to your liking
# Note that these tests should not throw any project or system errors when run

from random import randint as r
from itertools import permutations

def main(nr_airports, nr_flights, last_command):
    # create strings for airports and flights
    letters = ["A", "B", "C", "D", "E", "F", "G"]
    airports = list(permutations(letters, 3))[:nr_airports] 
    flights = list(permutations(letters, 2))[:nr_airports]
    airports = [''.join(el) for el in airports]
    flights = [''.join(el) for el in flights]

    # create nr of airpors specified
    with open("extensive_test.in", "w") as f:
        for airport in airports:
            print(f"a {airport} Country City", file=f)
    
    # create nr of random flights specified, evenly distributed by all airports created as flight's origin
    with open("extensive_test.in", "a") as f:
        x = tuple(zip(airports, airports[1:]))
        for i in range(len(x)):
            n = 1
            while n <= nr_flights / (nr_airports - 1):
                print(f"v {flights[i]}{n} {x[i][0]} {x[i][1]} {r(1, 30):02}-{r(1, 12):02}-2022 {r(0,23):02}:{r(0, 59):02} {r(0, 11):02}:{r(0, 59):02} 50", file=f)
                n += 1
        print(f"{last_command}\nq", file=f)

    return

if __name__ == '__main__':
    # Change this to your liking
    nr_airports = 20
    nr_flights = 15000
    last_command = 'l'
    main(nr_airports, nr_flights, last_command)
