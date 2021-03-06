import wx

APP_EXIT = 1  # id для кнопки в меню
VIEW_STATUS = 2
VIEW_RGB = 3
VIEW_SRGB = 4


# Класс для создания меню на правой копке мыши
class AppContextMenu(wx.Menu):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()

        minimaz = self.Append(wx.ID_ANY, "Свернуть")
        maximaz = self.Append(wx.ID_ANY, "Развернуть")
        self.Bind(wx.EVT_MENU, self.onMinimize, minimaz)
        self.Bind(wx.EVT_MENU, self.onMaximize, maximaz)

    def onMinimize(self, event):
        self.parent.Iconize()

    def onMaximize(self, event):
        self.parent.Maximize()


# Основной класс для создания отображения приложения (окно)
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()

        # подменю в главном меню
        myMenu = wx.Menu()
        # item3 = wx.MenuItem(myMenu, wx.ID_FILE1,  "Tools")
        # myMenu.Append(item3)
        myTools = myMenu.Append(wx.ID_ANY, "tools")

        # кнопки в главном меню
        new_menu_button = fileMenu.Append(wx.ID_NEW, "&Новый\tCtrl+N")
        open_menu_button = fileMenu.Append(wx.ID_OPEN, "&Открыть\tCtrl+O")
        save_menu_button = fileMenu.Append(wx.ID_SAVE, "&Сохранить\tCtrl+S")
        fileMenu.AppendSubMenu(myMenu, "&Tools")
        fileMenu.AppendSeparator()

        # кнопка выхода в главном меню
        exit_menu_button = wx.MenuItem(fileMenu, APP_EXIT, "Выход\tCtrl+Q", "Выход из приложения")
        fileMenu.Append(exit_menu_button)

        # Вторая вкладка меню с кнопками
        viewMenu = wx.Menu()
        self.vStatus = viewMenu.Append(VIEW_STATUS, "Строка", kind=wx.ITEM_CHECK)
        self.vRGB = viewMenu.Append(VIEW_RGB, "Тип RGB", "Тип RGB", kind=wx.ITEM_RADIO)
        self.vsRGB = viewMenu.Append(VIEW_SRGB, "Тип sRGB", "Тип sRGB", kind=wx.ITEM_RADIO)

        menubar.Append(fileMenu, "&File")
        menubar.Append(viewMenu, "&Вид")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.onQuit, id=APP_EXIT)
        self.Bind(wx.EVT_MENU, self.onStatus, id=VIEW_STATUS)
        self.Bind(wx.EVT_MENU, self.onImageType, id=VIEW_RGB)
        self.Bind(wx.EVT_MENU, self.onImageType, id=VIEW_SRGB)

        # меню отображаемое на правую кнопку мыши
        self.ctx = AppContextMenu(self)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightDown)

        # Создаем панель toolbar
        toolbar = self.CreateToolBar()
        bt_quit = toolbar.AddTool(wx.ID_ANY, "Выход", wx.Bitmap("Выход.png"))
        toolbar.AddSeparator()

        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.onQuit, bt_quit)

        # Отобразим виджеты на экране
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label="Путь к файлу: ")
        tc = wx.TextCtrl(panel)

        hbox1.Add(st1, flag=wx.RIGHT, border=8)
        hbox1.Add(tc, proportion=1)

        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        st2 = wx.StaticText(panel, label="Содержание файла")
        vbox.Add(st2, flag=wx.EXPAND | wx.ALL, border=10)

        tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        vbox.Add(tc2, proportion=1,
                 flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        btnok = wx.Button(panel, label="Да", size=(70, 30))
        btncn = wx.Button(panel, label="Отмена", size=(70, 30))

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(btnok, flag=wx.LEFT, border=10)
        hbox2.Add(btncn, flag=wx.LEFT, border=10)

        vbox.Add(hbox2, flag=wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT, border=10)

        panel.SetSizer(vbox)


    # Пишем функции

    def onRightDown(self, event):
        self.PopupMenu(self.ctx, event.GetPosition())

    def onStatus(self, event):
        if self.vStatus.IsChecked():
            print("Показать строку")
        else:
            print("Скрыть строку")

    def onImageType(self, event):
        if self.vRGB.IsChecked():
            print("Выбрано: RGB")
        if self.vsRGB.IsChecked():
            print("Выбрано: sRGB")

    def onQuit(self, event):
        self.Close()


app = wx.App()

frame = MyFrame(None, title="Hello World")
frame.Center()
frame.Show()

app.MainLoop()
