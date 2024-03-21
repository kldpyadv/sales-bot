Repository Structure
app.py: The main Flask application file that handles routing, initiates the chatbot conversation, and processes user inputs.
functions.py: Contains all the logic for interacting with the OpenAI API, processing user inputs, generating responses, and fetching laptop recommendations.
chat.html: The frontend HTML template that provides the user interface for the chatbot.

app.py
Purpose
Serves as the entry point for the Flask application, managing routing and session state for the chatbot conversation.
Key Functions
default_func(): Renders the chat interface and initiates a new chatbot conversation.
getresponse(): Processes user inputs and generates chatbot responses.
end_conv(): Ends the current chatbot conversation and resets the session.

functions.py
Purpose
Contains utility functions for the chatbot, including OpenAI API interactions, user input processing, and recommendation logic.
Key Functions
initialize_conversation(): Initializes the conversation with a system message defining the chatbot's objective.
get_chat_model_completions(messages): Sends messages to the OpenAI API and retrieves chat completions.
moderation_check(user_input): Performs a moderation check on user inputs.
intent_confirmation_layer(response_assistant): Confirms if the user's intent has been fully captured.
dictionary_present(response): Extracts a dictionary of user requirements from the chatbot's response.
compare_laptops_with_user(user_req_string): Matches the user's requirements against the laptop database and generates recommendations.
send_user_email() : Function Call api is used to call this function for sending mail to user.

chat.html
Purpose
Provides the frontend interface for the chatbot, allowing users to interact with the chatbot through a web browser.
Key Elements
Chat Window: Displays messages from both the user and the chatbot.
Input Field: Allows the user to type their messages to the chatbot.
Submit Button: Sends the user's message to the backend for processing.
JavaScript Functions
appendUserMessage(message): Displays the user's message in the chat window.
appendBotMessage(data): Displays the chatbot's response in the chat window.
showProcessingIndicator(): Shows a loading indicator while waiting for the chatbot's response.
removeProcessingIndicator(processingId): Removes the loading indicator once the response is received.
saveChatHistory() : saves the chat history in case of refresh, loads only history doesn't set the context for Bot
loadChatHistory() : loads the saved chat history in case of refresh, loads only history doesn't set the context for Bot
clearChatHistory() : clears the chat history and starts a new conversation