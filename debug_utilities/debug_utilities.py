# 1. Basic syntax checker
def check_syntax(code_snippet: str) -> bool:
    """
    Returns True if the Python code snippet has valid syntax, False otherwise.
    """
    import ast
    try:
        ast.parse(code_snippet)
        return True
    except SyntaxError:
        return False


# 2. Run code snippet safely
def run_code_safely(code_snippet: str) -> tuple:
    """
    Executes the code snippet in a sandboxed environment using exec().
    Returns a tuple of (output, error).
    """
    import io
    import sys

    # Capture output
    backup_stdout = sys.stdout
    backup_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        exec(code_snippet, {})
        output = sys.stdout.getvalue()
        error = sys.stderr.getvalue()
    except Exception as e:
        output = ""
        error = str(e)

    # Restore original stdout/stderr
    sys.stdout = backup_stdout
    sys.stderr = backup_stderr

    return (output, error)


# 3. List global variables
def list_globals(code_snippet: str) -> list:
    """
    Executes the code and returns a list of all global variables defined.
    """
    local_env = {}
    exec(code_snippet, local_env)
    return [k for k in local_env.keys() if not k.startswith('__')]


# 4. Trace function calls
def trace_calls(code_snippet: str) -> list:
    """
    Uses sys.settrace to keep track of function calls in the code snippet.
    Returns a list of called function names.
    """
    import sys

    calls = []

    def trace_func(frame, event, arg):
        if event == "call":
            calls.append(frame.f_code.co_name)
        return trace_func

    original_trace = sys.gettrace()
    sys.settrace(trace_func)
    try:
        exec(code_snippet, {})
    except Exception:
        pass
    finally:
        sys.settrace(original_trace)

    return calls


# 5. Check for common mistakes
def check_common_mistakes(code_snippet: str) -> list:
    """
    Checks for a few common Python pitfalls (like indentation errors, print usage).
    Returns a list of warnings, if any.
    """
    warnings = []
    lines = code_snippet.splitlines()

    for index, line in enumerate(lines, start=1):
        # Check indentation
        if line.startswith(" ") and (len(line) - len(line.lstrip(" "))) % 4 != 0:
            warnings.append(f"Line {index}: Odd indentation spacing.")
        # Check Python 3 print usage
        if "print " in line and "(" not in line and ")" not in line:
            warnings.append(f"Line {index}: Consider using print() instead of print statement.")
    return warnings


# 6. Measure execution time
def measure_execution_time(code_snippet: str) -> float:
    """
    Returns the execution time (in seconds) for the code snippet.
    """
    import time
    start_time = time.time()
    try:
        exec(code_snippet, {})
    except:
        pass
    return time.time() - start_time


# 7. Collect exception details
def collect_exceptions(code_snippet: str) -> list:
    """
    Runs the code and gathers any exceptions that occur.
    Returns a list of exception messages.
    """
    exceptions = []
    lines = code_snippet.split('\n')
    for i, line in enumerate(lines, start=1):
        try:
            exec(line, {})
        except Exception as e:
            exceptions.append(f"Line {i}: {e}")
    return exceptions


# 8. Search for TODO or FIX comments
def find_todos(code_snippet: str) -> list:
    """
    Returns lines with 'TODO' or 'FIX' comments.
    """
    results = []
    lines = code_snippet.splitlines()
    for index, line in enumerate(lines, start=1):
        if 'TODO' in line or 'FIX' in line:
            results.append(f"Line {index}: {line.strip()}")
    return results


# 9. Variable usage logger
def log_variable_usage(code_snippet: str) -> dict:
    """
    Tracks variable assignment and usage within the code. Returns a dictionary
    mapping variable names to the count of how many times they are referenced.
    """
    import re
    variable_pattern = re.compile(r"\b([a-zA-Z_]\w*)\b")
    usage = {}

    for line in code_snippet.splitlines():
        matches = variable_pattern.findall(line)
        for m in matches:
            if m not in usage:
                usage[m] = 0
            usage[m] += 1
    return usage


# 10. Capture and analyze logs
def capture_logs(code_snippet: str, log_level="DEBUG") -> str:
    """
    Configures logging at the specified level, runs the code snippet,
    and returns any captured log messages.
    """
    import io
    import sys
    import logging

    # Prepare logger
    logger = logging.getLogger("debug_logger")
    logger.setLevel(getattr(logging, log_level.upper(), logging.DEBUG))
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    logger.addHandler(handler)

    # Inject logger into code snippet globals
    globals_dict = {"logger": logger}

    # Execute code
    try:
        exec(code_snippet, globals_dict)
    except Exception as e:
        logger.error(f"Error while running code: {e}")

    logger.removeHandler(handler)
    return log_stream.getvalue()
