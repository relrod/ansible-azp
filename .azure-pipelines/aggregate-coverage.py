#!/usr/bin/env python
"""
Aggregate coverage data from multiple jobs, keeping the data only from the most recent attempt from each job.
Coverage artifacts must be named using the format: "Coverage $(System.JobAttempt) {StableUniqueNameForEachJob}"
One possible value for "{StableUniqueNameForEachJob}" is: $(System.JobDisplayName)
Keep in mind that Azure Pipelines does not enforce unique job display names (only names).
It is up to pipeline authors to avoid name collisions.
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import re
import shutil
import sys

source_directory, destination_directory = sys.argv[1:]

if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

jobs = {}
count = 0

for name in os.listdir(source_directory):
    match = re.search('^Coverage (?P<attempt>[0-9]+) (?P<label>.+)$', name)
    label = match.group('label')
    attempt = int(match.group('attempt'))
    jobs[label] = max(attempt, jobs.get(label, 0))

for label, attempt in jobs.items():
    name = 'Coverage {attempt} {label}'.format(label=label, attempt=attempt)
    source = os.path.join(source_directory, name)
    source_files = os.listdir(source)

    for source_file in source_files:
        source_path = os.path.join(source, source_file)
        destination_path = os.path.join(destination_directory, source_file)
        shutil.copyfile(source_path, destination_path)
        count += 1

print('Coverage file count: %d' % count)
print('##vso[task.setvariable variable=CoverageFileCount]%d' % count)
