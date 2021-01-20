import json
import sys
import time

options_complete = dict()

with open("json/options_complete.json") as file:
    options_complete = json.load(file)

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
# Replace the dash with an underscore.
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
# ------------------------------------- #

# Generated at: %s

# Find serial devices on Mac and Linux
_get_modems()
{
  if [[ "$(uname -s)" == "Darwin" ]]; then
    ls /dev/cu.usbmodem* 2>/dev/null
  else
    ls /dev/ttyACM* 2>/dev/null
  fi
}

# Bash completion function for particle-cli
_particle()
{
    local cur prev prevprev prevprevprev first second third prevraw prevprevraw prevprevnonflag

    COMPREPLY=()                       # Completion suggestions array
    cur="${COMP_WORDS[COMP_CWORD]}"    # Current word being typed

    prev="${COMP_WORDS[COMP_CWORD-1]}"         # Previous word typed
    prevprev="${COMP_WORDS[COMP_CWORD-2]}"     # Previous previous word typed
    prevprevprev="${COMP_WORDS[COMP_CWORD-3]}" # Previous previous previous word typed

    prevraw="${prev}"
    prevprevraw="${prevprev}"
    prevprevnonflag="${prevprev/-/_}"

    prev="${prev//-/_}"
    prevprev="${prevprev//-/_}"
    prevprevprev="${prevprevprev//-/_}"

    first="${COMP_WORDS[1]//-/_}"
    second="${COMP_WORDS[2]//-/_}"
    third="${COMP_WORDS[3]//-/_}"
''' % time.ctime()
)

# Remove update-cli since its empty and invalid variable name
top_level.remove("update-cli")

print("    local %s" % " ".join(["_%s" % key for key in top_level]))
print()

# Add update-cli back, and add help and --version
top_level.extend(['update-cli', 'help', '--version'])

print('    _primary="%s"' % " ".join(top_level))
print()

# Override, use long flags for `login` and `cloud login`
first_dict['_login'] = "--username --password --token --otp"
second_dict['_cloud_login'] = "--username --password --token --otp"

for key in first_dict:
    print('    %s="%s"' % (key, first_dict[key]))
print()

print("    local %s" % " ".join(second_dict.keys()))
print()

for key in second_dict:
    print('    %s="%s"' % (key, second_dict[key]))
print()

print("    local %s" % " ".join(third_dict.keys()))
print()

for key in third_dict:
    print('    %s="%s"' % (key, third_dict[key]))

print('''
    # Suggest primary subcommands after `particle` or `particle help`
    if [[ "$COMP_CWORD" == 1 ]] || [[ "$prev" == "help" ]]; then
        COMPREPLY=($(compgen -W "$_primary" -- "$cur"))
        return 0
    fi

    # Use _get_modems (not always perfect, but handy most of the time)
    if [[ "$prev" == "__port" ]] && [[ ! "$first" == "keys" ]]; then
        COMPREPLY=($(compgen -W "$(_get_modems)" -- "$cur"))
        return 0
    fi

    # Suggest files
    if [[ "$prev" == "__file" ]]; then
        COMPREPLY=($(compgen -fd -- "$cur"))
        return 0
    fi

    # More file overrides''')

def file_completion(pattern_list):
    pattern = " ".join(pattern_list)
    print('''    if [[ ! "$first" == "$cur" ]] && [[ "%s" == *"$first"* ]]; then
        COMPREPLY=($(compgen -fd -- "$cur"))
    fi''' % pattern)

file_completion(["flash", "compile", "preprocess"])

def file_override_completion(first_arg, pattern_list):
    pattern = " ".join(pattern_list)
    print('''
    if [[ "$first" == "%s" ]] && [[ ! "$second" == "$cur" ]] && [[ "%s" == *"$second"* ]]; then
        COMPREPLY=($(compgen -fd -- "$cur"))
    fi''' % (first_arg, pattern))

file_override_completion("cloud", ["flash", "compile"])
file_override_completion("binary", ["inspect"])
file_override_completion("keys", ["new", "load", "save", "send", "server"])
file_override_completion("library", ["migrate"])
file_override_completion("webhook", ["create"])
print()

def indirect_completion(pattern):
    print('    local _lookup _options')
    print('    _lookup="_%s"' % pattern)
    print('    _lookup="${_lookup//\//_}"')
    print('    _lookup="${_lookup//./_}"')
    print('    _options="${!_lookup}"')

    print('    if [[ -n "$_options" ]] && [[ ! " ${_options} " =~ " ${prev} " ]] && [[ ! "${_options}" == "${prevraw}" ]] && [[ ! " ${_options} " =~ " ${prevprev} " ]] && [[ ! "${_options}" == "${prevprevraw}" ]] && [[ ! " ${_options} " =~ " ${prevprevnonflag} " ]]; then')

    print('        COMPREPLY=(${COMPREPLY[@]} $(compgen -W "$_options" -- "$cur"))')
    print('        return 0')
    print('    fi')
    print()

print("    # Command matching using indirection")

# Relative matching (indirection)
indirect_completion('${prevprevprev}_${prevprev}_${prev}')
indirect_completion('${prevprev}_${prev}')
indirect_completion('${prev}')

# Absolute matching (indirection)
indirect_completion('${first}_${second}_${third}')
indirect_completion('${first}_${second}')
indirect_completion('${first}')

print('''    # Suggest files and directories if there is not a match
    COMPREPLY=($(compgen -fd -- "$cur"))
}

complete -F _particle particle # Apply the _particle completion function
complete -F _particle p
alias p="particle"''')
