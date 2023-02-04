"""

Name: Justin Hardy
NETID: JEH180008
Class: Human Language Technologies (CS 4395.001)
Professor: Dr. Mazidi

"""


import sys as system
import os.path as path
import re as regex
import pickle


# Create static data
pattern_id = regex.compile("^[A-Za-z]{2}[0-9]{4}$")
pattern_phone = regex.compile("^([0-9]{3}[^0-9]?){2}[0-9]{4}$")


# Create object to store input data.
class Person:
    def __init__(self, last, first, mi, id, phone):
        """
        :param last: person's last name
        :param first: person's first name
        :param mi: person's middle initial, single letter character or "X" if N/A
        :param id: person's id in format of AB1234
        :param phone: person's phone number in format of 123-456-7890
        """
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
    """
    Informs user of incorrectly formatted string (original_input), and requests for them to input a new string that
    matches the specified format (split_type), and returns the user's input when it matches the specified format.

    :param split_type: string of specific data name we are working with (id or phone)
    :param original_input: the original input string that does not match expected pattern
    :return user_input: corrected input string that matches expected pattern
    """
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
    """
    Processes the given input file, as per the format specified by the assignment. Returns a dictionary of all
    processed input stored in a dictionary.

    :param file_input: input stream of file to be read from
    :return people: dictionary of persons that were read & processed from the input file
    """
    # Create Person dictionary
    people = dict()

    # Remove first line, so long as it exists...
    if file_input.readable():
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
    """
    This program is designed to process text of a data file that is formatted to store employee IDs, names, and phone
    numbers using regex, and store them into a dictionary. It will then serialize the dictionary and then perform a
    read of that serialization in order to confirm that the serialization of the dictionary was successful.

    :return: exit code (0 = success, 1 = missing argument(s), 2 = invalid input file name)
    """
    # Create input file stream...
    print("Opening file stream...")

    # Check if user inputted an argument...
    if len(system.argv) < 2:
        # Error in user input, terminate the program. (exit code 1)
        print("Unable to open file stream. User must input relative path of data.csv as program argument.")
        print("Terminating program...")
        exit(1)
    argument = system.argv[1]
    print("Inputted argument: \"" + argument + "\"")

    # Check if user argument leads to existing file
    if not path.exists(argument):
        # Error in user input, terminate the program. (exit code 2)
        print("Unable to open file stream. Inputted file path leads to file that doesn't exist.")
        print("Terminating program...")
        exit(2)

    # Set up file stream.
    file_input = open(argument, mode="r")
    print("Successfully opened file stream.\n")

    # Process through input file.
    print("Processing input data...")
    people = process_input(file_input)
    print("Finished processing all input data.\n")
    file_input.close()

    # Write to pickle file.
    print("Writing people to pickle file...")
    pickle.dump(people, open("people.p", "wb"))
    print("Finished writing pickle file.\n")

    # Read from pickle file, save into new variable.
    print("Reading pickle file...")
    read_people = pickle.load(open("people.p", "rb"))
    print("Finished reading pickle file. Printing input...\n")

    # Print each person in the people dictionary.
    print("Employees:\n")
    for person in read_people:
        read_people[person].display()

    # Program complete, terminate the program. (exit code 0)
    exit(0)


if __name__ == "__main__":
    main()
