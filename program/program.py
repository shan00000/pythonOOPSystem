import tkinter as tk
import sqlite3
from functools import partial
from PIL import Image, ImageTk
import unittest


# products Class used to store all the products as objects
class Product:
    def __init__(self, id, name, quantity, price, description, image, category, specs):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.description = description
        self.image = image
        self.category = category
        self.specs = specs


# class Containing all the reviews
class Review:
    def __init__(self, id, proid, review):
        self.id = id
        self.proid = proid
        self.review = review


# class containing all the categories
class Categories:
    def __init__(self, id, name):
        self.id = id
        self.name = name


# main class used to initialise the objects, Frames, database
class main(tk.Tk):  # main class inherits from the TK inter class
    def __init__(self, *args):  # initialise the class with any number of arguments (parameters)
        tk.Tk.__init__(self, *args)  # calls tk inter and initialise any argument given

        # Load products, reviews and Categories to the above shown classes done using the function that is defined below
        self.products = self.loadproducts()
        self.reviews = self.loadreviews()
        self.catergories = self.loadcatergory()

        # a Root Frame that allows to fill other frames inside
        self.framesbox = tk.Frame(self)
        self.framesbox.pack(side="top", fill="both", expand="true")

        # calls the first Frame using the show function
        self.show(displaypage)

    # show function allow to place each frame inside the root that is mentioned earlier,
    def show(self, frame, *args, **kwargs):  # show function to uses frames and takes any arguments or keywords to pass with it
        framee = frame(self.framesbox, self, *args, **kwargs)  # creates a dictionary objects that contains the keywords arguments and all the properties from the main class
        framee.place(x=0, y=0, relwidth=1, relheight=1)  # place the frame to the root
        framee.tkraise()  # raise the widget frame using the stacking order

    def database(self, value, command):  # function to access the database
        mydb = sqlite3.connect("CourseworkDB.db")
        mycursor = mydb.cursor()  # cursor to execute commands
        mycursor.execute(command)  # take the command parameter and execute it
        if value == True:  # if the 1st parameter given is true
            result = mycursor.fetchall()  # take the result
            mydb.commit()
            mycursor.close()
            mydb.close()
            return result  # close the database and return the results

        else:  # in a case a result is not necessary value == false
            mydb.commit()
            mycursor.close()
            mydb.close()

    def loadproducts(self):  # a function that is used to load products
        product_info = self.database(True, "Select * FROM Product")  # calls the database execute the command
        products = []  # create a list of products
        for product in product_info:  # for each tuple returned from the database
            singleproduct = Product(*product)  # add each all the elements in the tuple to the class and create objects
            products.append(singleproduct)  # take the object and add it to the products list
        return products

    def loadreviews(self):  # a function that is used to load reviews
        review_info = self.database(True, "Select * FROM review")
        reviews = []
        for review in review_info:
            singlereview = Review(*review)
            reviews.append(singlereview)
        return reviews

    def loadcatergory(self):  # a function that is used to load categories
        review_info = self.database(True, "Select * FROM Category")
        catergory = []
        for review in review_info:
            singlereview = Categories(*review)
            catergory.append(singlereview)
        return catergory


# A Frame class that is used to display products
class displaypage(tk.Frame):
    def __init__(self, framebox, superself, *args, **kwargs):
        tk.Frame.__init__(self, framebox)  # initialise the frame

        print("display page working")
        products = superself.products
        # take the products from the main class
        print("Its loading")
        # print labels above the products
        tk.Label(self, text="Product ID").grid(row=0, column=0)
        tk.Label(self, text="Name").grid(row=0, column=1)
        tk.Label(self, text="Quantity").grid(row=0, column=2)
        tk.Label(self, text="Price £").grid(row=0, column=3)
        tk.Label(self, text="Description").grid(row=0, column=4)

        for i in range(len(products)):  # loop to go through the products
            # print all the products information using the labels below
            x = i + 1
            tk.Label(self, text=products[i].id).grid(row=x, column=0)
            tk.Label(self, text=products[i].name).grid(row=x, column=1)
            tk.Label(self, text=products[i].quantity).grid(row=x, column=2)
            tk.Label(self, text=products[i].price).grid(row=x, column=3)
            tk.Label(self, text=products[i].description).grid(row=x, column=4)
            tk.Button(self, text="view product",
                      command=partial(superself.show, singleproductpage, productid=products[i].id)).grid(row=x,
                                                                                                         column=5)
            # above I used partial to call the single product page from the main class and passed the product id with it.
            tk.Label(self, text="                             ").grid(row=x + 1, column=6)

        tk.Button(self, text="search product", command=partial(superself.show, searchpage)).grid(row=x + 2, column=2)
        # above I used partial to call the search page from the main class.partial is included in the functools library


