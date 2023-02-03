#
# Name: Justin Hardy
# NETID: JEH180008
# Class: Human Language Technologies (CS 4395)
# Section: 001
# Professor: Dr. Mazidi
#


import sys
import re as regex


# Create static data
pattern_id = regex.compile("^[A-Za-z]{2}[0-9]{4}$")
pattern_phone = regex.compile("^([0-9]{3}[^0-9]?){2}[0-9]{4}$")


# Create object to store input data.
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    def display(self):
        print("Employee ID: " + self.id)
        print("\t" + self.first + " " + (self.mi + " " if self.mi != "X" else "") + self.last)
        print("\t" + self.phone + "\n")


# Create functions to process data
def get_clarification(split_type, original_input):
    # Create string to refer to particular data we need clarification on...
    data_name = "ID" if split_type == "id" else "Phone Number" if split_type == "phone" else "ERROR"
    data_format = "AB1234" if split_type == "id" else "123-456-7890" if split_type == "phone" else "ERROR"

    # Print prompt to user...
    print(data_name + " " + original_input + " is invalid.")
    print(data_name + " must be entered in the format of " + data_format + "\n")

    # Get input from user.
    user_input = ""
    while not (pattern_id.match(user_input) if split_type == "id" else pattern_phone.match(user_input) if split_type == "phone" else True):
        if user_input != "":
            print(data_name + " " + user_input + " is invalid.")
            print(data_name + " must be entered in the format of " + data_format + "\n")
        user_input = input("Please enter a valid " + data_name.lower() + ":\n>")
        print()  # (print newline for format sake)
    return user_input


def process_input(file_input):
    # Create Person dictionary
    people = dict()

    # Remove first line, so long as it exists...
    file_input.readline()

    # Process another line if there is another line to read...
    while file_input.readable():
        # Read line...
        line = file_input.readline()

        # Break if there is no more data to process
        if line == "":
            break

        # Split by comma delimiter...
        splits = line.split(",")

        # Normalize data...
        last = splits[0].capitalize()
        first = splits[1].capitalize()
        mi = splits[2][0].upper() if len(splits[2]) != 0 else "X"
        id = splits[3].upper() if pattern_id.match(splits[3]) else get_clarification("id", splits[3])

        p = splits[4].replace("\n", "")
        phone = p if pattern_phone.match(p) else get_clarification("phone", p)

        # clean up phone format (if necessary)
        if len(phone) == 10:
            phone = phone[:3] + "-" + phone[3:6] + "-" + phone[6:]  # add dashes if no delimiters were inputted
        phone = regex.sub("[^0-9]", "-", phone)  # replace delimiter(s) with dashes

        # Create person object...
        person = Person(last, first, mi, id, phone)

        # Put person object in people dictionary, and print if duplicate id is detected.
        if id not in people.keys():
            people[id] = person
        else:
            print("\nERROR. Duplicate ID " + id + " detected.\n")

    # Return people dictionary
    return people


def main():
    # Create input file stream...
    print("Opening file stream...")

    # Check if user inputted an argument...
    if len(sys.argv) < 2:
        # Error in user input, terminate the program. (exit code 1)
        print("Unable to open file stream. User must input relative path of data.csv as program argument.")
        print("Terminating program...")
        exit(1)

    # Set up file stream.
    file_input = open(sys.argv[1], mode="r")
    print("Successfully opened file stream.\n")

    # Process through input file.
    print("Processing input data...")
    people = process_input(file_input)
    print("Finished processing all input data.\n")

    # Print each person in the people dictionary.
    print("Employees:\n")
    for person in people:
        people[person].display()

    # Write to pickle file
    ### CODE

    # Program complete, terminate the program. (exit code 0)
    exit(0)


if __name__ == "__main__":
    main()
