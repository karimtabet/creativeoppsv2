import yaml
from voluptuous import Schema, Required, MultipleInvalid
from logging import getLogger, basicConfig

logger = getLogger(__name__)

config_schema = Schema({
    Required("postgresql"): {
        Required("role"): str,
        Required("password"): str,
        Required("host"): str,
        Required("port"): int,
        Required("db"): str
    }
})

with open("/opt/creativeopportunities.yml") as configuration_file:
    try:
        config = yaml.safe_load(configuration_file)
        config_schema(config)
        logger.info("config loaded - valid")
    except IOError:
        basicConfig()
        logger.critical("unable to open configuration file")
        exit(1)
    except MultipleInvalid as e:
        basicConfig()
        logger.critical("invalid config file: {e}".format(e=e))
        exit(1)
