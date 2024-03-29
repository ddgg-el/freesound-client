class ListMaker:
	def __init__(self, fields:list[str]):
		self._param_array:list[str] = [str(field) for field in fields]
	
	def _make_coma_separated(self) -> str:
		return ",".join(self._param_array)

	def _make_list(self) -> str:
		return " ".join(self._param_array)