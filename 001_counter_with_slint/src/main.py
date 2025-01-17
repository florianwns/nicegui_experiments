import slint

# slint.loader will look in `sys.path` for `app-window.slint`.
class App(slint.loader.ui.app_window.AppWindow):
    @slint.callback
    def request_increase_value(self):
        self.counter = self.counter + 1


if __name__ == '__main__':
    app = App()
    app.run()