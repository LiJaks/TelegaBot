from loader import bot
import handlers
from utils.update_state import UpdateStateFilter
from utils.set_bot_commands import set_default_commands


if __name__ == '__main__':
    bot.add_custom_filter(UpdateStateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
