#!/usr/bin/env python
import sys


def percentage(total, missing):
    return (total - missing) * 100.0 / total


statements_total = int(sys.argv[1])
statements_missing = int(sys.argv[2])
statements_percentage = percentage(statements_total, statements_missing)

branches_total = int(sys.argv[3])
branches_missing = int(sys.argv[4])
branches_percentage = percentage(branches_total, branches_missing)

print("statement coverage:  total: %4d, missing: %4d, percentage: %5.2f%%"
      % (statements_total, statements_missing, statements_percentage))
print("branch coverage:     total: %4d, missing: %4d, percentage: %5.2f%%"
      % (branches_total, branches_missing, branches_percentage))
print("total coverage: %5.3f%%" % ((statements_percentage + branches_percentage) / 2.0))
