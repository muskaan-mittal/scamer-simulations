import numpy as np
from causallearn.utils.cit import CIT

# performs conditional independence test on X1, ..., Xn
# test x independent of y given z
def kci_test(df, n, condition_on):
    cit = CIT(

        df.sample(n=1000, random_state=0).to_numpy(),
        method='kci',
    )
    
    y_idx = df.columns.get_loc("Y")
    z_idx = df.columns.get_indexer(condition_on)

    p_values = []
    
    for i in range(n):
        x_idx = df.columns.get_loc(f"X{i}")

        p_value = cit(x_idx, y_idx, z_idx)
        p_values.append(p_value)

    return p_values