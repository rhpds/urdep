#!/usr/bin/env python3

import logging
import os

import urdep

logger = logging.getLogger('urdep')
mode = os.getenv('URDEP_MODE')

def main():
    if mode == 'api':
        import urdep.api
        urdep.api.run()
    elif mode == 'manager':
        import urdep.manager
        urdep.manager.run()
    elif mode == None:
        logger.error(
            "URDEP_MODE must be set to 'api' or 'manager'"
        )
    else:
        logger.error(
            f"Invalid URDEP_MODE '{mode}'. URDEP_MODE be 'api' or 'manager'"
        )

if __name__ == '__main__':
    main()
