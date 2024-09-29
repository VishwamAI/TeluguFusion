import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from integrated_framework import టెన్సర్_సృష్టించు

def పరీక్ష_టెన్సర్_సృష్టించు():
    print("టెన్సర్ సృష్టి పరీక్ష ప్రారంభం...")

    # సాధారణ కేసు పరీక్ష
    try:
        టెన్సర్ = టెన్సర్_సృష్టించు([1, 2, 3, 4], (2, 2))
        print("సాధారణ కేసు పరీక్ష విజయవంతం")
    except Exception as e:
        print(f"సాధారణ కేసు పరీక్ష విఫలమైంది: {e}")

    # తప్పుడు డేటా రకం పరీక్ష
    try:
        టెన్సర్_సృష్టించు("తప్పుడు డేటా", (2, 2))
        print("తప్పుడు డేటా రకం పరీక్ష విఫలమైంది")
    except ValueError as e:
        print(f"తప్పుడు డేటా రకం పరీక్ష విజయవంతం: {e}")

    # తప్పుడు ఆకారం రకం పరీక్ష
    try:
        టెన్సర్_సృష్టించు([1, 2, 3, 4], [2, 2])
        print("తప్పుడు ఆకారం రకం పరీక్ష విఫలమైంది")
    except ValueError as e:
        print(f"తప్పుడు ఆకారం రకం పరీక్ష విజయవంతం: {e}")

    # తప్పుడు పరిమాణం పరీక్ష
    try:
        టెన్సర్_సృష్టించు([1, 2, 3], (2, 2))
        print("తప్పుడు పరిమాణం పరీక్ష విఫలమైంది")
    except ValueError as e:
        print(f"తప్పుడు పరిమాణం పరీక్ష విజయవంతం: {e}")

    print("టెన్సర్ సృష్టి పరీక్ష ముగిసింది.")

if __name__ == "__main__":
    పరీక్ష_టెన్సర్_సృష్టించు()
