## Initial Project Setup Required:
* cd to the project directory
* create a virtual environment 
```
python -m venv venv
```
or on the school Linux desktops
```
python3 -m venv venv
```
* activate the environment (every startup)
```
venv\Scripts\activate
```
or on Linux
```
source venv/bin/activate
```
* install all dependencies from ```requirements.txt``` file:
```sh
pip install -r requirements.txt
```

## Running the project
* cd to the project directory
* activate the virtual environment, as above, if you haven't already done so in the current terminal
* to run on Windows:
```
start_windows.bat
```
or to run on Linux:
```
./start.sh
```

## Running the test script
First, have a look at the test script:
* `pytest` is a python testing framework that first *collects* all tests - by looking for python methods beginning with `test_` in subdirectories of your project.  In the current case, these are found in `tests\test_all.py`
* This repository also uses [Pylenium](https://docs.pylenium.io/) (the Python interface to [Selenium](https://www.selenium.dev/)). Pylenium *simulates a browser pointing at your website*, which the test script can control to automatically search for HTML elements, click on them, enter text and so on.
* Open up `tests\test_all.py` and scroll to the bottom. You will see a small example test:
```python
def test_example(py):
    print (f"Visiting main page on {local_url}")
    py.visit(local_url)
    print ("Checking webpage contains word 'shop'")
    assert py.contains("shop")
```
This takes the pylenium object `py` (which simulates a browser), and tells it to visit `local_url` (which is set at the top of the script to `"http://localhost:5000"` - if you later want to test your code running on Openshift you can change this URL). It then asserts that the webpage contains the word "shop".

* Have a look at the rest of the project template. So far the "online shop" consists of a single route in `shop\routes.py` which says
```python
@app.route("/")
def front_page():
    return "TODO: make a shop!"
```
Although that's not much of a shop, it *does* contain the word "shop" so it should pass `test_example`!

Let's try running the test script. Open a new terminal, as we will need the server launched above to keep running still. `cd` to the project directory and activate the virtual environment. Then run the tests with:
```
python -m pytest
```
The first time you try this you should get a LONG output ending with
```
 1 failed, 1 passed
```
The test that the code is passing is `test_example` - so far so good!

The test that is failing is the much longer `test_system`, also defined in `tests\test_all.py`. This is the test your coursework will need to pass.

If you scroll up the output of `pytest`, you will see the first reason why it's failing:
```
====================================================== FAILURES =======================================================
_____________________________________________________ test_system _____________________________________________________

py = <pylenium.driver.Pylenium object at 0x000001C0CDA9B070>

    def test_system(py):
        '''A single system level test for the whole website.
        Ordinarily we would use the pytest framework to write multiple unit tests.
        For the purpose of efficiently assissing coursework, our needs are different:
        This *one* test function will check *multiple* behaviours of the site
        and store the results in 'results' for marking'''
        results = OrderedDict()

        py.viewport(1800,1200)

        print (f"Visiting main page on {local_url}")
        py.visit(local_url)
        py.screenshot("test_results/mainpage.png")
        min_items = 4
        print (f"Looking for at least {min_items} elements of class gallery_item")
        gallery_items = py.find(".gallery_item")
        results["At least 4 gallery items"] = len(gallery_items)>=min_items

>       py.find(".gallery_item")[0].get(".details").click()
E       IndexError: list index out of range

tests\test_all.py:120: IndexError
------------------------------------------------ Captured stdout call -------------------------------------------------
Visiting main page on http://localhost:5000
Looking for at least 4 elements of class gallery_item
------------------------------------------------ Captured stderr call -------------------------------------------------
```
The long message above is
1. Telling you which part of the test script has failed (by simply repeating lines from the test script)
2. The line prefixed with `>` is where it all went wrong
3. The line prefixed with `E` is the error message - in this case "list index out of range"
4. Under the line `-------- Captured stdout call -------------` you can see the output from the test up to the point where it failed.

The output says "Looking for at least 4 elements of class gallery_item". Currently there are no such elements on the shop website, so when Selenium tries to get the first one and click the "details" button with `py.find(".gallery_item")[0].get(".details").click()` - it goes wrong because `find` returns no results, so the list index `[0]` (for the first item found) is out of range.

Before the test failed, however, the script took a screen grab of the main page - have a look in the `test_results\` directory to see it.

At this point you should focus your attention on implementing your coursework website in `shop`, as this system test should pass if you exactly follow the specification in the coursework brief. However, after each stage of development, you may like to run the tests again to see how your work is performing against them.

When you eventually get `system_test` test to pass, your code will qualify for 60% of your coursework marks. Happy coding! :-)


