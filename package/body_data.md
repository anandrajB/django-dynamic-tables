# TABLE MANAGEMENT

## Create Table

### Endpoint: POST /api/table/

##### Example Request:

- Single Column

```
{
   "tblname": "mytable",
   "columns": [
      {
         "colname": "username",
         "coltype": "string"
      }
   ]
}
```

- Multiple Columns

```
{
   "tblname": "mytable",
   "columns": [
      {
         "colname": "username",
         "coltype": "string"
      },
      {
         "colname": "phone_number",
         "coltype": "string"
      }
   ]
}
```

## Get Table Information

### Endpoint: GET /api/table/

Query Parameters:

table_name (required): The name of the table to retrieve.
Example Request:

GET /api/table/?table_name=mytable

---

# COLUMN MANAGEMENT

### Add Column

---

#### Endpoint: POST /api/table/columns/

Example Requests:

- Add a Standard Column

```
{
   "change": "add",
   "colname": "useremail_id",
   "coltype": "string"
}
```

- Add a Foreign Key Column

```
{
   "change": "add",
   "colname": "kyc_info",
   "to_table": "7717",
   "to_row_id": 1,
   "coltype": "foreignkey"
}
```

### Remove Column

---

#### Endpoint: POST /api/table/columns/

Example Requests:

- Remove a Standard Column

```
{
   "change": "remove",
   "colname": "phone_number"
}
```

- Remove a Column with Relation

```
{
   "change": "remove",
   "colname": "kyc_info",
   "to_table": 7717
}
```

### Rename Column

---

### Endpoint: POST /api/table/columns/

Example Request:

```
{
   "change": "alter",
   "oldcolname": "first_name",
   "colname": "full_name",
   "coltype": "string"
}
```

---

## Modify Column Type

### Endpoint: POST /api/table/columns/

Example Requests:

- Change Column Type (Keeping Column Name)

```
{
   "change": "alter",
   "oldcolname": "emp_id",
   "colname": "emp_id",
   "coltype": "number"
}
```

- Change Column Type and Name

```
{
   "change": "alter",
   "oldcolname": "emp_id",
   "colname": "is_checked",
   "coltype": "boolean"
}
```

# Row Management

## Adding Rows

### Endpoint: POST /table/api/row//

Example Request:

```
{
   "employee_name": "Jerome jack",
   "product_details": "sample",
   "is_completed": true,
   "email_id": "jack@proton.me",
   "kyc_info_id": null
}
```

## Modify Rows

Endpoint: PUT /table/api/row/{table_id}/

Example Request:

```
{
   "id": 4,
   "employee_name": "Jerome jackson",
   "product_details": "sample",
   "kyc_info_id": null
}
```



## Delete Rows

Endpoint: DELETE /table/api/row/{table_id}/

Query Parameters:

id (required): The ID of the row to delete.

Example Request:
DELETE /table/api/row/3313421/?id=4
