import numpy as np
from ogind import demographics


def test_get_pop_objs():
    """
    Test of the that omega_SS and the last period of omega_path_S are
    close to each other.
    """
    E = 20
    S = 80
    T = int(round(4.0 * S))
    start_year = 2019

    pop_dict = demographics.get_pop_objs(
        E, S, T, 1, 100, start_year, start_year + 1, False
    )

    assert np.allclose(pop_dict["omega_SS"], pop_dict["omega"][-1, :])


def test_omega_sum1():
    """
    Test of the that omega sums to one in each period
    """
    E = 20
    S = 80
    T = int(round(4.0 * S))
    start_year = 2019

    pop_dict = demographics.get_pop_objs(
        E, S, T, 1, 100, start_year, start_year + 1, False
    )

    assert np.allclose(pop_dict["omega_SS"].sum(), 1.0)
    assert np.allclose(pop_dict["omega"].sum(axis=1).max(), 1.0)
    assert np.allclose(pop_dict["omega"].sum(axis=1).min(), 1.0)


def test_pop_smooth():
    """
    Test that population growth rates evolve smoothly.
    """
    E = 20
    S = 80
    T = int(round(4.0 * S))
    start_year = 2019

    pop_dict = demographics.get_pop_objs(
        E, S, T, 1, 100, start_year, start_year + 1, False
    )

    assert np.any(
        np.absolute(pop_dict["omega"][:-1, :] - pop_dict["omega"][1:, :])
        < 0.0001
    )
    assert np.any(
        np.absolute(pop_dict["g_n"][:-1] - pop_dict["g_n"][1:]) < 0.0001
    )


def test_imm_smooth():
    """
    Test that population growth rates evolve smoothly.
    """
    E = 20
    S = 80
    T = int(round(4.0 * S))
    start_year = 2019

    pop_dict = demographics.get_pop_objs(
        E, S, T, 1, 100, start_year, start_year + 1, False
    )

    assert np.any(
        np.absolute(
            pop_dict["imm_rates"][:-1, :] - pop_dict["imm_rates"][1:, :]
        )
        < 0.0001
    )


def test_get_fert():
    """
    Test of function to get fertility rates from data
    """
    S = 100
    fert_rates = demographics.get_fert(S, 0, 100, graph=False)
    assert fert_rates.shape[0] == S


def test_get_mort():
    """
    Test of function to get mortality rates from data
    """
    S = 100
    mort_rates, _ = demographics.get_mort(S, 0, 100, graph=False)
    assert mort_rates.shape[0] == S


def test_get_mort_lt1():
    """
    Test that mortality rates don't exceed 1
    """
    S = 100
    mort_rates, _ = demographics.get_mort(S, 0, 100, graph=False)
    assert mort_rates.max() <= 1.0


def test_get_mort_lastperiod():
    """
    Test that mortality rate in last period is 1
    """
    S = 100
    mort_rates, _ = demographics.get_mort(S, 0, 100, graph=False)
    assert np.allclose(mort_rates[-1], 1.0)


def test_infant_mort():
    """
    Test of function to get mortality rates from data
    """
    _, infmort_rate = demographics.get_mort(100, 0, 100, graph=False)
    # check that infant mortality equals rate hardcoded into
    # demographics.py
    assert np.allclose(infmort_rate, 0.02693456)


def test_pop_rebin():
    """
    Test of population rebin function
    """
    curr_pop_dist = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    totpers_new = 5
    rebinned_data = demographics.pop_rebin(curr_pop_dist, totpers_new)
    assert rebinned_data.shape[0] == totpers_new


def test_get_imm_rates():
    """
    Test of function to solve for immigration rates from population data
    """
    S = 100
    imm_rates = demographics.get_imm_rates(S, 0, 100)
    assert imm_rates.shape[0] == S
