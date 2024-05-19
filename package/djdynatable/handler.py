from typing import Dict, Optional, Type
from django.db.backends.base.base import BaseDatabaseWrapper

from django.db import ProgrammingError, models
from django.db.utils import DataError
from django.shortcuts import get_object_or_404
from .exception import BaseException
from .models import (
    DEFAULT_FIELD_TYPES,
    DEFAULT_MODEL_ATTRS,
    RELATIONSHIP_FIELD,
    SchemaModel,
    Generated_model_objects,
)
from dataclasses import dataclass
from django.db import connections


@dataclass(slots=True)
class DynamicTableQueryHandler:

    data: Dict
    model_cls: Type[models.Model] = models.Model
    db_conn: Optional[None] = None

    def __post_init__(self) -> None:
        self.db_conn: BaseDatabaseWrapper = connections["default"]

    def get_modifiers(self, coldef: Dict) -> Dict:
        """returns the column that is being modified"""
        return list(
            filter(
                lambda col: col["colname"] == coldef["oldcolname"],
                self.data["columns"],
            )
        )[0]

    def column_to_db(self, coldef: Dict, change: str = "add") -> None:
        schema_table_obj = SchemaModel.objects.filter(
            table_name=self.data["tblname"]
        ).first()
        if change == "add":
            del coldef["change"]
            schema_table_obj.columns.append(coldef)
            schema_table_obj.save()
        elif change == "remove":
            schema_table_obj.columns = list(
                filter(
                    lambda col: col["colname"] != coldef["colname"],
                    schema_table_obj.columns,
                )
            )
            schema_table_obj.save()
        elif change == "alter":
            for i in range(len(schema_table_obj.columns)):
                col = schema_table_obj.columns[i]
                if col["colname"] == coldef["oldcolname"]:
                    schema_table_obj.columns[i] = {
                        "colname": coldef["colname"],
                        "coltype": coldef["coltype"],
                    }
            schema_table_obj.save()

    def get_relation_table_object(self, data: Dict) -> models.Model:
        return (
            get_object_or_404(
                Generated_model_objects[data["to_table"]], pk=data["to_row_id"]
            )
            if "to_row_id" in data
            else Generated_model_objects[data["to_table"]]
        )

    # return (
    #     get_object_or_404(
    #         self.load_table_schema(data["to_table"]).model_cls.objects.all(),
    #         pk=data["to_row_id"],
    #     )
    #     if "to_row_id" in data
    #     else self.load_table_schema(data["to_table"]).model_cls
    # )

    def add_column(self, coldef: Dict) -> None:
        """adds column to dynamic table and saves metadata to schema table"""

        if coldef["coltype"] in RELATIONSHIP_FIELD:

            field = DEFAULT_FIELD_TYPES[coldef["coltype"]](
                to=self.get_relation_table_object(coldef),
                on_delete=models.DO_NOTHING,
                blank=True,
                null=True,
                related_name=coldef["colname"],
                db_column=coldef["colname"],
                related_query_name=coldef["colname"],
            )

        else:
            field = DEFAULT_FIELD_TYPES[coldef["coltype"]](
                **DEFAULT_MODEL_ATTRS[coldef["coltype"]]
            )
        field.column = coldef["colname"]

        try:
            with self.db_conn.schema_editor() as schema_editor:
                schema_editor.add_field(self.model_cls, field)
        except ProgrammingError:
            tblexc = BaseException(
                code="field_add_error",
                detail=f"Error while creating field: '{coldef['colname']}'. Field already exists.",
            )
            tblexc.status_code = 400
            raise tblexc
        else:
            self.column_to_db(coldef, "add")

    def remove_column(self, coldef: Dict) -> None:
        """removes column to dynamic table and saves metadata to schema  table"""
        try:
            local_coldef = list(
                filter(
                    lambda col: col["colname"] == coldef["colname"],
                    self.data["columns"],
                )
            )[0]
        except IndexError:
            tblexc = BaseException(
                code="not_found", detail=f"Column '{coldef['colname']}' was not found"
            )
            tblexc.status_code = 404
            raise tblexc
        if local_coldef["coltype"] in RELATIONSHIP_FIELD:
            field = DEFAULT_FIELD_TYPES[local_coldef["coltype"]](
                to=self.get_relation_table_object(coldef),
                on_delete=models.DO_NOTHING,
                blank=True,
                null=True,
            )
        field = DEFAULT_FIELD_TYPES[local_coldef["coltype"]]()
        field.column = coldef["colname"]

        try:
            with self.db_conn.schema_editor() as schema_editor:
                schema_editor.remove_field(self.model_cls, field)
        except ProgrammingError:
            tblexc = BaseException(
                code="remove_column_error",
                detail=f"Error while removing column '{coldef['colname']}'",
            )
            tblexc.status_code = 400
            raise tblexc
        else:
            self.column_to_db(coldef, "remove")

    def alter_column(self, coldef: Dict) -> None:
        try:
            old_column = self.get_modifiers(coldef)
        except IndexError:
            tblexc = BaseException(
                code="not_found",
                detail=f"Column '{coldef['oldcolname']}' was not found",
            )
            tblexc.status_code = 404
            raise tblexc

        old_field = DEFAULT_FIELD_TYPES[old_column["coltype"]]()
        old_field.column = old_column["colname"]

        new_field = DEFAULT_FIELD_TYPES[coldef["coltype"]](
            **DEFAULT_MODEL_ATTRS[coldef["coltype"]]
        )
        new_field.column = coldef["colname"]
        try:
            if old_column["coltype"] != coldef["coltype"]:
                """check current column type and new column type"""
                try:
                    self.model_cls.objects.all().update(**{old_column["colname"]: None})
                except:
                    try:
                        self.model_cls.objects.all().update(
                            **{old_column["colname"]: False}
                        )
                    except:
                        self.model_cls.objects.all().update(
                            **{old_column["colname"]: None}
                        )
            with self.db_conn.schema_editor() as schema_editor:
                schema_editor.alter_field(self.model_cls, old_field, new_field)
        except ProgrammingError:
            tblexc = BaseException(
                code="column_error",
                detail=f"Column '{coldef['colname']}' already exists.",
            )
            tblexc.status_code = 404
            raise tblexc
        except DataError:
            tblexc = BaseException(
                code="data_convert_error",
                detail=f"Column '{coldef['oldcolname']}' cannot be converted to '{coldef['coltype']}'",
            )
            tblexc.status_code = 404
            raise tblexc
        else:
            self.column_to_db(coldef, "alter")

    def rename_db_table(self, new_table_name: str, old_table_name: str) -> None:
        """renames the table name"""
        try:
            with self.db_conn.schema_editor() as schema_editor:
                schema_editor.alter_db_table(
                    model=self.model_cls,
                    old_db_table=old_table_name,
                    new_db_table="tables_" + new_table_name,
                )
        except ProgrammingError as e:
            BaseException(
                code="table_rename_error",
                detail=f"Table {self.data['table_name']} does not exists.",
            )
