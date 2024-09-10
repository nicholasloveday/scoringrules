import numpy as np
import pytest
from scoringrules import _logs

from .conftest import BACKENDS


@pytest.mark.parametrize("backend", BACKENDS)
def test_binomial(backend):
    # test correctness
    res = _logs.logs_binomial(8, 10, 0.9, backend=backend)
    expected = 1.641392
    assert np.isclose(res, expected)

    res = _logs.logs_binomial(-8, 10, 0.9, backend=backend)
    expected = float("inf")
    assert np.isclose(res, expected)

    res = _logs.logs_binomial(18, 30, 0.5, backend=backend)
    expected = 2.518839
    assert np.isclose(res, expected)


@pytest.mark.parametrize("backend", BACKENDS)
def test_exponential(backend):
    obs, rate = 0.3, 0.1
    res = _logs.logs_exponential(obs, rate, backend=backend)
    expected = 2.332585
    assert np.isclose(res, expected)

    obs, rate = -1.3, 2.4
    res = _logs.logs_exponential(obs, rate, backend=backend)
    expected = float("inf")
    assert np.isclose(res, expected)

    obs, rate = 0.0, 0.9
    res = _logs.logs_exponential(obs, rate, backend=backend)
    expected = 0.1053605
    assert np.isclose(res, expected)


@pytest.mark.parametrize("backend", BACKENDS)
def test_gamma(backend):
    obs, shape, rate = 0.2, 1.1, 0.7
    expected = 0.6434138

    res = _logs.logs_gamma(obs, shape, rate, backend=backend)
    assert np.isclose(res, expected)

    res = _logs.logs_gamma(obs, shape, scale=1 / rate, backend=backend)
    assert np.isclose(res, expected)

    with pytest.raises(ValueError):
        _logs.logs_gamma(obs, shape, rate, scale=1 / rate, backend=backend)
        return

    with pytest.raises(ValueError):
        _logs.logs_gamma(obs, shape, backend=backend)
        return


@pytest.mark.parametrize("backend", BACKENDS)
def test_hypergeometric(backend):
    res = _logs.logs_hypergeometric(5, 7, 13, 12)
    expected = 1.251525
    assert np.isclose(res, expected)

    res = _logs.logs_hypergeometric(5 * np.ones((2, 2)), 7, 13, 12, backend=backend)
    assert res.shape == (2, 2)

    res = _logs.logs_hypergeometric(5, 7 * np.ones((2, 2)), 13, 12, backend=backend)
    assert res.shape == (2, 2)


@pytest.mark.parametrize("backend", BACKENDS)
def test_logis(backend):
    obs, mu, sigma = 17.1, 13.8, 3.3
    res = _logs.logs_logistic(obs, mu, sigma, backend=backend)
    expected = 2.820446
    assert np.isclose(res, expected)

    obs, mu, sigma = 3.1, 4.0, 0.5
    res = _logs.logs_logistic(obs, mu, sigma, backend=backend)
    expected = 1.412808
    assert np.isclose(res, expected)


@pytest.mark.parametrize("backend", BACKENDS)
def test_loglogistic(backend):
    obs, mulog, sigmalog = 3.0, 0.1, 0.9
    res = _logs.logs_loglogistic(obs, mulog, sigmalog, backend=backend)
    expected = 2.672729
    assert np.isclose(res, expected)

    obs, mulog, sigmalog = 0.0, 0.1, 0.9
    res = _logs.logs_loglogistic(obs, mulog, sigmalog, backend=backend)
    expected = float("inf")
    assert np.isclose(res, expected)

    obs, mulog, sigmalog = 12.0, 12.1, 4.9
    res = _logs.logs_loglogistic(obs, mulog, sigmalog, backend=backend)
    expected = 6.299409
    assert np.isclose(res, expected)


@pytest.mark.parametrize("backend", BACKENDS)
def test_lognormal(backend):
    obs, mulog, sigmalog = 3.0, 0.1, 0.9
    res = _logs.logs_lognormal(obs, mulog, sigmalog, backend=backend)
    expected = 2.527762
    assert np.isclose(res, expected)

    obs, mulog, sigmalog = 0.0, 0.1, 0.9
    res = _logs.logs_lognormal(obs, mulog, sigmalog, backend=backend)
    expected = float("inf")
    assert np.isclose(res, expected)

    obs, mulog, sigmalog = 12.0, 12.1, 4.9
    res = _logs.logs_lognormal(obs, mulog, sigmalog, backend=backend)
    expected = 6.91832
    assert np.isclose(res, expected)


