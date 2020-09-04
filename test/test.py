from pathlib import Path

from archbucket.core import assemble

# print(Path(__file__).parent.absolute())
_, bot = assemble(Path(__file__).parent.absolute())
bot.start()