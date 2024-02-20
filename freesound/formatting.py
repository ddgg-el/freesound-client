from typing import Any


def headline(text: str, centered: bool = False) -> str:
	if not centered:
		return f"{text}\n{'-' * len(text)}"
	else:
		print("".center(50,"="))
		return f" {text} ".center(50, "o")
	
def separator(length:int=20)->None:
	print(f"{'-'*length}")

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def warning(text:str)->None:
	print(colors.YELLOW + text + colors.END)

def ask(text:str)->str:
	return input(colors.BLUE + text + colors.END)

def error(text:str)->None:
	print(colors.RED + text + colors.END)

def info(text:str)->None:
	print(colors.GREEN + text + colors.END)

def log(key:Any,value:Any):
	print(colors.GREEN + str(key) + colors.END + ":" + str(value))