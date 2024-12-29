from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo

from dotenv import load_dotenv
load_dotenv()



agent = Agent(
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    markdown=True,tools=[DuckDuckGo()], 
    show_tool_calls=True,
    description="You are a news agent that helps users find the latest news.",
    instructions=[
        # "Given a topic by the user, respond with 4 latest news items about that topic.",
        # "Search for 10 news items and select the top 4 unique iteccccms.",
        "Search in English",
    ],
    debug_mode=True,
)

# Get the response in a variable
# run: RunResponse = agent.run("Share a 2 sentence horror story.")
# print(run.content)

# Print the response in the terminal
agent.print_response("whats happening in chennai")

