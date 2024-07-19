import sys
import modelinfo

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print(f'usage: {sys.argv[0]} [binary config input] [lua config output]')
		sys.exit()

	with open(sys.argv[1], 'rb') as f: a = modelinfo.ModelInfo.from_file(f)
	with open(sys.argv[2], 'w') as f:
		f.write(f'''\
do
	emu:model({{
		model_name = "{a.model_name}",
		interface_image_path = "{a.interface_path}",
		rom_path = "{a.rom_path}",
		flash_path = "{a.flash_path}",
		hardware_id = {a.hardware_id},
		real_hardware = {int(a.real_hardware)},
		csr_mask = 0x{a.csr_mask:x},
		pd_value = 0x{a.pd_value:02x},
''')
		b = max([len(k) for k in a.sprites])
		f.write('\n'.join([f'\t\t{k}{" "*(b-len(k))} = {{{v.src.x:4}, {v.src.y:4}, {v.src.w:4}, {v.src.h:4}, {v.dest.x:3}, {v.dest.y:3}}}, ' for k, v in a.sprites.items()]))
		f.write('\n\t\tbutton_map = {\n')
		for j in range(len(a.buttons)):
			i = a.buttons[j]
			f.write(f'\t\t\t{{{i.rect.x:4}, {i.rect.y:4}, {i.rect.w:2}, {i.rect.h:2}, 0x{i.kiko:02x}, "{i.keyname}"}}{", " if j < len(a.buttons)-1 else ""}\n')
		f.write('\t\t}\n\t})\nend\n')
