#!/usr/bin/python3
import json
import sys
import sqlite3

def update_sqlite(pkgs):

    conn = sqlite3.connect('/var/ideascube/main/default.sqlite')
    c = conn.cursor()

    req = c.execute("select value from configuration_configuration where namespace='home-page'")

    result = req.fetchall()
    try:
        new_visible_pkg_list = eval(result[0][0])
    except IndexError:
        new_visible_pkg_list = []

    sql = "UPDATE configuration_configuration set value='{}' where namespace='home-page'".format(json.dumps(new_visible_pkg_list + pkgs))
    c.execute(sql)

    conn.commit()
    conn.close()


if __name__ == '__main__':
  update_sqlite(sys.argv[1:][0].split())
