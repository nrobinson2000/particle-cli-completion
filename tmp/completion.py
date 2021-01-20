import json
from subprocess import run, PIPE

# Remove left whitespace form all lines
def strip_lines(input):
	return [line.lstrip() for line in input]

# Create a dict of commands and descriptions
def get_commands(input):
	left_slice = input[input.index('Commands:')+1:]
	right_slice = left_slice[:left_slice.index('')]
	command_dict = {line.split(maxsplit=1)[0]:line.split(maxsplit=1)[1] for line in right_slice}
	return command_dict

def get_options(input):
	left_slice = input[input.index('Options:')+1:]
	right_slice = left_slice[:left_slice.index('')]
	command_dict = {line.split(maxsplit=1)[0].split(",")[0]:line.split(maxsplit=1)[1] for line in right_slice}

	# command_dict = [line.split(maxsplit=1)[0].split(",")[0] for line in right_slice]


	return command_dict

# Initial top level of commands
output = run(["particle", "help"], stderr=PIPE).stderr.decode('utf-8').splitlines()
command_map = get_commands(output)
top_level = command_map.keys()

# Generate some BASH completion code
print("local %s" % " ".join(top_level))
print('_primary="%s"' % " ".join(top_level))

# Raw debug contents
help_output = dict()

# Command dicts
description = dict()
usage = dict()
commands = dict()
options = dict()

# Populate description, usage, and commands
for command in command_map:
	output = run(["particle", "help", command], stderr=PIPE).stderr.decode('utf-8').splitlines()
	
	stripped = strip_lines(output)
	help_output[command] = stripped
	description[command] = stripped[0]
	usage[command] = stripped[1].removeprefix('Usage: ')

	try:
		sub_commands = get_commands(stripped)
		commands[command] = sub_commands
	except ValueError:
		commands[command] = {}
	
	try:
		sub_options = get_options(stripped)
		options[command] = sub_options
	except ValueError:
		options[command] = {}


# Generate more BASH completion code

# print(*['_%s="%s"' % (key, " ".join(commands[key])) for key in commands], sep="\n")

# print('case "$prev" in')
# for command in top_level:
# 	print("\t%s)" % command)
# 	print('\t\tCOMPREPLY=($(compgen -W "$_%s" -- "$cur"));;' % command)

# Write help.json
with open("help.json", "w") as file:
	json.dump(help_output, file, indent=4)

# Write JSON files
with open("commands.json", "w") as file:
	json.dump(commands, file, indent=4)
with open("description.json", "w") as file:
	json.dump(description, file, indent=4)
with open("options.json", "w") as file:
	json.dump(options, file, indent=4)


# Raw debug contents
help_sub = dict()

# Command dicts
description_sub = dict()
usage_sub = dict()
commands_sub = dict()
options_sub = dict()

# Go deeper
for command in commands:
	sub_commands = commands[command]

	help_sub[command] = dict()

	description_sub[command] = dict()
	usage_sub[command] = dict()
	commands_sub[command] = dict()
	options_sub[command] = dict()

	if not sub_commands:
		continue

	for sub_command in sub_commands:
		output = run(["particle", "help", command, sub_command], stderr=PIPE).stderr.decode('utf-8').splitlines()
		stripped = strip_lines(output)
		help_sub[command][sub_command] = stripped
		description_sub[command][sub_command] = stripped[0]
		usage_sub[command][sub_command] = stripped[1].removeprefix('Usage: ')

		try:
			sub_sub_commands = get_commands(stripped)
			commands_sub[command][sub_command] = sub_sub_commands
		except ValueError:
			commands_sub[command][sub_command] = {}
		
		try:
			sub_options = get_options(stripped)
			options_sub[command][sub_command] = sub_options
		except ValueError:
			options_sub[command][sub_command] = {}

# Write massive JSON file
with open("help_sub.json", "w") as file:
	json.dump(help_sub, file, indent=4)

# Write cool JSON files
with open("commands_sub.json", "w") as file:
	json.dump(commands_sub, file, indent=4)
with open("description_sub.json", "w") as file:
	json.dump(description_sub, file, indent=4)
with open("options_sub.json", "w") as file:
	json.dump(options_sub, file, indent=4)


# Raw debug contents
help_sub_sub = dict()

# Command dicts
description_sub_sub = dict()
usage_sub_sub = dict()
commands_sub_sub = dict()
options_sub_sub = dict()

# Go even deeper
for command in commands_sub:
	sub_commands = commands_sub[command]

	help_sub_sub[command] = dict()

	description_sub_sub[command] = dict()
	usage_sub_sub[command] = dict()
	commands_sub_sub[command] = dict()
	options_sub_sub[command] = dict()

	if not sub_commands:
		continue

	for sub_command in sub_commands:
		sub_sub_commands = sub_commands[sub_command]


		help_sub_sub[command][sub_command] = dict()

		description_sub_sub[command][sub_command] = dict()
		usage_sub_sub[command][sub_command] = dict()
		commands_sub_sub[command][sub_command] = dict()
		options_sub_sub[command][sub_command] = dict()

		if not sub_sub_commands:
			continue

		for sub_sub_command in sub_sub_commands:
			output = run(["particle", "help", command, sub_command, sub_sub_command], stderr=PIPE).stderr.decode('utf-8').splitlines()
			stripped = strip_lines(output)
			help_sub_sub[command][sub_command][sub_sub_command] = stripped
			description_sub_sub[command][sub_command][sub_sub_command] = stripped[0]
			usage_sub_sub[command][sub_command][sub_sub_command] = stripped[1].removeprefix('Usage: ')

			try:
				sub_sub_sub_commands = get_commands(stripped)
				commands_sub_sub[command][sub_command][sub_sub_command] = sub_sub_sub_commands
			except ValueError:
				commands_sub_sub[command][sub_command][sub_sub_command] = {}
			
			try:
				sub_options = get_options(stripped)
				options_sub_sub[command][sub_command][sub_sub_command] = sub_options
			except ValueError:
				options_sub_sub[command][sub_command][sub_sub_command] = {}

# Write cool JSON files
with open("commands_sub_sub.json", "w") as file:
	json.dump(commands_sub_sub, file, indent=4)
with open("description_sub_sub.json", "w") as file:
	json.dump(description_sub_sub, file, indent=4)
with open("options_sub_sub.json", "w") as file:
	json.dump(options_sub_sub, file, indent=4)

# Write massive JSON file
with open("help_sub_sub.json", "w") as file:
	json.dump(help_sub_sub, file, indent=4)