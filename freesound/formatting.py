from typing import Any


def headline(text: str, centered: bool = False) -> str:
	if not centered:
		return f"{text}\n{'-' * len(text)}"
	else:
		print("".center(50,"="))
		return f"{text} ".center(50, "o")
	
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

def reduce_list(array:list[float|int]) -> str:
	formatted_list = str(array[:3])[:-1] + ', ... ' + str(array[-1:])[1:]
	return formatted_list

def unpack_features(infos:Any):
		result = ""
		if "lowlevel" in infos:
			for key,value in infos["lowlevel"].items():
				if isinstance(value,dict):
					result += f"\n\t{colors.GREEN}{key}{colors.END}:".expandtabs(2)
					for feat,feat_val in value.items(): # type:ignore
						if isinstance(feat_val, list):
							feat_val = reduce_list(feat_val) # type:ignore
							result += f"\n\t\t{colors.GREEN}{feat}{colors.END}:{feat_val}".expandtabs(2)
						else:
							result += f"\n\t\t{colors.GREEN}{feat}{colors.END}:{feat_val}".expandtabs(2)
				else:
					result += f"\n\t{colors.GREEN}{key}{colors.END}:{value}".expandtabs(2)
				
		return result