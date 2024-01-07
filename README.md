### snake_case converter for raylib.h

version 1.0, Jan 5 2024

(MIT license) - @keyle

This is a converter from raylib's traditional CamelCase to lowercase snake_case.
In C, I prefer the old traditional naming style, it fits better with other libraries, as well as mine(s)
also I found it weird to have uint16_t etc. mixed with Vector2 etc. I don't like the mish-mash.

NOTE: this converter is NOT part of the raylib library (https://www.raylib.com/) and is provided "as-is".

Process:

- parses raylib.h in the current folder
- creates macros for all "_FunctionName_" to "**_r_function_name_**"
- creates macros for all "_TypeName_" to "**_type_name_t_**"
- saves the content into _raylib_s.h_

this approach is non-destructive, so you can copy-paste a raylib examples, they will work
then eventually rewrite it to snake_case and it will work just the same
there is also no cost added at runtime

Usage: 

- put this script in the same folder as "raylib.h" 
- python converter.py # python 3
- if all goes well, you should have an additional file "raylib_s.h"
- #include "raylib_s.h" # instead of "raylib.h" but keep it as it's not a replacement
