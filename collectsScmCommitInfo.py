#!/usr/bin/env python
#################################################################################################
# require python3
# -----------    ----------------  -------------------------------------
#  Date           Author            Comment
# -----------    ----------------  -------------------------------------
# July-26-2019  Prangya Parmita Kar  Initial Version,
#
#
# python3 collectsScmCommitInfo.py --repo <repo-name>
#
#################################################################################################

import os
import logging
import sys
import timeit
import datetime
import getopt
import time
#gitpython
from git import Repo

logging.getLogger("requests").setLevel(logging.WARNING)

logger = logging.getLogger()
logger.addHandler(logging.NullHandler())


list_group = []
commitinfoFile = 'commitinfoFile.csv'
logging.getLogger("requests").setLevel(logging.WARNING)
DIR_NAME = "logs"


def print_repo(repo):
      logger.info("Begin method print_repository.")
      file_array=[]

      try:
        branch_name = repo.active_branch
        print('Repo active branch is {}'.format(branch_name))
        file_array.append('Repo active branch is '+str(branch_name)+'\n')
        for remote in repo.remotes:
            remote_name = remote

            remote_url = remote.url

            file_array.append('remote_name = '+str(remote)+'\n')
            file_array.append('remote_url = ' + str(remote_url)+'\n')

            print('Remote named "{}" with URL "{}"'.format(remote_name, remote_url))

           # print('Last commit for repo is {}.'.format(str(repo.head.commit.hexsha)))
            print('Last commit for repo is {}.'.format(str(repo.commit(repo.active_branch))))

            commit_id = repo.commit(repo.active_branch)
            file_array.append('commit_id = ' + str(commit_id)+'\n')
            #commit_message_array['commit_id'] = commit_id
            #print('Last commit for repo is {}.'.format(str(commit_id)))

            print('-------------------')
            # commit_sha = commit_id.hexsha
            # file_array.append('commit_sha = ' + str(commit_sha)+'\n')
            # commit_sum = commit_id.summary
            # file_array.append('commit_sum = ' + str(commit_sum)+'\n')
            commit_auth = commit_id.author.name
            file_array.append('commit_auth = ' + str(commit_auth)+'\n')
            commit_auth_email = commit_id.author.email
            file_array.append('commit_auth_email = ' + str(commit_auth_email)+'\n')
            commit_mesg = commit_id.message
            file_array.append('commit_message = ' + str(commit_mesg)+'\n')
            commit_auth_dt = commit_id.authored_datetime
            file_array.append('commit_auth_dt = ' + str(commit_auth_dt)+'\n')

            #print(str(commit_sha))
            print("\"{}\" by {} ({})".format(commit_mesg,
                                             commit_auth,
                                             commit_auth_email))
            print(str(commit_auth_dt))
            #file_array.append(str("\"{}\" by {} ({})".format(commit_mesg,commit_auth,commit_auth_email)))

            with open(commitinfoFile, mode='w') as outfile:
                outfile.writelines(file_array)

      except:
        logger.error("Error in print_repo : " + repo)
        print("Error in print_repo : " + repo)


def main(argv):
    logger.info("In main method .................")
    start = timeit.default_timer()
    dt = datetime.datetime.now().strftime('%m/%d/%Y-%H:%M')
    print('Process started at: ' + str(dt))

    if len(sys.argv) <= 2:
        usage()
        sys.exit(1)

    try:
        opts, args = getopt.getopt(argv, "hl:r:", ["repo="])

    except getopt.GetoptError as  exc:
        print(exc.msg)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-r", "--repo"):
            repo = arg
    check_or_create_report_directory(DIR_NAME)
    create_log_file()
    # start = timeit.default_timer()
    try:
        start_message = "Start Proces finding commit info."
        logger.info(start_message)
        print("\n" + start_message + "\n")

        validate_inputs(repo)

        # repo_path = os.getenv('GIT_REPO_PATH')  #need to handle this
        repo_path = os.path.join('.', repo)
        print(repo_path)
        # if file exists in previous run then delete that

        if os.path.exists(commitinfoFile):
            os.remove(commitinfoFile)
        # Repo object used to programmatically interact with Git repositories
        repo = Repo(repo_path)
        # check that the repository loaded correctly
        if not repo.bare:
            print('Repo at {} successfully loaded.'.format(repo_path))
            print_repo(repo)
        else:
            print('Could not load repository at {} :('.format(repo_path))

        print("-----------------------------------")
        exit_status = 0
        exit_message = 'Success'

    except Exception as ex:
        if str(ex):
            print(str(ex) + "\n")
        logger.exception(ex)
        exit_status = 1
        exit_message = 'Failed'
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print(exc_tb)

    finally:
        stop = timeit.default_timer()
        total_time = stop - start

        print("\nEnd Proces of main.\n")

        logger.info(
            "Script execution status [" + exit_message + "], time taken [" + str(
                datetime.timedelta(seconds=total_time)) + "]")
        sys.exit(exit_status)



def validate_inputs(repo):
    logger.info("Begin method validate_inputs")

    if not repo:
        err_msg = "repo is a mandatory field. "
        logger.error(err_msg)
        raise AttributeError(err_msg)


def check_or_create_report_directory(dir_name):
    report_directory = os.path.join('.', dir_name)
    if not os.path.exists(report_directory):
        logging.info("Directory [" + str(report_directory) + "] does not exist. Creating it.")
        os.makedirs(report_directory)
    else:
        logging.info("Directory [" + str(report_directory) + "] exists.")
    return report_directory


def create_log_file():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.basename(__file__)
    script_file_path = os.path.splitext(__file__)[0]
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    log_file = filename + timestamp + '.log'
    log_file_path = os.path.join(cur_dir, DIR_NAME, log_file)
    # reset the default log file
    open(log_file_path, 'w').close()
    logger.setLevel(logging.DEBUG)

    if log_file is None:
        # use the console handler for logging
        handler = logging.StreamHandler()
    else:
        # use the file handler for logging
        handler = logging.FileHandler(log_file_path)

    # create formatter
    fmt = '%(asctime)s %(filename)-15s %(levelname)-6s: %(message)s'
    fmt_date = '%Y-%m-%dT%H:%M:%S%Z'
    formatter = logging.Formatter(fmt, fmt_date)
    handler.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(handler)



def usage():
    print("\n")
    usage_message_main1 = ("Usage: " + __file__ + "[--help] --repo <repo> ")
    usage_message_main2 = ("Usage: " + __file__ + " [-h] -r <repo> ")
    usage_message_add = (
            " This script will find scm details for each repo" + '\n'
             "please see the file")

    print(usage_message_main1)
    print("OR")
    print(usage_message_main2)
    print(usage_message_add)
    print("\n")



if __name__ == "__main__":
    main(sys.argv[1:])
