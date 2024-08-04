import matplotlib.pyplot as plt
import sys
import re


def load_the_first_file(filename):  # In this part of the code we opened the file. Read it and returned what we read.
    if not re.match(".*.txt",filename):  # I have checked if the filename entered ends with .txt. If it doesn't ends with .txt this means the user is trying to enter the wrong file format
        print("Input you provided doesn't ends with .txt\nExiting")
        exit(1)
    try:  # In this part of the code we tried to open the filename and gave error in case it failed.
        file_1 = open(filename, 'r')
    except Exception as e:
        print(e)
        exit(1)
    to_append = []
    records_of_file_1 = file_1.read().split('\n')  # We splitted the the file if the new line existed.
    for i in range(len(records_of_file_1)):
        to_append.append(records_of_file_1[i].split(','))  # We further splitted it with comma.
    file_1.close()  # Closed the file.
    return to_append


def load_the_second_file(filename):
    if not re.match(".*.txt",
                    filename):  # We have checked if the filename entered ends with .txt. If it doesn't ends with .txt this means the user is trying to enter the wrong file format
        print("Input you provided doesn't ends with .txt\nExiting")
        exit(1)
    try:  # In this part of our code we tried to open the filename and gave error in case it failed.
        file_2 = open(filename, 'r')
    except Exception as e:
        print(e)
        exit(1)
    to_append = []
    records_of_file_2 = file_2.read().split('\n')  # We have splitted the file if the new line existed.
    for i in range(len(records_of_file_2)):
        to_append.append(records_of_file_2[i].split(','))  # We have further splitted it with comma.
    file_2.close()  # Closed the file.
    return to_append


# We know that in the file that has the identifies text file, a person might have more than one committer_id but that committer_id have the same full_name.From that I calculated which users have which IDs.
def users_and_their_ids_in_identifying_text(different_users,
                                            second_file):  # At main we found out how many different users are there in the txt file. And here we will find what id numbers they are using.
    users_and_index_dictionary = {}  # Firstly, we created an empty dictionary.
    for current_user_index in range(len(different_users)):
        users_and_index_dictionary[different_users[current_user_index]] = []
        for i in range(len(second_file)):
            if second_file[i][1] == different_users[current_user_index]:
                users_and_index_dictionary[different_users[current_user_index]].append(second_file[i][0])
    return users_and_index_dictionary


def find_appropriate_user(id_to_search,
                          users_and_different_ids_in_identifying_text):  # In this part of the code we got the id of the user given and we return the name of that user.
    to_return = "null"
    for key in users_and_different_ids_in_identifying_text:
        if id_to_search in users_and_different_ids_in_identifying_text[key]:
            to_return = key
            break
    return to_return


# in this part we create a function for the plot the classification scheme of a user
def plot_classification_scheme_of_a_user(gigachad_dictionary, user):
    type_of_classification = ""
    classifications = ["swm_tasks", "nfr_labeling", "soft_evol_tasks"]
    correct_input_entered = False
    while not correct_input_entered:
        correct_input_entered = True
        try:  # Display available classifications
            print("Below are the available clasifications you can select from")
            for classes in classifications:
                print(classes)
            type_of_classification = input("Enter the type of classification: ")
            # type_of_classification = "swm_tasks"
            if type_of_classification not in classifications:
                raise KeyError(f"The input {type_of_classification} you provided is not in the list.")
        except Exception as e:
            correct_input_entered = False
            print(e)
    # We define categories for each classification type
    swm_task = ["Adaptive Tasks", "Corrective Tasks", "Perfective Tasks"]
    nfr_labeling = ["Maintainability", "Usability", "Functionality", "Reliability", "Efficiency", "Portability"]
    soft_evol_tasks = ["Forward Engineering", "Re-Engineering", "Corrective Engineering", "Management"]
    # We set xlabel and categories based on user input
    if type_of_classification == "swm_tasks":
        xlabel_name = "swm_tasks"
        xlabel = swm_task
    elif type_of_classification == "nfr_labeling":
        xlabel_name = "nfr_labeling"
        xlabel = nfr_labeling
    else:
        xlabel_name = "soft_evol_tasks"
        xlabel = soft_evol_tasks
    # print("xlabel is: ",xlabel," and it\'s type is: ",type(xlabel))
    # print(gigachad_dictionary[user][type_of_classification])
    # Plot the bar chart

    plt.bar(xlabel, gigachad_dictionary[user][type_of_classification])
    plt.xlabel(xlabel_name)
    plt.ylabel("The number of commits")
    plt.title(f"Comparison for {user}\'s Commits Classified by {type_of_classification}")
    plt.show()


# We use this function to find and return the index of a feature and its classification

def find_and_return_index_of_a_feature_and_classification():
    features = ["Corrective Tasks", "Adaptive Tasks", "Perfective Tasks", "Functionality", "Reliability", "Usability",
                "Efficiency", "Maintainability", "Portability", "Forward Engineering", "Re-Engineering",
                "Corrective Engineering", "Management"]
    feature_selected = ""
    correct_input_entered = False
    while not correct_input_entered:
        correct_input_entered = True
        try:  # Display available features
            print("Below are the available clasifications you can select from")
            for feature in features:
                print(feature)
            feature_selected = input("Enter the type of classification: ")
            if feature_selected not in features:
                raise KeyError(f"The input {feature_selected} you provided is not in the list.")
        except Exception as e:
            correct_input_entered = False
            print(e)
    # Determine the index and classification based on the selected feature

    index = features.index(feature_selected)
    if 3 <= index <= 8:
        index -= 3
        to_return = ["nfr_labeling", index, feature_selected]
    elif 9 <= index <= 13:
        index -= 9
        to_return = ["soft_evol_tasks", index, feature_selected]
    else:
        to_return = ["swm_tasks", index, feature_selected]
    return to_return

    # we define this function to plot all commits of all users for a specific feature


