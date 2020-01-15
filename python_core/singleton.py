class Singleton(object):
	_instance = None  # Keep instance reference

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = object.__new__(cls, *args, **kwargs)
		return cls._instance



class SingletonType(type):
	def __call__(cls):
		if getattr(cls, '__instance__', None) is None:
			instance = cls.__new__(cls)
			instance.__init__()
			cls.__instance__ = instance
		return cls.__instance__

