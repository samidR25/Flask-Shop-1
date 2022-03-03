## Initial Project Setup Required:
* cd to the project directory
* to create a virtual environment (first run only)
```
python -m venv venv
```
or on the school Linux desktop
```
python3 -m venv venv
```
* to activate the environment (every startup)
```
venv\Scripts\activate
```
or on Linux
```
source venv/bin/activate
```
* to install a particular library:
```
pip install <LIBRARY>
```
&nbsp;&nbsp;&nbsp; e.g.: ```  pip install flask  ```

* to install all dependencies recursively from ```requirements.txt``` file:
```sh
pip install -r requirements.txt
```

* to see all installed dependencies in the console:
```console
pip freeze
```

* to save the project dependencies in ```requirements.txt``` file:

```console
pip freeze > requirements.txt
```
## Running the project
* to run (after `venv/Scripts/activate`)
```
flask run
```
* to coursework automated test script (n.b. server launched by `flask run` must be running still. This will fail on the project template - you need to start writing your code!)
```
python -m pytest
```
