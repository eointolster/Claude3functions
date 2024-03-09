import os
import sys
from pydub import AudioSegment
from tool_use_package.tools.base_tool import BaseTool
from tool_use_package.tool_user import ToolUser
from tool_use_package.tools.search.brave_search_tool import BraveSearchTool
import shutil
import subprocess
from pydub import AudioSegment
from pydub.playback import play
import winsound

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

class FileCopyTool(BaseTool):
    """Copies a file or folder to another location."""
    def use_tool(self, source_path, destination_path):
        print(f"Copying from {source_path} to {destination_path}")
        shutil.copy(source_path, destination_path)
        return f"File/folder copied from {source_path} to {destination_path}"
    
class MinicondaStartTool(BaseTool):
    """Starts a Miniconda application."""
    def use_tool(self, app_name):
        print(f"Starting Miniconda application: {app_name}")
        try:
            miniconda_path = r"C:\Users\eoint\miniconda3"
            activate_script = os.path.join(miniconda_path, "Scripts", "activate.bat")
            subprocess.run([activate_script, miniconda_path], shell=True, check=True)
            subprocess.run([app_name], shell=True, check=True)
            return f"Miniconda application '{app_name}' started successfully."
        except subprocess.CalledProcessError as e:
            return f"Error starting Miniconda application '{app_name}': {str(e)}"
        
class StartCMDTool(BaseTool):
    """Starts a new Command Prompt (cmd.exe) window."""
    def use_tool(self):
        print("Starting a new Command Prompt window...")
        subprocess.Popen('cmd.exe', creationflags=subprocess.CREATE_NEW_CONSOLE)
        return "A new Command Prompt window has been started."
    
