import matplotlib.pyplot as plt

def plot_appendix(df_array,
                label_list,
                true_mr_list,
                x_var_list,
                x_label_list,
                y_label):
    
    plt.rcParams['text.usetex'] = True
    colors = ['#ff7f00', '#377eb8', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']

    fig, axs = plt.subplots(1, len(x_label_list), figsize=(16, 4))
    
    for exp_num in range(len(x_label_list)):
        true_mr = true_mr_list[exp_num]
        x_var = x_var_list[exp_num]
        x_label = x_label_list[exp_num]

        for i in range(len(label_list)):
            df_results = df_array[exp_num][i]
            label = label_list[i]
            axs[exp_num].errorbar(df_results[x_var], df_results['mean'], 
                               yerr=df_results['std'], fmt='o',
                               label=label, capsize=5, color=colors[i])
        
        if x_var == 'true_mr':
            xy1 = (df_array[exp_num][0]['true_mr'].iloc[0], df_array[exp_num][0]['true_mr'].iloc[0])
            xy2 = (df_array[exp_num][0]['true_mr'].iloc[-1], df_array[exp_num][0]['true_mr'].iloc[-1])
            axs[exp_num].axline(xy1=xy1, xy2=xy2, color='grey', linestyle='--')
            axs[exp_num].set_xlabel(x_label, fontsize=20, fontweight='bold')
            axs[exp_num].grid(True)
        else:
            axs[exp_num].axhline(y=true_mr, color='grey', linestyle='--')
            axs[exp_num].set_xlabel(x_label, fontsize=20, fontweight='bold')
            axs[exp_num].grid(True)
        
        axs[exp_num].tick_params(axis='x', labelsize=20)
        axs[exp_num].tick_params(axis='y', labelsize=20)
    
    axs[0].set_ylabel(y_label, fontsize=20, fontweight='bold')
    
    axs[0].legend(
        loc='upper left',
        bbox_to_anchor=(-0.25, -0.25),
        ncol=6,
        fontsize=18,
    )

    return plt


def plot_main_paper(df_array,
                label_list,
                true_mr_list,
                x_var_list,
                x_label_list,
                y_label):
    
    plt.rcParams['text.usetex'] = True
    colors = ['#ff7f00', '#377eb8', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']

    fig, axs = plt.subplots(1, len(x_label_list), figsize=(16, 4))
    
    for exp_num in range(len(x_label_list)):
        true_mr = true_mr_list[exp_num]
        x_var = x_var_list[exp_num]
        x_label = x_label_list[exp_num]

        for i in range(len(label_list)):
            df_results = df_array[exp_num][i]
            label = label_list[i]
            axs[exp_num].errorbar(df_results[x_var], df_results['mean'], 
                               yerr=df_results['std'], fmt='o',
                               label=label, capsize=5, color=colors[i])
        
        if x_var == 'true_mr':
            xy1 = (df_array[exp_num][0]['true_mr'].iloc[0], df_array[exp_num][0]['true_mr'].iloc[0])
            xy2 = (df_array[exp_num][0]['true_mr'].iloc[-1], df_array[exp_num][0]['true_mr'].iloc[-1])
            axs[exp_num].axline(xy1=xy1, xy2=xy2, color='grey', linestyle='--')
            axs[exp_num].set_xlabel(x_label, fontsize=20, fontweight='bold')
            axs[exp_num].grid(True)
        else:
            axs[exp_num].axhline(y=true_mr, color='grey', linestyle='--')
            axs[exp_num].set_xlabel(x_label, fontsize=20, fontweight='bold')
            axs[exp_num].grid(True)
        
        axs[exp_num].tick_params(axis='x', labelsize=20)
        axs[exp_num].tick_params(axis='y', labelsize=20)
    
    axs[0].set_ylabel(y_label, fontsize=20, fontweight='bold')
    
    axs[2].legend(fontsize=16, ncols=2, loc='upper center', borderaxespad=2.5)
    
    plt.tight_layout()

    return plt