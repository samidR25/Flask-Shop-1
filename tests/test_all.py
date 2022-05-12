import random,string,pytest
from collections import OrderedDict

local_url = "http://localhost:5000"

def get_prices_names(py):
    '''Get list of [(price1,name1),(price2,name2),...] from the current page
    Prices returns as integer number of pence'''
    gallery_items = py.find(".gallery_item")
    items = []
    for item in gallery_items:
        name = item.get(".item_name").text()
        price = round(100*float(item.get(".item_price").text()))
        items.append((price,name))
    return items
        
def register_and_login(py,results={}):
    '''Test registration
    Test failed login 
    Test correct login
    Save the results in results dict (if passed in)'''
    
    # Register a new account
    py.visit(local_url).get("#register").click()
    test_username = "pylenium"+''.join(random.choices(string.ascii_letters + string.digits, k=10))
    test_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    print (f"Testing registration for {test_username}:{test_password}")
    py.get("#username_new").type(test_username)
    py.get("#password_new").type(test_password)
    py.get("#password_confirm").type(test_password)
    py.get('input[type="submit"]').click()
    results["Can register"] = True
    
    # Try login with incorrect details
    test_username2 = "pylenium"+''.join(random.choices(string.ascii_letters + string.digits, k=10))
    test_password2 = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    print (f"Testing bad login {test_username2}:{test_password2}")
    py.visit(local_url).get("#login").click()
    py.get("#username").type(test_username2)
    py.get("#password").type(test_password2)
    py.get('input[type="submit"]').click()
    results["Login error correctly shown"] = bool(py.get(".login_error").text())
    
    # Login with correct details
    print (f"Testing login for {test_username}:{test_password}")
    py.visit(local_url).get("#login").click()
    py.get("#username").type(test_username)
    py.get("#password").type(test_password)
    py.get('input[type="submit"]').click()
    results["Can login"] = True
    
def add_to_cart(py,my_shoplist):
    '''Add items with indices specified in my_shoplist to cart,
    return [(price,name),...] for each item added'''
    print (f"Adding items {my_shoplist} to cart")
    items = get_prices_names(py)
    my_items = []
    for item_no in my_shoplist:
        items_on_page = py.find(".gallery_item")
        print(f"{len(items_on_page)} items found on page, trying to add item {item_no}")
        items_on_page[item_no].get(".add_to_cart").click()
        my_items.append(items[item_no])
    return my_items
    
def check_cart(py,my_items):
    '''Check cart contains my_items (list of [(price,name),...])
    Check total price is correct
    Remove and item and check price is correctly updated
    Return all three test results'''
    py.get("#show_cart").click()
    my_total_price = sum([p for p,n in my_items])
    print (f"Checking total comes to {my_total_price}p as I expected")
    total_price = round(100*float(py.get("#total_price").text()))
    total_price_correct = total_price==my_total_price
    
    all_items_present = True
    for price,item_name in my_items:
        print (f"Checking cart contains {item_name}")
        all_items_present &= bool(py.contains(item_name))
    
    if len(my_items)>1:
        item_to_remove = 0
        price_to_deduct = round(100*float(py.find(".item_price")[0].text()))
        py.find(".remove")[0].click()
        new_price = round(100*float(py.get("#total_price").text()))
        remove_works = (new_price == total_price-price_to_deduct)
    else:
        remove_works = None # don't test removal if cart only has one item
        
    return total_price_correct,all_items_present,remove_works
    
def num_displayed_tips(py):
    '''Return number of elements of class 'tip' that are currently displayed'''
    return len([1 for tip in py.find(".tip") if tip.is_displayed()])
    
class ResultsDict(OrderedDict):
    def __setitem__(self,key,value):
        print(f"RESULT: {key}: {value}")
        super().__setitem__(key,value)
    