class CMDInteractionTool(BaseTool):
    """Interacts with a Command Prompt (cmd.exe) window by writing commands and reading the output."""
    def use_tool(self, command):
        print(f"Running command in Command Prompt: {command}")
        try:
            process = subprocess.Popen('cmd.exe', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
            stdout, stderr = process.communicate(command + '\n')
            if stderr:
                return f"Error executing command: {stderr}"
            else:
                return stdout.strip()
        except Exception as e:
            return f"Error interacting with Command Prompt: {str(e)}"    

class CreateAudioFileTool(BaseTool):
    """Creates an audio file (.wav or .mp3) with the specified content."""
    def use_tool(self, file_path, content, format="wav"):
        print(f"Creating audio file: {file_path}")
        
        # Create an AudioSegment from the content
        audio_segment = AudioSegment.from_file(content, format=format)
        
        # Export the AudioSegment to the specified file path
        audio_segment.export(file_path, format=format)
        
        return f"Audio file created: {file_path}"
    
class PlayAudioFileTool(BaseTool):
    """Plays an audio file (.wav or .mp3)."""
    def use_tool(self, file_path):
        print(f"Playing audio file: {file_path}")
       
        try:
            # Play the audio file using winsound
            winsound.PlaySound(file_path, winsound.SND_FILENAME)
           
            return f"Audio file played successfully: {file_path}"
        except Exception as e:
            return f"Error playing audio file: {str(e)}"

# 2. Tool Descriptions
addition_tool_name = "perform_addition"
addition_tool_description = """Add one number (a) to another (b), returning a+b.
Use this tool WHENEVER you need to perform any addition calculation, as it will ensure your answer is precise."""
addition_tool_parameters = [
    {"name": "a", "type": "float", "description": "The first number in your addition equation."},
    {"name": "b", "type": "float", "description": "The second number in your addition equation."}
]
addition_tool = AdditionTool(addition_tool_name, addition_tool_description, addition_tool_parameters)
###########################################
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
###########################################
file_write_tool_name = "file_write"
file_write_tool_description = """Writes content to a file.
Use this tool to create files or scripts as requested by the user."""
file_write_tool_parameters = [
    {"name": "file_path", "type": "str", "description": "The path of the file to write to."},
    {"name": "content", "type": "str", "description": "The content to write to the file."}
]
file_write_tool = FileWriteTool(file_write_tool_name, file_write_tool_description, file_write_tool_parameters)
###########################################
file_read_tool_name = "file_read"
file_read_tool_description = """Reads content from a file.
Use this tool to read files when needed to answer a question or provide information."""
file_read_tool_parameters = [
{"name": "file_path", "type": "str", "description": "The path of the file to read from."}
]
file_read_tool = FileReadTool(file_read_tool_name, file_read_tool_description, file_read_tool_parameters)
###########################################
create_folder_tool_name = "create_folder"
create_folder_tool_description = """Creates a new folder at the specified path.
Use this tool to create folders as requested by the user."""
create_folder_tool_parameters = [
    {"name": "folder_path", "type": "str", "description": "The path of the folder to create."}
]
create_folder_tool = CreateFolderTool(create_folder_tool_name, create_folder_tool_description, create_folder_tool_parameters)
###########################################
file_copy_tool_name = "file_copy"
file_copy_tool_description = """Copies a file or folder from a source path to a destination path.
Use this tool to copy files or folders to a different location."""
file_copy_tool_parameters = [
    {"name": "source_path", "type": "str", "description": "The path of the file or folder to copy."},
    {"name": "destination_path", "type": "str", "description": "The path where the file or folder should be copied to."}
]
file_copy_tool = FileCopyTool(file_copy_tool_name, file_copy_tool_description, file_copy_tool_parameters)
###########################################
miniconda_start_tool_name = "miniconda_start"
miniconda_start_tool_description = """Starts a Miniconda application.
Use this tool to start a Miniconda application by providing the application name."""
miniconda_start_tool_parameters = [
    {"name": "app_name", "type": "str", "description": "The name of the Miniconda application to start."}
]
miniconda_start_tool = MinicondaStartTool(miniconda_start_tool_name, miniconda_start_tool_description, miniconda_start_tool_parameters)
###########################################
start_cmd_tool_name = "start_cmd"
start_cmd_tool_description = """Starts a new Command Prompt (cmd.exe) window.
Use this tool to open a new Command Prompt window for running commands."""
start_cmd_tool_parameters = []
start_cmd_tool = StartCMDTool(start_cmd_tool_name, start_cmd_tool_description, start_cmd_tool_parameters)
###########################################
cmd_interaction_tool_name = "cmd_interaction"
cmd_interaction_tool_description = """Interacts with a Command Prompt (cmd.exe) window by writing commands and reading the output.
Use this tool to execute commands in a Command Prompt window and retrieve the output."""
cmd_interaction_tool_parameters = [
    {"name": "command", "type": "str", "description": "The command to execute in the Command Prompt window."}
]
cmd_interaction_tool = CMDInteractionTool(cmd_interaction_tool_name, cmd_interaction_tool_description, cmd_interaction_tool_parameters)
###########################################
create_audio_file_tool_name = "create_audio_file"
create_audio_file_tool_description = """Creates an audio file (.wav or .mp3) with the specified content.
Use this tool to create audio files as requested by the user."""
create_audio_file_tool_parameters = [
    {"name": "file_path", "type": "str", "description": "The path of the audio file to create."},
    {"name": "content", "type": "str", "description": "The path of the audio content file to use."},
    {"name": "format", "type": "str", "description": "The format of the audio file (default: 'wav')."}
]
create_audio_file_tool = CreateAudioFileTool(create_audio_file_tool_name, create_audio_file_tool_description, create_audio_file_tool_parameters)
###########################################
play_audio_file_tool_name = "play_audio_file"
play_audio_file_tool_description = """Plays an audio file (.wav or .mp3).
Use this tool to play audio files when requested by the user."""
play_audio_file_tool_parameters = [
    {"name": "file_path", "type": "str", "description": "The path of the audio file to play."}
]
play_audio_file_tool = PlayAudioFileTool(play_audio_file_tool_name, play_audio_file_tool_description, play_audio_file_tool_parameters)
###########################################

#3. Assign Tools and Ask Claude
tool_user = ToolUser([addition_tool, search_tool, file_write_tool, file_read_tool, create_folder_tool, file_copy_tool, start_cmd_tool, miniconda_start_tool, cmd_interaction_tool, create_audio_file_tool, play_audio_file_tool])


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
    print("- File Copy: python app.py copy file example.txt to backup/example.txt")
    print("- start miniconda: python app.py start the Miniconda application 'jupyter'")
    print("- python app.py run the command 'dir' in a new Command Prompt window")
    print("- python app.py create an audio file named example.wav with content from audio_content.wav")    
    print("- python app.py play the audio file example.wav")