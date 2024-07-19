import copy

def read_std_string(f):
	str_length = int.from_bytes(f.read(8), 'little')
	return f.read(str_length)

class SDL_Rect:
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	@staticmethod
	def from_file(f):
		x = int.from_bytes(f.read(4), 'little')
		y = int.from_bytes(f.read(4), 'little')
		w = int.from_bytes(f.read(4), 'little')
		h = int.from_bytes(f.read(4), 'little')
		return SDL_Rect(x, y, w, h)

	def __str__(self): return f'{self.__class__.__name__}({", ".join(k+"="+repr(v) for k, v in vars(self).items())})'
	def __repr__(self): return self.__str__()

class SpriteInfo:
	def __init__(self, src, dest):
		self.src = src
		self.dest = dest
		if src.w != dest.w or src.h != dest.h: raise ValueError('source and destination width and/or height does not match')

	@staticmethod
	def from_file(f):
		src = SDL_Rect.from_file(f)
		dest = SDL_Rect.from_file(f)
		return SpriteInfo(src, dest)

	def __str__(self): return f'{self.__class__.__name__}({", ".join(k+"="+repr(v) for k, v in vars(self).items())})'
	def __repr__(self): return self.__str__()

class ColourInfo:
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b

	@staticmethod
	def from_file(f):
		r = int.from_bytes(f.read(4), 'little')
		g = int.from_bytes(f.read(4), 'little')
		b = int.from_bytes(f.read(4), 'little')
		return ColourInfo(r, g, b)

	def __str__(self): return f'{self.__class__.__name__}({", ".join(k+"="+repr(v) for k, v in vars(self).items())})'
	def __repr__(self): return self.__str__()

class Button:
	def __init__(self, rect, kiko, keyname):
		self.rect = rect
		self.kiko = kiko
		self.keyname = keyname

	@staticmethod
	def from_file(f):
		rect = SDL_Rect.from_file(f)
		kiko = int.from_bytes(f.read(4), 'little')
		keyname = read_std_string(f).decode()
		return Button(rect, kiko, keyname)

	def __str__(self): return f'{self.__class__.__name__}({", ".join(k+"="+repr(v) for k, v in vars(self).items())})'
	def __repr__(self): return self.__str__()

class ModelInfo:
	def __init__(self, csr_mask = 2, hardware_id = 3, real_hardware = True, pd_value = 0, buttons = [], sprites = {}, ink_color = None, interface_path = '', model_name = '', rom_path = '', flash_path = ''):
		self.csr_mask = csr_mask
		self.hardware_id = hardware_id
		self.real_hardware = real_hardware
		self.pd_value = pd_value
		self.buttons = copy.deepcopy(buttons)
		self.sprites = copy.deepcopy(sprites)
		self.ink_color = ink_color
		self.interface_path = interface_path
		self.model_name = model_name
		self.rom_path = rom_path
		self.flash_path = flash_path

	@staticmethod
	def from_file(f):
		string = read_std_string(f).decode('gb2312')
		if string != '\n\nGenshin Configuration file v48\n\n原神配置文件v48\n\n': raise RuntimeError('Binary config file is not Genshin configuration file v48')

		csr_mask = int.from_bytes(f.read(2), 'little')
		hardware_id = int.from_bytes(f.read(2), 'little')
		real_hardware = bool(f.read(1)[0])
		pd_value = f.read(1)[0]

		len_buttons = int.from_bytes(f.read(8), 'little')
		buttons = [Button.from_file(f) for i in range(len_buttons)]

		len_sprites = int.from_bytes(f.read(8), 'little')
		sprites = {read_std_string(f).decode(): SpriteInfo.from_file(f) for i in range(len_sprites)}

		ink_color = ColourInfo.from_file(f)
		interface_path = read_std_string(f).decode()
		model_name = read_std_string(f).decode()
		rom_path = read_std_string(f).decode()
		flash_path = read_std_string(f).decode()

		return ModelInfo(csr_mask, hardware_id, real_hardware, pd_value, buttons, sprites, ink_color, interface_path, model_name, rom_path, flash_path)

	def __str__(self): return f'{self.__class__.__name__}({", ".join(k+"="+repr(v) for k, v in vars(self).items())})'
	def __repr__(self): return self.__str__()
