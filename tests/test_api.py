from __future__ import annotations
from pathlib import Path
import pytest
import pandas as pd

from composapy.dataflow.api import DataFlow
from composapy.dataflow.models import DataFlowObject


@pytest.mark.parametrize("dataflow_object", ["calculator_test.json"], indirect=True)
def test_run_dataflow_get_output(dataflow_object: DataFlowObject):
    dataflow_run = dataflow_object.run()

    modules = dataflow_run.modules
    assert len(modules) == 5
    assert modules[0].result.value == 3.0
    assert modules[1].result.value == 5.0
    assert (
        modules.first_with_name("String Formatter 2").result.value
        == "This is a bad format"
    )


@pytest.mark.parametrize("dataflow_object", ["tablecreator.json"], indirect=True)
def test_convert_table_to_pandas(dataflow_object: DataFlowObject, dataflow: DataFlow):
    dataflow_run = dataflow_object.run()

    table = dataflow_run.modules.first_with_name("Table Creator").result.value
    df = dataflow.convert_table_to_dataframe(table)

    assert type(df) == type(pd.DataFrame())


@pytest.mark.parametrize(
    "dataflow_object", ["datetimeoffset_table_column_dtypes.json"], indirect=True
)
def test_convert_table_to_pandas_dtypes(
    dataflow_object: DataFlowObject, dataflow: DataFlow
):
    dataflow_run = dataflow_object.run()

    modules = dataflow_run.modules
    table = modules.first_with_name("Column Type Converter").result.value
    df = dataflow.convert_table_to_dataframe(table)

    assert type(df) == type(pd.DataFrame())
    assert str(df.dtypes["DATETIMEOFFSETCOLUMN"]) == "datetime64[ns]"


@pytest.mark.parametrize(
    "dataflow_object", ["external_input_table.json"], indirect=True
)
@pytest.mark.parametrize(
    "dataflow_object_extra", ["datetimeoffset_table_column_dtypes.json"], indirect=True
)
def test_external_input_table(
    dataflow_object: DataFlowObject, dataflow_object_extra: DataFlowObject
):
    # lazily create a new table contract by running a dataflow that has a table result
    table = (
        dataflow_object_extra.run()
        .modules.first_with_name("Column Type Converter")
        .result.value
    )

    dataflow_run = dataflow_object.run(external_inputs={"TableInput": table})

    assert list(dataflow_run.modules.first().result.value.Headers) == list(
        table.Headers
    )
    assert dataflow_run.modules.first().result.value.SqlQuery == table.SqlQuery


@pytest.mark.parametrize(
    "dataflow_object,file_path_object",
    [("external_file_input.json", "external_input_file.txt")],
    indirect=True,
)
def test_external_input_file_using_path_object(
    dataflow_object: DataFlowObject, file_path_object: Path
):
    run = dataflow_object.run(
        external_inputs={"my external file input": file_path_object}
    )
    # my IDE automatically adds \r\n, so I just leave it that way in test
    assert str(run.modules.get(name="File Reader").result.value) == "success\r\n"


@pytest.mark.parametrize(
    "dataflow_object,file_path_string",
    [("external_file_input.json", "external_input_file.txt")],
    indirect=True,
)
def test_external_input_file_using_path_string(
    dataflow_object: DataFlowObject, file_path_string: str
):
    run = dataflow_object.run(
        external_inputs={"my external file input": file_path_string}
    )
    # my IDE automatically adds \r\n, so I just leave it that way in test
    assert str(run.modules.get(name="File Reader").result.value) == "success\r\n"
