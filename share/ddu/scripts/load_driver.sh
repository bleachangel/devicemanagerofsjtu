#!/bin/ksh
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#
# Copyright 2008 Sun Microsystems, Inc. All rights reserved.
# Use is subject to license terms.
#
# ident "@(#)load_driver.sh 1.6 09/02/24 SMI"
#
#load_driver.sh driver_name
if [ $# != 1 ]
then
    echo "Usage: load_driver.sh driver_name"
    exit 1
fi

if [ ! -a /usr/bin/pkg ]
then
   echo  "/usr/bin/pkg doesn't exist"
   exit
fi

driver_name=$1
pfexec /usr/bin/pkg install $driver_name
