import os
from subprocess import run
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
    ),
)

def run_python_file(working_dir, file_path, args=None):
    try:

        working_dir_abs = os.path.abspath(working_dir)
        target_file = os.path.normpath(
            os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath(
            [working_dir_abs, target_file]) == working_dir_abs
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory.'
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'"{file_path}" is not a Python file'
        command = ["python", target_file]
        if args != None:
            command.extend(args)

        result = run(command, text=True, timeout=30,
                     cwd=working_dir_abs, capture_output=True)
        output_string = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

        if result.returncode != 0:
            output_string += f"Process exited with code {result.returncode}"

        return output_string

    except Exception as e:
        print(f"Error: executing Python file: {e}")
