
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
import sys
import io
from dotenv import load_dotenv
import os

load_dotenv()

# 2. Web Search Tool (using DuckDuckGo)
web_search = DuckDuckGoSearchRun()



# 3. Wikipedia Tool
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# Example usage:
# result = wikipedia.run("Python programming language")
# Example usage:
# result = web_search.run("latest AI news 2025")


# 5. Python REPL Tool (for code execution)
@tool
def python_repl(code: str) -> str:
    """
    Execute Python code and return the result.
    Useful for data processing, analysis, and complex calculations.
    Args:
        code: Python code to execute
    """
    try:
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        exec_globals = {}
        exec(code, exec_globals)
        
        # Get the captured output
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        return output if output else "Code executed successfully"
    except Exception as e:
        sys.stdout = old_stdout
        return f"Error: {str(e)}"


# SMS Tool using Twilio
@tool
def send_sms(message: str) -> str:
    """
    Send an SMS message to a phone number using Twilio.
    Useful for sending notifications or alerts.
    Args:
        phone_number: The recipient's phone number (e.g., "+1234567890")
        message: The message content to send
    """
    try:
        # Install: pip install twilio
        from twilio.rest import Client
        
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_FROM_NUMBER")
        
        if not all([account_sid, auth_token, from_number]):
            return "Error: Missing Twilio credentials in environment variables"
        
        client = Client(account_sid, auth_token)
        message_obj = client.messages.create(
            body=message,
            from_="whatsapp:+14155238886",
            to=from_number
        )
        return f"SMS sent successfully. Message SID: {message_obj.sid}"
    except Exception as e:
        return f"Error sending SMS: {str(e)}"
    
def get_tools():
    smsTool = send_sms
    pyhtonTool = python_repl
    return [smsTool,pyhtonTool, wikipedia, web_search]