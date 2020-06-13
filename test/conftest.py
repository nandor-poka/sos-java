#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import json
import os
import pytest
import requests
from subprocess import Popen
import sys
from testpath.tempdir import TemporaryDirectory
import time
from urllib.parse import urljoin

from selenium.webdriver import Firefox, Chrome
from selenium import webdriver
from sos_notebook.test_utils import Notebook

pjoin = os.path.join


def _wait_for_server(proc, info_file_path):
    """Wait 30 seconds for the notebook server to start."""
    i=0
    while i <= 3000:
        if proc.poll() is not None:
            raise RuntimeError("Notebook server failed to start")
        if os.path.exists(info_file_path):
            try:
                with open(info_file_path) as f:
                    return json.load(f)
            except ValueError:
                # If the server is halfway through writing the file, we may
                # get invalid JSON; it should be ready next iteration.
                pass
        time.sleep(0.1)
        i+=1
    raise RuntimeError("Didn't find %s in 30 seconds", info_file_path)


@pytest.fixture(scope='session')
def notebook_server():
    info = {}
    temp_dir = TemporaryDirectory()
    td = temp_dir.name
    # do not use context manager because of https://github.com/vatlab/sos-notebook/issues/214
    if True:
        nbdir = info['nbdir'] = pjoin(td, 'notebooks')
        os.makedirs(pjoin(nbdir, u'sub ∂ir1', u'sub ∂ir 1a'))
        os.makedirs(pjoin(nbdir, u'sub ∂ir2', u'sub ∂ir 1b'))
        # print(nbdir)
        info['extra_env'] = {
            'JUPYTER_CONFIG_DIR': pjoin(td, 'jupyter_config'),
            'JUPYTER_RUNTIME_DIR': pjoin(td, 'jupyter_runtime'),
            'IPYTHONDIR': pjoin(td, 'ipython'),
        }
        env = os.environ.copy()
        env.update(info['extra_env'])

        command = [
            sys.executable,
            '-m',
            'notebook',
            '--no-browser',
            '--notebook-dir',
            nbdir,
            # run with a base URL that would be escaped,
            # to test that we don't double-escape URLs
            '--NotebookApp.base_url=/a@b/',
        ]
        print("command=", command)
        proc = info['popen'] = Popen(command, cwd=nbdir, env=env)
        info_file_path = pjoin(td, 'jupyter_runtime',
                               'nbserver-%i.json' % proc.pid)
        info.update(_wait_for_server(proc, info_file_path))

        print("Notebook server info:", info)
        yield info

    # manually try to clean up, which would fail under windows because
    # a permission error caused by iPython history.sqlite.
    try:
        temp_dir.cleanup()
    except Exception as ex:
        print(ex)
    # Shut the server down
    requests.post(
        urljoin(info['url'], 'api/shutdown'),
        headers={'Authorization': 'token ' + info['token']})


@pytest.fixture(scope='session')
def selenium_driver():

    if "JUPYTER_TEST_BROWSER" not in os.environ:
        os.environ["JUPYTER_TEST_BROWSER"] = 'chrome'

    if os.environ.get('JUPYTER_TEST_BROWSER') == 'live':
        driver = Chrome()
    elif os.environ.get('JUPYTER_TEST_BROWSER') == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = Chrome(options=chrome_options)
    elif os.environ.get('JUPYTER_TEST_BROWSER') == 'firefox':
        driver = Firefox()
    else:
        raise ValueError(
            'Invalid setting for JUPYTER_TEST_BROWSER. Valid options include live, chrome, and firefox'
        )

    yield driver

    # Teardown
    driver.quit()


@pytest.fixture(scope='module')
def authenticated_browser(selenium_driver, notebook_server):
    selenium_driver.jupyter_server_info = notebook_server
    selenium_driver.get("{url}?token={token}".format(**notebook_server))
    return selenium_driver


@pytest.fixture(scope="class")
def notebook(authenticated_browser):
    return Notebook.new_notebook(
        authenticated_browser, kernel_name='kernel-sos')
