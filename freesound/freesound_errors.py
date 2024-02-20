class AuthorizationError(Exception):
	def __init__(self,message:str) -> None:
		super().__init__(message)

class DataError(Exception):
	def __init__(self,message:str) -> None:
		super().__init__(message)

class FreesoundError(Exception):
	def __init__(self,message:str) -> None:
		super().__init__(message)