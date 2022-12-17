#Cod facut de @ανα @Héi si @daniela
import os
import shutil
from pathlib import Path

def createdir(dir_name: str, place_on_disk: str) -> None:
    #creaza un folder *dir_name* in folder-ul *place_in_disk*

    path = os.path.join(place_on_disk,dir_name)
    path_backup = os.path.join(place_on_disk, "BACKUP")
    try:
        os.mkdir(path) # creaza folder
        os.mkdir(path_backup)  # creaza backup pentru folder
    except OSError as e:
        print(e)



def movfile(dir_path: str, new_path: str) -> None:
    #muta un intreg directory (cu tot ce e in el) sau un singur file
    try:
        shutil.move(dir_path, new_path)
    except OSError as e:
        print(e)

def compfiles(file1_path:str, file2_path) -> bool:
    """returneaza valoare boolean True daca file1 == file2 (au aceiasi bytes)
    si False altfel, in cazul in care avem o eroare de permisiune returneaza
    -1"""
    try:
        return Path(file1_path).read_bytes() == Path(file2_path).read_bytes()
    except PermissionError as err:
        print(err)
        return -1

def updatebackup(original_dir_name: str, backup_dir_name: str = "")-> None:
    #...
    pass

def is_dir(file_path: str) -> bool:
    #verifica daca un string reprezinta numele unei file sau a unui folder
    return os.path.isdir(file_path)

def deletedir(dir_path: str) -> None:
    #sterge un folder specificat prin path-ul sau
    files_in_dir = os.listdir(dir_path) #numele tuturor filelor
                                        #si a folderelor dintr-un
                                        #folder *dir_path* salvate
                                        #intr-o lista
    for x in files_in_dir:
        #iteram prin acea lista
        y = os.path.join(dir_path, x)
        if is_dir(y):
            #daca e folder mergem recursiv si stergem ce e prin el
            if dir_path[-1] != '/':
                altdir = y
            else:
                altdir = dir_path + x
            deletedir(altdir)
        else:
            #daca e fila o stergem direct
            if dir_path[-1] != '/':
                filename = y
            else:
                filename = dir_path + x
            os.remove(filename)
    os.rmdir(dir_path)

#if __name__ == "__main__":
    #print(compfiles(r"C:\Users\Alex\Desktop\Coding\PYTHON\FACULTA\PROIECT\New folder", r"C:\Users\Alex\Desktop\Coding\PYTHON\FACULTA\PROIECT\ok2.txt"))
