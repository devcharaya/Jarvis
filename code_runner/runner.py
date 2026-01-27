import subprocess
import os
from datetime import datetime

def is_safe_path(base, path):
    return os.path.realpath(path).startswith(os.path.realpath(base))


BASE_SANDBOX = os.path.join(os.getcwd(), "jarvis_sandbox")
PYTHON_DIR = os.path.join(BASE_SANDBOX, "python")
CPP_DIR = os.path.join(BASE_SANDBOX, "cpp")

LOG_FILE = "execution_log.txt"


def log_execution(action, filename):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {action} | {filename}\n")


def run_python(filename):
    if not filename.endswith(".py"):
        return "Only Python (.py) files are allowed."

    file_path = os.path.join(PYTHON_DIR, filename)
    if not is_safe_path(PYTHON_DIR, file_path):
     return "Access denied."


    if not os.path.exists(file_path):
        return "Python file not found in sandbox."

    log_execution("PYTHON_RUN", filename)

    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout if result.stdout else result.stderr
        return output if output.strip() else "Program executed successfully with no output."

    except subprocess.TimeoutExpired:
        return "Execution timed out."
    except Exception as e:
        return str(e)


def run_cpp(filename):
    if not filename.endswith(".cpp"):
        return "Only C++ (.cpp) files are allowed."
    

    source_path = os.path.join(CPP_DIR, filename)
    if not is_safe_path(CPP_DIR, source_path):
     return "Access denied."

    exe_path = os.path.join(CPP_DIR, "program.exe")

    if not os.path.exists(source_path):
        return "C++ file not found in sandbox."

    log_execution("CPP_RUN", filename)

    try:
        compile_result = subprocess.run(
            ["g++", source_path, "-o", exe_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        if compile_result.returncode != 0:
            return compile_result.stderr

        run_result = subprocess.run(
            [exe_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = run_result.stdout if run_result.stdout else run_result.stderr
        return output if output.strip() else "Program executed successfully with no output."

    except subprocess.TimeoutExpired:
        return "Execution timed out."
    except Exception as e:
        return str(e)
