from pathlib import Path

p = Path(__file__).with_name('statistics10_week5_five_number_summary_workshop_senior.py')
s = p.read_text(encoding='utf-8')

old_def = '    def data_cards(self, values, y=Y_DATA, max_width=13.2, show_indices=True):'
new_def = '    def make_data_cards(self, values, y=Y_DATA, max_width=13.2, show_indices=True):'

if old_def not in s and new_def not in s:
    raise SystemExit('data_cards helper definition not found')

s = s.replace(old_def, new_def)
s = s.replace('self.data_cards(', 'self.make_data_cards(')

p.write_text(s, encoding='utf-8')
