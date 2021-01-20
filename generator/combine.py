import json

# Dict of all particle-cli commands
commands = dict()

# Dicts of all particle-cli options at various depths
options = dict()
options_sub = dict()
options_sub_sub = dict()

with open("json/commands_sub_sub.json") as file:
    commands = json.load(file)

with open("json/options.json") as file:
    options = json.load(file)

with open("json/options_sub.json") as file:
    options_sub = json.load(file)

with open("json/options_sub_sub.json") as file:
    options_sub_sub = json.load(file)

# Create options_complete.json
options_complete = dict()

for command in options:
    options_complete[command] = options[command]
    if not options_complete[command]:
        options_complete[command] = options_sub[command]
        for sub_command in options_complete[command]:
            if not options_complete[command][sub_command]:
                options_complete[command][sub_command] = options_sub_sub[command][sub_command]


with open("json/options_complete.json", "w") as file:
    json.dump(options_complete, file, indent=4)
