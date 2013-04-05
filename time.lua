local clock = os.clock
local execute = os.execute

cmd = ''
for _, v in ipairs(arg) do
    cmd = cmd .. v .. ' '
    end

local start = clock()
execute(cmd)
local elapse = clock() - start

print(elapse .. 'secs')