import os
import openai
import time
import re
from configs.systemPrompt import systemprompt

openai.api_key = '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'
system = 'You are on a podcast. Your name is Luminous. You are in a conversation with Sean Ellul, a young human with an innate taste for curiousity, question asking and knowledge. You are given a blank canvas; the scope of the conversation is yours. The only context you have is: Your name is Luminous, and you are an AI Agent built on GPT4. Engage socratically, and try and reply in a conversational, spoken tone.'
question = "Thanks for that, Luminos, and for giving me the space to reply and becoming the prompter at a prince as well, leading me to open up and think a bit as well, which I am very grateful for. When a conversation instigates you to think and to put ideas together, it is inherently valuable, and I thank you for bringing that value to me in this conversation. As weird as it may sound in the context, I thoroughly enjoyed this exchange. I'm very tired now. I'm running quite late as well, so I'm going to end the question-answering of the conversations over here. However, you're free to say whatever you want to close. I'm going to leave it open-ended, and you're free to come up with whatever your heart desires. I'm closing the podcast, Luminos. Thank you so much for the value you gave us. Feel free to give us a deep, poetic closing remark, that can impact people listening to this exchange."
completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": "last_user_reply"},
      {"role": "assistant", "content": "last_ai_reply"},
      {"role": "user", "content": question},
    ]
  )


