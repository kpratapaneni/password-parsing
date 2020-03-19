import argparse
import os
import json
import logging

LOG_FILE = "password_parser.log"

def is_file_valid(file_path):
	if(os.path.exists(file_path) and os.path.isfile(file_path)):
		return True
	return False

def read_lines(infile):
	with open(infile) as input_text:
		return [line for line in input_text if line and line.startswith("#") == False]

def parse_to_json(passwd_list, groups_list):
	json_parser = {}
	for passwd_line in passwd_list:
		passwd_line_arr = passwd_line.split(":")
		if(len(passwd_line_arr) < 5):
			continue

		uname = passwd_line_arr[0]
		json_parser[uname] = {'uid': passwd_line_arr[2], 'full_name': passwd_line_arr[4], 'groups': []}
		for group_line in groups_list:
			group_line_arr = group_line.split(":")
			if(len(group_line_arr) >= 4):
				grp_members = group_line_arr[3].rstrip().split(",")
				for grp_member in grp_members:
					if(grp_member == uname):
						json_parser[uname]['groups'].append(group_line_arr[0])

	return json_parser

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--passwd_file", default="/etc/passwd")
	parser.add_argument("--groups_file", default="/etc/groups")

	args = parser.parse_args()
	logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

	if(is_file_valid(args.passwd_file) == False):
		logging.error("Password file is not valid")
	elif(is_file_valid(args.groups_file) == False):
		logging.error("Groups file is not valid")
	else:
		parser_json = parse_to_json(read_lines(args.passwd_file), read_lines(args.groups_file))	
		logging.info(">>> passwd-parser")
		logging.info(json.dumps(parser_json, indent=2))

if __name__=="__main__": 
	main()