#!/bin/bash

module add prun

reservation_id=$(preserve -# $1 -t 00:15:00)

echo $reservation_id
