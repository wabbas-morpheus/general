FILE_PATH="/var/opt/morpheus/morpheus-local/repo/git/fa1eb481e857370c888c18e7bf13536c"
DESTINATION_PATH="/var/opt/morpheus/morpheus-ui/tempRepoTest"

#Set Customer Names Here 
USER_NAMES="Internal"

#Set Files to Change Names Here
FILE_TO_CHANGE="SSH.py"

cp $FILE_PATH/$FILE_TO_CHANGE $DESTINATION_PATH/$USER_NAMES/
echo "Hello"

#for i in $USER_NAMES; do
#    for n in $FILE_TO_CHANGE; do
#        cp $FILE_PATH/$n $DESTINATION_PATH/$i/
#    done
#done
