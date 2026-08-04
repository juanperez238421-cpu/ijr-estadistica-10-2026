#!/usr/bin/env bash
set -euo pipefail
mkdir -p delivery
for spec in \
  '48db4f88fbf8681cc9c0e4f9e5ecec867e3c1dd82e491c395c1752f3716dd489 part_00' \
  'da7ac4653debd634c5844169cc01b8de26645a257f7b3ac98e221850042f2f9a part_01' \
  '2b67bbf03cd3a97d09ba495d109643bf3c3b9d6aa2d6dc843069035c51e0e3f1 part_02' \
  '11d48c7ac1ec329544d983ab6f12c21ee50d41eb64aa25f2f74b5941e61157c8 part_03' \
  'cbd48451171fe787cf45fd3b24df25dbafc7dcb962a80ea70acf58f38cb2fd2f part_04'; do
  set -- $spec
  echo "$1  source_chunks_iqr_problems_v3/$2" | sha256sum -c -
done
cat source_chunks_iqr_problems_v3/part_0{0,1,2,3,4} > source.gz.b64
test "$(wc -c < source.gz.b64)" -eq 12892
echo 'e92eb07cdf97a70d190a3806dc80dbd14135e20e71335a4675ef9afc5955266a  source.gz.b64' | sha256sum -c -
base64 -d source.gz.b64 | gzip -d > statistics10_iqr_graph_construction_problems.py
echo '6be9eec5fa7dcfd4438e7c978b7b9d37bc33841ec1c46b4ba20df6309dcd22d9  statistics10_iqr_graph_construction_problems.py' | sha256sum -c -
python -m py_compile statistics10_iqr_graph_construction_problems.py
grep -q '^class Statistics10IQRGraphConstructionProblems' statistics10_iqr_graph_construction_problems.py
grep -q 'def quartile_tag' statistics10_iqr_graph_construction_problems.py
cp statistics10_iqr_graph_construction_problems.py delivery/
