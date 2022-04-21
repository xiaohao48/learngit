# import re
#
# s = 'hello python'
# pattern = 'hell'
# v = re.match(pattern, s)
# print(v)
# print(v.group())
# print(v.span())

# import re
#
# s = 'hello Python!'
# m = re.match('hello python', s, re.I)
# if m is not None:
#     print('匹配成功结果是：', m.group())
# else:
#     print('匹配失败')

import re

print('----.的使用-----')
pattern = '.'
s = 'a'
v = re.match(pattern, s)
print(v)
