import fastapi
import uvicorn
import PythonScript
from fastapi.middleware.cors import CORSMiddleware
import os
import git

origins = ["http://localhost:3000", "http://localhost:3001"]

app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/process-all/")
async def process_all(dir_path: str = None):
    
    if not dir_path:
        raise fastapi.HTTPException(status_code=400, detail="Please provide a 'dir_path'.")

    dir_path = dir_path.replace('\\', '/')
    
    if dir_path.__contains__('github.com/'):
        print('Detected GitHub repo link.')
        branch_name = 'not given'
        if dir_path.__contains__('/tree/'):    
            repo_url, branch_name = dir_path.split('/tree/')
            print(f"Repo URL: {repo_url}, Branch: {branch_name}")
        else:
            repo_url = dir_path
            print(f"Repo URL: {repo_url}, Branch: default")
        
        if not repo_url.endswith('.git'):
            repo_url += '.git'

        try:
            clone_dir = f"{os.path.dirname(__file__)}/cloned/"
            if not os.path.exists(clone_dir):
                os.mkdir(clone_dir)

            if branch_name == 'not given':
                git.Repo.clone_from(repo_url, clone_dir)
            else:
                git.Repo.clone_from(repo_url, clone_dir, branch=branch_name)

            dir_path = clone_dir
            print(f'Git clone successful, dir_path: {dir_path}')

        except Exception as e:
            print(f'\nException occured while cloning the github repo: {e}\n')
            raise fastapi.HTTPException(status_code=400, detail=f"Could not clone the github repo, please check the link or if it is public.")
    elif not os.path.exists(dir_path):
        raise fastapi.HTTPException(status_code=400, detail=f"Directory not found: '{dir_path}'!")
    
    print(f'Validated dir path: {dir_path}')

    msg = PythonScript.read_directory(dir_path)
    return {"message": msg if msg else "Directory processed"}

if __name__ == "__main__":
   uvicorn.run("api_endpoints:app", host="127.0.0.1", port=8090, reload=True)