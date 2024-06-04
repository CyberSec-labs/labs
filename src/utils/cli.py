import os
from pathlib import Path


class settings:
    destination: Path = Path.home() / "Desktop" / "generated_labs"
    input: str = None
    
class CLIHandler:
    @staticmethod
    def handle(args: list[str]):
        """Parse optional arguments from command line.
        """

        cmdArgs = args[1::]
        cmdArgLen = len(cmdArgs)

        # parsing all our options given in the command line.

        for i in range(0, cmdArgLen, 2):
            flag = cmdArgs[i]
            value = cmdArgs[i + 1]

            if flag == None or value == None:
                continue

            if not flag.startswith("--"):
                print(
                    f"Invalid flag: {flag} with value: {value}\nThis flag/value pair will be ignored."
                )
                continue

            if value.startswith("--"):
                print(
                    f"Invalid value {value} for flag: {flag}.\n Values should not begin with '--'\nThis flag/value pair will be ignored."
                )
                continue

            flagName = flag[2::]
            match flagName:
                case "out":
                    if value == "cwd":
                        settings.destination = Path(os.getcwd())#os.path.dirname(os.path.realpath(__file__))
                    else:
                        settings.destination = Path(value)
                case "in":
                    settings.input = Path(value)
                case _:
                    print(f"Unknown flag: '{flagName}' with value: '{value}'")
        
        return settings 
