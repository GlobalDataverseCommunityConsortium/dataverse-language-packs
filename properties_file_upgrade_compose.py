#!/usr/bin/python3

import argparse
import re

# PARSE INPUT ARGUMENTS
parser = argparse.ArgumentParser(description='Compose/update properties file based on a base file and an auxiliary file.')
parser.add_argument('base_file', type=str, help='source file used as the base for comparison/composition')
parser.add_argument('aux_file', type=str, help='file used to complement base file')
parser.add_argument('-o', '--out_file', type=str, help='custom file containing result from comparison/composition tasks. Defaults to a file named "out.properties" being created in current directory', default='./out.properties')
parser.add_argument('-enc', '--encoding', type=str, help='encoding to use in file operations (read/write). Defaults to "utf-8".', default='utf-8', choices=['utf-8', 'latin-1'])
exc_group = parser.add_mutually_exclusive_group()
exc_group.add_argument('-c', '--compose', action='store_true', help='merge data from aux file into base file. Returns data from base file with the values from base file entries replaced with the corresponding data from aux file (DEFAULT)')
exc_group.add_argument('-d', '--diff', action='store_true', help='return count and list of keys present in base file that are missing in aux file')
exc_group2 = parser.add_mutually_exclusive_group()
exc_group2.add_argument('-l', '--line', type=int, help='start properties file processing starting on a specific line')
exc_group2.add_argument('-k', '--key', type=str, help='start properties file processing starting on a specific key')
args = parser.parse_args()

def get_keys_in_file(fp):
    k_list = []
    for line in fp:
        #print(line)
        if re.match(r'^(.+)=.*$', line):
            k_list.append(re.match(r'^(.+)=.*$', line).groups()[0])
    return k_list

def get_file_diffs(bf, af):
    with open(af, "r", encoding=args.encoding) as aux_fp:
        with open(bf, "r", encoding=args.encoding) as base_fp:
            diff_k_list = []
            base_k_list = get_keys_in_file(base_fp)
            aux_k_list = get_keys_in_file(aux_fp)

            for k in base_k_list:
                if not (k in aux_k_list):
                    diff_k_list.append(k)
    return diff_k_list

if args.diff:
    diff_k_list = get_file_diffs(args.base_file, args.aux_file)

    if len(diff_k_list) > 0:
        if args.out_file:
            with open(args.out_file, "w", encoding=args.encoding) as out_fp:
                for k in diff_k_list:
                    out_fp.write(k)
        else:
            print(f'--> Found {len(diff_k_list)} keys from base file that do not exist in aux file:\n{diff_k_list}')
    else:
        print(f'--> Base file and Aux file have the same keys!')
    exit(0)

if args.line:
    #print(f'LINE ARG DETECTED! VALUE: {args.line}')
    line_count = 0
    with open(args.base_file, "r", encoding=args.encoding) as base_fp:
        for l in base_fp:
            line_count  += 1
    #print(f'FILE LINE COUNT: {line_count}')

    if args.line <= line_count:
        c = 1
        with open(args.base_file, "r", encoding=args.encoding) as base_fp:
            with open(args.aux_file, "r", encoding=args.encoding) as aux_fp:
                with open(args.out_file, "w", encoding=args.encoding) as out_fp:
                    for line in base_fp:
                        if c >= args.line:
                            # GET KEY AND VALUE IN LINE
                            m_base = re.match(r'^(.+)=(.*)$', line)
                            #print(m_base)
                            if m_base:
                                #print(m_base.groups())
                                # CHECK IF KEY EXISTS IN AUX FILE
                                for l in aux_fp:
                                    m_aux = re.match(r'^(.+)=(.*)$', l)
                                    if m_aux:
                                        #print (m_aux.groups())
                                        if m_base.groups()[0] == m_aux.groups()[0]:
                                            m_found = True
                                            break
                                    #else:
                                    #    print("Unable to get key/value from aux properties file!!! Empty line?")

                                aux_fp.seek(0)

                                if m_found and (len(m_aux.groups()[1]) > 0):
                                    m_found = False
                                    out_fp.write("{}={}\n".format(m_aux.groups()[0], m_aux.groups()[1]))
                                    print(f"-->> {m_aux.groups()[0]}: Match found in aux file! Value updated!")
                                else:
                                    out_fp.write("{}={}\n".format(m_base.groups()[0], m_base.groups()[1]))
                                    print(f"-->> {m_aux.groups()[0]}: NO match found in aux file! Keeping data from base file!")
                            else:
                                #print("Unable to get key/value from base properties file!!! Empty line?")
                                out_fp.write(line)
                        c += 1
        exit(0)
    else:
        print(f"--> ERROR! Value for '--line' argument ({args.line}) exceeds number of lines available in base file ({line_count})")
        exit(1)

