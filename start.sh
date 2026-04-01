#!/usr/bin/env bash

gunicorn krmappbackend.wsgi:application --bind 0.0.0.0:$PORT
