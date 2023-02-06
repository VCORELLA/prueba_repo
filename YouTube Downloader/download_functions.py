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
        self.misc = misc

    # Mensaje de aviso de elegir una dirección.
    def advice_choose_location(self):
        messagebox.showinfo('Advertencia', ('Debe elegir una dirección'
                                            ' donde guardar su video.'))

    # Mensaje de aviso si una dirección no existe.
    def advice_nonexistent_location(self):
        messagebox.showinfo('Advertencia', ('La dirección no se ha '
                                            'encontrado,'
                                            'intente otra dirección.'))

    # Mensaje de aviso de descarga completada.
    def successful_download(self):
        messagebox.showinfo('Descarga Completada',
                            'Su descarga ha sido exitosa.')

    # Mensaje de aviso de descarga completada, pero con posible error de audio.
    def no_audio_download(self):
        messagebox.showinfo('Descarga Completada',
                            'La resolución pudo haber afectado el audio, '
                            'se recomienda elegir otra resolución.')

    # Mensaje de aviso de descarga no exitosa.
    def error_download(self):
        messagebox.showinfo('Advertencia',
                            'Hubo un problema con su descarga, intente '
                            'de nuevo más tarde.')

    # Mensaje de aviso para elegir un tipo de formato general.
    def advice_chose_type(self):
        messagebox.showinfo('Advertencia', 'Debe elegir un formato de video.')

    # Mensaje de aviso para elegir una resolución.
    def advice_chose_resolution(self):
        messagebox.showinfo('Advertencia',
                            'Debe elegir una resolución.')

    # Mensaje de aviso para elegir un formato de archivo.
    def advice_chose_file_type(self):
        messagebox.showinfo('Advertencia',
                            'Debe eligir un formato de archivo.')

    # Mensaje de aviso para corregir el link.
    def advice_nonexistent_link(self):
        messagebox.showinfo('Advertencia', ('Ha ocurrido un error, '
                                            'verifique que puso bien su '
                                            'link.'))


