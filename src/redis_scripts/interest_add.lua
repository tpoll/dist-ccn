--Script to add interests
if redis.call('EXISTS', KEYS[1]) == 1 then
	redis.call('SADD', KEYS[1], ARGV[1])
	return 1
else
	redis.call('SADD', KEYS[1], ARGV[1])
	return 0
end
