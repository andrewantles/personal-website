**Notes from code review of file `./build.py`:**

AskClaude:  
Is shutil safe to use? Something about it not copying permissions and ACLs.

Ignore:  
I don’t think we need line 174 in pbuild.py, we should assume the file is there:  
    `BLOG_DIR.mkdir(parents=True, exist_ok=True)`
- On the other hand, this doesn't hurt anything.

ToDo:  
I want to move the posts directory under src/  
And also .gitignore src/

ToDo:  
Would like to add author(s) to the frontmatter, in case there is ever a guest blogger, or multiple authors on a post

AskClaude:  
Is it not “wrong” to use relative paths? I think as long as they are not being consumed as input anywhere, it’s okay?  
Same question with format strings.

ToDo - AskClaude:  
I want alt text for all thumbnails, and all html img tags. Looks like this is completely omitted in the build script.

ToDo:
Build script needs to NOT build the README.md file in the /src/posts directory