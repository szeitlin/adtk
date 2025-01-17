"""Test 1D transformors on some simple cases."""
import pytest
import pandas as pd
import adtk.transformer as transformer

nan = float("nan")

testCases = [
    {
        "model": transformer.RollingAggregate,
        "params": {"agg": "mean", "window": 3, "center": True},
        "s": [0, 1, 2, 3, nan, 5, 6, 7, 8, 9],
        "t": [nan, 1, 2, nan, nan, nan, 6, 7, 8, nan],
    },
    {
        "model": transformer.RollingAggregate,
        "params": {"agg": "mean", "window": 3, "center": False},
        "s": [0, 1, 2, 3, nan, 5, 6, 7, 8, 9],
        "t": [nan, nan, 1, 2, nan, nan, nan, 6, 7, 8],
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "mean",
            "window": 3,
            "center": True,
            "min_periods": 2,
        },
        "s": [0, 1, 2, 3, nan, 5, 6, 7, 8, 9],
        "t": [0.5, 1, 2, 2.5, 4, 5.5, 6, 7, 8, 8.5],
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "mean",
            "window": "3D",
            "center": False,
            "min_periods": 3,
        },
        "s": [0, 1, 2, 3, nan, 5, 6, 7, 8, 9],
        "t": [nan, nan, 1, 2, nan, nan, nan, 6, 7, 8],
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "iqr",
            "window": 3,
            "center": True,
            "min_periods": 1,
        },
        "s": [0, 1, 2, 3, nan, 5, 6, 7, 8, 9],
        "t": [0.5, 1, 1, 0.5, 1, 0.5, 1, 1, 1, 0.5],
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "iqr",
            "window": "3D",
            "center": False,
            "min_periods": 1,
        },
        "s": [0, 1, 2, 3, nan, 5, 6, 7, 8, 9],
        "t": [0, 0.5, 1, 1, 0.5, 1, 0.5, 1, 1, 1],
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "idr",
            "window": 3,
            "center": True,
            "min_periods": 1,
        },
        "s": [0, 1, 2, 3, nan, 5, 6, 7, 8, 9],
        "t": [0.8, 1.6, 1.6, 0.8, 1.6, 0.8, 1.6, 1.6, 1.6, 0.8],
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "nunique",
            "window": 3,
            "center": False,
            "min_periods": 2,
        },
        "s": [1, 2, 2, nan, 3, 3, 4, 4, 4, 4],
        "t": [nan, 2, 2, 1, 2, 1, 2, 2, 1, 1],
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "nnz",
            "window": 3,
            "center": True,
            "min_periods": 3,
        },
        "s": [1, 0, 2, nan, 3, 0, 0, 4, 0, 4],
        "t": [nan, 2, nan, nan, nan, 1, 1, 1, 2, nan],
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "quantile",
            "agg_params": {"q": 0.5},
            "window": 3,
            "center": True,
            "min_periods": 2,
        },
        "s": [0, 1, 2, 3, nan, 5, 6, 7, 8, 9],
        "t": [0.5, 1, 2, 2.5, 4, 5.5, 6, 7, 8, 8.5],
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "quantile",
            "agg_params": {"q": [0.5]},
            "window": 3,
            "center": True,
            "min_periods": 2,
        },
        "s": [0, 1, 2, 3, nan, 5, 6, 7, 8, 9],
        "t": {"q0.5": [0.5, 1, 2, 2.5, 4, 5.5, 6, 7, 8, 8.5]},
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "quantile",
            "agg_params": {"q": [0.25, 0.5]},
            "window": 3,
            "center": True,
            "min_periods": 2,
        },
        "s": [0, 1, 2, 3, nan, 5, 6, 7, 8, 9],
        "t": {
            "q0.25": [0.25, 0.5, 1.5, 2.25, 3.5, 5.25, 5.5, 6.5, 7.5, 8.25],
            "q0.5": [0.5, 1, 2, 2.5, 4, 5.5, 6, 7, 8, 8.5],
        },
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "hist",
            "agg_params": {"bins": [0, 3, 7, 9]},
            "window": 3,
            "center": False,
            "min_periods": 2,
        },
        "s": [0, 1, 2, 3, nan, 5, 6, 7, 8, 9],
        "t": {
            "[0, 3)": [nan, 2, 3, 2, 1, 0, 0, 0, 0, 0],
            "[3, 7)": [nan, 0, 0, 1, 1, 2, 2, 2, 1, 0],
            "[7, 9]": [nan, 0, 0, 0, 0, 0, 0, 1, 2, 3],
        },
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": "hist",
            "agg_params": {"bins": 3},
            "window": 3,
            "center": False,
            "min_periods": 1,
        },
        "s": [0, 1, 2, 3, 4, nan, 5, 6, 7, 8, 9],
        "t": {
            "[0.0, 3.0)": [1, 2, 3, 2, 1, 0, 0, 0, 0, 0, 0],
            "[3.0, 6.0)": [0, 0, 0, 1, 2, 2, 2, 1, 1, 0, 0],
            "[6.0, 9.0]": [0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 3],
        },
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": lambda x: x.max() - x.min(),
            "window": 3,
            "center": False,
            "min_periods": 3,
        },
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": [nan, nan, 2, 2, 2, 2, 2, 2, 2, 2],
    },
    {
        "model": transformer.RollingAggregate,
        "params": {
            "agg": lambda x: [x.min(), x.max()],
            "agg_params": {"names": ["min", "max"]},
            "window": 3,
            "center": False,
            "min_periods": 3,
        },
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": {
            "min": [nan, nan, 0, 1, 2, 3, 4, 5, 6, 7],
            "max": [nan, nan, 2, 3, 4, 5, 6, 7, 8, 9],
        },
    },
    {
        "model": transformer.DoubleRollingAggregate,
        "params": {
            "agg": "mean",
            "window": 2,
            "center": True,
            "diff": "l1",
            "min_periods": 1,
        },
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": [nan, 1.5, 2, 2, 2, 2, 2, 2, 2, 1.5],
    },
    {
        "model": transformer.DoubleRollingAggregate,
        "params": {
            "agg": "mean",
            "window": 2,
            "center": True,
            "diff": "l1",
            "min_periods": 2,
        },
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": [nan, nan, 2, 2, 2, 2, 2, 2, 2, nan],
    },
    {
        "model": transformer.DoubleRollingAggregate,
        "params": {
            "agg": "mean",
            "window": 2,
            "center": False,
            "diff": "l1",
            "min_periods": 2,
        },
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": [nan, nan, nan, 2, 2, 2, 2, 2, 2, 2],
    },
    {
        "model": transformer.DoubleRollingAggregate,
        "params": {
            "agg": "mean",
            "window": (2, 1),
            "center": True,
            "diff": "l1",
            "min_periods": (2, 1),
        },
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": [nan, nan, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
    },
    {
        "model": transformer.DoubleRollingAggregate,
        "params": {
            "agg": ("quantile", "median"),
            "agg_params": ({"q": 0.5}, None),
            "window": (2, 1),
            "center": True,
            "diff": "l1",
            "min_periods": (2, 1),
        },
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": [nan, nan, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
    },
    {
        "model": transformer.DoubleRollingAggregate,
        "params": {
            "agg": ("quantile", "quantile"),
            "agg_params": {"q": 0.5},
            "window": (2, 1),
            "center": True,
            "diff": "l1",
            "min_periods": (2, 1),
        },
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": [nan, nan, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
    },
    {
        "model": transformer.DoubleRollingAggregate,
        "params": {
            "agg": "quantile",
            "agg_params": ({"q": 0.5}, {"q": 0.5}),
            "window": (2, 1),
            "center": True,
            "diff": "l1",
            "min_periods": (2, 1),
        },
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": [nan, nan, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
    },
    {
        "model": transformer.DoubleRollingAggregate,
        "params": {
            "agg": "quantile",
            "agg_params": {"q": [0, 1]},
            "window": 2,
            "center": True,
            "diff": "l1",
            "min_periods": 2,
        },
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": [nan, nan, 4, 4, 4, 4, 4, 4, 4, nan],
    },
    {
        "model": transformer.DoubleRollingAggregate,
        "params": {
            "agg": "quantile",
            "agg_params": {"q": [0, 1]},
            "window": 2,
            "center": True,
            "diff": "l2",
            "min_periods": 2,
        },
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": [nan, nan] + [8 ** 0.5] * 7 + [nan],
    },
    {
        "model": transformer.Retrospect,
        "params": {"n_steps": 3, "step_size": 2, "till": 3},
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": {
            "t-3": [nan] * 3 + list(range(7)),
            "t-5": [nan] * 5 + list(range(5)),
            "t-7": [nan] * 7 + list(range(3)),
        },
    },
    {
        "model": transformer.Retrospect,
        "params": {"n_steps": 3, "step_size": 2, "till": 0},
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": {
            "t-0": list(range(10)),
            "t-2": [nan] * 2 + list(range(8)),
            "t-4": [nan] * 4 + list(range(6)),
        },
    },
    {
        "model": transformer.Retrospect,
        "params": {"n_steps": 1, "step_size": 2, "till": 2},
        "s": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "t": {"t-2": [nan] * 2 + list(range(8))},
    },
    {
        "model": transformer.NaiveSeasonalDecomposition,
        "params": {},
        "s": [0, 1, 2, 3, 2, 1] * 5,
        "t": [0] * 30,
    },
    {
        "model": transformer.NaiveSeasonalDecomposition,
        "params": {"freq": 12},
        "s": [0, 1, 2, 3, 2, 1] * 5,
        "t": [0] * 30,
    },
    {
        "model": transformer.CustomizedTransformer1D,
        "params": {"transform_func": lambda x: x > 0},
        "s": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        "t": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    },
    {
        "model": transformer.CustomizedTransformer1D,
        "params": {
            "transform_func": lambda x, a: x > a,
            "transform_func_params": {"a": 0},
        },
        "s": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        "t": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    },
    {
        "model": transformer.CustomizedTransformer1D,
        "params": {
            "transform_func": lambda x, a: x > a,
            "fit_func": lambda x: {"a": x.median()},
        },
        "s": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        "t": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    },
    {
        "model": transformer.CustomizedTransformer1D,
        "params": {
            "transform_func": lambda x, a: x > a,
            "fit_func": lambda x, q: {"a": x.quantile(q)},
            "fit_func_params": {"q": 0.5},
        },
        "s": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        "t": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    },
    {
        "model": transformer.CustomizedTransformer1D,
        "params": {
            "transform_func": lambda x, a, b: (x > a) | (x < b),
            "transform_func_params": {"b": -0.5},
            "fit_func": lambda x: {"a": x.median()},
        },
        "s": [0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0],
        "t": [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    },
    {
        "model": transformer.CustomizedTransformer1D,
        "params": {
            "transform_func": lambda x, a, b: (x > a) | (x < b),
            "transform_func_params": {"b": -0.5},
            "fit_func": lambda x, q: {"a": x.quantile(q)},
            "fit_func_params": {"q": 0.5},
        },
        "s": [0, 0, 0, 0, 0, 1, 0, 0, 0, -1, 0],
        "t": [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    },
]


@pytest.mark.parametrize("testCase", testCases)
def test_fit_transform(testCase):
    """Test fit_transform the transformer."""
    s = pd.Series(
        testCase["s"],
        pd.date_range(start="2017-1-1", periods=len(testCase["s"]), freq="D"),
    )
    model = testCase["model"](**testCase["params"])
    t = model.fit_transform(s)
    if not isinstance(testCase["t"], dict):
        t_true = pd.Series(testCase["t"], index=s.index)
        pd.testing.assert_series_equal(t, t_true, check_dtype=False)
    else:
        t_true = pd.DataFrame(testCase["t"], index=s.index)
        pd.testing.assert_frame_equal(t, t_true, check_dtype=False)


@pytest.mark.parametrize("testCase", testCases)
def test_fit_and_transform(testCase):
    """Test fit the transformer and then transform."""
    s = pd.Series(
        testCase["s"],
        pd.date_range(start="2017-1-1", periods=len(testCase["s"]), freq="D"),
    )
    model = testCase["model"](**testCase["params"])
    model.fit(s)
    t = model.transform(s)
    if not isinstance(testCase["t"], dict):
        t_true = pd.Series(testCase["t"], index=s.index)
        pd.testing.assert_series_equal(t, t_true, check_dtype=False)
    else:
        t_true = pd.DataFrame(testCase["t"], index=s.index)
        pd.testing.assert_frame_equal(t, t_true, check_dtype=False)


@pytest.mark.parametrize("testCase", testCases)
def test_dataframe(testCase):
    """Test apply the transformer to dataframe."""
    s = pd.Series(
        testCase["s"],
        pd.date_range(start="2017-1-1", periods=len(testCase["s"]), freq="D"),
    )
    df = pd.concat([s.rename("A"), s.rename("B")], axis=1)
    model = testCase["model"](**testCase["params"])
    t = model.fit_transform(df)
    if not isinstance(testCase["t"], dict):
        t_true = pd.Series(testCase["t"], index=s.index)
        t_true = pd.concat([t_true.rename("A"), t_true.rename("B")], axis=1)
    else:
        t_true = pd.DataFrame(testCase["t"], index=s.index)
        t_true = pd.concat(
            [
                t_true.rename(
                    columns={col: "A_{}".format(col) for col in t_true.columns}
                ),
                t_true.rename(
                    columns={col: "B_{}".format(col) for col in t_true.columns}
                ),
            ],
            axis=1,
        )
    pd.testing.assert_frame_equal(t, t_true, check_dtype=False)
