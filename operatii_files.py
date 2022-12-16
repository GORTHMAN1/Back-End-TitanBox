import os
import shutil

def createdir(dir_name: str, place_on_disk: str) -> None:
    #creaza un folder *dir_name* in folder-ul *place_in_disk*

    path = os.path.join(place_on_disk,dir_name)
    path_backup = os.path.join(place_on_disk, "BACKUP")
    try:
        os.mkdir(path) # creaza folder
        os.mkdir(path_backup)  # creaza backup pentru folder
    except OSError as e:
        print(e)




#muta un intreg directory (cu tot ce e in el) sau un singur file
def movfile(dir_path: str, new_path: str) -> None:
    try:
        shutil.move(dir_path, new_path)
    except OSError as e:
        print(e)

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

createdir("Shiii","S:/TestFisier")
