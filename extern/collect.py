import subprocess


def run_program(cmd) -> list[float]:
    try:
        # Run the command and capture stdout (text mode)
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=True
        )
        # Split the output on whitespace and convert each part to float
        numbers = [float(num) for num in result.stdout.strip().split()]
        return numbers
    except Exception as e:
        print(f"Error running command {cmd}: {e}")
        return []


def main(
    n: int = 1000,
    commands: dict[str, str] = {
        "C": "gcc ./gcc/rand.c -o ./gcc/rand.out && ./gcc/rand.out",
        "C++": "g++ ./gcc/rand.cpp -o ./gcc/rand.out && ./gcc/rand.out",
        "Rust": "cd ./rust && cargo run --release --",
        "JS": "node rand.js",
        "Java": "javac ./java/Rand.java && java -cp ./java Rand",
        "PHP": "php rand.php",
    },
) -> dict[str, list[float]]:
    results = {}
    for key, cmd in commands.items():
        results[key] = run_program(f"{cmd} {n}")
    return results


if __name__ == "__main__":
    data = main()
    for key, value in data.items():
        print(f"{key}: {len(value)}")
