#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime, os, shutil, json


class Backup(object):

	def __init__(self):
		current_dir = os.path.dirname(os.path.realpath(__file__))
		config_file = os.path.join(current_dir, 'backupscript.json')
		if not os.path.isfile(config_file):
			print 'Config-File not found. `backupscript.conf` has to be placed in the same directory as `backupscript.py`'
			raise

		with open(config_file, 'r') as config_file_content:
			config_data = json.loads(config_file_content.read())
			config_file_content.close()

		self.db_credentials = config_data['DB_CREDENTIALS']
		self.path_config = config_data['PATH_CONFIG']
		self.gdrive_credentials = config_data['GDRIVE_CREDENTIALS']
		self.gdrive_config_path = self.gdrive_credentials.get('gdrive_config_path', None)

		self.log_file = os.path.join(self.path_config['local_backup_path'], '_completed_backups.log')
		self.do_backup()

	def get_readable_datetime(self):
		return datetime.datetime.now().strftime('%a, %d %b %Y')

	def get_today_folder_name(self):
		return datetime.datetime.now().strftime('%m-%d-%Y')

	def do_backup(self):
		print '--------- START BACKUP: %s ---------' % self.get_readable_datetime()
		todays_folder = os.path.join(self.path_config['local_backup_path'], self.get_today_folder_name())


		"""
		Remove existing and recreate temporary backup dirs.
		"""
		if os.path.exists(todays_folder):
			shutil.rmtree(todays_folder)
		os.mkdir(todays_folder)
		db_backups_path = os.path.join(todays_folder, '_mysql_backup')
		os.mkdir(db_backups_path)


		"""
		Define db-dump command. If no password required, -p argument is not used.
		"""
		dumpcmd = 'mysqldump -h %(host)s -u %(user)s -p%(password)s %(db)s > %(db_backup_file_path)s'
		if self.db_credentials['password'] == '':
			dumpcmd = 'mysqldump -h %(host)s -u %(user)s %(db)s > %(db_backup_file_path)s'

		"""
		Loop through all databases and dump them into the backup folder.
		"""
		for db in self.db_credentials['db_names']:
			execute_dump = dumpcmd % {
				'host': self.db_credentials['host'],
				'user': self.db_credentials['username'],
				'password': self.db_credentials['password'],
				'db': db,
				'db_backup_file_path': '%s/%s.sql' % (db_backups_path, db)
			}
			os.system(execute_dump)
			print 'Dumped DB %s' % db


		"""
		Sync backup-folder to Google Drive
		"""
		sync_command = 'rclone copy %(source_dir)s %(remote_name)s:%(remote_path)s %(gdrive_config)s' % {
			'source_dir': todays_folder,
			'remote_name': self.gdrive_credentials['remote_name'],
			'remote_path': '%s/%s' % (self.gdrive_credentials['remote_path'], self.get_today_folder_name()),
			'gdrive_config': '--config="%s"' % self.gdrive_config_path if self.gdrive_config_path else ''
		}
		os.system(sync_command)
		print 'Folder synced to Google Drive'


		"""
		Delete backup-folder
		"""
		shutil.rmtree(todays_folder)
		self.end_backup()

	def end_backup(self):
		# delete files
		print '\n---------- END BACKUP: %s ----------' % self.get_readable_datetime()


backupInstance = Backup()
