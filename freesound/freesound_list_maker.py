from typing import List

class ListMaker:
	def __init__(self, fields:List[str]):
		self._param_array:list[str] = [str(field) for field in fields]
	
	def _make_coma_separated(self) -> str:
		return ",".join(self._param_array)

	def _make_list(self) -> str:
		return " ".join(self._param_array)
	
if __name__ == "__main__":
	lm = ListMaker(["ciao","papà","ciao","mamma"])
	print(lm)