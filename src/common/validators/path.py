from fastapi import Path

"""
Postgresql bigint max value
"""
MAX_INT_VALUE = 9223372036854775807

PathIdParam = Path(..., gt=0, lt=MAX_INT_VALUE)
