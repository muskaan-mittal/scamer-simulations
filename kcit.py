import numpy as np
# from causallearn.utils.cit import CIT

from causalai.models.common.CI_tests.kci import KCI
from causalai.models.common.CI_tests.kernels import GaussianKernel

# performs conditional independence test on X1, ..., Xn
# test x independent of y given z
# def kci_test(df, n, condition_on):
#     cit = CIT(

#         df.sample(n=1000, random_state=0).to_numpy(),
#         method='kci',
#     )
    
#     y_idx = df.columns.get_loc("Y")
#     z_idx = df.columns.get_indexer(condition_on)

#     p_values = []
    
#     for i in range(n):
#         x_idx = df.columns.get_loc(f"X{i}")

#         p_value = cit(x_idx, y_idx, z_idx)
#         p_values.append(p_value)

#     return p_values


def efficient_kci_test(df, hcc_list, z_vars):
    kci_test = KCI(
        Xkernel=GaussianKernel(width='empirical'),
        Ykernel=GaussianKernel(width='empirical'),
        Zkernel=GaussianKernel(width='empirical'),
        null_space_size=5000,
        approx=True,
        chunk_size=5000)
    kci_test.epsilon_x = 1e-3
    kci_test.epsilon_y = 1e-3

    anchor_var = 'Y'
    y_idx = df.columns.get_loc(anchor_var)
    z_idx = df.columns.get_indexer(z_vars)
    x_idx = df.columns.get_indexer(hcc_list)

    if y_idx < 0 or  (z_idx < 0).any() or (x_idx < 0).any():
        raise ValueError("kci_test: some columns (x, y or z) not found in DataFrame")
    
    data = df.values

    Y = data[:, y_idx:y_idx+1].astype(np.float64)
    Z = data[:, z_idx].astype(np.float64)
    X = data[:, x_idx].astype(np.float64)
    _, p_value = kci_test.run_test(data_x=X, data_y=Y, data_z=Z)

    return p_value