if args.key:
    #print(f'KEY ARG DETECTED! VALUE: {args.key}')
    with open(args.base_file, "r", encoding=args.encoding) as base_fp:
        base_k_list = get_keys_in_file(base_fp)

    if args.key in base_k_list:
        with open(args.base_file, "r", encoding=args.encoding) as base_fp:
            with open(args.aux_file, "r", encoding=args.encoding) as aux_fp:
                with open(args.out_file, "w", encoding=args.encoding) as out_fp:
                    proceed = False

                    for line in base_fp:
                        # GET KEY AND VALUE IN LINE
                        m_base = re.match(r'^(.+)=(.*)$', line)
                        #print(m_base)
                        if m_base:
                            #print(m_base.groups())
                            if (m_base.groups()[0] == args.key) and not proceed:
                                proceed = True
                                #print("PROCEED FROM NOW ON!!")

                            if proceed:
                                # CHECK IF KEY EXISTS IN AUX FILE
                                for l in aux_fp:
                                    m_aux = re.match(r'^(.+)=(.*)$', l)
                                    if m_aux:
                                        #print (m_aux.groups())
                                        if m_base.groups()[0] == m_aux.groups()[0]:
                                            m_found = True
                                            break
                                    #else:
                                    #    print("Unable to get key/value from aux properties file!!!")

                                aux_fp.seek(0)

                                if m_found and (len(m_aux.groups()[1]) > 0):
                                    m_found = False
                                    out_fp.write("{}={}\n".format(m_aux.groups()[0], m_aux.groups()[1]))
                                    print(f"-->> {m_aux.groups()[0]}: Match found in aux file! Value updated!")
                                else:
                                    out_fp.write("{}={}\n".format(m_base.groups()[0], m_base.groups()[1]))
                                    print(f"-->> {m_aux.groups()[0]}: NO match found in aux file! Keeping data from base file!")
                            #else:
                            #    print("DO NOTHING")
                        else:
                            #print("Unable to get key/value from base properties file!!! Empty line?")
                            out_fp.write(line)
        exit(0)
    else:
        print(f"--> ERROR! Value for '--key' argument ({args.key}) does not exist in base file")
        exit(1)

if args.out_file:
    m_found = False
    with open(args.aux_file, "r", encoding=args.encoding) as aux_fp:
        with open(args.base_file, "r", encoding=args.encoding) as base_fp:
            with open(args.out_file, "w", encoding=args.encoding) as out_fp:
                for line in base_fp:
                    # GET KEY AND VALUE IN LINE
                    m_base = re.match(r'^(.+)=(.*)$', line)
                    #print(m_base)
                    if m_base:
                        print(m_base.groups())
                        # CHECK IF KEY EXISTS IN AUX FILE
                        for l in aux_fp:
                            m_aux = re.match(r'^(.+)=(.*)$', l)
                            if m_aux:
                                #print (m_aux.groups())
                                if m_base.groups()[0] == m_aux.groups()[0]:
                                    m_found = True
                                    break
                            else:
                                print("Unable to get key/value from aux properties file!!! Empty line?")

                        aux_fp.seek(0)

                        if m_found and (len(m_aux.groups()[1]) > 0):
                            m_found = False
                            out_fp.write("{}={}\n".format(m_aux.groups()[0], m_aux.groups()[1]))
                            print(f"-->> {m_aux.groups()[0]}: Match found in aux file! Value updated!")
                        else:
                            out_fp.write("{}={}\n".format(m_base.groups()[0], m_base.groups()[1]))
                            print(f"-->> {m_aux.groups()[0]}: NO match found in aux file! Keeping data from base file!")
                    else:
                        print("Unable to get key/value from base properties file!!! Empty line?")
                        out_fp.write(line)

print("FINISHED: ")
# NOT NEEDED WHEN USING WITH TO HANDLE FILE OBJECTS
#src_fp.close()
#target_fp.close()
#out_fp.close()
