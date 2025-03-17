from collections import namedtuple

CommandTexts = namedtuple('CommandTexts', ['start', 'help', 'other_commands'])
CommonTexts = namedtuple('CommonTexts', ["actions"])
commands = CommandTexts(
    start="Welcome to the NUtinder bot!",
    help="Here's a list of commands you can use:\n/start - Start the bot\n/help - Get help",
    other_commands="This is another command's response."
)

menu_text = CommonTexts(
    actions=(
        f"1. View profiles\n"
        f"2. My profile\n"
        f"3. History\n"
        f"4. Link Instagram\n"
    )
)