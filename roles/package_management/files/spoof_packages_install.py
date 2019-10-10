#!/usr/local/bin/python3
import sqlalchemy as db
import os.path
import mimetypes
import sys
import requests
from datetime import datetime
from unidecode import unidecode


def guess_kind_from_filename(filepath):
    """Return a document kind (image, audio...) guessed from a filename. If
    no kind can be guessed, returns None."""
    if filepath:
        content_type, _ = mimetypes.guess_type(filepath)
        kind = guess_kind_from_content_type(content_type)
        if kind:
            return kind
        return guess_kind_from_extension(filepath)


def guess_kind_from_extension(filepath):
    """Return a document kind (image, audio...) guessed from a filename.
    Guess is based on the extension. If no kind can be guessed, returns None."""
    ext_to_kind = {
        '.epub': 'epub',
        '.mobi': 'mobi',
        '.exe': 'app',
    }
    extension = os.path.splitext(filepath)[1].lower()
    return ext_to_kind.get(extension)


def guess_kind_from_content_type(content_type):
    """Return a document kind (image, audio...) guessed from a content_type. If
    no kind can be guessed, returns None."""
    lookups = ['image', 'video', 'audio', 'text', 'pdf', 'epub', 'mobi']
    if content_type:
        for lookup in lookups:
            if lookup in content_type:
                return lookup


class mediacenter_document_model:
    """
    This is the wanted model :
        CREATE TABLE "mediacenter_document" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "created_at" datetime NOT NULL,
            "modified_at" datetime NOT NULL,
            "title" varchar(100) NOT NULL,
            "lang" varchar(10) NOT NULL,
            "original" varchar(10240) NOT NULL,
            "preview" varchar(10240) NOT NULL,
            "credits" varchar(300) NOT NULL,
            "kind" varchar(5) NOT NULL,
            "package_id" varchar(100) NOT NULL,
            "hidden" bool NOT NULL,
            "summary" text NOT NULL);
    """
    def __init__(self,
                 title,
                 lang,
                 original,
                 preview,
                 credits,
                 package_id,
                 summary):
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.title = title
        self.lang = lang
        self.original = "catalog/" + package_id + "/" + original
        self.preview = str() if preview is str() else "catalog/" + package_id + "/" + preview
        self.credits = credits
        self.kind = guess_kind_from_filename(original)
        self.package_id = package_id
        self.hidden = 0
        self.summary = summary


class taggit_tag_model:
    """
    This is the wanted model :
        CREATE TABLE "taggit_tag" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "name" varchar(100) NOT NULL UNIQUE,
            "slug" varchar(100) NOT NULL UNIQUE)
    """
    def __init__(self, name):

        self.names = name.split(',')
        self.slugs = [unidecode(x) for x in self.names]


class taggit_taggeditem_model:
    """
    This is the wanted model :
        CREATE TABLE "taggit_taggeditem" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "object_id" integer NOT NULL,
            "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id"),
            "tag_id" integer NOT NULL REFERENCES "taggit_tag" ("id"));
    """

    def __init__(self, object_id, tag_id):
        self.object_id = object_id
        self.content_type_id = 11
        self.tag_id = tag_id


class configuration_configuration_model:
    """
    This is the wanted model :
    CREATE TABLE IF NOT EXISTS "configuration_configuration" (
        "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        "namespace" varchar(40) NOT NULL,
        "key" varchar(40) NOT NULL,
        "value" text NOT NULL,
        "date" datetime NOT NULL,
        "actor_id" integer NOT NULL REFERENCES "ideascube_user" ("id"));
    """
    def __init__(self, value):
        self.namespace = "home-page"
        self.key = "displayed-package-ids"
        try:
            assert isinstance(value, list)
            self.value = str(value)  # Ideascube wants a stringified list...
        except AssertionError:
            print("In configuration_configuration_model, given value is not a list, exiting.")
            sys.exit(1)
        self.date = datetime.now()
        self.actor_id = 1


def get_db_handlers():
    engine = db.create_engine('sqlite:////var/ideascube/main/default.sqlite')
    connection = engine.connect()
    metadata = db.MetaData()
    return connection, metadata, engine


def insert_items(item, pkg, metadata, connection, engine):
    mcd = mediacenter_document_model(
        item['title'],
        item['lang'],
        item['path'],
        item['preview'],
        item['credits'],
        pkg['slug'],
        item['summary'])

    tm = taggit_tag_model(item['tags'])

    conf = db.Table('mediacenter_document', metadata, autoload=True, autoload_with=engine)
    # Insert item
    query = db.insert(conf).values(
        created_at=mcd.created_at,
        modified_at=mcd.modified_at,
        title=mcd.title,
        lang=mcd.lang,
        original=mcd.original,
        preview=mcd.preview,
        credits=mcd.credits,
        kind=mcd.kind,
        package_id=mcd.package_id,
        hidden=mcd.hidden,
        summary=mcd.summary
    )
    ResultMCD = connection.execute(query)

    for tagid in range(len(tm.names)):
        # insert item tags
        if tm.names[tagid] != str():  # if tag is not empty.
            x = db.Table('taggit_tag', metadata, autoload=True, autoload_with=engine)
            q1b = db.select([x.columns.id]).where(x.columns.name == tm.names[tagid])
            ResultTag = connection.execute(q1b).fetchone()
            tid = None if ResultTag is None else ResultTag[0]

            if tid is None:  # tag is already in db, so get it.
                x = db.Table('taggit_tag', metadata, autoload=True, autoload_with=engine)
                q1 = db.insert(x).values(name=tm.names[tagid], slug=tm.slugs[tagid])
                ResultTag = connection.execute(q1)
                tid = ResultTag.inserted_primary_key[0]

            # Link tag to item is this table.
            y = db.Table('taggit_taggeditem', metadata, autoload=True, autoload_with=engine)
            tagged_item = taggit_taggeditem_model(ResultMCD.inserted_primary_key[0], tid)

            q2 = db.insert(y).values(
                object_id=tagged_item.object_id,
                content_type_id=tagged_item.content_type_id,
                tag_id=tagged_item.tag_id
                )
            connection.execute(q2)


def update_visible_items(pkg_list, metadata, connection, engine):
    """
    We assume here that configuration_configuration table is empty. It's fail otherwise.
    """
    cf = configuration_configuration_model(pkg_list)
    table = db.Table('configuration_configuration', metadata, autoload=True, autoload_with=engine)
    query = db.insert(table).values(
        namespace=cf.namespace,
        key=cf.key,
        value=cf.value,
        date=cf.date,
        actor_id=cf.actor_id
    )
    connection.execute(query)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        API_URL = sys.argv[1].strip()
    else:
        print("Missing API_URL/project_id, exiting.")
        sys.exit(1)

    r = requests.get(API_URL)

    connection, metadata, engine = get_db_handlers()

    pkg_list = list()
    for pkg in r.json()['content']:
        pkg_list.append(pkg['slug'])
        for item in pkg['items']:
            insert_items(item, pkg, metadata, connection, engine)

    
    update_visible_items(pkg_list, metadata, connection, engine)
