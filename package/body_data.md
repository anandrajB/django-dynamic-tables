# create table

### example 1

```


{


    "tblname":"mytable",


    "columns":[


       {


          "colname":"username",


          "coltype":"string"


       }


    ]


 }


```

### example 2

```


{


   "tblname":"mytable",


   "columns":[


      {


         "colname":"username",


         "coltype":"string"


      },


      {


         "colname":"phone_number",


         "coltype":"string"


      }


   ]


}


```

# add column

### example 1

```


 {


    "change":"add",


    "colname":"useremail_id",


    "coltype":"string"


 }


```

### example 2

#### for to add foreign key fields

```


{


   "change":"add",


   "colname":"kyc_info",


   "to_table":"7717",


   "to_row_id":1,


   "coltype":"foreignkey"


}


```

# remove column

```


 {


    "change":"remove",


    "colname":"phone_number"


 }


```

### remove with relation column in the current table

```


{


   "change":"remove",


   "colname":"kyc_info",


   "to_table":7717


}


```

# rename column name

```


{


   "change":"alter",


   "oldcolname":"first_name",


   "colname":"full_name",


   "coltype":"string"


}


```

# modify column type

```


{


   "change":"alter",


   "oldcolname":"emp_id",


   "colname":"emp_id",


   "coltype":"number"


}


```

```


{


   "change":"alter",


   "oldcolname":"emp_id",


   "colname": "is_checked",


   "coltype":"boolean"


}


```

# ADD ROWS

## http://127.0.0.1:8000/table/api/row/3313421/

#### when on adding rows , the data should be same as the column serializer's data

```


{


   "employee_name":"Jerome jack",


   "product_details":"sample",


   "is_completed":true,


   "email_id":"jack@proton.me",


   "kyc_info_id":null


}


```

# MODIFYING ROWS

```


{


   "id":4,


   "employee_name":"Jerome jackson",


   "product_details":"sample",


   "kyc_info_id":null


}


```

# DELETING ROWS

#### i.e id = my_row_id

#### http://127.0.0.1:8000/table/api/row/3313421/?id=4
