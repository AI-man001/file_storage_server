import time
import subprocess


def push():
  try:
    start = time.time()
    print('\npusher: ------> adding changes')
    git_add = subprocess.check_output(["git", "add", '.'])
    #----------------------------------------------------------
    if type(git_add == bytes):
      print('✔️.   finished adding changes')
      #------------------------------------------------------
      print('pusher: ------> committing changes')
      git_commit = subprocess.check_output(["git", "commit", '-am', 'make it better'])
      #------------------------------------------------------
      if type(git_commit == bytes):
        print('✔️.   finished committing changes')
        #--------------------------------------------------
        print('pusher: ------> pushing changes\n')
        git_push = subprocess.check_output(["git", "push", 'heroku', 'master'])
        #--------------------------------------------------
        if type(git_push == bytes):
          end = time.time()
          print('\n⌚.  time elapsed', end - start)
          print('✔️.   everything is up to date')

  except Exception as e:
    print('❌. ', e, 'in', __file__, ' @ line ', e.__traceback__.tb_lineno)


push()