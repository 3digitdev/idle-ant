import npyscreen


class TestApp(npyscreen.NPSApp):
    def main(self):
        # These lines create the form and populate it with widgets.
        f = npyscreen.Form(
            name='Welcome to Npyscreen',
        )
        t = f.add(
            npyscreen.TitleText,
            name='Text:',
        )
        fn = f.add(npyscreen.TitleFilename, name='Filename:')
        fn2 = f.add(npyscreen.TitleFilenameCombo, name='Filename2:')
        dt = f.add(npyscreen.TitleDateCombo, name='Date:')
        s = f.add(npyscreen.TitleSlider, out_of=12, name='Slider')
        ml = f.add(
            npyscreen.MultiLineEdit,
            value="""try typing here!\nMutiline text, press ^R to reformat.\n""",
            max_height=5,
            rely=9,
        )
        ms = f.add(
            npyscreen.TitleSelectOne,
            max_height=4,
            value=[
                1,
            ],
            name='Pick One',
            values=['Option1', 'Option2', 'Option3'],
            scroll_exit=True,
        )
        ms2 = f.add(
            npyscreen.TitleMultiSelect,
            max_height=-2,
            value=[
                1,
            ],
            name='Pick Several',
            values=['Option1', 'Option2', 'Option3'],
            scroll_exit=True,
        )
        # This lets the user interact with the Form.
        f.edit()
        print(ms.get_selected_objects())


if __name__ == '__main__':
    App = TestApp()
    App.run()
