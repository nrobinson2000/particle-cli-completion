import json
import sys

options_complete = dict()

with open("options_complete.json") as file:
    options_complete = json.load(file)

def suggest(args):
    if isinstance(args, str):
        args = args.split()

    suggestions = list()
    length = len(args)

    try:
        selection = options_complete
        for i in range(length):
            selection = selection[args[i]]
        suggestions.extend(selection.keys())
    except KeyError:
        pass
    except AttributeError:
        pass
    print(*suggestions, sep=" ")

# suggest(sys.argv[1:])

top_level = options_complete.keys()
commands = options_complete

# Generate some BASH completion code
print("local %s" % " ".join(["_%s" % key for key in top_level]))
print()

print('_primary="%s"' % " ".join(top_level))
print()

# Helper
def len_val(data):
    length = len(data)
    value = " ".join(data)
    return (length, value)

# First level completion dict
first_dict = dict()
for command in commands:
    length, value = len_val(commands[command])
    key = "_%s" % command
    if length > 0:
        first_dict[key] = value

for key in first_dict:
    print('%s="%s"' % (key, first_dict[key]))
print()

# Second level completion dict
second_dict = dict()
for command in commands:
    command_dict = commands[command]
    if command_dict:
        for key in command_dict:
            if not isinstance(command_dict[key], str):
                length, value = len_val(command_dict[key])
                sub_key = '_%s_%s' % (command, key)
                if length > 0:
                    second_dict[sub_key] = value

# Some keys in seconds_dict have dashes. Bash does not accept this.
# Replace the dash with and underscore. A workaround will be needed soon.

# TODO: Replace - with _ for prev, prevprev, prevprevprev

bad_keys = "_usb_start-listening _usb_stop-listening _usb_safe-mode _usb_setup-done _usb_cloud-status"
bad_keys = bad_keys.split()

replace_keys = [key.replace('-', '_') for key in bad_keys]
replace_dict = second_dict.copy()

for key in second_dict:
    if key in bad_keys:
        new_key = replace_keys[bad_keys.index(key)]
        replace_dict[new_key] = second_dict[key]
        replace_dict.pop(key)

second_dict = replace_dict

# Third level completion dict
third_dict = dict()
for command in commands:
    command_dict = commands[command]
    if command_dict:
        for key in command_dict:
            if not isinstance(command_dict[key], str):
                sub_command_dict = command_dict[key]
                if sub_command_dict:
                    for sub_key in sub_command_dict:
                        if not isinstance(sub_command_dict[sub_key], str):
                            length, value =  len_val(sub_command_dict[sub_key])
                            sub_sub_key = '_%s_%s_%s' % (command, key, sub_key)
                            if length > 0:
                                third_dict[sub_sub_key] = value


print("local %s" % " ".join(second_dict.keys()))
print()

for key in second_dict:
    print('%s="%s"' % (key, second_dict[key]))
print()

print("local %s" % " ".join(third_dict.keys()))
print()

for key in third_dict:
    print('%s="%s"' % (key, third_dict[key]))
print()





# First level matching
# print('case "$prev" in')
# for command in top_level:
# 	print("\t%s)" % command)
# 	print('\t\tCOMPREPLY=($(compgen -W "$_%s" -- "$cur"));;' % command)
# print("esac")
# print()
# print()



# First level matching (indirection)
print('local _lookup _options')
print('_lookup="_${prev}"')
print('_options="${!_lookup}"')
print('if [[ -n "$_options" ]]; then')
print('\tCOMPREPLY=($(compgen -W "$_options" -- "$cur"))')
print('\treturn 0')
print('fi')
print()







# Second level matching (indirection)
print('local _lookup _options')
print('_lookup="_${prevprev}_${prev}"')
print('_options="${!_lookup}"')
print('if [[ -n "$_options" ]]; then')
print('\tCOMPREPLY=($(compgen -W "$_options" -- "$cur"))')
print('\treturn 0')
print('fi')
print()





# Third level matching (indirection)
print('local _lookup _options')
print('_lookup="_${prevprevprev}_${prevprev}_${prev}"')
print('_options="${!_lookup}"')
print('if [[ -n "$_options" ]]; then')
print('\tCOMPREPLY=($(compgen -W "$_options" -- "$cur"))')
print('\treturn 0')
print('fi')
print()

