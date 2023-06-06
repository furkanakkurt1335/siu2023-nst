#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --gpu-bind=closest
#SBATCH --gpus=1
#SBATCH --output=/clusterusers/bounllm/nst/outs/%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=furkanakkurt9285@gmail.com
#SBATCH --mem=40GB
#SBATCH -t 1-00:00

echo -e "Start date and time: $(date)\nEnvironment:"
env
echo
/clusterusers/bounllm/nst/.venv/bin/python3 /clusterusers/bounllm/nst/ft-eval.py --feature $1
echo -e "\nEnd date and time: $(date)"

RET=$?

exit $RET
