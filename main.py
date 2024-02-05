


indent_size = 4 #setting

def code_level(string):
    lines = string.splitlines()
    data_buffer = []
    for line in lines:
        if line.strip():
            striped_line = line.lstrip()
            indentation = len(line)-len(striped_line)
            level = indentation/indent_size
            data = (striped_line,level)
            data_buffer.append(data)
    return data_buffer
        
def decode_level(string_array):
    string = ""
    
    for code,level in string_array:
        for nspace in range(int(level)*indent_size):
            string+=" "
        string +=code+"\n"
    return string     

# Example usage:
python_code = """
import numpy
import test
array = numpy.zeros(10)
print(array)
"""

processed = code_level(python_code)

print(decode_level(processed))
exec(decode_level(processed))
test.example_function()
