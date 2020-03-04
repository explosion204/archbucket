from bot_interface import BotInterface
from api.telegram.telegram_api import TelegramAPI

# init bot interface
bot = BotInterface()
# set API
bot.set_api(TelegramAPI(bot))
# creating request processing pipelines (milti threading implementation)
bot.create_pipeline()
bot.create_pipeline()
bot.create_pipeline()
# start bot
bot.start_bot()