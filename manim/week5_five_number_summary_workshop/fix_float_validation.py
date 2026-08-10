from pathlib import Path

p = Path(__file__).with_name('statistics10_week5_five_number_summary_workshop_senior.py')
s = p.read_text(encoding='utf-8')

# Idempotent compatibility patch: if the robust validation is already present,
# leave the source unchanged. Otherwise replace the original exact-float block.
if 'def close_tuple(actual, expected, tol=1e-9):' in s:
    raise SystemExit(0)

old = '''    def _validate(self):\n        assert self.r1.five == (5.0, 7.5, 11.0, 17.0, 20.0)\n        assert self.r2.five == (2.0, 7.0, 12.0, 18.0, 24.0)\n        assert self.r3.five == (3.0, 4.0, 7.0, 9.0, 12.0)\n        assert self.r4.five == (1.2, 1.5, 1.95, 2.5, 2.9)\n        assert self.r8.five == (-2.0, 1.0, 5.0, 9.0, 12.0)\n        assert self.ra.five == (4.0, 8.0, 12.0, 17.0, 21.0)\n        assert self.rb.five == (3.0, 7.0, 12.0, 18.0, 22.0)\n        assert self.ra.q2 == self.rb.q2 == 12\n        assert self.ra.iqr == 9 and self.rb.iqr == 11\n'''
new = '''    def _validate(self):\n        def close_tuple(actual, expected, tol=1e-9):\n            return len(actual) == len(expected) and all(abs(a-b) < tol for a, b in zip(actual, expected))\n\n        assert close_tuple(self.r1.five, (5.0, 7.5, 11.0, 17.0, 20.0))\n        assert close_tuple(self.r2.five, (2.0, 7.0, 12.0, 18.0, 24.0))\n        assert close_tuple(self.r3.five, (3.0, 4.0, 7.0, 9.0, 12.0))\n        assert close_tuple(self.r4.five, (1.2, 1.5, 1.95, 2.5, 2.9))\n        assert close_tuple(self.r8.five, (-2.0, 1.0, 5.0, 9.0, 12.0))\n        assert close_tuple(self.ra.five, (4.0, 8.0, 12.0, 17.0, 21.0))\n        assert close_tuple(self.rb.five, (3.0, 7.0, 12.0, 18.0, 22.0))\n        assert abs(self.ra.q2 - 12) < 1e-9 and abs(self.rb.q2 - 12) < 1e-9\n        assert abs(self.ra.iqr - 9) < 1e-9 and abs(self.rb.iqr - 11) < 1e-9\n'''
if old not in s:
    raise SystemExit('validation block not found')
p.write_text(s.replace(old, new), encoding='utf-8')
