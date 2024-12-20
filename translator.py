import argparse
import yaml
import re
import sys


class ConfigTranslator:
    def __init__(self):
        self.constants = {}

    def parse_and_translate(self, yaml_content):
        try:
            data = yaml.safe_load(yaml_content)
            # Обработка и сохранение констант
            self._extract_constants(data)
            # Трансляция оставшихся значений
            return self._translate(data)
        except yaml.YAMLError as e:
            raise ValueError(f"YAML parsing error: {e}")

    def _extract_constants(self, data):
        """Извлекает и сохраняет константы."""
        for key, value in data.items():
            if isinstance(value, int) or isinstance(value, list):
                self._validate_name(key)
                self.constants[key] = value

    def _translate(self, data, depth=0):
        if isinstance(data, dict):
            result = []
            for key, value in data.items():
                self._validate_name(key)
                if isinstance(value, (int, list)):
                    result.append(f"{key} <- {self._translate(value, depth + 1)};")
                elif isinstance(value, str):
                    if value.startswith("@"):
                        const_value = self._evaluate_constant(value)
                        result.append(f"{key} <- {const_value};")
                    else:
                        result.append(f"{key} <- \"{value}\";")  # Строки берутся в кавычки
                elif isinstance(value, dict):
                    result.append(f"{key} <- {{\n{self._translate(value, depth + 1)}\n}};")
                else:
                    raise ValueError(f"Invalid value for key '{key}': {value}")
            return "\n".join(result)
        elif isinstance(data, list):
            return f"array({', '.join(map(str, data))})"
        elif isinstance(data, int):
            return str(data)
        else:
            raise ValueError(f"Unsupported type: {type(data)}")

    def _validate_name(self, name):
        if not re.match(r"^[A-Z]+$", name):
            raise ValueError(f"Invalid name '{name}'. Names must consist of uppercase letters only.")

    def _evaluate_constant(self, value):
        const_name = value[1:]  # Remove '@'
        if const_name not in self.constants:
            raise ValueError(f"Undefined constant reference: {value}")
        return self.constants[const_name]


def main():
    parser = argparse.ArgumentParser(description="Educational configuration language translator")
    parser.add_argument("input_file", help="Path to input YAML file")
    args = parser.parse_args()

    translator = ConfigTranslator()

    try:
        with open(args.input_file, "r") as file:
            yaml_content = file.read()

        translated_content = translator.parse_and_translate(yaml_content)
        print(translated_content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
