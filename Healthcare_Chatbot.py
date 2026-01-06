# import os
# import google.generativeai as genai

# # MAKE SURE YOUR API IS SET
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("models/gemini-2.5-flash")

# chat = model.start_chat(history=[])

# # Generate Text
# while True:
#     user_input = input("How can I help you? : ")
#     if user_input.lower() in ["quit",'exit','bye']:
#         break
#     response = chat.send_message(
#         f"You are a helpful , kind and empathetic health assistant. "
#         f"Provide general wellness guidance. "
#         f"you give short and precise answers."
#         f"you must only give response related to health and wellness."
#         f"you must give elaborated response only ywhen the user asks you for that"
#         f"User said: {user_input}"
#     )
#     print(response.text)

