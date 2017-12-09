#!/usr/bin/python
#
# Author: Matt Pichelmayer
# Hopefully this isn't a waste of time.
# Created this as a complement to Robert J. Hansen's (https://github.com/rjhansen) NSRL server and NSRL lookup client.  
# The intent is to: 
# 	1) Add flexibility and interoperability with whitelisting tools.   
# 	2) Be modular; this script can be ran as a server, ran as an imported module or ran locally.
#	  3) Interoperate with the nsrllookup client.

try:
	import argparse
	import pandas as pd # Panda... Panda, Panda, PANDA!
	import os.path
	import re
except:
	print "Missing Required Module(s)" #Expand this to detect pandas.__version__

class nsrl_store():

	def __init__(self, nsrl_file, hdfs_store_path):
		self.nsrl_file = nsrl_file
		self.hdfs_store_path = hdfs_store_path
		names = ["sha1","md5","crc32","FileName","FileSize","ProductCode","OpSystemCode","SpecialCode"] 	#Re-name columns
		nsrl_import = pd.read_csv(nsrl_file, sep=",", header=None, skiprows=0, names=names, dtype=object)	#Import the file
		nsrl_import_convert = nsrl_import.convert_objects()													#Convert to storable objects
		nsrl_import_convert.to_hdf(hdfs_store_path,'hashdata', mode='w',format='table',data_columns=True)
		del nsrl_import																						#Clean mem since store is created
																											#Research for in-mem instance/Calc mem reqs?

	def detect_hash_type(self, hash_string):
		print self.hash_string
		md5regex = re.compile("([a-fA-F\d]{32})")
		sha1regex = re.compile("([a-fA-F\d]{40})")
		if re.match(md5regex,self.hash_string):
			result = 1
		elif re.match(sha1regex,self.hash_string):
			result = 2
		else:
			result = 3
		return result

	def sha1_lookup(self, sha1hash):
		self.sha1hash = sha1hash
		file_name =  pd.read_hdf(self.hdfs_store_path,'hashdata', where="sha1=sha1hash")
		for i in file_name["FileName"]:
			return "%s %s" % (str(sha1hash), str(i))
		
	def md5_lookup(self, md5hash):
		self.md5hash = md5hash
		file_name =  pd.read_hdf(self.hdfs_store_path,'hashdata', where='md5=md5hash')
		for i in file_name["FileName"]:
			return "%s %s" % (str(md5hash), str(i))

	def file_query(self, file_name):
		hash_names = pd.read_hdf(self.hdfs_store_path,'hashdata', where='FileName=file_name')
		print hash_names["md5"], hash_names["sha1"]

	def hash_query(self,hash_string):
		self.hash_string = hash_string
		hash_type = self.detect_hash_type(hash_string)
		if hash_type == 1:
			response = self.md5_lookup(hash_string)
		elif hash_type == 2:
			response = self.sha1_lookup(hash_string)
		else: response = None
		return response

	#This function cleans the NSRL csv of multiple lines for the sake of reducing the size of the database created.
	#Check for multiple sha1/md5 hashes, keep initial line, remove the rest.
	#Not done...pffft
	def clean_import_file(nsrl_file):
		with open(nsrl_file,'r') as f:
			parse_line = f.readlines()

if __name__ == "__main__":
  # Need to work out the logic for args below.
  # If file or store only fed??
  # In-mem only?
  # Line options up with nsrl options
	parser = argparse.ArgumentParser(description="NSRL Server Project")
	parser.add_argument("-f","--file", dest="nsrl_filename", required=True, help="NSRL source file with hashes")
	parser.add_argument("-s","--store", dest="store_filename", required=False, help="HD5 database store")
	parser.add_argument("-u","--unknown", required=False, help="List unknown files")
	parser.add_argument("-k","--known", required=False, help="List known files")
	args = parser.parse_args()
	nsrl_file = args.nsrl_filename
	try:
		hdfs_store_path = args.store_filename
	except:
    # Clean this shit up
		ask_hdfs = str(raw_input("""Since you did not specify an HDFS Storage, one will be written to path: /usr/share/store.h5
		Do you want to confinue?[Y/n] """)).lower().strip()
		if not ask_hdfs or ask_hdfs == "y" or ask_hdfs == "yes":
			hdfs_store_path = "/usr/share/store.h5"
		else:
			sys.exit()
	if not os.path.exists(nsrl_file):
		parser.error("NSRL File %s not found." % nsrl_file)
		sys.exit()
	build_store(nsrl_file,hdfs_store_path)
	sha1hash = raw_input("Enter SHA1 hash: ")
	sha1_query(hdfs_store_path,sha1hash)

