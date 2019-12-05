def does_not_decrease(pw):
    previous_val = int(pw[0])
    for char in pw:
        if int(char) < previous_val:
            return False
        previous_val = int(char)
    return True


def has_adjacent_doubles(pw):
    previous = 'a'
    for char in pw:
        if char == previous:
            return True
        previous = char
    return False


def has_adjacent_doubles_no_longer_than_2(pw):
    longer = False
    adj = False
    previous = 'a'
    for char in pw:
        if char == previous:
            if adj:
                longer = True
            adj = True
        elif adj:
            if not longer:
                return True
            else:
                adj = False
                longer = False
        previous = char
    return adj and not longer


def no_longer_than_doubles(pw):
    previous = pw[0]
    counter = -1
    for char in pw:
        if char == previous:
            counter = counter + 1
        elif counter > 1 and counter % 2 != 1:
            return False
        else:
            counter = 0
        previous = char
    return True


def is_valid(pw):
    return does_not_decrease(pw) and has_adjacent_doubles(pw)


def is_valid_part2(pw):
    return does_not_decrease(pw) and has_adjacent_doubles_no_longer_than_2(pw)


if __name__ == "__main__":
    counter = 0
    for pw in range(234208, 765869):
        pw = str(pw).zfill(6)
        if is_valid(pw):
            counter = counter + 1
    print(counter)

