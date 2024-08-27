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
	supported_versions = (49, 50)
	supported_versions2 = (51,)

	def __init__(self, version,
				csr_mask = 2, hardware_id = 3, real_hardware = True, pd_value = 0, buttons = [], sprites = {}, ink_color = None, interface_path = '', model_name = '', rom_path = '', flash_path = '',
				enable_new_screen = False, is_sample_rom = False, legacy_ko = False,
				u16_mode = False, LARGE_model = True, ml620_mirroring = False,
		):
		self.version = version
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
		self.enable_new_screen = enable_new_screen
		self.is_sample_rom = is_sample_rom
		self.legacy_ko = legacy_ko
		self.u16_mode = u16_mode
		self.LARGE_model = LARGE_model
		self.ml620_mirroring = ml620_mirroring

	@staticmethod
	def from_file(f):
		string = read_std_string(f)
		version = None
		try:
			tmp = string.decode('gb2312')
			if tmp == f'\n\nGenshin Configuration file v{v}\n\n原神配置文件{v}\n\n': version = v
		except UnicodeDecodeError: pass
		try:
			string = string.decode('utf-8')
			for v in ModelInfo.supported_versions:
				if string == f'\n\nGenshin Configuration file v{v}\n\n原神配置文件v{v}\n\n': version = v
			for v in ModelInfo.supported_versions2:
				if string == f'\n\nnx-U16/U8 Emulator Configuration file v{v}\n\n模拟器配置文件v{v}\n\ntệp cấu hình giả lập v{v}\n\n': version = v
		except UnicodeDecodeError: raise RuntimeError('Invalid binary config file')

		if version is None: raise RuntimeError('Invalid binary config file')

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

		enable_new_screen = False
		is_sample_rom = False
		legacy_ko = False
		u16_mode = False
		LARGE_model = True
		ml620_mirroring = False

		if version >= 49:
			enable_new_screen = bool(f.read(1)[0])
			is_sample_rom = bool(f.read(1)[0])

		if version >= 50: legacy_ko = bool(f.read(1)[0])

		if version >= 51:
			u16_mode = bool(f.read(1)[0])
			LARGE_model = bool(f.read(1)[0])
			ml620_mirroring = bool(f.read(1)[0])

		return ModelInfo(
			version,
			csr_mask, hardware_id, real_hardware, pd_value, buttons, sprites, ink_color, interface_path, model_name, rom_path, flash_path,
			enable_new_screen, is_sample_rom, legacy_ko,
			u16_mode, LARGE_model, ml620_mirroring
			)

	def __str__(self): return f'{self.__class__.__name__}({", ".join(k+"="+repr(v) for k, v in vars(self).items())})'
	def __repr__(self): return self.__str__()
