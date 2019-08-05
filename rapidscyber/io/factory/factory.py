import logging
from rapidscyber.io.factory.kafka_factory import KafkaFactory
from rapidscyber.io.factory.fs_factory import FileSystemFactory

log = logging.getLogger(__name__)

class Factory:

    __cls_dict = {"kafka": "KafkaFactory", "fs": "FileSystemFactory"}

    @staticmethod
    def cls_dict():
        return Factory.__cls_dict

    class InstanceGenerator(object):
        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):
            class_name, config = self.func(*args, **kwargs)
            try:
#                for k,v in globals().items():
#                   log.info("GLOBALS " + k + " " + v)
                target_cls = globals()[class_name](config)
                return target_cls
            except KeyError as error:
                log.error(error)
                log.exception(error)
                raise

    @InstanceGenerator
    def get_instance(io_comp, config):
        io_comp = io_comp.lower()
        if io_comp and io_comp in Factory.cls_dict():
            return Factory.cls_dict()[io_comp], config
        else:
            raise KeyError(
                "Dictionary doesn't have { %s } corresponding component class."
                % (io_comp)
            )

    @staticmethod
    def get_reader(io_comp, config):
        return Factory.get_instance(io_comp, config).get_reader()

    @staticmethod
    def get_writer(io_comp, config):
        return Factory.get_instance(io_comp, config).get_writer()