# a frame class that is used to display a single product information
class singleproductpage(tk.Frame):
    def __init__(self, framebox, superself, *args, **kwargs):
        tk.Frame.__init__(self, framebox)

        print("single product page working")

        self.framebox = framebox  # root box
        self.superself = superself  # take the class main

        productid = kwargs.get('productid')  # get the product id from the keyword arguments passed
        singleproduct_info = superself.database(True,
                                                f"Select * FROM Product WHERE Code ={productid}")  # using the database in the main class

        productlist = []  # create a list of products using the same method that is used in the main
        for product in singleproduct_info:  # instead of all the products the information about the single product is saved
            singleproduct = Product(*product)  # as a object
            productlist.append(singleproduct)

        for i in range(len(productlist)):  # take the products list that is created above

            # from PIL import Image, ImageTk
            try:
                load = Image.open(productlist[i].image)  # load the image using the name of the image
                resized = load.resize((200, 300), Image.ANTIALIAS)  # resize the photo using the function
                render = ImageTk.PhotoImage(resized,
                                            master=self.framebox, )  # render the image, defined the master as it get confused with the main-interface tk root
                img = tk.Label(self, image=render, height=200, width=300)  # print the image using a label
                img.image = render  # define the image for the label
                img.grid(row=1, column=1)  # grid pack the image
            except:
                label = tk.Label(self,
                                 text=f"image not found in the directory, Please put {productlist[i].image} into the directory"
                                 ).grid()  # print the image using a label

            # prints the rest of the product information by calling each attributes of the objects

            tk.Label(self, text="product Name-").grid(row=2, column=0)
            tk.Label(self, text=productlist[i].name).grid(row=2, column=1)

            tk.Label(self, text="Product Availability- ").grid(row=3, column=0)

            # the below if statement checks the quantity of the products and print a label based on the product quantity
            print(productlist[i].quantity)
            if int(productlist[i].quantity) == 0:
                tk.Label(self, text="Product Unavailable").grid(row=3, column=1)
            elif int(productlist[i].quantity) < 20:
                tk.Label(self, text="Low Stock").grid(row=3, column=1)
            else:
                tk.Label(self, text="Product Available").grid(row=3, column=1)

            # prints the rest of the products using the products class attributes
            tk.Label(self, text=productlist[i].quantity).grid(row=3, column=3)
            tk.Label(self, text="Product Price").grid(row=4, column=0)
            tk.Label(self, text=productlist[i].price).grid(row=4, column=1)

            tk.Label(self, text="Description").grid(row=5, column=0)
            tk.Label(self, text=productlist[i].description).grid(row=5, column=1)
            tk.Button(self, text="Buy Product").grid(row=6, column=0)
            tk.Button(self, text="Reviews and Specs",
                      command=partial(superself.show, reviewpage, productid=productlist[i].id)).grid(row=6, column=1)
            # used partial to show the review page, pass the product id as kwarg to the page
            button1 = tk.Button(self, text="Back to Home",
                                command=partial(superself.show, displaypage))
            button1.grid(row=7, column=1)
            ##used partial to show the displaypage, using the main class


