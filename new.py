
import os
import git
remote_repo_url='https://github.com/venkannagunaganti/pythonscript.git'

repo_path = "C:/Users/venky/Desktop/test" 
commit_message = "second push"
branch_name = "master"  

os.chdir(repo_path)

repo =git.Repo(repo_path)

repo.index.add(["new.py"])


repo.index.commit(commit_message)
repo.create_remote('ori', remote_repo_url)

origin = repo.remote(name="ori")
origin.push(refspec=f"{branch_name}:{branch_name}")

print(f"Pushed changes to {branch_name} branch.")

