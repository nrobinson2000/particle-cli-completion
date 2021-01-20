import json
import sys
import time

options_complete = dict()

with open("json/options_complete.json") as file:
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

top_level = list(options_complete.keys())
commands = options_complete

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

# Generate some BASH completion code

print(
'''#!/bin/bash

# ------------------------------------- #
# particle-cli-completion               #
# Made by Nathan Robinson               #
# @nrobinson2000                        #
# File: particle-cli                    #
# Desc: Tab completion for particle-cli #
# ------------------------------------- #

# Generated at: %s

# Find serial devices on Mac and Linux
getModems()
{
  if [[ "$(uname -s)" == "Darwin" ]]; then
    ls /dev/cu.usbmodem* 2>/dev/null
  else
    ls /dev/ttyACM* 2>/dev/null
  fi
}

_particle() # This is the bash completion function
{
	local cur prev prevprev prevprevprev

    COMPREPLY=()                       # Completion suggestions array
    cur="${COMP_WORDS[COMP_CWORD]}"    # Current word being typed

	prev="${COMP_WORDS[COMP_CWORD-1]}" # Previous word typed
	prevprev="${COMP_WORDS[COMP_CWORD-2]}" # Previous previous word typed
	prevprevprev="${COMP_WORDS[COMP_CWORD-3]}" # Previous previous previous word typed

	prev="${prev//-/_}"
	prevprev="${prevprev//-/_}"
	prevprevprev="${prevprevprev//-/_}"
''' % time.ctime()
)

# Remove update-cli since its empty and invalid varibale name
top_level.remove("update-cli")

print("\tlocal %s" % " ".join(["_%s" % key for key in top_level]))
print()

# Add update-cli back, and add help and --version
top_level.extend(['update-cli', 'help', '--version'])

print('\t_primary="%s"' % " ".join(top_level))
print()

for key in first_dict:
    print('\t%s="%s"' % (key, first_dict[key]))
print()


print("\tlocal %s" % " ".join(second_dict.keys()))
print()

for key in second_dict:
    print('\t%s="%s"' % (key, second_dict[key]))
print()

print("\tlocal %s" % " ".join(third_dict.keys()))
print()

for key in third_dict:
    print('\t%s="%s"' % (key, third_dict[key]))

print('''
    # Suggest primary subcommands when typing the first word after 'particle'
    if [[ "$COMP_CWORD" == 1 ]] || [[ "$prev" == "help" ]]; then
        COMPREPLY=($(compgen -W "$_primary" -- "$cur"))
        return 0
    fi

	# Use getModems
    if [[ "$COMP_CWORD" == 3 ]] && [[ "$prev" == "monitor" ]]; then
        COMPREPLY=($(compgen -W "$(getModems) --follow" -- "$cur"))
        return 0
    fi

    if [[ "$COMP_CWORD" == 4 ]] && [[ "$prev" == "__follow" ]]; then
        COMPREPLY=($(compgen -W "$(getModems)" -- "$cur"))
        return 0
    fi

    # Suggest corresponding subcommands and arguments for each command''')

def indirect_completion(pattern):
    print('\tlocal _lookup _options')
    print('\t_lookup="_%s"' % pattern)
    print('\t_options="${!_lookup}"')
    print('\tif [[ -n "$_options" ]]; then')
    print('\t\tCOMPREPLY=($(compgen -W "$_options" -- "$cur"))')
    print('\t\treturn 0')
    print('\tfi')
    print()

# First level matching (indirection)
indirect_completion('${prev}')

# Second level matching (indirection)
indirect_completion('${prevprev}_${prev}')

# Third level matching (indirection)
indirect_completion('${prevprevprev}_${prevprev}_${prev}')


print('''	# Suggest files and directories if there is not a match
	COMPREPLY=($(compgen -fd -- "$cur"))
}

complete -F _particle particle # Apply the _particle completion function
complete -F _particle p
alias p="particle"''')