def test_system(py):
    '''A single system level test for the whole website.
    Ordinarily we would use the pytest framework to write multiple unit tests.
    For the purpose of efficiently assissing coursework, our needs are different:
    This *one* test function will check *multiple* behaviours of the site
    and store the results in 'results' for marking'''
    results = ResultsDict()
    
    py.viewport(1800,1200)
    
    print (f"Visiting main page on {local_url}")
    py.visit(local_url)
    py.screenshot("test_results/mainpage.png")
    min_items = 4
    print (f"Looking for at least {min_items} elements of class gallery_item")
    gallery_items = py.find(".gallery_item")
    results["At least 4 gallery items"] = len(gallery_items)>=min_items
    
    py.find(".gallery_item")[0].get(".details").click()
    py.screenshot("test_results/details.png")
    
    print ("Checking gallery items all have name, price, description")
    py.visit(local_url)
    gallery_items = py.find(".gallery_item")
    success = True
    for item in gallery_items:
        name = item.get(".item_name")
        success &= bool(name.text())
        price = item.get(".item_price")
        try:
            float(price.text())
        except ValueError:
            print (f"Item {name.text()} has invalid price")
            success = False
        description = item.get(".item_description")
        success &= bool(description.text())
    results["All gallery items have name, price, description"] = success
  
    sort_success = True
    print ("Getting gallery sorted by price_low")
    py.get('[value="price_low"]').click()
    price_low_list = get_prices_names(py)
    print ("Checking sort order is correct")
    sort_success &=  price_low_list==sorted(price_low_list)
    print ("Getting gallery sorted by price_high")
    py.get('[value="price_high"]').click()
    price_high_list = get_prices_names(py)
    print ("Checking sort order is correct")
    price_high_list.reverse()
    sort_success &= price_high_list==price_low_list
    results["Items sort correctly"] = sort_success 
    
    register_and_login(py,results)
    items_in_cart = add_to_cart(py,[0,2])
    py.screenshot("test_results/gallery_items_added.png")
    total_price_correct, all_items_present, remove_works = check_cart(py,items_in_cart)
    results["Total price correct"] = total_price_correct 
    results["All items present"] = all_items_present
    results["Remove works"] = remove_works
    py.screenshot("test_results/cart.png")
        
    print ("Starting new session to check cart is independent")
    py.delete_all_cookies()
    register_and_login(py)
    session2_items_in_cart = add_to_cart(py,[1])
    total_price_correct,_,_ = check_cart(py,session2_items_in_cart)
    results["Second cart ok"] = total_price_correct 
    py.screenshot("other_cart.png")
    
    print ("Testing checkout")
    py.get("#checkout").click()
    py.screenshot("test_results/checkout.png")
    results["Checkout form appears"] = bool(len(py.find(".checkout_form")))
    
    print ("Checking form field tip behaviour")
    initially_no_tips = (num_displayed_tips(py)==0)
    py.get("#name").click()
    tip_appears = (num_displayed_tips(py)==1)
    tips_work_key = "Tips work (*this is now optional*)"
    results[tips_work_key] = initially_no_tips and tip_appears
    
    print ("Checking form does not successfully submit if bad card number entered")
    py.get("#name").type("test name")
    py.get("#card_no").type("a")
    py.get("#submit").click()
    py.screenshot("test_results/bad_card_no.png")
    no_success_initially = len(py.find("#checkout_success"))==0
    
    print ("Checking form successfully submits with good card number")
    py.get("#card_no").webelement.clear()
    py.get("#card_no").type("1234567890123456")
    py.get("#submit").click()
    py.screenshot("test_results/good_card_no.png")
    success_checkout = len(py.find("#checkout_success"))>0
    results["Checkout validation"] = no_success_initially and success_checkout
    
    # Display contents of 'results' and assert all are true
    # (When your coursework is marked, the contents of 'results' is transferred to the marking sheet)
    print()
    print("All test results:")
    for k,v in results.items():
        print (f"{k}: {v}")
        
    del results[tips_work_key] # you don't need this to pass now, it's extra credit
    
    assert all(results.values())


def test_example(py):
    print (f"Visiting main page on {local_url}")
    py.visit(local_url)
    print ("Checking webpage contains word 'shop'")
    assert py.contains("shop")
    