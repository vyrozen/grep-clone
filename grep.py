from genericpath import isfile
import os, sys, re, fnmatch
import string

def scan_file(path_to_folder):
    real_path = []
    for (root,dir,files) in os.walk(path_to_folder):
        for name in files:
            real_path.append(os.path.join(root, name))
    return (real_path)

def print_line(path_to_file, string_search, argument_length, options):
    with open (path_to_file, 'r') as j:
        data = j.readlines()
        l_num = 1
        for line in data:
            if argument_length == 4:
                if options == "-w" : #Case sensitive, whole words
                    if bool(re.search(rf"\b{string_search}\b", line)):
                        new_line = line.strip()
                        print(f"{path_to_file : <40} line {l_num : <8}{new_line[:40]}")
                if options == "-i" : #Case insensitive, substring
                    if bool(re.search(rf"{string_search}", line, re.IGNORECASE)):
                        new_line = line.strip()
                        print(f"{path_to_file : <40} line {l_num : <8}{new_line[:40]}")
            if argument_length == 3:
                if bool(re.search(rf"{string_search}", line)):
                    new_line = line.strip()
                    print(f"{path_to_file : <40} line {l_num : <8}{new_line[:40]}")
            l_num += 1

def error():
    print("Argumen program tidak benar")
    sys.exit()

opt = ['-i', '-w'] # Membatasi agar hanya terdapat 2 opsi
# usage : python grep.py [options (-w / -i)] [string pattern yang dicari] [nama file / direktori]
# print(f"Arguments : {str(sys.argv[1:])}") #Hilangkan tanda "#" untuk melihat argument yang digunakan

try :
    if len(sys.argv) == 4 :
        path = sys.argv[3]
        s_search = sys.argv[2]
        options = sys.argv[1]
        if not options in opt : error()
    else :
        path = sys.argv[2]
        s_search = sys.argv[1]
        options = None

except IndexError : error()
if len(sys.argv) > 4 : error()
else :
    isExists = os.path.exists(path)
    if isExists == False :
        print(f"Path {path} tidak ditemukan") #Jika File/Folder tidak ada
    else :
        if "*" in s_search: #Uji wildcard (*)
            ls_wildcards=[]
            for pos,char in enumerate(s_search):
                if(char == "*"):
                    ls_wildcards.append(pos)
            if len(ls_wildcards) > 1 : 
                error()
            else:
                s_search = s_search.replace("*",".+")      
        if os.path.isfile(path) == False : #Uji apakah path di argumen merupakan sebuah folder atau file
            list_file = scan_file(path) #Jika path merupakan folder
            for i in range (len(list_file)):
                print_line(list_file[i], s_search, len(sys.argv), options)
        else :
            print_line(path, s_search, len(sys.argv), options) #Jika path merupakan sebuah file
