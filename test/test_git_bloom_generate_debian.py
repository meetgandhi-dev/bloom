#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from __future__ import unicode_literals

import os
import unittest
# from subprocess import check_call, Popen, PIPE
import tempfile
import argparse
import shutil

from export_bloom_from_src import get_path_and_pythonpath

# from vcstools import VcsClient


class BloomSetUpstreamTestSetups(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.current_directory = os.getcwd()
        self.root_directory = tempfile.mkdtemp()
        # helpful when setting tearDown to pass
        self.directories = dict(setUp=self.root_directory)
        self.git_repo = os.path.join(self.root_directory, "git_repo")
        os.makedirs(self.git_repo)

        # Setup environment for running commands
        path, ppath = get_path_and_pythonpath()
        os.putenv('PATH', path)
        os.putenv('PYTHONPATH', ppath)

    @classmethod
    def tearDownClass(self):
        for d in self.directories:
            shutil.rmtree(self.directories[d])
        os.chdir(self.current_directory)

    def tearDown(self):
        os.chdir(self.current_directory)


class BloomSetUpstreamTest(BloomSetUpstreamTestSetups):

    def test_get_argument_parser(self):
        from bloom.generate_debian import get_argument_parser
        parser = get_argument_parser()
        assert type(parser) == argparse.ArgumentParser, type(parser)
        args = parser.parse_args(['groovy'])
        assert args.rosdistro == 'groovy', args.rosdistro
        assert args.working == None, args.working
        assert args.debian_revision == 0, args.debian_revision
        assert args.install_prefix == None, args.install_prefix
        assert args.distros == [], args.distros
        test = ['--working', '.tmp/somedir',
                '--debian-revision', '3',
                '--install-prefix', '/opt/ros/groovy',
                '--distros', 'lucid', 'precise', '--',
                'groovy']
        args = parser.parse_args(test)
        assert args.rosdistro == 'groovy', args.rosdistro
        assert args.working == '.tmp/somedir', args.working
        assert args.debian_revision == '3', args.debian_revision
        assert args.install_prefix == '/opt/ros/groovy', args.install_prefix
        assert args.distros == ['lucid', 'precise'], args.distros

    def test_process_stack_xml(self):
        pass