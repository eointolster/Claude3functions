import os
import sys
from tool_use_package.tools.base_tool import BaseTool
from tool_use_package.tool_user import ToolUser
from tool_use_package.tools.search.brave_search_tool import BraveSearchTool

# 1. Define the Tools
class AdditionTool(BaseTool):
    """Adds together two numbers, a + b."""
    def use_tool(self, a, b):
        print(f"Adding {a} and {b}")
        return a+b

class FileWriteTool(BaseTool):
    """Writes content to a file."""
    def use_tool(self, file_path, content):
        print(f"Writing to file: {file_path}")
        with open(file_path, 'w') as file:
            file.write(content)
        return f"Content written to file: {file_path}"

class FileReadTool(BaseTool):
    """Reads content from a file."""
    def use_tool(self, file_path):
        print(f"Reading from file: {file_path}")
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    
class CreateFolderTool(BaseTool):
    """Creates a new folder at the specified path."""
    def use_tool(self, folder_path):
        print(f"Creating folder: {folder_path}")
        os.makedirs(folder_path, exist_ok=True)
        return f"Folder created: {folder_path}"


# 2. Tool Descriptions
addition_tool_name = "perform_addition"
addition_tool_description = """Add one number (a) to another (b), returning a+b.
Use this tool WHENEVER you need to perform any addition calculation, as it will ensure your answer is precise."""
addition_tool_parameters = [
    {"name": "a", "type": "float", "description": "The first number in your addition equation."},
    {"name": "b", "type": "float", "description": "The second number in your addition equation."}
]
addition_tool = AdditionTool(addition_tool_name, addition_tool_description, addition_tool_parameters)

search_tool_name = "search_brave"
search_tool_description = "The search engine will search using the Brave search engine for web pages similar to your query. It returns for each page its url and the full page content. Use this tool if you want to make web searches about a topic."
search_tool_parameters = [
    {"name": "query", "type": "str", "description": "The search query to enter into the Brave search engine."},
    {"name": "n_search_results_to_use", "type": "int", "description": "The number of search results to return, where each search result is a website page."}
]
search_tool = BraveSearchTool(
    name=search_tool_name,
    description=search_tool_description,
    parameters=search_tool_parameters,
    brave_api_key=os.environ["BRAVE_API_KEY"],
    truncate_to_n_tokens=5000
)

file_write_tool_name = "file_write"
file_write_tool_description = """Writes content to a file.
Use this tool to create files or scripts as requested by the user."""
file_write_tool_parameters = [
    {"name": "file_path", "type": "str", "description": "The path of the file to write to."},
    {"name": "content", "type": "str", "description": "The content to write to the file."}
]
file_write_tool = FileWriteTool(file_write_tool_name, file_write_tool_description, file_write_tool_parameters)

file_read_tool_name = "file_read"
file_read_tool_description = """Reads content from a file.
Use this tool to read files when needed to answer a question or provide information."""
file_read_tool_parameters = [
{"name": "file_path", "type": "str", "description": "The path of the file to read from."}
]
file_read_tool = FileReadTool(file_read_tool_name, file_read_tool_description, file_read_tool_parameters)

create_folder_tool_name = "create_folder"
create_folder_tool_description = """Creates a new folder at the specified path.
Use this tool to create folders as requested by the user."""
create_folder_tool_parameters = [
    {"name": "folder_path", "type": "str", "description": "The path of the folder to create."}
]
create_folder_tool = CreateFolderTool(create_folder_tool_name, create_folder_tool_description, create_folder_tool_parameters)




#3. Assign Tools and Ask Claude
tool_user = ToolUser([addition_tool, search_tool, file_write_tool, file_read_tool, create_folder_tool])

if len(sys.argv) > 1:
    query = ' '.join(sys.argv[1:])
    messages = [
        {
            "role":"user",
            "content": query
        }
        ]
    try:
        response = tool_user.use_tools(messages, execution_mode="automatic")
        print(response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
else:
    print("Please provide a search query, an addition task, a file write task, or a file read task as command-line arguments.")
    print("Examples:")
    print("- Search: python app.py what is the current date and time in Melbourne Australia, do a search online for the current date and time first")
    print("- Addition: python app.py add 5 and 7")
    print("- File Write: python app.py create a file named example.txt with content 'This is an example file.'")
    print("- File Read: python app.py read the content of file example.txt")
    print("- Folder Creation: python app.py create a folder named example_folder")