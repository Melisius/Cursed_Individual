while true; do
	timeout 3600 python bot.py >> bot.output
	sleep 5
done
