#!/usr/bin/env python

import sys, os, signal
import subprocess
import argparse
import json
from pathlib import Path

class ConfigFileError(Exception):
	pass

def signal_handler(signal, frame):
	print("Ctrl+C signal received from keyboard. Closing. \n")
	sys.exit(0)

def main():
	signal.signal(signal.SIGINT, signal_handler)

	rasp_root = Path("~/Rasp-Sync")
	home_dir = Path.home()
	config_dir = home_dir.joinpath(".config/rasp-sync")
	config_list = config_dir.joinpath("dir-list")
	config_file = config_dir.joinpath("config")

	def sync(dir_from, dir_to, compress, delete, test, update):
		args = ["-avr"]

		if compress:
			args.append("-z")

		if update:
			args.append("-u")

		if test:
			args.append("--list-only")

		if delete:
			args.append("--delete")

		subprocess.call(["rsync"] + args + ["--progress", "--files-from=" + str(config_list), dir_from, dir_to])
		

	parser = argparse.ArgumentParser(description="Sync files with raspberry Pi")	

	parser.add_argument("action", type=str, choices=["push", "pull"])
	parser.add_argument("--rasp-user", "-ru", type=str)
	parser.add_argument("--rasp-ip", "-ip", type=str)
	parser.add_argument("--update", "-u", action="store_true", default=False)
	parser.add_argument("--test", "-t", action="store_true", default=False)
	parser.add_argument("--compress", "-c", action="store_true", default=True)
	parser.add_argument("--delete", "-d", action="store_true", default=True)

	args = parser.parse_args()

	pushing = True if args.action == "push" else False

	if not home_dir.joinpath(".config").exists():
		print("Creating ~/.config directory...")
		os.mkdir(home_dir.joinpath(".config"))

	if not config_dir.exists():
		print("Creating rasp-sync directory in ~/.config...")
		os.mkdir(config_dir)

	if not config_file.exists() or not config_list.exists():
		print("Creating config files...")

	if not config_list.exists():
		with open(config_list, 'w') as f:
			pass

	if not config_file.exists():
		with open(config_file, 'w') as f:
			json_file = json.loads("{\n}\n")

			if args.rasp_user:
				json_file["rasp-user"] = args.rasp_user

			if args.rasp_ip:
				json_file["rasp-ip"] = args.rasp_ip

			json_file["update"] = args.update
			json_file["compress"] = args.compress
			json_file["delete"] = args.delete
			json_file["test"] = args.test

			f.write(json.dumps(json_file))

	if os.stat(config_list).st_size == 0:
		print("Empty dir-list file. Please specify directories to sync.")
		return

	with open(config_file, 'r') as f:
		json_file = json.load(f)

		user_cond = args.rasp_user or "rasp-user" in json_file
		ip_cond = args.rasp_ip or "rasp-ip" in json_file

		if not user_cond or not ip_cond:
			print("Missing ip or user. Please specify it in the config file.")
			return

		# Use command line value if provided else use config file
		rasp_user = args.rasp_user if args.rasp_user else json_file["rasp-user"]
		rasp_ip = args.rasp_ip if args.rasp_ip else json_file["rasp-ip"]

		if not "update" in json_file or not "compress" in json_file or not "delete" in json_file or not "test" in json_file:
			raise ConfigFileError("Missing config arguments in file")

		# Use command line value if provided else use config file
		compress = False if not args.compress else json_file["compress"]
		delete = False if not args.delete else json_file["delete"]
		test = True if args.test else json_file["test"]
		update = True if args.update else json_file["update"]


	rasp_server = rasp_user + "@" + rasp_ip + ":" + str(rasp_root)

	dir_from = str(home_dir) if pushing else rasp_server
	dir_to = rasp_server if pushing else str(home_dir)

	sync(dir_from, dir_to, compress, delete, test, update)


if __name__ == '__main__':
	main()