import os
import io
import json
import shutil
import uvicorn
import argparse
import warnings
import webbrowser
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from jinja2 import Environment, PackageLoader

def is_valid_json(json_object)->bool:
    """
    Check if the given JSON object is in the desired format.
    This function takes a JSON object and verifies whether it adheres to the desired JSON format.

    Parameters:
    json_object: The JSON object to be validated.

    Returns:
    bool: True if the JSON object is in the desired format; False otherwise.
    """
    try:
        desired_format = {
            "contractName":str,
            "abi":list,
            "networks":dict
        }
        # Check the structure and data types
        for key, data_type in desired_format.items():
            if key not in json_object:
                print(f"Key '{key}' is missing in the JSON object.")
                return(False)
            if not isinstance(json_object[key], data_type):
                print(f"Key '{key}' should be of type '{data_type.__name__}'.")
                return(False)
        return(True)
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"JSON validation error: {str(e)}")
        return(False)
def has_json_files(directory_path):
    """
    Check if a directory contains any JSON files.

    Parameters:
    directory_path (str): The path to the directory to be checked.

    Returns:
    bool: True if the directory contains JSON files, False otherwise.
    """
    # Get the list of files in the specified directory
    file_list = os.listdir(directory_path)

    # Check if any file has a JSON extension
    for file_name in file_list:
        if file_name.endswith('.json'):
            return True

    return False

def read_json_files(directory):
    """
    Read and load JSON files from the specified directory.
    This function reads all the JSON files from the given directory and loads their contents into a list of JSON objects.
    Each JSON object is represented as a Python dictionary.

    Parameters:
    directory (str): The path to the directory containing the JSON files.

    Returns:
    list: A list of JSON objects, where each object is represented as a Python dictionary.
    """
    try:
        json_data = []
        if not has_json_files(directory):
            print(f"No JSON files found in the directory '{directory}'")
        for filename in os.listdir(directory):
            if filename.endswith('.json') and os.path.isfile(os.path.join(directory, filename)):
                with open(os.path.join(directory, filename), 'r') as file:
                    jsonData=json.load(file)
                    if not is_valid_json(jsonData):
                        print(f"Skipped '{filename}' as it contains invalid JSON data.")
                        continue
                    else:
                        json_data.append(jsonData)
        return json_data
        
    except Exception as e:
        raise RuntimeError("Failed reading JSON files.", str(e))

def generate_ui_files(output_directory,rendered_template):
    """
    Copy all files from the 'public' directory to the specified output directory.
    Create index.html

    Parameters:
    output_directory (str): The path to the output directory where the files will be copied.
    rendered_template (str): The rendered template that should be written into an html file

    Returns:
    None
    """
    # Get the path of the package directory
    package_directory = os.path.dirname(__file__)

    # Get the path of the 'public' directory
    public_directory = os.path.join(package_directory, 'public')

    # Create the output directory if it doesn't exist
    output_directory=output_directory+"/public"
    os.makedirs(output_directory, exist_ok=True)
    path_without_public = output_directory.replace('/public', '')

    # Copy all files from 'public' directory to the output directory
    for filename in os.listdir(public_directory):
        src_file = os.path.join(public_directory, filename)
        dst_file = os.path.join(output_directory, filename)
        shutil.copy(src_file, dst_file)
    # Create  the HTML file with the rendered template content
    with open(f'{path_without_public}/index.html', 'w') as file:
        file.write(rendered_template)
    

def parse_args():
    parser = argparse.ArgumentParser(description='Convert contract ABI to Interactive GUI')
    parser.add_argument('--contract', type=str, help='Path to the JSON file or directory')
    parser.add_argument('--output', type=str, help='Path to the output folder')
    parser.add_argument('--serve', action='store_true', help='Serve Live webserver with generated UI')
    return parser.parse_args()

def main():
    args = parse_args()
    if args.contract:
        if os.path.isdir(args.contract):
            json_data = read_json_files(args.contract)
        elif os.path.isfile(args.contract):
            with open(args.contract, 'r') as file:
                json_data = [json.load(file)]
        else:
            print(f"Invalid path: {args.contract}")
            json_data = []
    else:
        json_data = read_json_files('.')
    
    
    if args.output:
        output_dir=args.output
    else:
        output_dir="."

    # Convert the JSON data to JSON-formatted strings
    json_data_str = json.dumps(json_data,indent=4,ensure_ascii=False)

    # Create a Jinja2 Environment with the PackageLoader
    env = Environment(loader=PackageLoader('py_contract_ui', 'template'))
    # Load the Jinja template
    template = env.get_template('template.j2')

    rendered_template = template.render(json_data=json_data_str)

    if args.serve:
        # Define the FastAPI app and the route to serve the template
        app = FastAPI()
        package_directory = os.path.dirname(__file__)
        # Get the path of the 'public' directory
        public_directory = os.path.join(package_directory, 'public')
        app.mount("/public", StaticFiles(directory=public_directory), name="public")
        @app.get("/", response_class=HTMLResponse)
        def read_item():
            return rendered_template
        # Start the uvicorn server programmatically
        uvicorn.run(app, host="0.0.0.0", port=8000)

    generate_ui_files(output_dir,rendered_template)


if __name__ == '__main__':
    main()





    
