#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from pytube import YouTube
import pytube
import tkinter_root as tr
from PIL import Image, ImageTk
import urllib.request
import io
import os


class Messages():
    def __init__(self, misc: tk.Tk):
        '''
        INICIALIZADOR:
        Se inicializa la clase Messages.

        :param tkinter misc: El root principal de la ventana en Tkinter.
        '''
        self.misc = misc

    def advice_choose_location(self):
        '''
        FUNCIÓN:
        Mensaje de aviso de elegir una dirección.
        '''
        messagebox.showinfo('Advertencia', ('Debe elegir una dirección'
                                            ' donde guardar su video.'))

    def advice_nonexistent_location(self):
        '''
        FUNCIÓN:
        Mensaje de aviso si una dirección no existe.
        '''
        messagebox.showinfo('Advertencia', ('La dirección no se ha '
                                            'encontrado,'
                                            'intente otra dirección.'))

    def successful_download(self):
        '''
        FUNCIÓN:
        Mensaje de aviso de descarga completada.
        '''
        messagebox.showinfo('Descarga Completada',
                            'Su descarga ha sido exitosa.')

    def no_audio_download(self):
        '''
        FUNCIÓN:
        Mensaje de aviso de descarga completada, pero con posible
        error de audio.
        '''
        messagebox.showinfo('Descarga Completada',
                            'La resolución pudo haber afectado el audio, '
                            'se recomienda elegir otra resolución.')

    def error_download(self):
        '''
        FUNCIÓN:
        Mensaje de aviso de descarga no exitosa (Si el video es muy largo
        puede dar problemas con la descarga).
        '''
        messagebox.showinfo('Advertencia',
                            'Hubo un problema con su descarga, intente '
                            'de nuevo más tarde.')

    def advice_chose_type(self):
        '''
        FUNCIÓN:
        Mensaje de aviso para elegir un tipo de formato general.
        '''
        messagebox.showinfo('Advertencia', 'Debe elegir un formato de video.')

    def advice_chose_resolution(self):
        '''
        FUNCIÓN:
        Mensaje de aviso para elegir una resolución.
        '''
        messagebox.showinfo('Advertencia',
                            'Debe elegir una resolución.')

    def advice_chose_file_type(self):
        '''
        FUNCIÓN:
        Mensaje de aviso para elegir un formato de archivo.
        '''
        messagebox.showinfo('Advertencia',
                            'Debe eligir un formato de archivo.')

    def advice_nonexistent_link(self):
        '''
        FUNCIÓN:
        Mensaje de aviso para corregir el link.
        '''
        messagebox.showinfo('Advertencia', ('Ha ocurrido un error, '
                                            'verifique que puso bien su '
                                            'link.'))


