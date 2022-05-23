FILE_PATH="/var/opt/morpheus/morpheus-local/repo/git/fa1eb481e857370c888c18e7bf13536c"
DESTINATION_PATH="/var/opt/morpheus/morpheus-ui/tempRepoTest"
USER_NAMES="Internal"
FILE_TO_CHANGE="SSH.py"
cp $FILE_PATH/$FILE_TO_CHANGE $DESTINATION_PATH/$USER_NAMES/
echo "Hello"
