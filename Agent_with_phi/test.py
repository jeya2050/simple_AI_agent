from phi.agent import Agent
from phi.tools.newspaper4k import Newspaper4k
from phi.model.groq import Groq

agent = Agent(    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
tools=[Newspaper4k(include_summary=True)], debug_mode=True, show_tool_calls=True)
agent.print_response("Please summarize https://www.geeksforgeeks.org/python-functions/")