@pytest.mark.parametrize("backend", BACKENDS)
def test_tlogis(backend):
    obs, location, scale, lower, upper = 4.9, 3.5, 2.3, 0.0, 20.0
    res = _logs.logs_tlogistic(obs, location, scale, lower, upper, backend=backend)
    expected = 2.11202
    assert np.isclose(res, expected)

    # aligns with logs_logistic
    # res0 = _logs.logs_logistic(obs, location, scale, backend=backend)
    # res = _logs.logs_tlogistic(obs, location, scale, backend=backend)
    # assert np.isclose(res, res0)


@pytest.mark.parametrize("backend", BACKENDS)
def test_tnormal(backend):
    obs, location, scale, lower, upper = 4.2, 2.9, 2.2, 1.5, 17.3
    res = _logs.logs_tnormal(obs, location, scale, lower, upper, backend=backend)
    expected = 1.577806
    assert np.isclose(res, expected)

    obs, location, scale, lower, upper = -1.0, 2.9, 2.2, 1.5, 17.3
    res = _logs.logs_tnormal(obs, location, scale, lower, upper, backend=backend)
    expected = float("inf")
    assert np.isclose(res, expected)

    # aligns with logs_normal
    res0 = _logs.logs_normal(obs, location, scale, backend=backend)
    res = _logs.logs_tnormal(obs, location, scale, backend=backend)
    assert np.isclose(res, res0)


@pytest.mark.parametrize("backend", BACKENDS)
def test_tt(backend):
    if backend in ["jax", "torch", "tensorflow"]:
        pytest.skip("Not implemented in jax, torch or tensorflow backends")

    obs, df, location, scale, lower, upper = 1.9, 2.9, 3.1, 4.2, 1.5, 17.3
    res = _logs.logs_tt(obs, df, location, scale, lower, upper, backend=backend)
    expected = 2.002856
    assert np.isclose(res, expected)

    obs, df, location, scale, lower, upper = -1.0, 2.9, 3.1, 4.2, 1.5, 17.3
    res = _logs.logs_tt(obs, df, location, scale, lower, upper, backend=backend)
    expected = float("inf")
    assert np.isclose(res, expected)

    # aligns with logs_t
    # res0 = _logs.logs_t(obs, df, location, scale, backend=backend)
    # res = _logs.logs_tt(obs, df, location, scale, backend=backend)
    # assert np.isclose(res, res0)


@pytest.mark.parametrize("backend", BACKENDS)
def test_normal(backend):
    obs, mu, sigma = 17.1, 13.8, 3.3
    res = _logs.logs_normal(obs, mu, sigma, backend=backend)
    expected = 2.612861
    assert np.isclose(res, expected)

    obs, mu, sigma = 3.1, 4.0, 0.5
    res = _logs.logs_normal(obs, mu, sigma, backend=backend)
    expected = 1.845791
    assert np.isclose(res, expected)


@pytest.mark.parametrize("backend", BACKENDS)
def test_poisson(backend):
    obs, mean = 1.0, 3.0
    res = _logs.logs_poisson(obs, mean, backend=backend)
    expected = 1.901388
    assert np.isclose(res, expected)

    obs, mean = 1.5, 2.3
    res = _logs.logs_poisson(obs, mean, backend=backend)
    expected = float("inf")
    assert np.isclose(res, expected)

    obs, mean = -1.0, 1.5
    res = _logs.logs_poisson(obs, mean, backend=backend)
    expected = float("inf")
    assert np.isclose(res, expected)


@pytest.mark.parametrize("backend", BACKENDS)
def test_t(backend):
    if backend in ["jax", "torch", "tensorflow"]:
        pytest.skip("Not implemented in jax, torch or tensorflow backends")

    obs, df, mu, sigma = 11.1, 5.2, 13.8, 2.3
    res = _logs.logs_t(obs, df, mu, sigma, backend=backend)
    expected = 2.528398
    assert np.isclose(res, expected)

    obs, df = 0.7, 4.0
    res = _logs.logs_t(obs, df, backend=backend)
    expected = 1.269725
    assert np.isclose(res, expected)


@pytest.mark.parametrize("backend", BACKENDS)
def test_uniform(backend):
    obs, min, max = 0.3, -1.0, 2.1
    res = _logs.logs_uniform(obs, min, max, backend=backend)
    expected = 1.131402
    assert np.isclose(res, expected)

    obs, min, max = -17.9, -15.2, -8.7
    res = _logs.logs_uniform(obs, min, max, backend=backend)
    expected = float("inf")
    assert np.isclose(res, expected)

    obs, min, max = 0.1, 0.1, 3.1
    res = _logs.logs_uniform(obs, min, max, backend=backend)
    expected = 1.098612
    assert np.isclose(res, expected)