class Functions():
    def __init__(self, misc: tk.Tk):
        '''
        INICIALIZADOR:
        Se inicializa la clase Functions.

        :param tkinter misc: El root principal de la ventana en Tkinter.
        '''
        # Nombre del video / archivo
        # por defecto, este se encontrará vacío.
        self.file_name = ''
        # Nombre de la dirección, por defecto
        # este se encontrará vacío.
        self.location = ''
        # Nombre del tipo de formato (Video/Audio)
        # por defecto, este se encontrará vacío.
        self.type = ''
        # Nombre de la resolución, por defecto
        # este se encontrará vacío.
        self.resolution = ''
        # Nombre del tipo de archivo, por defecto
        # este se encontrará vacío.
        self.file_type = ''
        # Se debe guardar la root.
        self.misc = misc
        # Se debe crear un objeto de tipo "YouTube", por defecto
        # este será el valor de NOne.
        self.video = None
        # Se crea un notificador de mensajes con la ayuda de la clase Messages.
        self.notifier = Messages(misc)

    def start_download(self, entry: tk.Entry):
        '''
        FUNCIÓN:
        Se pide el link de un video de Youtube y se convierte en un
        objeto de tipo "Youtube". Se borra la pantalla del inicio y se crea una
        totalmente nueva.

        :param tkinter entry: El valor del link/enlace
        del video de YouTube.
        '''
        # Se obtiene el valor del link en formato string.
        get_link = str(entry.get())
        # Se verifica si el video existe.
        my_video = self.check_video_exists(get_link)
        # Si no se retorna False entonces, se puede proceder.
        if my_video is not False:
            # Se obtienen las resoluciones disponibles para el video.
            resolutions = self.get_resolutions(my_video)
            # Se inserta la calidad automática.
            resolutions.insert(0, 'Auto Quality')

            # Se crea una lista donde se almacenan todos los "widgets"
            # de la aplicación.
            wlist = self.misc.winfo_children()
            # Se vacía toda la ventana para luego poder insertar cosas nuevas.
            # Para ello, se debe vaciar la lista de los widgets.
            for widge in wlist:
                widge.destroy()

            # Se obtiene el link del thumbnail del video de YouTube.
            thumbnail_link = my_video.thumbnail_url
            # Se obtiene la imagen del video de youtube mediante
            # su link de YouTube.
            my_thumbnail = self.get_thumbnail(thumbnail_link)
            # Se despliega en la ventana la imagen del video solicitado.
            th_picture = tk.Label(self.misc, image=my_thumbnail)
            th_picture.image = my_thumbnail
            th_picture.place(x=405, y=5)

            # Se despliega en la ventana el nombre del video solicitado.
            tk.Label(self.misc, text='Video:',
                     font='arial 10 bold').place(x=10, y=140)
            # Este puede crear de 1 a 2 etiquetas dependiendo del nombre
            # del título, por lo que es importante para el orden
            # de los elementos de la ventana para más tarde hacer que el título
            # pueda encajar bien.
            title_exceeds = self.title_fits(my_video._title)

            # Se crea una caja para dedicir el tipo de formato que se quiere.
            types_cb = ttk.Combobox(self.misc, values=['Video', 'Audio'])
            # Se guarda la referencia del tipo de formato en el init.
            self.type = str(types_cb.get())
            # Se despliega en la ventana el nombre de los formatos disponibles.
            tk.Label(self.misc, text='Formato de video').place(x=10, y=10)
            types_cb.place(x=10, y=40)
            types_cb.bind('<<ComboboxSelected>>', lambda event:
                          self.type_choice(event, resolutions,
                                           title_exceeds))

            # Se crea una variable en donde guardar el nombre para el archivo
            # si es que el usuario desea renombrarlo. Si este espacio queda
            # vacío, se pondrá el nombre por defecto del video.
            f_entry = tk.Entry(self.misc, width=50)
            # Se guarda la referencia del tipo de archivo en el init.
            self.file_name = f_entry
            # Se despliega en la ventana la solicitud para
            #  el nombre del archivo.
            tk.Label(self.misc, text='Nombre del archivo:',
                     font='arial 10 bold').place(x=10, y=180)
            f_entry.place(x=150, y=182)

            # Se crea una variable en donde guardar la dirección del video.
            my_location = tk.Entry(self.misc, width=48)
            # Se guarda la referencia de la dirección en el init.
            self.location = my_location
            # Se despliega en la ventana la solicitud para
            # la ubicación en donde guardar el archivo.
            tk.Label(self.misc, text='Dirección:',
                     font='arial 10 bold').place(x=10, y=220)
            my_location.place(x=85, y=222)
            location_button = tk.Button(self.misc, text='Elegir', width=10,
                                        command=lambda:
                                        self.insertPath(my_location))
            location_button.place(x=482, y=220)

            # Se crea un botón para proceder con la descarga del video.
            download_button = tk.Button(self.misc, text='Descargar',
                                        bg='green',
                                        foreground='white', padx=2,
                                        command=lambda:
                                        self.download_video())
            download_button.place(x=190, y=270)
            # Se crea una botón para abrir una nueva ventana del video.
            again_button = tk.Button(self.misc, text='Nueva Descarga',
                                     bg='brown',
                                     foreground='white', padx=2,
                                     command=lambda:
                                     self.open_again())
            again_button.place(x=290, y=270)

            # NOTA: Cada elemento de Tkinter (Button, Entry, Label o Combobox)
            # fue contado de manera manual, ya que el número de elementos es
            # necesario para luego crear más elementos sin crear copias y así
            # que el número de elementos sea exacto. (Esto se ve en
            # funciones posteriores).
        # En caso de que se retorne False entonces se emitirá una advertencia.
        else:
            self.notifier.advice_nonexistent_link()

    def download_video(self):
        '''
        FUNCIÓN:
        Comenzar el proceso de descarga.
        '''
        # Lo primero que se debe hacer es verificar que exista
        # una dirección en donde guardar el video.
        my_direction = self.check_direction()
        # Si la dirección es correcta (no retorna False), se procede a
        # verificar los siguientes pasos.
        if my_direction is not False:
            # Si la respuesta del tipo de formato es Audio, se debe verificar
            # que luego se elija el tipo de archivo.
            if self.type == 'Audio':
                # Si se obtiene respuesta al tipo de archivo, entonces se
                # procederá a descargar según los datos que se encuentren.
                if self.file_type == 'mp3':
                    # Se obtendrá el nombre mediante la ayuda de una función.
                    video_name = self.set_name(self.file_name.get(),
                                               self.file_type)
                    # Si se obtiene False, el nombre será modificado.
                    if video_name is False:
                        video_name = self.video._title +\
                            '.' + self.file_type
                    # Se intentará descargar el audio en
                    # formato mp3 y sin audio.
                    try:
                        self.video.streams.filter(only_audio=True).first(
                        ).download(my_direction, video_name)
                        self.notifier.successful_download()
                    # Cualquier excepción que pueda afectar a la
                    # descarga se alertará al usuario
                    # (se tratan todas las excepciones posibles).
                    except Exception:
                        self.notifier.error_download()
                # Si no se logra obtener una respuesta, saltará
                # un mensaje de advertencia.
                else:
                    self.notifier.advice_chose_file_type()
            # Si la respuesta del tipo de formato es Video, se debe verificar
            # que luego se elija el tipo de archivo.
            elif self.type == 'Video':
                # Si no se ha elegido una resolución, saltará un
                # mensaje de advertencia.
                if self.resolution == '':
                    self.notifier.advice_chose_resolution()
                # Si la resolución es automática, se procedará a hacer
                # la descarga de manera automática.
                elif self.resolution == 'Auto Quality':
                    # Si se obtiene respuesta al tipo de archivo, entonces se
                    # procederá a descargar según los datos que se encuentren.
                    if self.file_type == 'mp4':
                        video_name = self.set_name(self.file_name.get(),
                                                   self.file_type)
                        # Si se obtiene False, se descargará sin necesidad de
                        # haber otorgado un nombre.
                        if video_name is False:
                            # Se intentará descargar el video en
                            # formato mp4 y con la resolución más alta.
                            try:
                                self.video.streams.get_highest_resolution(
                                                ).download(my_direction)
                                self.notifier.successful_download()
                            # Cualquier excepción que pueda afectar a la
                            # descarga se alertará al usuario
                            # (se tratan todas las excepciones posibles).
                            except Exception:
                                self.notifier.error_download()
                        # Si se pudo obtener un nombre, se descargará según
                        # el nombre que haya sido otorgado.
                        else:
                            # Se intentará descargar el video en
                            # formato mp4 y con la resolución más alta.
                            try:
                                self.video.streams.get_highest_resolution(
                                    ).download(my_direction, video_name)
                                self.notifier.successful_download()
                            # Cualquier excepción que pueda afectar a la
                            # descarga se alertará al usuario
                            # (se tratan todas las excepciones posibles).
                            except Exception:
                                self.notifier.error_download()
                    # Si no se logra obtener una respuesta, saltará
                    # un mensaje de advertencia.
                    else:
                        self.notifier.advice_chose_file_type()
                # La resolución 144p tendrá dos tipos de archivo.
                elif self.resolution == '144p':
                    # Si se obtiene respuesta al tipo de archivo y verificar
                    # que este sea mp4, entonces se procederá a descargar
                    #  según los datos que se encuentren.
                    if self.file_type == 'mp4':
                        video_name = self.set_name(self.file_name.get(),
                                                   self.file_type)
                        self.download_proccess(video_name, my_direction, True)
                    # Si se obtiene respuesta al tipo de archivo y verificar
                    # que este sea 3gp, entonces se procederá a descargar
                    #  según los datos que se encuentren.
                    elif self.file_type == '3gp':
                        video_name = self.set_name(self.file_name.get(),
                                                   self.file_type)
                        self.download_proccess(video_name, my_direction, False)
                    # Si no se logra obtener una respuesta, saltará
                    # un mensaje de advertencia.
                    else:
                        self.notifier.advice_chose_file_type()
                # Todas las demás resoluciones solo tendrán un tipo
                # de archivo (mp4) y lo único a destacar será la resolución.
                else:
                    # Si se obtiene respuesta al tipo de archivo, entonces se
                    # procederá a descargar según los datos que se encuentren.
                    if self.file_type == 'mp4':
                        video_name = self.set_name(self.file_name.get(),
                                                   self.file_type)
                        self.download_proccess(video_name, my_direction, True)
                    # Si no se logra obtener una respuesta,
                    # saltará un mensaje de advertencia.
                    else:
                        self.notifier.advice_chose_file_type()
            # Si no hay respuesta del tipo de formato, entonces se
            # notificará al usuario.
            else:
                self.notifier.advice_chose_type()

    def download_proccess(self, name: str, direction: str, set_name: bool):
        '''
        FUNCIÓN:
        Facilitar el proceso de descarga según las necesidades del usuario.
        :param str name: El valor del nombre para guardar el archivo.
        :param str direction: El valor de la dirección en donde
        guardar el archivo.
        :param bool set_name: El valor que determina si el nombre ya está
        establecido o si hay que modificarlo de alguna manera.
        '''
        # Si set name es True (el nombre ya está establecido) se ejecutará
        # el siguiente bloque:
        if set_name is True:
            # Si el nombre es False (no hay nombre) se ejecuta
            # el siguiente bloque:
            if name is False:
                # Se crea una lista de los streams de video que cumplen
                # con los requisitos para la descarga.
                download_list = self.video.streams.filter(
                    res=self.resolution,
                    type='video',
                    progressive=True
                    )
                # Si la lista de descarga tiene cero elementos
                # (está vacía), se procederá a intentar descargar
                # pero sin audio.
                if len(download_list) == 0:
                    # Se intentará descargar el video en
                    # la resolución solicitada pero sin audio.
                    try:
                        self.video.streams.filter(
                            res=self.resolution,
                            type='video'
                        ).first().download(direction)
                        self.notifier.no_audio_download()
                    # Cualquier excepción que pueda afectar a la
                    # descarga se alertará al usuario
                    # (se tratan todas las excepciones posibles).
                    except Exception:
                        self.notifier.error_download()
                # Si la lista de descarga no está vacía, se procederá a
                # descargar el video con todos los requisitos solicitados.
                else:
                    # Se intentará descargar el video en
                    # la resolución solicitada y con audio.
                    try:
                        download_list.first().download(direction)
                        self.notifier.successful_download()
                    # Cualquier excepción que pueda afectar a la
                    # descarga se alertará al usuario
                    # (se tratan todas las excepciones posibles).
                    except Exception:
                        self.notifier.error_download()
            # Si el nombre existe, se agregará como un parámetro
            # a la hora de descargar el video.
            else:
                # Se crea una lista de los streams de video que cumplen
                # con los requisitos para la descarga.
                download_list = self.video.streams.filter(
                    res=self.resolution,
                    type='video',
                    progressive=True
                    )
                # Si la lista de descarga tiene cero elementos
                # (está vacía), se procederá a intentar descargar
                # pero sin audio.
                if len(download_list) == 0:
                    # Se intentará descargar el video en
                    # la resolución solicitada pero sin audio.
                    try:
                        self.video.streams.filter(
                            res=self.resolution,
                            type='video'
                        ).first().download(direction, name)
                        self.notifier.no_audio_download()
                    # Cualquier excepción que pueda afectar a la
                    # descarga se alertará al usuario
                    # (se tratan todas las excepciones posibles).
                    except Exception:
                        self.notifier.error_download()
                # Si la lista de descarga no está vacía, se procederá a
                # descargar el video con todos los requisitos solicitados.
                else:
                    # Se intentará descargar el video en
                    # la resolución solicitada y con audio.
                    try:
                        download_list.first().download(direction, name)
                        self.notifier.successful_download()
                    # Cualquier excepción que pueda afectar a la
                    # descarga se alertará al usuario
                    # (se tratan todas las excepciones posibles).
                    except Exception:
                        self.notifier.error_download()
        # Si set name es False (el nombre NO está establecido) se ejecutará
        # el siguiente bloque:
        else:
            # Si el nombre es False (no hay nombre) el nombre
            # será modificado.
            if name is False:
                video_name = self.video._title +\
                    '.' + self.file_type
            # Se crea una lista de los streams de video que cumplen
            # con los requisitos para la descarga.
            download_list = self.video.streams.filter(
                res=self.resolution,
                type='video',
                progressive=True
                )
            # Si la lista de descarga tiene cero elementos
            # (está vacía), se procederá a intentar descargar
            # pero sin audio.
            if len(download_list) == 0:
                # Se intentará descargar el video en
                # la resolución solicitada pero sin audio.
                try:
                    self.video.streams.filter(
                        res=self.resolution,
                        type='video'
                    ).first().download(direction, video_name)
                    self.notifier.no_audio_download()
                # Cualquier excepción que pueda afectar a la
                # descarga se alertará al usuario
                # (se tratan todas las excepciones posibles).
                except Exception:
                    self.notifier.error_download()
            # Si la lista de descarga no está vacía, se procederá a
            # descargar el video con todos los requisitos solicitados.
            else:
                # Se intentará descargar el video en
                # la resolución solicitada y con audio.
                try:
                    download_list.first().download(direction, video_name)
                    self.notifier.successful_download()
                # Cualquier excepción que pueda afectar a la
                # descarga se alertará al usuario
                # (se tratan todas las excepciones posibles).
                except Exception:
                    self.notifier.error_download()

    # COPIA, PEGA Y COMENTA (PERSONA 2)
    def open_again(self):
        '''
        FUNCIÓN:
        Abrir una nueva ventana y cerrar la actual.
        '''
        self.misc.destroy()
        tr.Window()

    def set_file_type(self, event):
        '''
        FUNCIÓN:
        Se escoge el tipo de formato de archivo.
        '''
        self.file_type = event.widget.get()

    def set_name(self, name, extension):
        '''
        FUNCIÓN:
        Se escoge el nombre para el archivo que se va a descargar.
        '''
        # Si el nombre está vacío, se retorna False.
        if name == '':
            return False
        # Si el nombre no está vacío se devolverá el nombre más la extensión.
        else:
            video_name = str(name) + '.' + str(extension)
            return video_name

    def check_video_exists(self, link):
        '''
        FUNCIÓN:
        Verificar la existencia de un video.
        '''
        # Se intentá crear un objeto de tipo YouTube
        # si se puede crear entonces será retornado.
        try:
            my_video = YouTube(link)
            self.video = my_video
            return my_video
        # Si surge que el link no existe o no se encuentra
        # se retornará False.
        except pytube.exceptions.RegexMatchError:
            return False

    def check_direction(self):
        '''
        FUNCIÓN:
        Revisar si la dirección se encuentra vacía.
        '''
        # Se obtiene el nombre de la dirección.

        # Si la dirección está vacía, surge un mensaje de advertencia para
        # que se solicite una dirección.
        if self.location.get() == '':
            self.notifier.advice_choose_location()
            return False
        # De no ser así, se regresará el valor de True.
        else:
            # Se debe verificar que la dirección exista.
            path_existance = os.path.exists(self.location.get())
            # Si la dirección no existe entonces surge un mensaje
            # de advertencia para que se ponga dirección que exista.
            if path_existance is False:
                # ARREGLAR ESTO.
                self.notifier.advice_nonexistent_location()
                return False
            # Si la dirección existe entonces se retornará True como valor.
            else:
                return self.location.get()

    def sort_resolutions(self, resolutions: list):
        '''
        FUNCIÓN:
        Acomoda las resoluciones de mayor a menor.
        '''
        # En esta lista se guardarán las resoluciones de mayor a menor.
        sorted_resolutions = []
        # Se quita la 'p' de cada elemento para así trabajar con
        # números enteros.
        for i in range(len(resolutions)):
            my_resolution = int(resolutions[i][:-1])
            sorted_resolutions.append(my_resolution)
        # Se acomodan los números de mayor a menor con sorted.
        sorted_resolutions = sorted(sorted_resolutions, reverse=True)
        # Luego, se vuelve a poner la 'p' nuevamente en cada elemento
        # de la lista.
        for i in range(len(sorted_resolutions)):
            sorted_resolutions[i] = str(sorted_resolutions[i]) + 'p'
        # Se regresan todas las resoluciones una vez ya se encuentren
        # ordenadas.
        return sorted_resolutions

    def get_resolutions(self, video: YouTube):
        '''
        FUNCIÓN:
        Obtener las resoluciones disponibles dado como parámetro un
        video de Youtube.
        '''
        # En esta lista se guardarán las resoluciones disponibles
        # para un video.
        resolutions = []
        # Con este ciclo se identificarán cuales son las
        # resoluciones disponibles.
        for i in video.streams:
            # Puede suceder que una resolución se repita o que aparezca como
            # 'None', si alguno de estos dos casos sucede
            # simplemente se ignorará y se procederá con el siguiente elemento.
            if str(i.resolution) in resolutions or str(i.resolution) == 'None':
                pass
            # De no presentarse el error mencionado anteriormente entonces se
            # agregará a la lista de resoluciones disponibles
            # para un video.
            else:
                resolutions.append(str(i.resolution))
        # Se acomodan las resoluciones de menor a mayor.
        resolutions = self.sort_resolutions(resolutions)
        # Se acomodan en orden númerico las resoluciones, desde la más baja
        # hasta la más alta.
        return resolutions

    # COPIA, PEGA Y COMENTA (PERSONA 3)
    def get_thumbnail(self, link):
        '''
        FUNCIÓN:
        Obtener el thumbnail de una imagen en base a su link sin tener
        que descargarla.
        '''
        # Se lee la información de la imagen con la librería url lib requist.
        with urllib.request.urlopen(link) as my_request:
            raw_data = my_request.read()
        # Se abre la imagen en base a la data recolectada.
        link_thumbnail = Image.open(io.BytesIO(raw_data))
        # Se hace la imagen más pequeña para que esta pueda
        # caber en la ventana.
        link_thumbnail = link_thumbnail.resize((160, 130))
        # Se transforma la imagen en el formato adecuado.
        picture = ImageTk.PhotoImage(link_thumbnail)
        return picture

    def erase_widgets(self, maximum: int):
        '''
        FUNCIÓN:
        Borrar todos los widgets después de cierto número.
        '''
        # Se obtienen todos los elementos dentro del root.
        wlist = self.misc.winfo_children()
        # Si la longitud de elementos es mayor al máximo que se busca,
        # entonces se van a eliminar
        if len(wlist) != maximum:
            # Se guarda en una variable la cantidad de veces a iterar por cada
            # elemento adicional que exista.
            ite_var = len(wlist) - maximum
            wlist.reverse()
            for i in range(ite_var):
                wlist[i].destroy()

    def directoryLocation(self):
        '''
        FUNCIÓN:
        Preguntar por la dirección.
        '''
        filename = filedialog.askdirectory()
        return filename

    def insertPath(self, entry: tk.Entry):
        '''
        FUNCIÓN:
        Insertar la dirección y su path.
        '''
        entry.delete(0, 'end')
        entry.insert(0, self.directoryLocation())

    def title_fits(self, video_title):
        '''
        FUNCIÓN:
        Con esta función se verifica que el texto pueda alcanzar el
        espacio para así poder acomodarlo según su longitud.
        '''
        # Lista donde se despliegará el texto según los espacios.
        list_texto = video_title.split(' ')
        # String que será usado como prueba para medir los caracteres.
        str_measure = ''
        # Variable donde se guardará el index de donde se
        # debe separar el texto.
        max_index = 0

        for i in range(len(list_texto)):
            # Si es la primer palabra, no se debe agregar espacio.
            if i == 0:
                str_measure = str_measure + list_texto[i]
            # Cualquier otra palabra sí debe tener espacio.
            else:
                str_measure = str_measure + ' ' + list_texto[i]

            # Si la longitud del texto supera los 70 caracteres entonces se
            # ejecutará el siguiente bloque de código.
            if len(str_measure) > 70:
                # Se debe separar el texto en donde existan espacios.
                nuevo_texto = str_measure.split(' ')
                # La última palabra es la que está causando el problema, por
                # que la longitud quedará hasta la penúltima palabra.
                max_index = len(nuevo_texto) - 1
                break

        # Si la variable cambia es por que el texto supera el número máximo de
        # caracteres permitidos.
        if max_index != 0:
            first_list = list_texto[:max_index]
            second_list = list_texto[max_index:]
            tk.Label(self.misc, text=' '.join(first_list),
                     font='arial 10').place(x=52, y=140)
            tk.Label(self.misc, text=' '.join(second_list),
                     font='arial 10').place(x=10, y=160)
            return True
        # De no ser así, simplemente se pondrá el título por defecto.
        else:
            tk.Label(self.misc, text=video_title,
                     font='arial 10').place(x=55, y=140)
            return False

    def resolution_choice(self, event, exceeding: bool):
        '''
        FUNCIÓN:
        Se escoge el tipo de formato de resolución.
        '''
        # Se obtiene la respuesta de la resolución.
        self.resolution = event.widget.get()
        # Estos datos deben ser vaciados para que no haya
        # problemas luego al descargar.
        self.file_type = ''
        # Si el título del video se excedió de caracteres, los elementos en la
        # ventana serán un total de 14.
        if exceeding is True:
            elements = 15
        # Si el título del video se excedió de caracteres, los elementos en la
        # ventana serán un total de 13.
        else:
            elements = 14
        # Si el formato de resolución es de 144p entonces se ejecutará todo el
        # siguiente bloque de código.
        if self.resolution == '144p':
            # Si hay más de 13 widgets, todas las añadidas recientemente
            # serán eliminadas.Esto se hace debido a que se crean varias
            # copias y esto puede sobrecargar la aplicación.
            self.erase_widgets(elements)
            # Se crea una caja para decidir el formato de archivo.
            file_types_cb = ttk.Combobox(self.misc, values=['3gp', 'mp4'])
            tk.Label(self.misc, text='Formato de archivo').place(x=10, y=70)
            file_types_cb.place(x=10, y=100)
            file_types_cb.bind('<<ComboboxSelected>>', lambda event:
                               self.set_file_type(event))
        # Si el formato de resolución es cualquier otro entonces se ejecutará
        # todo el siguiente bloque de código.
        else:
            # Si hay más de 13 widgets, todas las añadidas recientemente
            # serán eliminadas.Esto se hace debido a que se crean varias
            # copias y esto puede sobrecargar la aplicación.
            self.erase_widgets(elements)
            # Se crea una caja para decidir el formato de archivo, en este
            # caso solo habrá formato mp4.
            file_types_cb = ttk.Combobox(self.misc, values='mp4')
            tk.Label(self.misc, text='Formato de archivo').place(x=10, y=70)
            file_types_cb.place(x=10, y=100)
            file_types_cb.bind('<<ComboboxSelected>>', lambda event:
                               self.set_file_type(event))

    def type_choice(self, event, resolutions: list, exceeding: bool):
        '''
        FUNCIÓN:
        Se escoge el tipo de formato de video.
        '''
        # Se obtiene la respuesta del tipo de formato.
        self.type = event.widget.get()
        # Estos datos deben ser vaciados para que no haya
        # problemas luego al descargar.
        self.file_type = ''
        self.resolution = ''
        # Si el título del video se excedió de caracteres, los elementos en la
        # ventana serán un total de 12.
        if exceeding is True:
            elements = 13
        # Si el título no se excedió, los elementos en la
        # ventana serán un total de 11.
        else:
            elements = 12
        # Si el formato es de video entonces se ejecutará todo el siguiente
        # bloque de código.
        if self.type == 'Video':
            # Si hay más de 11 o 12 widgets, todas las añadidas recientemente
            # serán eliminadas.
            # Esto se hace debido a que se crean varias copias y esto puede
            # sobrecargar la aplicación.
            self.erase_widgets(elements)
            # Se crea una caja para decidir la resolución de
            # video que se quiere.
            resolutions_cb = ttk.Combobox(self.misc, values=resolutions)
            tk.Label(self.misc, text='Resolución').place(x=200, y=10)
            resolutions_cb.place(x=200, y=40)
            resolutions_cb.bind('<<ComboboxSelected>>', lambda event:
                                self.resolution_choice(event, exceeding))
        # Si el formato es de audio entonces se ejecutará todo el siguiente
        # bloque de código.
        else:
            # Si hay más de 11 widgets, todas las añadidas
            # recientemente serán eliminadas.
            # Esto se hace debido a que se crean varias copias y esto puede
            # sobrecargar la aplicación.
            self.erase_widgets(elements)
            # Se crea una variable en donde guardar el formato de archivo.
            file_types_cb = ttk.Combobox(self.misc, values='mp3')
            tk.Label(self.misc, text='Formato de archivo').place(x=200, y=10)
            file_types_cb.place(x=200, y=40)
            file_types_cb.bind('<<ComboboxSelected>>', lambda event:
                               self.set_file_type(event))
