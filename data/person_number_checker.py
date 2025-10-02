def personnummer_checker(personal_number):
    personal_number = str(personal_number)
    if personal_number[0:1] == "1" or personal_number[0:1] == "2":
        personal_number = personal_number[2:]
    multy = []
    lst = [number for number in str(personal_number) if number not in "-.,/*_"]
    #print(f"# Debugging list: {lst}")

    numbers = [int(letter) for letter in lst]
    #print(f"# Debugging int_lst: {numbers}")

    for i in range(len(numbers)):
        if i % 2 == 0:
            multy.append(2 * numbers[i])
        else:
            multy.append(1 * numbers[i])
    #print(f"# Debugging Multi_lst: {multy}")

    addition = 0
    for number in multy:
        current = str(number)
        if len(current) == 2:
            addition += int(current[0]) + int(current[1])
        else:
            addition += int(current[0])
    #print(f"# Debugging sum: {addition}")

    if addition % 10 == 0:
        return True
    return False


def gender_checker(personal_number):
    personal_number = str(personal_number)
    lst = [letter for letter in personal_number]
    if len(lst) != 0:
        third_number = int(lst[-2])
        if third_number % 2 != 0:
            return "man"
        return "woman"
    #print("# Debugging value are is None")
    return "None"


if __name__ == "__main__":
    print("#===================== Welcome to personal number validation detector =====================#")
    user_pno = input("Enter your personal number (YYMMDD-XXXX or YYMMDDXXXX or YYYYMMDD-XXXX): ")
    if personnummer_checker(user_pno):
        print("personal number is working, OK!")
        print(f"The person is a {gender_checker(user_pno)}")
    else:
        print("personal number is not working, Not OK!")
