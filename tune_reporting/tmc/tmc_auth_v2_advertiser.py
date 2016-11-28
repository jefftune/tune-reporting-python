#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @copyright 2016 TUNE, Inc. (http://www.tune.com)
#  @namespace tune_reporting
"""
TUNE Multiverse Reporting Base
================================
"""

import logging

from logging_mv_integrations import (TuneLoggingFormat)
from tune_mv_integration.auth_validator import (AuthenticationError)

from tune_reporting.errors import (get_exception_message, print_traceback, TuneRequestErrorCodes)
from tune_reporting.exceptions import (TuneReportingError, TuneReportingAuthError)
from tune_reporting.support import (base_class_name)
from tune_reporting.tmc.v2.management.tmc_v2_advertisers import (TuneV2Advertisers)
from tune_reporting.tmc.v2.management.tmc_v2_session_authenticate import (TuneV2AuthenticationTypes)

log = logging.getLogger(__name__)


def tmc_auth_v2_advertiser(tmc_api_key, logger_level=logging.NOTSET, logger_format=TuneLoggingFormat.JSON):
    """TMC Authentication

    :return:
    """
    log.info("TMC v2 Advertiser: Authentication: Start")

    response_auth = None

    tune_v2_advertisers = \
        TuneV2Advertisers(
            logger_level=logger_level,
            logger_format=logger_format
        )

    try:
        try:
            if tune_v2_advertisers.get_advertiser_id(
                auth_type=TuneV2AuthenticationTypes.API_KEY, auth_value=tmc_api_key, request_retry=None
            ):
                advertiser_id = tune_v2_advertisers.advertiser_id

                log.debug("TMC v2 Advertiser: {}".format(advertiser_id))

        except TuneReportingError as tmv_ex:
            print(str(tmv_ex))

        except Exception as ex:
            print_traceback(ex)
            print(get_exception_message(ex))
    except AuthenticationError as auth_ex:
        log.error("TMC v2 Advertiser: Authentication: Failed", extra=auth_ex.to_dict())

        raise TuneReportingAuthError(
            error_message="TMC v2 Advertiser: Authentication: Failed",
            error_code=auth_ex.remote_status,
            errors=auth_ex.errors,
            error_request_curl=auth_ex.request_curl
        )

    except Exception as ex:
        print_traceback(ex)
        error_code = TuneRequestErrorCodes.REQ_ERR_SOFTWARE

        log.error(
            'TMC v2 Advertiser: Authentication: Failed: Unexpected',
            extra={
                'error_code': error_code,
                'error_exception': base_class_name(ex),
                'error_details': get_exception_message(ex)
            }
        )

        raise TuneReportingAuthError(
            error_message="TMC v2 Advertiser: Authentication: Failed: Unexpected",
            error_code=error_code,
            errors=ex,
        )

    if response_auth:
        log.debug("TMC v2 Advertiser: Authentication: Details", extra=response_auth.to_dict())

    return response_auth
