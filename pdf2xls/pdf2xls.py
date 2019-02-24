'hi level iface'
import typing

from .model import db
from .reader import abcreader
from .writer import abcwriter


def read_infos(input_stream: typing.BinaryIO,
               reader: abcreader.ABCReader,
               db_: db.Db) -> None:
    'wraps the load from a stream to the db'
    for info in reader.read_infos(input_stream):
        db_.add_info(info)


def write_infos(output_stream: typing.BinaryIO,
                writer: abcwriter.ABCWriter,
                db_: db.Db) -> None:
    'wraps the write to a stream from the db'
    for feature, infos in db_.group_infos_by_feature().items():
        writer.write_feature_infos(output_stream, feature, infos)
