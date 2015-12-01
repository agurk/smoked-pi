#!/bin/bash

sed -i "s/id=\"gauge\"/id=\"gauge_$2\"/" $1
sed -i "s/id=\"needle\"/id=\"gauge_$2-needle\"/" $1
sed -i "s/id=\"temp_c\"/id=\"gauge_$2-temp_c\"/" $1
sed -i "s/id=\"temp_f\"/id=\"gauge_$2-temp_f\"/" $1
sed -i "s/id=\"temp_range\"/id=\"gauge_$2-temp_range\"/" $1
sed -i "s/id=\"no_connection\"/id=\"gauge_$2-no_connection\"/" $1
