import sqlite3


conn = sqlite3.connect("project.sqlite3")
c = conn.cursor()


def db():
    c.execute(
        """ CREATE TABLE "attend" (
              "pk" INTEGER,
              "student" INTEGER,
              "date" DATE,
              "presence" BOOL,
              FOREIGN KEY("student") REFERENCES "student_info"("PK"),
              PRIMARY KEY("pk" AUTOINCREMENT)
              ); 
    """
    )

    conn.commit()
    c.close()
    conn.close()


db()
