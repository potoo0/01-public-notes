SESSION_NAME="batch-job"

# associative arrays(hash, no order):
# 1. `declare -A array=([k1]='v1' [k2]='v2')`
# 2. `${!array[*]}` is the key of array
# 3. `for k in ${!array[*]}` to iterate key, `${array[$k]}` get value
# # demo:
# declare -A array=([k1]='v1' [k2]='v2')
# for k in ${!array[*]}; do
#   echo "key: ${k}, val: ${array[$k]}"
# done

# order by key
PROJECT_DIR='/prj-test/'
PY_DIR='/miniconda3/envs/'
declare -A WINDOW_JOBS=(
    [1-server-8001]="cd ${PROJECT_DIR}server;${PY_DIR}/py311_dj32/python manage.py runserver 8001"
    [2-ui-8081]="cd ${PROJECT_DIR}ui/vue_app;npm run serve -- --port 8081"
)


tmux has-session -t ${SESSION_NAME}
if [ $? = 0 ]; then
    echo ${SESSION_NAME} "already exist. attaching..."
    tmux attach-session -t ${SESSION_NAME}
    # #tmux kill-session -t ${SESSION_NAME}
else
    echo ${SESSION_NAME} "doesn't exist. creating..."
    tmux new-session -d -s ${SESSION_NAME} -n home
    # #-d detach, -n for first windows name

    # #new windows and start job
    # #tmux new-window -n itsm-web -t ${SESSION_NAME}
    # #tmux send-keys -t ${SESSION_NAME}:1 "echo 'run...'" Enter

    keys=( $( echo ${!WINDOW_JOBS[@]} | tr ' ' $'\n' | sort ) )
    idx=0
    for k in ${keys[@]}; do
        echo "start: ${k}"
        idx=$(($idx+1))
        tmux new-window -n "${k}" -t ${SESSION_NAME}
        IFS=';;' read -ra CMDS <<< ${WINDOW_JOBS[$k]}
        for cmd in "${CMDS[@]}"; do
            tmux send-keys -t ${SESSION_NAME}:$idx "$cmd" Enter
        done
    done
fi
