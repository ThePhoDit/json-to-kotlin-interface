import json
import argparse

def generate_kotlin_interface(json_data, class_name):
    kotlin_code = f"interface {class_name} {{\n"

    for key, value in json_data.items():
        if isinstance(value, dict):
            data_class_name = class_name + key.capitalize()
            if is_kotlin_reserved_word(key):
                kotlin_code += f"    val `{key}`: {data_class_name}\n"
            else:
                kotlin_code += f"    val {key}: {data_class_name}\n"
        else:
            kotlin_type = get_kotlin_type(value)
            if is_kotlin_reserved_word(key):
                kotlin_code += f"    val `{key}`: {kotlin_type}\n"
            else:
                kotlin_code += f"    val {key}: {kotlin_type}\n"

    kotlin_code += "}"

    return kotlin_code

def generate_kotlin_data_class(json_data, class_name):
    kotlin_code = f"data class {class_name}(\n"

    for key, value in json_data.items():
        if isinstance(value, dict):
            data_class_name = class_name + key.capitalize()
            if is_kotlin_reserved_word(key):
                kotlin_code += f"    val `{key}`: {data_class_name},\n"
            else:
                kotlin_code += f"    val {key}: {data_class_name},\n"
        else:
            kotlin_type = get_kotlin_type(value)
            if is_kotlin_reserved_word(key):
                kotlin_code += f"    val `{key}`: {kotlin_type},\n"
            else:
                kotlin_code += f"    val {key}: {kotlin_type},\n"

    kotlin_code += ")"

    return kotlin_code

def generate_linked_data_classes(json_data, class_name):
    kotlin_code = ""

    for key, value in json_data.items():
        if isinstance(value, dict):
            data_class_name = class_name + key.capitalize()
            kotlin_code += generate_kotlin_data_class(value, data_class_name) + "\n\n"
            kotlin_code += generate_linked_data_classes(value, data_class_name)

    return kotlin_code

def is_kotlin_reserved_word(word):
    # List of Kotlin reserved words
    reserved_words = [
        "as", "as?", "break", "class", "continue", "do", "else", "false",
        "for", "fun", "if", "in", "interface", "is", "null", "object",
        "package", "return", "super", "this", "throw", "true", "try", "typealias",
        "typeof", "val", "var", "when", "while"
    ]
    return word in reserved_words


def get_kotlin_type(value):
    if isinstance(value, str):
        return "String"
    elif isinstance(value, int):
        return "Int"
    elif isinstance(value, float):
        return "Double"
    elif isinstance(value, bool):
        return "Boolean"
    elif isinstance(value, list):
        if value and all(isinstance(x, str) for x in value):
            return "List<String>"
        elif value and all(isinstance(x, int) for x in value):
            return "List<Int>"
        elif value and all(isinstance(x, float) for x in value):
            return "List<Double>"
        elif value and all(isinstance(x, bool) for x in value):
            return "List<Boolean>"
        else:
            return "List<Any>"
    else:
        return "Any"

# Usage
def main(args):
    parser = argparse.ArgumentParser(description="Convert JSON to Kotlin interface")

    parser.add_argument("-f", "--file", help="JSON file path.", required=True, type=str)
    parser.add_argument("-o", "--output", help="Kotlin file path where contents should be dumped. If the file exists it overrides its contents", type=str, default="Interface.kt")

    parsed_args = parser.parse_args(args)

    json_file_path = parsed_args.file
    output_file_path = parsed_args.output
    class_name = output_file_path.split("/")[-1].split(".")[0]

    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    # Generate Kotlin interface
    kotlin_interface = generate_kotlin_interface(json_data, class_name)

    # Generate Kotlin data class
    kotlin_data_class = generate_kotlin_data_class(json_data, class_name)

    # Generate Kotlin linked data classes
    kotlin_linked_data_classes = generate_linked_data_classes(json_data, class_name)

    # Output the results to a file. It does override the file contents.
    with open(output_file_path, "w") as kotlin_file:
        kotlin_file.write(kotlin_interface  + "\n\n" + kotlin_linked_data_classes)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
