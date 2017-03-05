#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @copyright 2017 TUNE, Inc. (http://www.tune.com)

import sys
from pprintpp import pprint
import logging

from requests_mv_integrations.exceptions import (TuneRequestBaseError)
from tune_reporting.errors import (print_traceback, get_exception_message)
from tune_reporting.tmc.v2.management import (TuneV2AuthenticationTypes, TuneV2AdvertiserSites)
from tune_reporting.exceptions import (TuneReportingError)


def main(tmc_api_key):
    tune_advertiser_sites = TuneV2AdvertiserSites(logger_level=logging.INFO)

    try:
        tune_advertiser_sites.tmc_auth(tmc_api_key=tmc_api_key)

        for collect_data_item, collect_error in tune_advertiser_sites.collect(
            auth_value=tmc_api_key,
            auth_type=TuneV2AuthenticationTypes.API_KEY,
            auth_type_use=TuneV2AuthenticationTypes.API_KEY,
            request_params={'limit': 5}
        ):
            pprint(collect_data_item)

    except TuneRequestBaseError as tmc_req_ex:
        print_traceback(tmc_req_ex)
        pprint(tmc_req_ex.to_dict())
        print(str(tmc_req_ex))

    except TuneReportingError as tmc_rep_ex:
        print_traceback(tmc_rep_ex)
        pprint(tmc_rep_ex.to_dict())
        print(str(tmc_rep_ex))

    except Exception as ex:
        print_traceback(ex)
        print(get_exception_message(ex))


if __name__ == '__main__':
    try:
        if len(sys.argv) < 2:
            raise ValueError("{} [tmc_api_key].".format(sys.argv[0]))
        tmc_api_key = sys.argv[1]
        sys.exit(main(tmc_api_key))
    except Exception as exc:
        print("Exception: {0}".format(exc))
        raise
