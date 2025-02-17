# Generates Binary Data File from an array of random numbers [0 < num < 1]
# Array -> Binary -> Binary File


def convert_to_bin(random_nums: list[float]) -> str:
    return "".join([str(round(num)) for num in random_nums])


def generate_binary_file(path: str, data: list[float]):
    with open(path, "wb") as f:
        bin = convert_to_bin(data)
        f.write(bin.encode("utf-8"))
