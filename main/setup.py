from cx_Freeze import setup, Executable

copyDependentFiles=True
silent = True
includes = ["pygame","random","pygame.gfxdraw", "sys", "datetime"]
setup(name='Independent Test Preperation',
     version = "4.4",
     description = "Программа для подготовки к ЗНО по английскому языку",
     author = "Чернышов Денис",
     options = {
       "build_exe" : {
           "includes": includes,
           "include_files":["pict2.jpg", "definition.txt", "irregular_verbs.txt", "font.otf", "icon.png"]
           },
       },
     executables=[Executable('main.py', targetName = "MAH.exe")],
 )