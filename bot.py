   import os
   import logging
   import re
   from telegram import Update
   from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
   import asyncio

   # Enable logging
   logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
   logger = logging.getLogger(__name__)

   TOKEN = os.getenv('7749031474:AAGDCmV6nW_VKd_tR1G_WN4_thet-dsuN2k')  # Fetch from environment variable

   # Default delay in seconds
   user_delays = {}

   async def delete_message(context: CallbackContext):
       await asyncio.sleep(context.job.context['delay'])
       await context.bot.delete_message(chat_id=context.job.context['chat_id'], message_id=context.job.context['message_id'])

   def start(update: Update, context: CallbackContext):
       update.message.reply_text('Hello! Use /setdelay <time> to set the message deletion delay. Example: /setdelay 20s or /setdelay 1h')

   def set_delay(update: Update, context: CallbackContext):
       if context.args:
           time_str = context.args[0]
           match = re.match(r'(d+)([smhd]?)', time_str)

           if match:
               value, unit = match.groups()
               value = int(value)

               # Convert time to seconds
               if unit == 's':
                   delay = value
               elif unit == 'm':
                   delay = value * 60
               elif unit == 'h':
                   delay = value * 3600
               elif unit == 'd':
                   delay = value * 86400
               else:
                   delay = value  # Default to seconds if no unit provided

               user_delays[update.message.chat_id] = delay
               update.message.reply_text(f'Delay set to {delay} seconds.')
           else:
               update.message.reply_text('Invalid format. Use /setdelay <time>. Example: /setdelay 20s or /setdelay 1h')
       else:
           update.message.reply_text('Please provide a time. Example: /setdelay 20s')

   def echo(update: Update, context: CallbackContext):
       update.message.reply_text(update.message.text)
       delay = user_delays.get(update.message.chat_id, 20)  # Default to 20 seconds if not set
       context.job_queue.run_once(delete_message, 0, context={'chat_id': update.message.chat_id, 'message_id': update.message.message_id, 'delay': delay})

   def main():
       updater = Updater(TOKEN)

       dp = updater.dispatcher
       
       dp.add_handler(CommandHandler("start", start))
       dp.add_handler(CommandHandler("setdelay", set_delay))
       dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

       updater.start_polling()
       updater.idle()

   if __name__ == '__main__':
       main()
  
