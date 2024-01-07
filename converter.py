#!/usr/bin/env python3
"""\
snake_case converter for raylib.h
version 1.0, Jan 5 2024
(MIT license) - @keyle

This is a converter from raylib's traditional CamelCase to lowercase snake_case.
In C, I prefer the old traditional naming style, it fits better with other libraries, as well as mine(s)
also I found it weird to have uint16_t etc. mixed with Vector2 etc. I don't like the mish-mash.
NOTE: this converter is NOT part of the raylib library (https://www.raylib.com/) and is provided "as-is".

Process:
    parses raylib.h in the current folder
    creates macros for all "FunctionName" to "r_function_name"
    creates macros for all "TypeName" to "type_name_t"
    saves the content into raylib_s.h
this approach is non-destructive, so you can copy-paste a raylib examples, they will work
then eventually rewrite it to snake_case and it will work just the same
there is also no cost added at runtime

Usage: 
    put this script in the same folder as "raylib.h" 
    python converter.py # python 3
    if all goes well, you should have an additional file "raylib_s.h"
    #include "raylib_s.h" # instead of "raylib.h" but keep it as it's not a replacement
"""

import re

type_suffix = '_t'
func_prefix = 'r_'
do_not_convert = ['bool']


def convert():
    with open('raylib.h', 'r') as file:
        original_header = file.read()

    processed_header = process_header(original_header)

    with open('raylib_s.h', 'w') as file:
        file.write(processed_header)


def camel_to_snake(name):
    # First, insert an underscore before a group of uppercase letters followed by lowercase (like 'POT' in 'ImageToPOT')
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    # Next, insert an underscore between lowercase letters and following uppercase letters
    name = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)  # Clea_rB_ackground
    # finally insert an underscore between a lowercased and digits, but it must have more after (e.g. 3D)
    name = re.sub(r'([a-z])([0-9][A-Z])', r'\1_\2',
                  name)  # BeginMode3D yes, Vector3 no

    # Finally, convert to lowercase
    return name.lower()


def process_header(file_content):
    new_content = """#ifndef RAYLIB_S_H\n#define RAYLIB_S_H\n\n#include "raylib.h"\n\n"""

    new_content += "// Types\n"

    # types, either :
    #   typedef some ____;
    #   typedef struct ____ {
    typedef_patterns = [
        r'typedef\s+.+\s+(\w+)\s*;', r'typedef\s+struct\s+(\w+)\s*\{'
    ]
    for pattern in typedef_patterns:
        types = re.findall(pattern, file_content)
        for type_name in types:
            if type_name in do_not_convert:
                continue
            snake_type = camel_to_snake(type_name) + type_suffix
            macro = f'#define {snake_type} {type_name}\n'
            new_content += macro

    new_content += "\n// Functions\n"

    # functions
    functions_pattern = re.findall(
        r'(?:RLAPI|extern)\s+(\w+)\s+([A-Z][a-zA-Z0-9]+)\(([\s\S]+?)\);',
        file_content)
    for return_type, func_name, params in functions_pattern:
        snake_func = func_prefix + camel_to_snake(func_name)
        macro = f'#define {snake_func} {func_name}\n'
        new_content += macro

    new_content += """\n#endif // RAYLIB_S_H\n"""

    return new_content


convert()
