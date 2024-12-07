def get_list_from_file(filepath, var_name):
    namespace = {}
    with open(filepath, "r") as file:
        code = file.read()
    
    exec(code, namespace)
    
    if var_name in namespace:
        return namespace[var_name]
    else:
        raise NameError(f"'{var_name}' is not defined in {filepath}")
