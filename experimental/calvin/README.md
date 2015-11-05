# Calvin's Notes

Currently, I'm assuming the local reviews database has been created as 'reviews.db'

Start the API's Flask web server on localhost:5000 with the command

    py -2 armAPI.py

# Example Usage

These examples are to demonstrate current functionality of our prototype.

*  Getting all apps from localhost:5000/apps:

*(14831371782 is the product ID of the Textra app)*

       [
           [
               14831371782
           ],
           ...
       ]


* Getting all reviews for app with given id from localhost:5000/apps/[string:app_id]

      [
         [
             "14831371782Ly32Dulcod7JrU9lHK24Hyg",
             14831371782,
             "I dont see a private box, i uninstalled GoSms and looks better but where is da private box",
             "2015-10-22T04:11:20",
             "Lashawn Gee",
             3,
             3.7
         ],
         ...
      ]
