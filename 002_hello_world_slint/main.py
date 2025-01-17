import slint

# slint.loader will look in `sys.path` for `app-window.slint`.
class App(slint.loader.app_window.AppWindow):
    pass

if __name__ == '__main__':
    app = App()
    app.run()