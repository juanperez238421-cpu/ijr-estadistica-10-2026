from pathlib import Path

p = Path(__file__).with_name('statistics10_week5_five_number_summary_workshop_senior.py')
s = p.read_text(encoding='utf-8')

old = '''    def t(self, content, size=28, weight=NORMAL, color=INK, **kwargs):\n        return Text(content, font_size=size, weight=weight, color=color,\n                    line_spacing=0.92, **kwargs)\n'''
new = '''    def t(self, content, size=28, weight=NORMAL, color=INK, **kwargs):\n        line_spacing = kwargs.pop("line_spacing", 0.92)\n        return Text(content, font_size=size, weight=weight, color=color,\n                    line_spacing=line_spacing, **kwargs)\n'''

if 'line_spacing = kwargs.pop("line_spacing", 0.92)' in s:
    raise SystemExit(0)
if old not in s:
    raise SystemExit('Text helper block not found')
p.write_text(s.replace(old, new), encoding='utf-8')
