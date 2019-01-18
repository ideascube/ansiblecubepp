#!/usr/bin/python3

from datetime import datetime
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
        sql = "UPDATE configuration_configuration set value='{}' where namespace='home-page'".format(json.dumps(new_visible_pkg_list + pkgs))
    except IndexError: # If no entries
        new_visible_pkg_list = []
        sql = "INSERT INTO configuration_configuration (namespace, key, value, date, actor_id) VALUES ('home-page', 'displayed-package-ids', '{}', '{}', 1)".format(json.dumps(pkgs), str(datetime.utcnow()))

    c.execute(sql)

    conn.commit()
    conn.close()


if __name__ == '__main__':
  update_sqlite(sys.argv[1:][0].split())