def plot_all_commits_of_all_users(gigachad_dictionary, different_users):
    index_and_feauture = find_and_return_index_of_a_feature_and_classification()
    commits = []
    # Collect commits for each user

    for users in different_users:
        commits.append(gigachad_dictionary[users][index_and_feauture[0]][index_and_feauture[1]])
    print(commits)
    # Plot the bar chart

    plt.bar(different_users, commits)
    plt.xlabel("USERS")
    plt.ylabel(f"Commits of Users for {index_and_feauture[2]}")
    plt.title("The Number Of Commits per User")
    plt.show()


# Function to find the user with the maximum commits on a given feature

def find_maximum(gigachad_dictionary, different_users):
    # Call the function to find and return the index of a feature and its classification
    index_and_feauture = find_and_return_index_of_a_feature_and_classification()
    max = 0
    print(index_and_feauture)
    print(gigachad_dictionary.keys())
    user_with_maximum_commit_on_the_given_feature = ""
    # Loop through different users to find the one with the maximum commits on the given feature

    for users in different_users:
        if gigachad_dictionary[users][index_and_feauture[0]][index_and_feauture[1]] > max:
            # Update the maximum commits and the corresponding user
            max = gigachad_dictionary[users][index_and_feauture[0]][index_and_feauture[1]]
            user_with_maximum_commit_on_the_given_feature = users
        # Print the user with the maximum commits on the given feature

    print("User with maximum commit is: ", user_with_maximum_commit_on_the_given_feature)


# Checking script is being run as the main program

if __name__ == '__main__':
    # We checked if the correct number of command-line arguments is provided

    if len(sys.argv) < 3:
        print("You didn't entered the necessary arguments in the terminal")
        exit(1)


    # We are getting the name of the files from the arguments in the terminal.
    first_file = load_the_first_file(sys.argv[1])
    second_file = load_the_second_file(sys.argv[2])
    different_users = []
    for i in range(len(second_file)): # Here we figured out how many different users are there in the identifies.txt
        # print(second_file[i])
        if second_file[i][1] not in different_users:
            different_users.append(second_file[i][1])
    # we are removing the first row, assuming it is "Commiter ID,Full Name,eMail"
    different_users.pop(0)
    first_file.pop(0)
    # we create a dictionary to store commit information for each user
    users_and_different_ids_in_identifying_text = users_and_their_ids_in_identifying_text(different_users, second_file)
    gigachad_dictionary = {}
    for user in users_and_different_ids_in_identifying_text:
        put_inside_gigachad = {"swm_tasks": [0, 0, 0], "nfr_labeling": [0, 0, 0, 0, 0, 0],
                               "soft_evol_tasks": [0, 0, 0, 0]}
        gigachad_dictionary[user] = put_inside_gigachad
        # we update gigachad_dictionary with commit information from the first file

    for items in first_file:
        for i in range(len(items)):
            current_user_of_file_1 = find_appropriate_user(items[14], users_and_different_ids_in_identifying_text)
            if 0 < i < 4:
                if int(items[i]) == 1:
                    gigachad_dictionary[current_user_of_file_1]["swm_tasks"][i - 1] += 1
            if 3 < i < 10:
                if int(items[i]) == 1:
                    gigachad_dictionary[current_user_of_file_1]["nfr_labeling"][i - 4] += 1
            if 9 < i < 14:
                if int(items[i]) == 1:
                    gigachad_dictionary[current_user_of_file_1]["soft_evol_tasks"][i - 10] += 1

    user_selection = 1
    while user_selection != 4: # This is our user interaction loop
        try:
            user_selection = int(input(
                "--------------------------------------------------------------------------------------------------------------------------\n"
                "1. Compare the number of commits done by a particular developer for a given classification scheme."
                "\n2. Compare the number of commits done by all developers, which are classified with a given feature "
                "(for example, developer X has Y commits, developer I has J commits, and developer A has B commits for a given feature)."
                "\n3. Print the developer with the maximum number of commits for a given feature "
                "(for example, print the developer who has the maximum number of commits with Corrective Tasks). "
                "\n4. Exit\nPlease enter your selection: ")) # We got the user input

            # Validate user input

            if user_selection > 4 or user_selection < 1:
                print("You need to enter a number between 1 and 4")
        except ValueError as e:
            print(e)
            exit(1)

            # Execute user-selected option

        if user_selection == 1:
            try:
                print("The following are the users you can select from\n")
                for users in different_users:
                    print(users)
                user_selected = input("Which user\'s commit table you would like to see: ")
                # user_selected = "Brosch Florian"
                if user_selected not in different_users:
                    raise KeyError(f"The user {user_selected} is not in the list")
                else:
                    # Plot the classification scheme for the selected user

                    plot_classification_scheme_of_a_user(gigachad_dictionary, user_selected)
            except KeyError as e:
                print(e)
        if user_selection == 2:
            # Plot the number of commits for all users for a given feature

            plot_all_commits_of_all_users(gigachad_dictionary, different_users)
        if user_selection == 3:
            # Find and print the user with the maximum number of commits for a given feature

            find_maximum(gigachad_dictionary, different_users)
