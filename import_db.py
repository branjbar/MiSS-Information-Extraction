import re


def init():
	global list_of_first_names  # around 10,200 first names are stored here
	list_of_first_names = []
	with open("db/first_name.txt", 'r') as f:
		for line in f:
			row = line.split(',')

			# make sure that words are not a combination of two capital letters
			if not re.match('"[A-Z][a-z]+[A-Z][a-z]+"', row[0]):
				word = row[0].replace('"', '').replace("'", '').strip()
				if len(word) > 1:
					list_of_first_names.append(word)

	global list_of_last_names_multiple  # around 10,200 first names are stored here
	list_of_last_names_multiple = []
	with open("db/last_name_multiple.txt", 'r') as f:
		for line in f:
			row = line.split(',')

			word = row[0].replace('"', '').replace("'", '').strip()
			list_of_last_names_multiple.append(word)

	global list_of_mean_names
	list_of_mean_names = []
	with open("db/mean_names.txt", 'r') as f:
		for line in f:
			word = line.replace('"', '').replace("'", '').strip()
			list_of_mean_names.append(word)

	global misleading_starting_names
	misleading_starting_names = []
	with open("db/misleading_starting_words.txt", 'r') as f:
		for line in f:
			word = line.replace('"', '').replace("'", '').strip()
			misleading_starting_names.append(word)

if __name__ == "__main__":
	init()
	print 'First Names', len(list_of_first_names)
	print 'Last Names', len(list_of_last_names_multiple)
	print 'Nasty Names', len(list_of_mean_names)
