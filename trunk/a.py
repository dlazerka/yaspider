User defined functions:
func_doc	The function's documentation string, or None if unavailable	Writable
__doc__	Another way of spelling func_doc	Writable
func_name	The function's name	Writable
__name__	Another way of spelling func_name	Writable
__module__	The name of the module the function was defined in, or None if unavailable.	Writable
func_defaults	A tuple containing default argument values for those arguments that have defaults, or None if no arguments have a default value	Writable
func_code	The code object representing the compiled function body.	Writable
func_globals	A reference to the dictionary that holds the function's global variables -- the global namespace of the module in which the function was defined.	Read-only
func_dict	The namespace supporting arbitrary function attributes.	Writable
func_closure	None or a tuple of cells that contain bindings for the function's free variables.	Read-only


Modules:
dir(module)
__dict__
__name__
__doc__
__file__