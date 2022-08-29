""" Copyright start
  Copyright (C) 2008 - 2022 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

from connectors.core.connector import Connector, get_logger, ConnectorError
from .operations import operations, _check_health
from connectors.cyops_utilities.builtins import make_cyops_request
from .constant import MACRO_LIST

logger = get_logger("activedirectory")


class ActiveDirectory(Connector):
    def execute(self, config, operation, params, **kwargs):
        try:
            logger.info('In execute() Operation: {}'.format(operation))
            operation = operations.get(operation)
            return operation(config, params)
        except Exception as err:
            raise ConnectorError('{}'.format(str(err)))

    def check_health(self, config):
        try:
            return _check_health(config)
        except Exception as err:
            raise ConnectorError('{}'.format(str(err)))

    def del_micro(self, config):
        for macro in MACRO_LIST:
            try:
                resp = make_cyops_request(f'/api/wf/api/dynamic-variable/?name={macro}', 'GET')
                if resp['hydra:member']:
                    macro_id = resp['hydra:member'][0]['id']
                    resp = make_cyops_request(f'/api/wf/api/dynamic-variable/{macro_id}/?format=json', 'DELETE')
            except Exception as e:
                logger.error(e)

    def on_deactivate(self, config):
        self.del_micro(config)

    def on_activate(self, config):
        self.del_micro(config)

    def on_add_config(self, config, active):
        self.del_micro(config)

    def on_delete_config(self, config):
        self.del_micro(config)
