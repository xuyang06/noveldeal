from crontab import CronTab

if __name__ == '__main__':
	#tab = CronTab(user='yangxu',fake_tab='True')
	tab = CronTab('yangxu')
	cmd = 'python test.py'
	#cron_job = tab.new(command = cmd, comment='main command')
	cron_job = tab.new(command = cmd)
	cron_job.minutes.every(1)
	cron_job.enable()
	print 'done'
	#cron_job.hour.every(3)
	#tab.write()
	#print tab.render()