# search page frame to search products and categories
class searchpage(tk.Frame):
    def __init__(self, framebox, superself, *args, **kwargs):
        tk.Frame.__init__(self, framebox)
        print("search page working")

        # get the products, categories and self to local attributes, so they can be used inside functions
        self.products = superself.products
        self.catergory = superself.catergories
        self.superself = superself

        # labels and entry fields for the search page
        tk.Label(self, text="Search Page").grid(row=0, column=1)
        self.entry_entry = tk.Entry(self)
        self.entry_entry.grid(row=1, column=1)
        # calls the self function with true to search for product
        prod_search_button = tk.Button(self, text="search Product", command=self.search).grid(row=2, column=1)
        # calls the self function to print using false to search categories
        categ_search_button = tk.Button(self, text="search Category",
                                        command=partial(self.search, product_name=False)).grid(row=3, column=1)
        # a button to show the display page (to go back to page 1)
        button1 = tk.Button(self, text="Back to Home",
                            command=partial(superself.show, displaypage))
        button1.grid(row=4, column=1)

    # search feature used to search for the products and print them if found
    def search(self, product_name=True):
        # using the get and self I get the user input given to the entry field declared before
        query = self.entry_entry.get()
        # define few variables to allow printing
        x = 7
        y = 5
        # initialise the frame as self, for some reason I though it would be easier
        frame = self
        # get the superself as a local variable
        superself = self.superself
        # loop through the products list which was initialised earlier
        for prod in self.products:
            # if true (if a product name is present)
            if product_name:
                # check if the product name == TRUE by default is true, but can be changed by passing argument in category
                if prod.name == query:
                    # if such product is found the following titles and the products will be printed,
                    # they are printed using labels
                    # product labels-
                    tk.Label(frame, text="Product ID").grid(row=y, column=0)
                    tk.Label(frame, text="Name").grid(row=y, column=1)
                    tk.Label(frame, text="Quantity").grid(row=y, column=2)
                    tk.Label(frame, text="Price £").grid(row=y, column=3)
                    tk.Label(frame, text="Description").grid(row=y, column=4)
                    # product information-
                    tk.Label(frame, text=prod.id).grid(row=x, column=0)
                    tk.Label(frame, text=prod.name).grid(row=x, column=1)
                    tk.Label(frame, text=prod.quantity).grid(row=x, column=2)
                    tk.Label(frame, text=prod.price).grid(row=x, column=3)
                    tk.Label(frame, text=prod.description).grid(row=x, column=4)
                    # tk.Label(frame, text=prod.category).grid(row=x, column=4)

                    # a button is printed to view the product, each one have the capability to call the
                    # single product page with the product id

                    tk.Button(frame, text="view product",
                              command=partial(superself.show, singleproductpage, productid=prod.id)).grid(row=x,
                                                                                                          column=5)
                    tk.Label(frame, text="                             ").grid(row=x + 1, column=6)
            else:
                # if the product name value is False,
                # use a loop to loop through each category
                for cat in self.catergory:
                    # if the category name == to the code that is inputted by the user
                    if cat.name == query:
                        # call the products and loop through the products
                        for prod in superself.products:
                            # when the product category id == category id
                            if prod.category == cat.id:
                                # prints the products that are in that category
                                #  labels-
                                x = x + 1
                                tk.Label(frame, text="Product ID").grid(row=y, column=0)
                                tk.Label(frame, text="Name").grid(row=y, column=1)
                                tk.Label(frame, text="Quantity").grid(row=y, column=2)
                                tk.Label(frame, text="Price £").grid(row=y, column=3)
                                tk.Label(frame, text="Description").grid(row=y, column=4)
                                # category product information-
                                tk.Label(frame, text=prod.id).grid(row=x, column=0)
                                tk.Label(frame, text=prod.name).grid(row=x, column=1)
                                tk.Label(frame, text=prod.quantity).grid(row=x, column=2)
                                tk.Label(frame, text=prod.price).grid(row=x, column=3)
                                tk.Label(frame, text=prod.description).grid(row=x, column=4)
                                # tk.Label(frame, text=prod.category).grid(row=x, column=4)
                                # using partial call the single product display while passing the product id as kwarg
                                tk.Button(frame, text="view product",
                                          command=partial(superself.show, singleproductpage, productid=prod.id)).grid(
                                    row=x,
                                    column=5)
                                tk.Label(frame, text="                             ").grid(row=x + 1, column=6)


# this is the review display frame which is initialised through the single product page button
class reviewpage(tk.Frame):
    def __init__(self, framebox, superself, *args, **kwargs):
        tk.Frame.__init__(self, framebox)
        # takes the superself as a local attribute (superself = mainclass)
        self.superself = superself
        # calls the reviews and save it as local attribute
        self.reviews = superself.reviews
        print("review page working")
        # take the product id from the kwarg argument given through the button
        self.productid = kwargs.get('productid')
        # calls the review print function within it self
        self.review_print()

        # entry field and button to add reviews
        self.review_entry = tk.Entry(self)
        self.review_entry.grid(row=2, column=1)
        tk.Button(self, text="add review", command=self.addreviewtoscreen).grid(row=6, column=0)

        # for review in reviews:
        #     if review.proid == self.productid:
        #         print(review)

    # use to add reviews to the database
    def addreviewtoscreen(self):
        # get the reiew and the main class
        review_entry = self.review_entry.get()
        superself = self.superself
        # using a try statement prints the insert database function to the database
        try:
            superself.database(False, f"INSERT INTO review VALUES (NULL, '{self.productid}', '{review_entry}');")
            tk.Label(self, text="Added- ").grid(row=4, column=0)
            tk.Label(self, text=review_entry).grid(row=4, column=1)
            self.review_print()
        except:  # if failed for some reason most likely the users use some kind of symbols that are not allowed
            # prints the error label
            tk.Label(self, text="Error Please Try Again").grid(row=4, column=0)

    # the function  is used to print the reviews to the screen
    def review_print(self):
        # reload=partial(self.superself.show, reviewpage, productid=)
        # get the reviews and superself(mainclass) as a local varibale
        reviews = self.reviews
        x = 5
        superself = self.superself

        tk.Label(self, text="products reviews: ").grid(row=x, column=0)
        # for each review in the class, print the review
        for review in reviews:
            if review.proid == self.productid:
                x = x + 2
                tk.Label(self, text=review.review).grid(row=x, column=1)
        # button to go back
        button1 = tk.Button(self, text="Back to Home", command=partial(superself.show, displaypage))
        button1.grid(row=6, column=1)


# a function to call the main class
def call():
    app = main()
    app.geometry("500x400")
    app.mainloop()



# uncomment if you are not running through the main interface
call()


# unit testing


# class Testdatabase(unittest.TestCase):
#     def test_database(self):
#         sql = True, "Select * FROM Product"
#         sql1 = True, "Select * FROM Category"
#         sql2 = True, "Select * FROM review"
#
#         self.assertIsNotNone(sql)
#         self.assertIsNotNone(sql1)
#         self.assertIsNotNone(sql2)


# if __name__ == '__main__':
#     unittest.main()
