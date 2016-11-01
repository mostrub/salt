# -*- coding: utf-8 -*-
'''
NAPALM Users
============

Manages the configuration of the users on network devices.

:codeauthor: Mircea Ulinic <mircea@cloudflare.com>
:maturity:   new
:depends:    napalm
:platform:   unix

Dependencies
------------
- :mod:`NAPALM proxy minion <salt.proxy.napalm>`

.. versionadded:: 2016.11.0
'''

from __future__ import absolute_import

import logging
log = logging.getLogger(__file__)


try:
    # will try to import NAPALM
    # https://github.com/napalm-automation/napalm
    # pylint: disable=W0611
    from napalm_base import get_network_driver
    # pylint: enable=W0611
    HAS_NAPALM = True
except ImportError:
    HAS_NAPALM = False

# ----------------------------------------------------------------------------------------------------------------------
# module properties
# ----------------------------------------------------------------------------------------------------------------------

__virtualname__ = 'users'
__proxyenabled__ = ['napalm']
# uses NAPALM-based proxy to interact with network devices

# ----------------------------------------------------------------------------------------------------------------------
# property functions
# ----------------------------------------------------------------------------------------------------------------------


def __virtual__():

    '''
    NAPALM library must be installed for this module to work.
    Also, the key proxymodule must be set in the __opts___ dictionary.
    '''

    if HAS_NAPALM and 'proxy' in __opts__:
        return __virtualname__
    else:
        return (False, 'The module napalm_users cannot be loaded: \
                NAPALM or proxy could not be loaded.')

# ----------------------------------------------------------------------------------------------------------------------
# helper functions -- will not be exported
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# callable functions
# ----------------------------------------------------------------------------------------------------------------------


def config():

    '''
    Returns the configuration of the users on the device

    CLI Example:

    .. code-block:: bash

        salt '*' users.config

    Output example:

    .. code-block:: python

        {
            'mircea': {
                'level': 15,
                'password': '$1$0P70xKPa$4jt5/10cBTckk6I/w/',
                'sshkeys': [
                    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC4pFn+shPwTb2yELO4L7NtQrKOJXNeCl1je\
                    l9STXVaGnRAnuc2PXl35vnWmcUq6YbUEcgUTRzzXfmelJKuVJTJIlMXii7h2xkbQp0YZIEs4P\
                    8ipwnRBAxFfk/ZcDsN3mjep4/yjN56ejk345jhk345jk345jk341p3A/9LIL7l6YewLBCwJj6\
                    D+fWSJ0/YW+7oH17Fk2HH+tw0L5PcWLHkwA4t60iXn16qDbIk/ze6jv2hDGdCdz7oYQeCE55C\
                    CHOHMJWYfN3jcL4s0qv8/u6Ka1FVkV7iMmro7ChThoV/5snI4Ljf2wKqgHH7TfNaCfpU0WvHA\
                    nTs8zhOrGScSrtb mircea@master-roshi'
                ]
            }
        }
    '''

    return __proxy__['napalm.call'](
        'get_users',
        **{
        }
    )


def set_users(users, test=False, commit=True):

    '''
    Configures users on network devices.

    :param users: Dictionary formatted as the output of the function config()
    :param test: Dry run? If set as True, will apply the config, discard and return the changes. Default: False
    and will commit the changes on the device.
    :param commit: Commit? (default: True) Sometimes it is not needed to commit the config immediately
        after loading the changes. E.g.: a state loads a couple of parts (add / remove / update)
        and would not be optimal to commit after each operation.
        Also, from the CLI when the user needs to apply the similar changes before committing,
        can specify commit=False and will not discard the config.
    :raise MergeConfigException: If there is an error on the configuration sent.
    :return a dictionary having the following keys:
        * result (bool): if the config was applied successfully. It is `False` only in case of failure. In case
        there are no changes to be applied and successfully performs all operations it is still `True` and so will be
        the `already_configured` flag (example below)
        * comment (str): a message for the user
        * already_configured (bool): flag to check if there were no changes applied
        * diff (str): returns the config changes applied

    CLI Example:

    .. code-block:: bash

        salt '*' users.set_users "{'mircea': {}}"
    '''

    return __salt__['net.load_template']('set_users',
                                         users=users,
                                         test=test,
                                         commit=commit)


def delete_users(users, test=False, commit=True):

    '''
    Removes users from the configuration of network devices.

    :param users: Dictionary formatted as the output of the function config()
    :param test: Dry run? If set as True, will apply the config, discard and return the changes. Default: False
    and will commit the changes on the device.
    :param commit: Commit? (default: True) Sometimes it is not needed to commit the config immediately
        after loading the changes. E.g.: a state loads a couple of parts (add / remove / update)
        and would not be optimal to commit after each operation.
        Also, from the CLI when the user needs to apply the similar changes before committing,
        can specify commit=False and will not discard the config.
    :raise MergeConfigException: If there is an error on the configuration sent.
    :return a dictionary having the following keys:
        * result (bool): if the config was applied successfully. It is `False` only in case of failure. In case
        there are no changes to be applied and successfully performs all operations it is still `True` and so will be
        the `already_configured` flag (example below)
        * comment (str): a message for the user
        * already_configured (bool): flag to check if there were no changes applied
        * diff (str): returns the config changes applied

    CLI Example:

    .. code-block:: bash

        salt '*' users.delete_users "{'mircea': {}}"
    '''

    return __salt__['net.load_template']('delete_users',
                                         users=users,
                                         test=test,
                                         commit=commit)
