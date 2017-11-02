#!/usr/bin/python
import os
import numpy as np
import sys, getopt
import glob

########################################################################
# Count the number of subdirs
########################################################################

def fcount(path, map = {}):
	count = 0
	for f in os.listdir(path):
		child = os.path.join(path, f)
		if os.path.isdir(child):
			child_count = fcount(child, map)
			count += child_count + 1 # unless include self
	map[path] = count

	return count


########################################################################
# Make the Tree
########################################################################


def main(argv):
        inputfile = ''
        outfile = ''
        topdir = ''
        try:
            opts, args = getopt.getopt(argv,"hi:o:d:",["ifile=","ofile=","directory"])
        except getopt.GetoptError:
            print('make_pdf_directory_tree.py -d <topdir> -f <file extensions> -o <outputfile>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('make_pdf_directory_tree.py -d <topdir> -f <file extensions> -o <outputfile>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-o", "--ofile"):
                outfile = arg
            elif opt in ("-d", "--directory"):
                topdir = arg

        print('Directory to parse is %s' % topdir)
        print('Input file is %s' % inputfile)
        print('Output file is %s' % outfile)

        first_dirs = write_dir_tree(topdir)
        make_sub_trees(topdir, first_dirs, outfile)

        return


def make_sub_trees(main_dir, first_dirs, outfile):
    """
    Make directory tree of each subd
    """

    exclude = set(['.git','media'])

    with open(outfile,'w') as z:
        for topdir in first_dirs:

            this_top_dir = os.path.join(main_dir, topdir)
            
            dir_tree_name = os.path.join(os.path.basename(this_top_dir) + 'dirtree.tex')
            
            i = 0
            end_bracket_locations = []
            
            for path,dirs,files in os.walk(this_top_dir, topdown=True):
                dirs[:] = [d for d in dirs if d not in exclude]
                i += 1
		
	        # Get the total # of subdirs
		map = {}
		subdirs = fcount(path,map)
		end_bracket_locations.append(i + subdirs)
		
		section_name = fix_file_string(os.path.basename(this_top_dir))

		z.write('\section{%s}\n' % section_name)
		z.write('\\input{%s}\n' % dir_tree_name)
		with open(dir_tree_name,'w') as g:
	
			write_preamble(g)
			n = 1

			for path,dirs,files in os.walk(this_top_dir, topdown=True):
	
				dirs[:] = [d for d in dirs if d not in exclude]
	
				new_path_string = fix_file_string(path)

				z.write('\subsection{%s}\n' % new_path_string)
	
				cdir = os.path.basename(new_path_string)
	
				g.write('[%s\n' %(cdir))
	
				# Print the files in the current DIR
				for f in files:
					if f.endswith('.py'):
						new_file = fix_file_string(f)
						g.write('[%s, file ]\n' % new_file)
						z.write('\subsubsection{%s}\n' % new_file)
						z.write('\\pythonexternal{%s}\n' % str(os.path.join(path,f)))
					#elif f.endswith('.html'):
						#new_file = fix_file_string(f)
						#g.write('[%s, file ]\n' % new_file)
						#z.write('\subsubsection{%s}\n' % new_file)
						#z.write('\\htmlexternal{%s}\n' % str(os.path.join(path,f)))
					#elif f.endswith('.tex'):
						#new_file = fix_file_string(f)
						#g.write('[%s, file ]\n' % new_file)
						#z.write('\subsubsection{%s}\n' % new_file)
						#z.write('\\pythonexternal{%s}\n' % str(os.path.join(path,f)))
				matches = np.size([i for i,x in enumerate(end_bracket_locations) if x == n])
				for match in xrange(matches):
					g.write(']\n')
				n+=1
	
				g.write(']\n')
			g.write('\\end{forest}')
	
	return


########################################################################
# Write the Figure
########################################################################


def write_dir_tree(main_dir):

	#main_dir = '/hg/ndfom/django'
        print(main_dir)

	i=0
	end_bracket_locations = []

	# exclude any dirs and subdirs/files in these directories
	exclude = set(['.git'])

	##############################################################
	# First loop to determine where to place the brackets
	##############################################################

	for path,dirs,files in os.walk(main_dir, topdown=True):

		# iterate
		i += 1

		# eliminate missing dirs
		dirs[:] = [d for d in dirs if d not in exclude]

		# Get the total # of subdirs
		# CAA ! TODO: Fix this and generalize with exclude
		map = {}
		subdirs = fcount(path,map)

		# create the locations
		end_bracket_locations.append(i + subdirs)

	##############################################################
	# Create the full tree and subdir tree
	# * full tree ignores files for now TODO: fix this
	##############################################################
	
	with open('directory_tree_full.tex','w') as g:

		with open('directory_tree_dirs.tex','w') as k:

			write_preamble(g)
			write_preamble(k)
			n = 1

			for path,dirs,files in os.walk(main_dir):

				dirs[:] = [d for d in dirs if d not in exclude]

				if n == 1:
				    top_dirs = dirs

				new_path_string = fix_file_string(path)

				cdir = os.path.basename(new_path_string)

				g.write('[%s\n' %(cdir))
				k.write('[%s\n' %(cdir))

				# Print the files in the current DIR
				for f in files:
					if f.endswith('.py'):
						new_file = fix_file_string(f)
						g.write('[%s, file ]\n' % new_file)
					elif f.endswith('.html'):
						new_file = fix_file_string(f)
						g.write('[%s, file ]\n' % new_file)
				matches = np.size([i for i,x in enumerate(end_bracket_locations) if x == n])
				for match in xrange(matches):
					g.write(']\n')
					k.write(']\n')
				n+=1

			k.write(']\n')
			#k.write(']\n')

			k.write('\\end{forest}')

		# SHOULDNT NEED THIS< BUT SOMETHING WRONG
		g.write(']\n')
		#g.write(']\n')

		g.write('\\end{forest}')

	return top_dirs


########################################################################
# This fixes the file string for latex purposes.
########################################################################


def fix_file_string(filestring):
	"""
	Fixes it for latex purposes, _ to \_
	"""

	escape_chars = set(['&','%','$','#','_','{','}','~','^','\\'])

	outstring = filestring.replace('_','\_')
	outstring = outstring.replace('#','\#')

	return outstring


def write_preamble_one(g):
	g.write('''\\begin{forest}
  	dir tree,
  	before drawing tree={
    	for tree={
     	 tikz+/.wrap 2 pgfmath args={\\node [anchor=west, font=\\footnotesize, text=red] at (.east) {L:#1; n:#2};}{level()}{n()}
    	}
  	}
	''')

	return


def write_preamble(g):
	g.write('''\\begin{forest}
              for tree={
        font=\\ttfamily,
        grow'=0,
        child anchor=west,
        parent anchor=south,
        anchor=west,
        calign=first,
        inner xsep=7pt,
        edge path={
          \\noexpand\path [draw, \\forestoption{edge}]
          (!u.south west) +(7.5pt,0) |- (.child anchor) pic {folder} \\forestoption{edge label};
        },
        % style for your file node 
        file/.style={edge path={\\noexpand\path [draw, \\forestoption{edge}]
          (!u.south west) +(7.5pt,0) |- (.child anchor) \\forestoption{edge label};},
          inner xsep=2pt,font=\small\\ttfamily
                     },
        before typesetting nodes={
          if n=1
            {insert before={[,phantom]}}
            {}
        },
        fit=band,
        before computing xy={l=15pt},
      }  
	''')

	return


########################################################################
# Run main function if nothing specified
########################################################################

#parser.add_option("-d" "--directory", action="get_base_dir")
	
if __name__ == "__main__":

    main(sys.argv[1:])
