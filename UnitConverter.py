from converter.skill import run_skill


def main():
    input_str = input("Insert value for converting (ex: meter:2.5): ")

    if ":" not in input_str:
        print("Invalid format. Use unit:value (ex: meter:2.5)")
        return

    unit, value_str = input_str.split(":", 1)
    unit = unit.strip()
    value_str = value_str.strip()

    try:
        value = float(value_str)
    except ValueError:
        print(f"Invalid number: {value_str}")
        return

    if unit not in ("meter", "feet", "yard"):
        print(f"Unknown unit: {unit}")
        return

    unit, value, equivalents = run_skill(f"{unit}:{value}")

    print(f"{value} {unit} = {equivalents['meter']} meter")
    print(f"{value} {unit} = {equivalents['feet']} feet")
    print(f"{value} {unit} = {equivalents['yard']} yard")


if __name__ == "__main__":
    main()
