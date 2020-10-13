# read the file into a list of lines
def file_to_array(name):
	with open(name,'r') as f:
	    lines = f.read().split("\n")
	return lines


def get_position_in_file(array_lines):
	word = '    ' # dummy word. you take it from input

	# iterate over lines, and print out line numbers which contain
	# the word of interest.
	for i,line in enumerate(array_lines):
		if word in line: # or word in line.split() to search for full words
			print("Word \"{}\" found in line {}".format(word, i+1))



name='asd.asd'
lines=file_to_array(name)

def get_identation():
	with open("asd.asd",'r') as f:
	    lines = f.read()
	print(lines)

print(lines)
print("Number of lines is {}".format(len(lines)))
get_position_in_file(lines)

# get_identation()

# fp = open("file")
# for i, line in enumerate(fp):
#     if i == 2:
#     	print(line)

class CodeBlock():
    def __init__(self, head, block):
        self.head = head
        self.block = block
    def __str__(self, indent=""):
        result = indent + self.head + ":\n"
        indent += "    "
        for block in self.block:
            if isinstance(block, CodeBlock):
                result += block.__str__(indent)
            else:
                result += indent + block + "\n"
        return result
ifblock = CodeBlock('if x>0', ['print x', 'print "Finished."'])
block = CodeBlock('def print_success(x)', [ifblock, 'print "Def finished"'])
print (block)