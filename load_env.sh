#!/bin/bash
set -euxo pipefail

# automatically export all variables
set -a
source .env
set +a