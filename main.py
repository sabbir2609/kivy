from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.recycleview import RecycleView  # <--- import RecycleView
import sqlite3
from kivy.metrics import sp
from datetime import datetime


conn = sqlite3.connect("project.sqlite3")
c = conn.cursor()


class HomeWindow(Screen):
    pass


class StudentAddWindow(Screen):
    def test_two(self):
        c = conn.cursor()
        c.execute(
            "INSERT INTO student_info (id, Name, email, mobile_number, address) VALUES (?, ?, ?, ?, ?)",
            (
                self.id_no.text,
                self.display_name.text,
                self.email.text,
                self.phone.text,
                self.address.text,
            ),
        )
        conn.commit()
        c.close()
        # conn.close()

        self.id_no.text = ""
        self.display_name.text = ""
        self.email.text = ""
        self.phone.text = ""
        self.address.text = ""

        print(
            f"{self.id_no.text}, {self.display_name.text}, {self.email.text}, {self.phone.text}, {self.address.text}"
        )


class StudentDataWindow(Screen):
    def test_three(self):
        pass


class StudentListWindow(Screen):
    def list_student(self):
        layout = GridLayout(
            cols=6,
            row_force_default=True,
            row_default_height=sp(40),
            padding=(20, 20, 20, 20),
            spacing=(10, 10),
        )

        columns = ["SL", "ID", "Name", "Email", "Phone", "Address"]

        for column in columns:
            layout.add_widget(
                Label(
                    text=column,
                    size_hint_x=None,
                    width=sp(120),
                    bold=True,
                    color=(1, 1, 1, 1),
                )
            )

        c = conn.cursor()
        c.execute("SELECT * FROM student_info")
        rows = c.fetchall()

        for row in rows:
            for item in row:
                layout.add_widget(
                    Label(
                        text=str(item),
                        size_hint_x=None,
                        width=sp(120),
                        color=(1, 1, 1, 1),
                    )
                )

        self.table.add_widget(layout)


class StudentNameListWindow(Screen):
    def attend(self, instance):
        c = conn.cursor()
        c.execute(
            "INSERT INTO attend (date, student, presence) VALUES (?, ?, ?)",
            (datetime.now().date(), int(instance.text), True),
        )
        conn.commit()

    def list_student_names(self):
        layout = GridLayout(
            cols=7,
            row_force_default=True,
            row_default_height=sp(40),
            padding=(20, 20, 20, 20),
            spacing=(10, 10),
        )

        columns = ["SL", "ID", "Name", "Email", "Phone", "Address", "Action"]

        for column in columns:
            layout.add_widget(
                Label(
                    text=column,
                    size_hint_x=None,
                    # width=sp(120),
                    bold=True,
                    color=(1, 1, 1, 1),
                )
            )

        c = conn.cursor()
        c.execute("SELECT * FROM student_info")
        rows = c.fetchall()

        for row in rows:
            for item in row:
                layout.add_widget(
                    Label(
                        text=str(item),
                        size_hint_x=None,
                        # width=sp(120),
                        color=(1, 1, 1, 1),
                    )
                )
            print(row[0])
            layout.add_widget(Button(text=f"{row[0]}", on_press=self.attend))

        self.list.add_widget(layout)


class AttendanceReportWindow(Screen):
    def report(self):
        layout = GridLayout(
            cols=4,
            row_force_default=True,
            row_default_height=sp(40),
            padding=(20, 20, 20, 20),
            spacing=(10, 10),
        )

        columns = ["SL", "ID", "Name", "Status"]

        for column in columns:
            layout.add_widget(
                Label(
                    text=str(column),
                    width=sp(120),
                    bold=True,
                    color=(1, 1, 1, 1),
                )
            )

        c.execute(
            "SELECT student_info.id, student_info.Name, attend.presence FROM attend INNER JOIN student_info ON student_info.pk = attend.student WHERE attend.date = '{0}'".format(
                datetime.strptime(self.search.text, "%Y-%m-%d").date()
            )
        )

        rows = c.fetchall()

        for sl, row in enumerate(rows):
            layout.add_widget(
                Label(
                    text=str(sl),
                    size_hint_x=None,
                    width=sp(120),
                    color=(1, 1, 1, 1),
                )
            )
            for item in row:
                layout.add_widget(
                    Label(
                        text=str(item),
                        size_hint_x=None,
                        width=sp(120),
                        color=(1, 1, 1, 1),
                    )
                )

        self.list_attendance.add_widget(layout)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("design.kv")


class MyApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyApp().run()
