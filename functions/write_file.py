import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)

def write_file(working_dir, file_path, content):
    try:

        working_dir_abs = os.path.abspath(working_dir)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath(
            [working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory."
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        if os.path.isdir(target_file):
            return f"Error: Cannot write to '{file_path}' as it is a directory"

        with open(target_file, 'w') as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print("Error:", e)
