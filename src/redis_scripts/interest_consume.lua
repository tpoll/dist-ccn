-- Scripte to add data and consume interest
local interest_name = "i-" .. KEYS[1]
local retv = redis.call('SMEMBERS', interest_name)

-- Create data and consume interest
redis.call('SET', KEYS[1], ARGV[1])
redis.call('DEL', interest_name)

return retv