class Functions():
    # Dentro del init se guardará la información necesaria
    # para proceder con la descarga del archivo.
    def __init__(self, misc: tk.Tk):
        # Nombre del video / archivo.
        self.file_name = ''
        # Nombre de la dirección.
        self.location = ''
        # Nombre del tipo de formato (Video/Audio).
        self.type = ''
        # Nombre de la resolución.
        self.resolution = ''
        # Nombre del tipo de archivo.
        self.file_type = ''
        # Se debe guardar la root.
        self.misc = misc
        # Se debe crear un objeto de tipo "YouTube".
        self.video = None
        # Se crea un notificador de mensajes.
        self.notifier = Messages(misc)

    def open_again(self):
        '''
        FUNCIÓN: Abrir una nueva ventana y cerrar la actual.
        '''
        self.misc.destroy()
        tr.Window()

    def set_file_type(self, event):
        '''
        FUNCIÓN: Se escoge el tipo de formato de archivo.
        '''
        self.file_type = event.widget.get()

    def set_name(self, name, extension):
        '''
        FUNCIÓN: Se escoge el nombre para el archivo que se va a descargar.
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
        FUNCIÓN: Verificar la existencia de un video.
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
        FUNCIÓN: Revisar si la dirección se encuentra vacía.
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

    def download_proccess(self, name, direction, set_name: bool):
        # Si set name es True se ejecuta el siguiente bloque:
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
                    # Se intentará descargar el video.
                    try:
                        self.video.streams.filter(
                            res=self.resolution,
                            type='video'
                        ).first().download(direction)
                        self.notifier.no_audio_download()
                    # Cualquier excepción que pueda afectar a la
                    # descarga se alertará al usuario
                    # (todas las excepciones).
                    except Exception:
                        self.notifier.error_download()
                else:
                    try:
                        download_list.first().download(direction)
                        self.notifier.successful_download()
                    # Cualquier excepción que pueda afectar a la
                    # descarga se alertará al usuario
                    # (todas las excepciones).
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
                    # Se intentará descargar el video.
                    try:
                        self.video.streams.filter(
                            res=self.resolution,
                            type='video'
                        ).first().download(direction, name)
                        self.notifier.no_audio_download()
                    # Cualquier error, se notificará al usuario.
                    except Exception:
                        self.notifier.error_download()
                else:
                    try:
                        download_list.first().download(direction, name)
                        self.notifier.successful_download()
                    except Exception:
                        self.notifier.error_download()
        # Si set name es False, se ejecutará el siguiente bloque:
        else:
            # Si el nombre es False (no hay nombre) se ejecuta
            # el siguiente bloque:
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
                # Se intentará descargar el video.
                try:
                    self.video.streams.filter(
                        res=self.resolution,
                        type='video'
                    ).first().download(direction, video_name)
                    self.notifier.no_audio_download()
                # Cualquier error, se notificará al usuario.
                except Exception:
                    self.notifier.error_download()
            else:
                try:
                    download_list.first().download(direction, video_name)
                    self.notifier.successful_download()
                except Exception:
                    self.notifier.error_download()

    def download_video(self):
        '''
        FUNCIÓN: Comenzar el proceso de descarga:
        '''
        # Lo primero que se debe hacer es verificar que exista
        # una dirección en donde guardar el video.
        my_direction = self.check_direction()
        print("-------------")
        print('dirección: ', my_direction)
        print('tipo: ', self.type)
        print('nombre: ', self.file_name.get())
        print('tipo archivo: ', self.file_type)
        print('resolución: ', self.resolution, '\n')
        # Si la dirección es correcta, se procede a verificar
        # los siguientes pasos.
        if my_direction is not False:
            # Si la respuesta es Audio, se debe verificar que luego
            # elija el formato.
            if self.type == 'Audio':
                # Si se obtiene respuesta, entonces se procederá
                # a descargar según los datos que se encuentren.
                if self.file_type == 'mp3':
                    video_name = self.set_name(self.file_name.get(),
                                               self.file_type)
                    if video_name is False:
                        video_name = self.video._title +\
                            '.' + self.file_type
                    try:
                        self.video.streams.get_lowest_resolution(
                            ).download(my_direction, video_name)
                        self.notifier.successful_download()
                    except Exception:
                        self.notifier.error_download()
                # Si no se logra obtener una respuesta, saltará
                # un mensaje de advertencia.
                else:
                    self.notifier.advice_chose_file_type()
            # Si la respuesta es Video, se debe verificar que luego
            # elija el formato.
            elif self.type == 'Video':
                # Si no se ha elegido una resolución, saltará un
                # mensaje de advertencia.
                if self.resolution == '':
                    self.notifier.advice_chose_resolution()
                # Si la resolución es automática, se procedará a hacer
                # la descarga de manera automática.
                elif self.resolution == 'Auto Quality':
                    # Si se obtiene respuesta, entonces se procederá
                    # a descargar según los datos que se encuentren.
                    if self.file_type == 'mp4':
                        video_name = self.set_name(self.file_name.get(),
                                                   self.file_type)
                        if video_name is False:
                            try:
                                self.video.streams.get_highest_resolution(
                                                ).download(my_direction)
                                self.notifier.successful_download()
                            # Cualquier excepción que pueda afectar a la
                            # descarga se alertará al usuario
                            # (todas las excepciones).
                            except Exception:
                                self.notifier.error_download()
                        else:
                            try:
                                self.video.streams.get_highest_resolution(
                                    ).download(my_direction, video_name)
                                self.notifier.successful_download()
                            # Cualquier excepción que pueda afectar a la
                            # descarga se alertará al usuario
                            # (todas las excepciones).
                            except Exception:
                                self.notifier.error_download()
                    # Si no se logra obtener una respuesta, saltará
                    # un mensaje de advertencia.
                    else:
                        self.notifier.advice_chose_file_type()
                # La resolución 144p tendrá dos formatos de archivo.
                elif self.resolution == '144p':
                    # Si se obtiene respuesta, entonces se procesedará a
                    # descargar según los datos que se encuentren.
                    if self.file_type == 'mp4':
                        video_name = self.set_name(self.file_name.get(),
                                                   self.file_type)
                        self.download_proccess(video_name, my_direction, True)
                    elif self.file_type == '3gp':
                        video_name = self.set_name(self.file_name.get(),
                                                   self.file_type)
                        self.download_proccess(video_name, my_direction, False)
                    # Si no se logra obtener una respuesta, saltará
                    # un mensaje de advertencia.
                    else:
                        self.notifier.advice_chose_file_type()

                # Todas las demás resoluciones solo tendrán un formato
                # de archivo y lo único que importará será la resolución.
                else:
                    # Si se obtiene respuesta, entonces se procesedará
                    # a descargar según los datos que se encuentren.
                    if self.file_type == 'mp4':
                        video_name = self.set_name(self.file_name.get(),
                                                   self.file_type)
                        self.download_proccess(video_name, my_direction, True)
                    # Si no se logra obtener una respuesta,
                    # saltará un mensaje de advertencia.
                    else:
                        self.notifier.advice_chose_file_type()
            # Si no hay respuesta, entonces se enviará una advertencia
            # para que se eliga el tipo de formato.
            else:
                self.notifier.advice_chose_type()

    def sort_resolutions(self, resolutions: list):
        '''
        FUNCIÓN: Acomoda las resoluciones de mayor a menor.
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
        FUNCIÓN: Obtener las resoluciones disponibles dado como parámetro un
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

    def get_thumbnail(self, link):
        '''
        FUNCIÓN: Obtener el thumbnail de una imagen en base a su link sin tener
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
        FUNCIÓN: Borrar todos los widgets después de cierto número.
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
        FUNCIÓN: Preguntar por la dirección.
        '''
        filename = filedialog.askdirectory()
        return filename

    def insertPath(self, entry: tk.Entry):
        '''
        FUNCIÓN: Insertar la dirección y su path.
        '''
        entry.delete(0, 'end')
        entry.insert(0, self.directoryLocation())

    def title_fits(self, video_title):
        '''
        FUNCIÓN: Con esta función se verifica que el texto pueda alcanzar el
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

            # Si la longitud del texto supera los 58 caracteres entonces se
            # ejecutará el siguiente bloque de código.
            if len(str_measure) > 58:
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
        FUNCIÓN: Se escoge el tipo de formato de resolución.
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
        # Si el título del video se excedió de caracteres, llos elementos en la
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
        FUNCIÓN: Se escoge el tipo de formato de video.
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
            tk.Label(self.misc, text='Resolución').place(x=170, y=10)
            resolutions_cb.place(x=170, y=40)
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
            tk.Label(self.misc, text='Formato de archivo').place(x=170, y=10)
            file_types_cb.place(x=170, y=40)
            file_types_cb.bind('<<ComboboxSelected>>', lambda event:
                               self.set_file_type(event))

    def start_download(self, entry: tk.Entry):
        '''
        FUNCIÓN: Se pide el link de un video de Youtube y se convierte en un
        objeto de tipo "Youtube". Se borra la pantalla del inicio y se crea una
        totalmente nueva.
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

            # Se borra todos los widgets.
            wlist = self.misc.winfo_children()
            # Se vacía toda la ventana para luego poder insertar cosas nuevas.
            for widge in wlist:
                widge.destroy()

            # Se obtiene el link del thumbnail del video de YouTube.
            thumbnail_link = my_video.thumbnail_url
            # Se obtiene la imagen del video de youtube mediante
            # su link de YouTube.
            my_thumbnail = self.get_thumbnail(thumbnail_link)
            # Se despliega la imagen del video solicitado.
            th_picture = tk.Label(self.misc, image=my_thumbnail)
            th_picture.image = my_thumbnail
            th_picture.place(x=325, y=5)

            # Se despliega el nombre del video solicitado 2.
            tk.Label(self.misc, text='Video:',
                     font='arial 10 bold').place(x=10, y=140)
            # Este puede crear de 1 a 2 etiquetas dependiendo del nombre
            # del título, por lo que es importante para el orden
            # de los elementos de la ventana para más tarde.
            title_exceeds = self.title_fits(my_video._title)

            # Se crea una caja para dedicir el tipo de formato que se quiere.
            types_cb = ttk.Combobox(self.misc, values=['Video', 'Audio'])
            # Se guarda la referencia del tipo de formato en el init.
            self.type = str(types_cb.get())
            tk.Label(self.misc, text='Formato de video').place(x=10, y=10)
            types_cb.place(x=10, y=40)
            types_cb.bind('<<ComboboxSelected>>', lambda event:
                          self.type_choice(event, resolutions,
                                           title_exceeds))

            # Se crea una variable en donde guardar el nombre para el archivo
            # si es que el usuario desea renombrarlo. Si este espacio queda
            # vacío, se pondrá el nombre por defecto del video.

            f_entry = tk.Entry(self.misc, width=50)
            self.file_name = f_entry
            tk.Label(self.misc, text='Nombre del archivo:',
                     font='arial 10 bold').place(x=10, y=180)
            f_entry.place(x=150, y=182)

            # Se crea una variable en donde guardar la dirección del video.
            my_location = tk.Entry(self.misc, width=50)
            self.location = my_location
            tk.Label(self.misc, text='Dirección:',
                     font='arial 10 bold').place(x=10, y=220)
            my_location.place(x=85, y=222)
            location_button = tk.Button(self.misc, text='Elegir', width=10,
                                        command=lambda:
                                        self.insertPath(my_location))
            location_button.place(x=405, y=220)

            # Se crea una variable para proceder con la descarga del video.
            download_button = tk.Button(self.misc, text='Descargar',
                                        bg='green',
                                        foreground='white', padx=2,
                                        command=lambda:
                                        self.download_video())
            download_button.place(x=150, y=260)
            # Se crea una variable para abrir una nueva ventana del video.
            # Aquí hay 2 más: normal es 11 con texto adicional 12.
            # en el otro son 13 y con texto adicional 14.
            #  normal es 12 con ta 13. en el otro 14 y con ta 15.
            again_button = tk.Button(self.misc, text='Nueva Descarga',
                                     bg='brown',
                                     foreground='white', padx=2,
                                     command=lambda:
                                     self.open_again())
            again_button.place(x=250, y=260)
        # En caso de que se retorne False entonces se emitirá una advertencia.
        else:
            messagebox.showinfo('Advertencia', ('Ha ocurrido un error, '
                                                'verifique que puso bien su '
                                                'link.'))
