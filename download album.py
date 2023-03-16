import flet
import os
import re
import time
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)


def main(page: Page):
    def btn_click(e):
        def base(e):
            page.clean()
            main(page)
        url = album.value
        
        verif = re.search(r"https://open.spotify.com/album/*", url)
        print("voici alb val : "+str(album.value))
        if album.value == "":
            
            album.error_text = "Please, enter an URL"
    

        if directory_path.value == None:
            directory_path.value == "Choose a path !"
            directory_path.update()
            print("dir")
            #page.update()
            print("dirl")

        #if directory_path.value != None and directory_path.value != "Choose a path !" and directory_path.value != "Choose a path !":
        if directory_path.value not in [None, "Choose a path !", ""] :
            print("voici : "+str(directory_path.value))
            page.clean()
            page.add(flet.Text(f"The album is downloading, please wait..."))
            #os.chdir(fr"{directory_path.value}")
            alb = f"spotdl {album.value}"
            time.sleep(0.5)
            output = os.popen(alb).read()
            page.clean()
            locate_quote = output.index('"')
            locate_tiret = output.index("-")
            artist = output[locate_quote+1:locate_tiret-1]
            ouput = output.split("\n")

            song_tab = []
            for elem in ouput:
                elem = elem[locate_tiret+2:]
                try:
                    locate_quote = elem.index('"')
                except:
                    pass
                elem = elem[:locate_quote]
                song_tab.append(elem)

            song ="\n\t\t\t".join(song_tab)
            page.add(flet.Text(f"The album of {artist} has been downloaded."))
            page.add(flet.Text(f"The songs are :\n\t\t\t{song}"))
            page.add(flet.ElevatedButton("Download a new album", on_click=base))

    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else ""
        directory_path.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()

    # hide all dialogs in overlay
    t = flet.Text()
    page.overlay.extend([ get_directory_dialog])
    album = flet.TextField(label="URL de l'album")
    button_next = flet.ElevatedButton("download", on_click=btn_click)
    page.add(album,
        Row(
            [
                ElevatedButton(
                    "Open directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: get_directory_dialog.get_directory_path(),
                  
                ),
                directory_path,
            ]
        ),
        button_next,t
    )



flet.app(target=main)

