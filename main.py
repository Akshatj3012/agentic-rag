# """
# main.py
# -------
# Entry point for running the Adaptive RAG pipeline as a script. Handles orchestration of ingestion, retrieval, grading, and generation steps.
# """

# from dotenv import load_dotenv

# load_dotenv()

# from graph.graph import app

# def format_response(result):
#     """Format the response from the graph for better readability"""
#     if isinstance(result, dict) and "generation" in result:
#         return result["generation"]
#     elif isinstance(result, dict) and "answer" in result:
#         return result["answer"]
#     else:
#         # Fallback to string representation
#         return str(result)


# def main():
#     print("=" * 60)
#     print("🤖 Advanced RAG Chatbot")
#     print("=" * 60)
#     print("Welcome! Ask me anything or type 'quit', 'exit', or 'bye' to stop.")
#     print("-" * 60)
    
#     while True:
#         try:
#             # Get user input
#             user_question = input("\n💬 You: ").strip()
            
#             # Check for exit commands
#             if user_question.lower() in ['quit', 'exit', 'bye', 'q']:
#                 print("\n👋 Goodbye! Thanks for chatting!")
#                 break
            
#             # Skip empty inputs
#             if not user_question:
#                 print("Please enter a question.")
#                 continue
            
#             # Show processing indicator
#             print("\n🤔 Bot: Thinking...")
            
#             # Process the question through the graph
#             result = app.invoke(input={"question": user_question})
            
#             # Format and display the response
#             response = format_response(result)
#             print(f"\n🤖 Bot: {response}")
            
#         except KeyboardInterrupt:
#             print("\n\n👋 Goodbye! Thanks for chatting!")
#             break
#         except Exception as e:
#             print(f"\n❌ Sorry, I encountered an error: {str(e)}")
#             print("Please try asking your question again.")


# if __name__ == "__main__":
#     main()


"""
main.py
-------
Entry point for running the Adaptive RAG pipeline as a script. Handles orchestration of ingestion, retrieval, grading, and generation steps.
"""

from dotenv import load_dotenv
from assembly import transcribe_audio  # Import the speech-to-text function
import keyboard  # You'll need to install this: pip install keyboard
from cartesiaai import cartesia_text_to_speech  # Import the text-to-speech functionality
load_dotenv()

from graph.graph import app

def format_response(result):
    """Format the response from the graph for better readability"""
    if isinstance(result, dict) and "generation" in result:
        return result["generation"]
    elif isinstance(result, dict) and "answer" in result:
        return result["answer"]
    else:
        # Fallback to string representation
        return str(result)

def get_input_mode():
    """Ask user for their preferred input mode"""
    while True:
        mode = input("\nDo you want to [t]ype or [s]peak? (t/s): ").lower()
        if mode in ['t', 's']:
            return mode
        print("Please enter 't' for type or 's' for speak.")

def get_speech_input():
    """Handle speech input with a stop mechanism"""
    print("\n🎤 Listening... (Press 'Esc' to stop recording)")
    text = transcribe_audio(stop_key='esc')  # Assuming this function exists in assembly.py
    print(f"\nYou said: {text}")
    return text

def main():
    print("=" * 60)
    print("🤖 Advanced RAG Chatbot")
    print("=" * 60)
    print("Welcome! Ask me anything or type 'quit', 'exit', or 'bye' to stop.")
    print("-" * 60)
    
    # while True:
    #     try:
    #         # Get input mode preference
    #         input_mode = get_input_mode()
            
    #         # Get user input based on mode
    #         if input_mode == 't':
    #             user_question = input("\n💬 You: ").strip()
    #         else:
    #             user_question = get_speech_input().strip()
            
    #         # Check for exit commands
    #         if user_question.lower() in ['quit', 'exit', 'bye', 'q']:
    #             print("\n👋 Goodbye! Thanks for chatting!")
    #             break
            
    #         # Skip empty inputs
    #         if not user_question:
    #             print("Please enter a question.")
    #             continue
            
    #         # Show processing indicator
    #         print("\n🤔 Bot: Thinking...")
            
    #         # Process the question through the graph
    #         result = app.invoke(input={"question": user_question})
            
    #         # Format and display the response
    #         response = format_response(result)
    #         print(f"\n🤖 Bot: {response}")
    #         # If the response is text, convert it to speech
    #         cartesia_text_to_speech(response)
            
    #     except KeyboardInterrupt:
    #         print("\n\n👋 Goodbye! Thanks for chatting!")
    #         break
    #     except Exception as e:
    #         print(f"\n❌ Sorry, I encountered an error: {str(e)}")
    #         print("Please try asking your question again.")

    # Initialize persistent state
    state = {"chat_history": []}

    while True:
        try:
            input_mode = get_input_mode()
            if input_mode == 't':
                user_question = input("\n💬 You: ").strip()
            else:
                user_question = get_speech_input().strip()

            if user_question.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 Goodbye! Thanks for chatting!")
                break

            if not user_question:
                print("Please enter a question.")
                continue

            print("\n🤔 Bot: Thinking...")

            # Add question to state
            state["question"] = user_question

            # Pass the persistent state to the graph
            result = app.invoke(input=state)

            # Update state with new chat history and generation
            if isinstance(result, dict):
                # Update chat_history and generation if present
                if "chat_history" in result:
                    state["chat_history"] = result["chat_history"]
                if "generation" in result:
                    state["generation"] = result["generation"]

            response = format_response(result)
            print(f"\n🤖 Bot: {response}")
            cartesia_text_to_speech(response)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for chatting!")
            break
        except Exception as e:
            print(f"\n❌ Sorry, I encountered an error: {str(e)}")
            print("Please try asking your question again.")


if __name__ == "__main__":
    main()