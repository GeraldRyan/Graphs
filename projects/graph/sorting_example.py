import math
array = ['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']

array.sort(key=lambda s: s[round(len(s)/2)])
for s in array:
  print(s)