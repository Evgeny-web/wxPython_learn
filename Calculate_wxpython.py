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
        super().__init__(parent, title=title, size=(600, 450))

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

        # Отобразим калькулятор на экране
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(12)
        panel.SetFont(font)

        self.tc = wx.ComboBox(panel)
        vbox.Add(self.tc, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        gbox = wx.GridSizer(5, 4, 5, 5) # кол-во строк, столбцов, отступов по вертикали и горизонтали
        gbox.AddMany([(wx.Button(panel, label="Cls"), wx.ID_ANY, wx.EXPAND),
                      (wx.Button(panel, label="Bck"), wx.ID_ANY, wx.EXPAND),
                      (wx.StaticText(panel), wx.EXPAND),
                      (wx.Button(panel, label="Close"), 0, wx.EXPAND),
                      (wx.Button(panel, label="7"), 0, wx.EXPAND),
                      (wx.Button(panel, label="8"), 0, wx.EXPAND),
                      (wx.Button(panel, label="9"), 0, wx.EXPAND),
                      (wx.Button(panel, label="/"), 0, wx.EXPAND),
                      (wx.Button(panel, label="4"), 0, wx.EXPAND),
                      (wx.Button(panel, label="5"), 0, wx.EXPAND),
                      (wx.Button(panel, label="6"), 0, wx.EXPAND),
                      (wx.Button(panel, label="*"), 0, wx.EXPAND),
                      (wx.Button(panel, label="1"), 0, wx.EXPAND),
                      (wx.Button(panel, label="2"), 0, wx.EXPAND),
                      (wx.Button(panel, label="3"), 0, wx.EXPAND),
                      (wx.Button(panel, label="-"), 0, wx.EXPAND),
                      (wx.Button(panel, label="."), 0, wx.EXPAND),
                      (wx.Button(panel, label="0"), 0, wx.EXPAND),
                      (wx.Button(panel, label="+"), 0, wx.EXPAND),
                      (wx.Button(panel, label="="), 0, wx.EXPAND)])

        vbox.Add(gbox, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.OnClicked)


    # Пишем функции
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

    def OnClicked(self, evt):
        label = evt.GetEventObject().GetLabel() # создаем переменную, чтобы записывать в нее имя нажимаемых кнопочек

        if label == '=':
            compute = self.tc.GetValue() # берем выражение из поля ввода
            # тут игнорируем пустой ввод
            if not compute.strip():
                return

            result = eval(compute) # тут считаем полученное выражение
            self.tc.Insert(compute, 0) # добавляем в историю наши расчеты
            self.tc.SetValue(str(result)) # показываем

        elif label == 'Cls':
            self.tc.SetValue("") # чистим все
        elif label == 'Close':
            frame.Destroy() # выходим из приложения
        else:
            self.tc.SetValue(self.tc.GetValue() + label)


app = wx.App()

frame = MyFrame(None, title="Hello World")
frame.Center()
frame.Show()

app.MainLoop()