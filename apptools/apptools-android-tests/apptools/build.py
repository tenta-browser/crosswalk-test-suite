#!/usr/bin/env python
#
# Copyright (c) 2015 Intel Corporation.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of works must retain the original copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the original copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of Intel Corporation nor the names of its contributors
#   may be used to endorse or promote products derived from this work without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL INTEL CORPORATION BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:
#         Hongjuan, Wang<hongjuanx.wang@intel.com>
#         Yun, Liu<yunx.liu@intel.com>

import unittest
import os
import comm
import shutil


class TestCrosswalkApptoolsFunctions(unittest.TestCase):

    def test_build_release(self):
        comm.setUp()
        comm.create(self)
        os.chdir('org.xwalk.test')
        buildcmd = comm.HOST_PREFIX + comm.PackTools + "crosswalk-app build release"
        comm.build(self, buildcmd)
        comm.run(self)
        comm.clear("org.xwalk.test")

    def test_build_missing_so_file(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-app create org.xwalk.test --android-crosswalk=" + \
            comm.crosswalkzip
        os.system(cmd)
        os.chdir('org.xwalk.test')
        if comm.ARCH_X86 != "":
            if comm.BIT == "64":
                shutil.rmtree(
                    os.getcwd() +
                    '/prj/android/xwalk_core_library/libs/arm64-v8a/')
            else:
                shutil.rmtree(
                    os.getcwd() +
                    '/prj/android/xwalk_core_library/libs/armeabi-v7a/')
            buildcmd = comm.HOST_PREFIX + comm.PackTools + "crosswalk-app build"
            buildstatus = os.system(buildcmd)
            self.assertEquals(buildstatus, 0)
            pkgs = os.listdir(os.getcwd())
            armLength = 0
            for i in range(len(pkgs)):
                if pkgs[i].endswith(".apk") and "arm" in pkgs[i]:
                    armLength = armLength + 1
            self.assertEquals(armLength, 0)
        elif comm.ARCH_ARM != "":
            if comm.BIT == "64":
                shutil.rmtree(
                    os.getcwd() +
                    '/prj/android/xwalk_core_library/libs/x86_64/')
            else:
                shutil.rmtree(
                    os.getcwd() +
                    '/prj/android/xwalk_core_library/libs/x86/')
            buildcmd = comm.HOST_PREFIX + comm.PackTools + "crosswalk-app build"
            buildstatus = os.system(buildcmd)
            self.assertEquals(buildstatus, 0)
            pkgs = os.listdir(os.getcwd())
            x86Length = 0
            for i in range(len(pkgs)):
                if pkgs[i].endswith(".apk") and "x86" in pkgs[i]:
                    x86Length = x86Length + 1
            self.assertEquals(x86Length, 0)
        comm.run(self)
        comm.clear("org.xwalk.test")

    def test_build_missing_both_so_file(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-app create org.xwalk.test --android-crosswalk=" + \
            comm.crosswalkzip
        os.system(cmd)
        os.chdir('org.xwalk.test')
        if comm.BIT == "64":
            shutil.rmtree(
                os.getcwd() +
                '/prj/android/xwalk_core_library/libs/arm64-v8a/')
            shutil.rmtree(
                os.getcwd() +
                '/prj/android/xwalk_core_library/libs/x86_64/')
        else:
            shutil.rmtree(
                os.getcwd() +
                '/prj/android/xwalk_core_library/libs/armeabi-v7a/')
            shutil.rmtree(
                os.getcwd() +
                '/prj/android/xwalk_core_library/libs/x86/')
        buildcmd = comm.HOST_PREFIX + comm.PackTools + "crosswalk-app build"
        buildstatus = os.system(buildcmd)
        pkgs = os.listdir(os.getcwd())
        armLength = 0
        x86Length = 0
        for i in range(len(pkgs)):
            if pkgs[i].endswith(".apk") and "x86" in pkgs[i]:
                x86Length = x86Length + 1
            if pkgs[i].endswith(".apk") and "arm" in pkgs[i]:
                armLength = armLength + 1
        comm.clear("org.xwalk.test")
        self.assertEquals(buildstatus, 0)
        self.assertEquals(x86Length, 0)
        self.assertEquals(armLength, 0)

if __name__ == '__main__':
    unittest.main()
