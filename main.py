from ts3qpy import *
q = QueryClient('cygame.ru')
q.connect()
q.use(1)
# print q.users()
print q.userCount()
