#!/usr/bin/python3
import json
import sys
import sqlite3

def update_sqlite(pkgs):

    conn = sqlite3.connect('/var/ideascube/main/default.sqlite')
    c = conn.cursor()

    req = c.execute("select value from configuration_configuration where id=2")

    result = req.fetchall()
    try:
        new_visible_pkg_list = eval(result[0][0])
    except IndexError:
        new_visible_pkg_list = []

    for pkg in pkgs:
        new_visible_pkg_list.append(pkg)

    c.execute("UPDATE configuration_configuration set value='{}' where id=2".format(json.dumps(new_visible_pkg_list)))

    conn.commit()
    conn.close()


if __name__ == '__main__':
  update_sqlite(list(sys.argv))
