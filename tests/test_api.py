import os
from pathlib import Path
import pandas as pd
from time import time
import ComposaPy as ca


TEST_API_KEY = os.getenv("TEST_API_KEY")
TEST_USERNAME = os.getenv("TEST_USERNAME")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
ROOT_PATH_COMPOSABLE = os.getenv("ROOT_PATH_COMPOSABLE")
ROOT_PATH_PYTHONNET = os.getenv("ROOT_PATH_PYTHONNET")


def test_run_dataflow_get_output():
    comp_session = ca.ComposableSession(TEST_USERNAME, TEST_PASSWORD)

    app_id = comp_session.import_app_from_json(
        str(Path(ROOT_PATH_COMPOSABLE, "UnitTests", "TestData", "CalculatorTest.json"))
    )

    run_id = comp_session.run_dataflow(app_id)
    modules = comp_session.get_run_modules(run_id)
    comp_session._services["ApplicationService"].DeleteApplication(app_id)

    assert len(modules) == 5
    assert modules[0]["ModuleOutputValues"]["Result"] == 3.0
    assert modules[1]["ModuleOutputValues"]["Result"] == 5.0

    first_string_format_module = next(
        (x for x in modules if x["Name"] == "String Formatter 2"), None
    )
    assert (
        first_string_format_module["ModuleOutputValues"]["Result"]
        == "This is a bad format"
    )


def test_queryview_to_pandas():
    comp_session = ca.ComposableSession("unittestadmin", "unittestadmin")
    df = comp_session.queryview_from_id(137072)
    print(df.head())
    print(df.dtypes)


def test_queryview_to_pandas_streaming():
    comp_session = ca.ComposableSession("unittestadmin", "unittestadmin")

    t = time()
    df = comp_session.queryview_from_id(137072)
    print(time() - t)
    print(df.head())
    print(df.dtypes)
    print(len(df))
    # print(df.read())
    # print(df.read())
    # print(df.read())
    # print(df.read())
    # print(df.read())
    # print(bytes(df.read()))
    # pd.read_csv(df)
    # with open(df,"r") as stream:
    #    print(stream)


def test_convert_table_to_pandas():
    comp_session = ca.ComposableSession("unittestadmin", "unittestadmin")
    app_id = comp_session.import_app_from_json(
        str(Path(ROOT_PATH_PYTHONNET, "tests", "TestFiles", "tablecreator.json"))
    )

    run_id = comp_session.run_dataflow(app_id)
    modules = comp_session.get_run_modules(run_id)
    comp_session._services["ApplicationService"].DeleteApplication(app_id)
    table = modules[0]["ModuleOutputValues"]["Result"]
    df = comp_session.convert_table_to_pandas(table)

    assert type(df) == type(pd.DataFrame())


def test_convert_table_to_pandas_dtypes():
    app_id = 137298  # change this

    comp_session = ca.ComposableSession("unittestadmin", "unittestadmin")
    run_id = comp_session.run_dataflow(app_id)
    modules = comp_session.get_run_modules(run_id)
    table = modules[0]["ModuleOutputValues"]["Result"]
    df = comp_session.convert_table_to_pandas(table)

    print(df)
    print(df.dtypes)

    assert type(df) == type(pd.DataFrame())
    assert df.dtypes["SystemDateTimeOffset"] == "datetime64[ns]"


# def test_all_external_inputs(self):
#     comp_session = ca.ComposableSession(api_key)
#     path_to_my_csv = r'C:\Composable\Product\UnitTests\TestData\DupColumns.csv'
#     dict_of_inputs = {'IntInput': 3, 'FileInput': path_to_my_csv, 'TableInput': pd.DataFrame({'a':[1]})}
#     dataflow_id = 7552
#     run_id = comp_session.run_dataflow_with_inputs(dataflow_id,dict_of_inputs)
#     #print(run_id)

# def test_all_external_inputs_pw(self):
#     comp_session = ca.ComposableSession(user,pw)
#     path_to_my_csv = r'C:\Composable\Product\UnitTests\TestData\DupColumns.csv'
#     dict_of_inputs = {'IntInput': 3, 'FileInput': path_to_my_csv, 'TableInput': pd.DataFrame({'a':[1]})}
#     dataflow_id = 7552
#     run_id = comp_session.run_dataflow_with_inputs(dataflow_id,dict_of_inputs)
#     #print(run_id)
