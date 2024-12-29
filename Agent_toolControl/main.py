import ollama
from pyfiglet import Figlet
from utils import search_duckduckgo,scrab_Data
from duckduckgo_search import DDGS


f = Figlet(font='small')  # or 'block', 'banner', etc.
print(f.renderText('Lets talk to the AI agent'))



websearch_tool={
      'type': 'function',
      'function': {
        'name': 'get_websearch',
        'description': "if user tells you websearch then only use and get the web data function otherwise shouldn't need and you may or maynot need for other tool",
        'parameters': {
          'type': 'object',
          'properties': {
            'query': {
              'type': 'string',
              'description': 'summary of whole user query',
            },
          },
          'required': ['query'],
        },
      },
    }

localsearch_tool={
      'type': 'function',
      'function': {
        'name': 'get_localsearch',
        'description': 'if user tells you search on local then only use and get the localsearch',
        'parameters': {
          'type': 'object',
          'properties': {
            'query': {
              'type': 'string',
              'description': 'summary of whole user query',
            },
          },
          'required': ['query'],
        },
      },
    }


# # query="age of python?"
# def get_websearch(query):
#     urls=search_duckduckgo(query, max_results=5)
#     scrabbed_Data=scrab_Data(urls)
#     return scrabbed_Data



def get_websearch(query):
    ddgs = DDGS()
    results = ddgs.news(query, max_results=5)
    articles = []
    for result in results:
        article = {
            "date": result.get("date"),
            "title": result.get("title"),
            "body": result.get("body"),
            "url": result.get("url"),
            "image": result.get("image"),
            "source": result.get("source")
        }
        articles.append(article)
    return articles

def get_localsearch(query):
    return "no realted data i had" 




def ollama_model(message):
    response = ollama.chat(
    model='granite3.1-dense:2b',
    messages=message,
    tools=[websearch_tool,localsearch_tool])
    return response




available_functions = {
  'get_websearch': get_websearch,
  'get_localsearch': get_localsearch,
}



while True:
    print('\nUser : ')
    user_int=input()

    messages = [{'role': 'user', 'content': f'{user_int}'}]

    response=ollama_model(messages)

    if response.message.tool_calls:
    # There may be multiple tool calls in the response
        for tool in response.message.tool_calls:
            print("******TOOL******",'\n')
            print("TOOL Name : ",tool.function.name)
            # Ensure the function is available, and then call it
            if function_to_call := available_functions.get(tool.function.name):
            #   print('Calling function:', tool.function.name)
                print('TOOL Arguments : ', tool.function.arguments)
                output = function_to_call(**tool.function.arguments)
                print("TOOL output : ",output,'\n')
                messages.append(response.message)
                messages.append({'role':'tool','content':str(output),'name':tool.function.name})
                #   print(messages)
                response=ollama_model(messages)
                print("Assistent : \n",response.message.content)
                print('___________________________________________________________________________________________________________________')

            else:
                print('Function', tool.function.name, 'not found')

    else:
        print("******TOOL******",'\n')
        print(None,'\n')
        print("Assistent : \n",response.message.content)
        print('_______________________________________________________________________________________________________________________________')


      

