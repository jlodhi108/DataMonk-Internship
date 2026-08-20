"""Small demo script used for the GitHub Super-Linter project."""

from typing import List


def hello(name: str) -> None:
    """Print a greeting for the given name."""
    print(f"hello {name}")


def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def build_report(name: str, age: int, items: List[str]) -> str:
    """Build a short summary report for a person and their items."""
    return (
        f"Report for {name} who is {age} years old "
        f"and owns these items: {items} end of report"
    )


def main() -> None:
    """Run the demo script."""
    hello("world")
    total = add(5, 3)
    print(total)
    print(build_report("Alice", 30, ["book", "pen", "laptop"]))


if __name__ == "__main__":
    main()
